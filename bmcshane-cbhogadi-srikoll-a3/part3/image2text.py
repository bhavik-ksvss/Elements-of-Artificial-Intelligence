#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: (insert names here)
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image, ImageDraw, ImageFont
import sys
import math
import copy

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25



def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print(im.size)
    print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)




m = .1
ms = {}
for key in train_letters.keys():
    if key == '"':
        ms[key] = .1
    else:
        ms[key] = .1




# gives P(observed letter | hidden/actual letter)
# I think!
# isn't normalized to be 1, but I don't think that necessarily matters
def emission_probabilities(input_image):
    total_pixels = 16*25
    probabilities = {}


    for letter, actual_image in train_letters.items():
        mismatches = 0
        m = ms[letter]

        for input_row, actual_row in zip(input_image, actual_image):
            #for input_pixel, actual_pixel in zip(input_row, actual_row):
                #if input_pixel != actual_row:
                    #mismatches += 1
            mismatches += sum([(lambda x,y : 1 if x==y else 0)(q, p) for q, p in zip(input_row, actual_row)])
        
        # for every pixel that mismatches, there's a m% probability the noise made it do so
        # for every pixel that matches, there's a (1-m)% chance the noise made it do so
        probabilities[letter] = ((1-m)**(mismatches))*((m)**(total_pixels - mismatches))

    
    return probabilities



def print_letter(ls):
    for row in ls:
        print(row)



def transition_probabilities():
    with open(train_txt_fname) as f:
        corpus = f.readlines()

    probabilities = {}
    init_distro = {}



    # it looks like the last 3 characters in each corpus string are just empty spaces I don't think we need to worry about.
    # every even indexed word in sentence.split(' ') is a word we're accounting for
    # odd indexed words are just the POS corresponding to the word behind it
    # WE NEED TO ASK IF WE'RE INCLUDING SPACES INTO OUR 'CHARACTER LIST'
    # this detail will change our implementation a good bit, we're assuming not for right now
    #print('before')
    #print(corpus[0])
    t=0
    for sentence in corpus:
        # this completely filters out the POS tags and the trailing spaces
        # note: this method puts spaces between quotations and the word between them, slightly altering transition probabilities

        ls = sentence.split(' ')[0::2][:-2]
        string = ' '.join(ls)
        punc = string[-1]
        string = string[:-2] # there was an extra space between the period at the end of the sentence and the last word
        string += punc # .?!

        if t == 0:
            #print('after')
            #print(string)
            t=1

        first = string[0]


        if first in init_distro.keys():
            init_distro[first] += 1
        else:
            init_distro[first] = 1

        for i in range(len(string)-1):
            char = string[i]
            next = string[i+1]

            if char in probabilities.keys():
                if next in probabilities[char].keys():
                    probabilities[char][next] += 1
                else:
                    probabilities[char][next] = 1
            else:
                probabilities[char] = {next: 1}


    # aka no sentence started with this character in the corpus (think punctuation, non-capital letters, spaces)
    for key in train_letters.keys():
        if key not in init_distro.keys():
            init_distro[key] = 0

        init_distro[key] += 1

    # need to normalize
    s = sum(init_distro.values())
    for key in init_distro.keys():
        init_distro[key] /= s



    #dictionary[curr_letter][next_letter] = t probability
    for key1 in probabilities.keys():
        # for every character we've encountered but that we never encountered after our current character
        for key2 in train_letters.keys():
            if key2 not in probabilities[key1].keys():
                probabilities[key1][key2] = 0

            probabilities[key1][key2] += 1

        s = sum(probabilities[key1].values())
        for key2 in probabilities[key1].keys():
            probabilities[key1][key2] /= s

        

    for k1 in train_letters.keys():
        if k1 not in probabilities.keys():
            probabilities[k1] = {}

            for k2 in train_letters.keys():
                probabilities[k1][k2] = 1/len(train_letters)
        

    
    return init_distro, probabilities




# this should be getting it close to correct, something wrong in emission_probabilities
def simple(test_letters):
    y_hat = ''

    for letter in test_letters:
        probabilities = emission_probabilities(letter)
        y_hat += max(probabilities, key=probabilities.get)

    return y_hat



def viterbi(test_letters):
    init_distro, transitions = transition_probabilities()

    prob_dic = {}
    for i in range(len(test_letters)):
        prob_dic[i] = {}
        curr = test_letters[i]
        emissions = emission_probabilities(curr)

        #if i == 1:
            #print(prob_dic) 

        

        for char_to_add in train_letters.keys():
            if i==0:
                prob_dic[i][char_to_add] = [char_to_add, math.log(init_distro[char_to_add]) + math.log(emissions[char_to_add])]
            else:
                best_ss = ''
                best_p = -math.inf

                for last_char_added, val in prob_dic[i-1].items():
                    #print(f'i {i} substring {val[0]}, prob: {val[1]}')
                    substring, ss_prob = copy.deepcopy(val[0]), val[1]

                    try:
                        p1 = math.log(ss_prob)
                    except:
                        p1 = 0

                    p2 = math.log(transitions[last_char_added][char_to_add])
                    p3 = math.log(emissions[char_to_add])

                    probability = p1 + p2 + p3

                    if probability > best_p:
                        best_ss = copy.deepcopy(substring)
                        best_p = probability

                best_ss = best_ss + char_to_add
                prob_dic[i][char_to_add] = [best_ss, best_p]

    final_dic = prob_dic[len(test_letters)-1]

    #print('final dic')
    #print(final_dic)

    best_ss, best_p = '', -math.inf
    for key, val in final_dic.items():
        ss, p = val[0], val[1]
        if p > best_p:
            best_p = p
            best_ss = copy.deepcopy(ss)

    return best_ss
        

    # I have no idea how to do this

print('=================')

#print(simple(test_letters))
#print(viterbi(test_letters))


#for i in range(len(test_letters)):
    #print_letter(test_letters[i])
    #print(simp[i])
    ##print(vit[i])



## Below is just some sample code to show you how the functions above work. 
# You can delete this and put your own code here!


## Each training letter is now stored as a list of characters, where black
##  dots are represented by *'s and white dots are spaces. For example,
##  here's what "a" looks like:
#print("\n".join([ r for r in train_letters['a'] ]))

## Same with test letters. Here's what the third letter of the test data
##  looks like:
#print("\n".join([ r for r in test_letters[2] ]))



## The final two lines of your output should look something like this:
print("Simple: " + simple(test_letters))
print("   HMM: " + viterbi(test_letters)) 


