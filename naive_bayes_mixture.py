# naive_bayes_mixture.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018
# Modified by Jaewook Yeom 02/02/2020

"""
This is the main entry point for Part 2 of this MP. You should only modify code
within this file for Part 2 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

from collections import Counter
from math import log

def naiveBayesMixture(train_set, train_labels, dev_set, bigram_lambda,unigram_smoothing_parameter, bigram_smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each email
    example: suppose I had two emails 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two emails, first one was ham and second one was spam.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each email that we are testing on
              It follows the same format as train_set

    bigram_lambda - float between 0 and 1

    unigram_smoothing_parameter - Laplace smoothing parameter for unigram model (between 0 and 1)

    bigram_smoothing_parameter - Laplace smoothing parameter for bigram model (between 0 and 1)

    pos_prior - positive prior probability (between 0 and 1)
    """

    # TODO: Write your code here
    # return predicted labels of development set

    # get prob for unigram
    spam_uniwords = Counter()
    email_uniwords = Counter()
    for words, label in zip(train_set, train_labels):
        if label:
            email_uniwords.update(words)
        else:
            spam_uniwords.update(words)

    # get the total uni words number
    spam_uniwords_num = sum(spam_uniwords.values())
    email_uniwords_num = sum(email_uniwords.values())

    spam_biwords = Counter()
    email_biwords = Counter()
    for words, label in zip(train_set, train_labels):
        bigrams = zip(words[:-1], words[1:])
        if label:
            email_biwords.update(bigrams)
        else:
            spam_biwords.update(bigrams)

    # get the total bi words number
    spam_biwords_num = sum(spam_biwords.values())
    email_biwords_num = sum(email_biwords.values())
    #print("uni num ", len(spam_uniwords), len(email_uniwords))
    #print("bi num ", len(spam_biwords), len(email_biwords))
    #print(email_biwords.most_common(30))
    #print(email_uniwords.most_common(30))

    # function for probability of P(biword | class)   
    def email_uniprob(word):
        return (email_uniwords[word] + unigram_smoothing_parameter) / (email_uniwords_num + unigram_smoothing_parameter * len(email_uniwords))
    def spam_uniprob(word):
        return (spam_uniwords[word] + unigram_smoothing_parameter) / (spam_uniwords_num + unigram_smoothing_parameter * len(spam_uniwords))
    def email_biprob(biword):
        return (email_biwords[biword] + bigram_smoothing_parameter) / (email_biwords_num + bigram_smoothing_parameter * len(email_biwords))
    def spam_biprob(biword):
        return (spam_biwords[biword] + bigram_smoothing_parameter) / (spam_biwords_num + bigram_smoothing_parameter * len(spam_biwords))

    # function for calculate probability of P(class | words)
    def email_uni(words):
        ret = log(pos_prior)
        for word in words:
            ret += log(email_uniprob(word))
        return ret
    def spam_uni(words):
        ret = log(1-pos_prior)
        for word in words:
            ret += log(spam_uniprob(word))
        return ret
    def email_bi(words):
        ret = log(pos_prior)
        bigrams = zip(words[:-1], words[1:])
        for word_pair in bigrams:
            ret += log(email_biprob(word_pair))
        return ret
    def spam_bi(words):
        ret = log(1-pos_prior)
        bigrams = zip(words[:-1], words[1:])
        for word_pair in bigrams:
            ret += log(spam_biprob(word_pair))
        return ret

    # functions calculating probability for each class
    def email_prob(words):
        return bigram_lambda * email_bi(words) + (1-bigram_lambda) * email_uni(words)
    def spam_prob(words):
        return bigram_lambda * spam_bi(words) + (1-bigram_lambda) * spam_uni(words)

    # applay the trained model on the testing set
    ret = []
    for words in dev_set:
        if email_uni(words) > spam_uni(words):
            ret.append(1)
        else:
            ret.append(0)
    return ret