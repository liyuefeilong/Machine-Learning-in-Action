# -*- coding: utf-8 -*-
"""
Created on Tue Sep 08 16:12:55 2015

@author: Administrator
"""

from numpy import *

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
    
loadData, dataLabel = loadDataSet()
vocList = createNonRepeatedList(loadData)
print vocList

result = detectInput(vocList, loadData[0])
print result

def trainNaiveBayes(trainMatrix, classLabel):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pBase = sum(classLabel) / float(numTrainDocs)
    # The following Settings aim at avoiding the probability of 0
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    p0Denom = 2.0
    p1Denom = 2.0
    for i in range(numTrainDocs):
        if classLabel[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])            
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])       
    p0 = log(p0Num / p0Denom)
    p1 = log(p1Num / p1Denom)
    return p0, p1, pBase
            
trainMat = []
for doc in loadData:
    trainMat.append(detectInput(vocList, doc))

p0,p1,pBase = trainNaiveBayes(trainMat, dataLabel)
print "trainMat : "
print trainMat
#print p0, p1

# test the algorithm
def naiveBayesClassify(vec2Classify, p0, p1, pBase):
    p0res = sum(vec2Classify * p0) + log(1 - pBase)
    p1res = sum(vec2Classify * p1) + log(pBase)
    if p1res > p0res:
        return 1
    else:
        return 0

