# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018

"""
This is the main entry point for Part 1 of this MP. You should only modify code
within this file for Part 1 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

from collections import Counter
from math import log

def naiveBayes(train_set, train_labels, dev_set, smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each email
    example: suppose I had two emails 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two emails, first one was ham and second one was spam.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each email that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter --laplace (1.0 by default)
    pos_prior - positive prior probability (between 0 and 1)
    """
    # TODO: Write your code here
    # return predicted labels of development set

    # calculate the number of presences of words in each class
    spam_words = Counter()
    email_words = Counter()
    email_num = 0
    spam_num = 0
    for i in range(len(train_labels)):
        if train_labels[i]:
            email_words.update(train_set[i])
            email_num += 1
        else:
            spam_words.update(train_set[i])
            spam_num += 1

    # get the total words number
    spam_words_num = sum(spam_words.values())
    email_words_num = sum(email_words.values())
    # get prob for each class
    emailProb = email_num / (email_num + spam_num)
    spamProb = spam_num / (email_num + spam_num)

    # function for probability of P(word | class)   
    def email_prob(word):
        return (email_words[word] + smoothing_parameter) / (email_words_num + smoothing_parameter * len(email_words))
    def spam_prob(word):
        return (spam_words[word] + smoothing_parameter) / (spam_words_num + smoothing_parameter * len(spam_words))

    # function for calculate probability of P(class | words)
    def email(words):
        ret = log(emailProb)
        for word in words:
            ret += log(email_prob(word))
        return ret
    def spam(words):
        ret = log(spamProb)
        for word in words:
            ret += log(spam_prob(word))
        return ret

    # compare the probability for testing data set
    ret = []
    for words in dev_set:
        if email(words) > spam(words):
            ret.append(1)
        else:
            ret.append(0)
    return ret
    