# -*- coding: utf-8 -*-
"""
Created on Tue Sep 08 16:12:55 2015

@author: Administrator
"""

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    listClass = [0, 1, 0, 1, 0, 1]
    return postingList, listClass

def createNonRepeatedList(data):
    vocList = set([])
    for doc in data:
        vocList = vocList | set(doc)
    return list(vocList)

def detectInput(vocList, inputStream):
    returnVec = [0]*len(vocList)
    for word in inputStream:
        if word in vocList:
            returnVec[vocList.index(word)] = 1 # ?
        else:
            print "The word :%s is not in the vocabulary!" % word
    return returnVec