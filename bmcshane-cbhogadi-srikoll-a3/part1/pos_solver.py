###################################
# CS B551 Spring 2021, Assignment #3
#
# Your names and user ids: Bhavik Kollipara, Chandra Sagar Bhogadhi, Brendan Mcshane
#
# (Based on skeleton code by D. Crandall)
#


import random
import math


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.


class Solver:

    def __init__(self):

        self.total_num_words=0

        #pos count in training data
        self.num_pos={}
        #words count in training data
        self.num_words={}

        #intial count
        self.pos_start_num={}
        #emission count
        self.w_pos_num={}
        self.pos_w_num={}
        #transition count
        self.transition_num={}
        

        #pos probability
        self.prob_pos={}
        #words probability
        self.prob_words={}

        
        #intial probability
        self.pos_start_prob={}
        #emission probability
        self.w_pos_prob={}
        self.pos_w_prob={}
        #transition probability
        self.transition_prob={}
       

    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):
        if model == "Simple":
            emissions =1
            for i in range(len(sentence)):
                if i in self.pos_w_prob[label[i]]:
                    emissions*=self.pos_w_prob[label[i]][sentence[i]]/self.num_pos[label[i]]
                else:
                    emissions*=1e-6/self.num_pos[label[i]]
            return math.log(emissions+(1e-25))
            
        elif model == "HMM":
            emissions = 1
            transitions = 1
            for i in range(len(sentence)):
                if i in self.pos_w_prob[label[i]]:
                    emissions*=self.pos_w_prob[label[i]][sentence[i]]/self.num_pos[label[i]]
                else:
                    emissions*=1e-6/self.num_pos[label[i]]
            for i in range(len(sentence)-1):
                if label[i-1] in self.transition_prob[label[i]]:
                    transitions=transitions*self.transition_prob[label[i]][label[i-1]] 
                else:
                    transitions=transitions*1e-4
            return math.log(emissions*transitions + (1e-25))
        elif model == "Complex":
            return -999
        else:
            print("Unknown algo!")

    # Do the training!

    def train(self, data):
        for i in data:
            self.total_num_words += len(i[0])

            for j in range(0,len(i[0])):

                #frequency of the pos 
                if i[1][j] in self.num_pos.keys():
                    self.num_pos[i[1][j]] += 1
                else:
                    self.num_pos[i[1][j]] = 1
                    self.pos_w_num[i[1][j]] = {}
                    self.transition_num[i[1][j]] = {}

                #frequency of the words
                if i[0][j] in self.num_words.keys():
                    self.num_words[i[0][j]] += 1
                else:
                    self.num_words[i[0][j]] = 1
                    self.w_pos_num[i[0][j]] = {}



                #frequency of the start
                if j == 0:
                    if i[1][j] in self.pos_start_num.keys():
                        self.pos_start_num[i[1][j]] += 1
                    else:
                        self.pos_start_num[i[1][j]] = 1  



                #frequency of the word given the pos
                if i[1][j] in self.w_pos_num[i[0][j]]:
                    self.w_pos_num[i[0][j]][i[1][j]] += 1
                else:
                    self.w_pos_num[i[0][j]][i[1][j]] = 1

                #frequency of the pos given the word
                if i[0][j] in self.pos_w_num[i[1][j]]:
                    self.pos_w_num[i[1][j]][i[0][j]] += 1
                else:
                    self.pos_w_num[i[1][j]][i[0][j]] = 1  



                #Updating frequency of the transitions between pos
                if j < len(i[0])-1:
                    if i[1][j+1] in self.transition_num[i[1][j]]:
                        self.transition_num[i[1][j]][i[1][j+1]] += 1
                    else:
                        self.transition_num[i[1][j]][i[1][j+1]] = 1   

                        
        # Calculating Prior Probabilties
        # 1. prior prob of the word
        for i in self.num_words.keys():
            self.prob_words[i] = self.num_words[i]/self.total_num_words
            self.w_pos_prob[i] = {}
        # 2. prior prob of the pos
        for i in self.num_pos.keys():
            self.prob_pos[i] = self.num_pos[i]/self.total_num_words
            self.pos_w_prob[i] = {}
            self.transition_prob[i] = {}


        # Calculating intial state probabilities
        for i in self.pos_start_prob.keys():
            self.pos_start_prob[i] = self.pos_start_num[i]/len(data)

            
        #Calculating Emission probabilties
        # 1. word given the pos
        for i in self.w_pos_prob.keys():
            for j in self.w_pos_num[i].keys():
                self.w_pos_prob[i][j] = self.w_pos_num[i][j]/self.num_words[i]
        # 2. pos given the word
        for i in self.pos_w_prob.keys():
            for j in self.pos_w_num[i].keys():
                self.pos_w_prob[i][j] = self.pos_w_num[i][j]/self.num_pos[i]


        # Calculating Transition Probabilties
        for i in self.transition_prob.keys():
            for j in self.transition_num[i].keys():
                self.transition_prob[i][j] = self.transition_num[i][j]/(self.num_pos[i])

                
        
       
    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    def simplified(self, sentence):
        """Returns most likely POS tags of words in a sentence
           by using simple inference on Baye's Nets.
        :param sentence: List of words (string)
        :return: List of tags
        """

        pos=['adj','adv','adp','conj','det','noun','num','pron','prt','verb','x','.']
        
        #intially all the pos of words are set to adj instead of noun in skeletal code
        res=['adj']*len(sentence)

        for word in range (0,len(sentence)):
            p=0
            if sentence[word] in self.w_pos_prob.keys():
                for word2 in range(0,len(self.num_pos)):
                    #check the max probabilties
                    if self.w_pos_prob[sentence[word]].get(pos[word2],0)>p:
                        p=self.w_pos_prob[sentence[word]][pos[word2]]
                        res[word]=pos[word2]
        return res



    def hmm_viterbi(self,sentence):
        """Returns most likely POS tags of words in a sentence
           by performing Viterbi algorithm
        :param sentence: List of words (string)
        :return: List of tags
        """

        res= []
        tprob= []
        posl=['adj','adv','adp','conj','det','noun','num','pron','prt','verb','x','.']
        print(posl)

        for index,word in enumerate(sentence):
            tprob.append({})

            #update the emission probabilties
            for pos in posl:
                if word in self.pos_w_num[pos]:
                    emission_prob=self.pos_w_num[pos][word]
                else:
                    emission_prob=1e-6/self.num_pos[pos]
                #multiplying emission probs to the lookup table
                if index == 0:
                    if pos in self.pos_start_prob:
                        tprob[index][pos]={'prob':emission_prob*self.pos_start_prob[pos],'t_pos':None}
                    else:
                        tprob[index][pos]={'prob':emission_prob*1e-3,'t_pos':None}
                else:
                    var = {}
                    #multiplying transistion probs to the lookup table
                    for p in posl:
                        if pos in self.transition_prob[p]:
                            var[p]=tprob[index-1][p]['prob']*self.transition_prob[p][pos]
                        else:
                            var[p]=tprob[index-1][pos]['prob'] * 1e-5   
                        #probs fot t and t+1 timestamp
                        val_max,pos_max = max(zip(var.values(),var.keys()))
                        tprob[index][pos] = {'prob':emission_prob * val_max,'t_pos':pos_max}

        
        #finding max probability of the previous timestamp
        prob_maximum = max(x['prob'] for x in tprob[-1].values())
        prev_prob = None
        for pos, values in tprob[-1].items():
            if values['prob'] == prob_maximum:
                res.append(pos)
                prev_prob = pos
                break

        # Update the final probs in the lookup table 
        for index in range(len(tprob)-2,-1,-1):
            res.insert(0,tprob[index+1][prev_prob]['t_pos'])
            prev_prob = tprob[index+1][prev_prob]['t_pos']
        return res


    def complex_mcmc(self, sentence):
        """Returns most likely POS tags of words in a sentence
           by performing MCMC using Gibb's Sampling algorithm
        :param sentence: List of words (string)
        :return: List of tags
        """
        import random
        posl=['adj','adv','adp','conj','det','noun','num','pron','prt','verb','x','.']
        parts=[]
        #assign a random pos
        for i in sentence:
            parts.append(random.choice(posl))    
        # iteration over all the random sample
        for j in range(10000):
            for i in sentence:
                s,poss=0,{}
                # update the emission probabilties
                for label in posl:
                    if i in self.pos_w_prob[label]:
                        s+=self.pos_w_prob[label][i]
                        poss[label]=s
                # sample from a uniform distribution
                r=random.uniform(0,s)
                keys=list(poss.keys())
                
                #assign the updated pos from the sample
                for j in range(len(keys)-1):
                    if poss[keys[j]]<r<=poss[keys[j+1]]:
                        parts[sentence.index(i)]=keys[j+1]
        return parts
         

    



    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")


###References are cited below
###1.https://stackoverflow.com/questions/53733510/pos-tagger-in-python-without-nltk
###2.(Approach taken from but absolutely not reproduced as it is ) https://github.com/Sumeets2597/Artificial-Intelligence/blob/master/Probablity%20and%20NLP/POS%20tagging/pos_solver.py
###3.https://github.com/ssghule/Hidden-Markov-Models-and-Viterbi-in-Natural-Language-Processing/blob/master/pos_solver.py
