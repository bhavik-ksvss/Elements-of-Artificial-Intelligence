# SeekTruth.py : Classify text objects into two categories
#
# Author: Sagar, Bhavik, Brendan
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys

import threading
import time


def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#

def classifier(train_data, test_data):
    # This is just dummy code -- put yours here!
    bwords = {} #contains truthfull and deceptive count of each word
    spl_chars = {'~', ':', "'", '+', '[', '\\', '@', '^', '{', '%', '(', '-', '"', '*', '|', ',', '&', '<', '`', '}', '.', '_', '=',
     ']', '!', '>', ';', '?', '#', '$', ')', '/'}

    for i in range(len(train_data["objects"])-1):
        for char in spl_chars: #to seperate special characters from the words
                train_data['objects'][i]=train_data["objects"][i].replace(char," "+char)
        #the below code counts truthfull and deceptive counts of each word and stores the counts in bwords dictionary
        for j in train_data["objects"][i].strip().split():
            if train_data["labels"][i]=="truthful" and j.strip().lower() in bwords :
                truthfull_count,deceptive_count=bwords[j.strip().lower()]
                #bwords.update({j.strip().lower():(a+1,b)})
                bwords[j.strip().lower()]=truthfull_count+1,deceptive_count
            elif train_data["labels"][i]=="deceptive" and j.strip().lower() in bwords:
                truthfull_count,deceptive_count = bwords[j.strip().lower()]
                #bwords.update({j.strip().lower(): (a, b+1)})
                bwords[j.strip().lower()]=truthfull_count,deceptive_count+1
            elif train_data["labels"][i] == "truthful" and j.strip().lower() not in bwords:
                #bwords.update({j.strip().lower(): (1,0)})
                bwords[j.strip().lower()]=1,0
            elif train_data["labels"][i] == "deceptive" and j.strip().lower() not in bwords:
                #bwords.update({j.strip().lower(): (0,1)})
                bwords[j.strip().lower()]=0,1
            else:
                continue
    truthfull_label__count=train_data["labels"].count("truthful")  #truthfull label count
    deceptive_label_count=train_data["labels"].count("deceptive")   # deceptive label count
    total_labels_count=(train_data["labels"].count("truthful")+train_data["labels"].count("deceptive")) #total label count
    prob_truthful_train=truthfull_label__count/total_labels_count #probabilty of truthfull labels
    prob_deceptive_train=deceptive_label_count/total_labels_count #probability of deceptive labels

    final_proba = {} #to store prior probabilities of each word

    final = []

    for i in bwords:
        truthfull_count,deceptive_count=bwords[i]
        #final_proba.update({i:((truthfull_count/(truthfull_count+deceptive_count)), (deceptive_count/(truthfull_count+deceptive_count)))})
        final_proba[i]=(truthfull_count/(truthfull_count+deceptive_count)), (deceptive_count/(truthfull_count+deceptive_count))
    
    

    

    for i in test_data["objects"]:
        for char in spl_chars:
            i.replace(char," "+char)
        p1=prob_truthful_train
        p2=prob_deceptive_train      
        for j in i.strip().split():
            if  j.strip().lower() not in list(final_proba.keys()):
                continue
            else:
                x,y = final_proba[j.strip().lower()]
                if x!=float(0):
                  p1*=x
                if y!=float(0):
                  p2*=y
        if p1/p2>1:
            final.append("truthful")
        else:
            final.append("deceptive")
    return  final


if __name__ == "__main__":
    if len(sys.argv) != 3:
         raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
