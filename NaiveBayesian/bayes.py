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

# print "The vocList is: "
# print vocList
print "The vocList is: "
print vocList

result = detectInput(vocList, loadData[0])
# print result

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
#print "trainMat : "
#print trainMat

# test the algorithm
def naiveBayesClassify(vec2Classify, p0, p1, pBase):
    p0res = sum(vec2Classify * p0) + log(1 - pBase)
    p1res = sum(vec2Classify * p1) + log(pBase)
    if p1res > p0res:
        return 1
    else:
        return 0

def testNaiveBayes():
    loadData, classLabel = loadDataSet()
    vocList = createNonRepeatedList(loadData)
    trainMat = []
    for doc in loadData:
         trainMat.append(detectInput(vocList, doc))
    p0, p1, pBase = trainNaiveBayes(array(trainMat), array(classLabel))
    testInput = ['love', 'my', 'dalmation']
    thisDoc = array(detectInput(vocList, testInput))
    print testInput, 'the classified as: ', naiveBayesClassify(thisDoc, p0, p1, pBase)
    testInput = ['stupid', 'garbage']
    thisDoc = array(detectInput(vocList, testInput))
    print testInput, 'the classified as: ', naiveBayesClassify(thisDoc, p0, p1, pBase)

# testNaiveBayes()

# test email

import re

def bagOfWords2VecMN(vocList, inputStream):
    returnVec = [0]*len(vocList)
    for word in inputStream:
        if word in vocList:
            returnVec[vocList.index(word)] += 1
    return returnVec

# split & compile test 
mysent = "This book is the best book in Python or M.L. I have ever laid!"
print mysent.split()

regEx = re.compile('\\W*')
listOfToken = regEx.split(mysent)
print listOfToken

tok = [tok.lower() for tok in listOfToken if len(tok) > 0]
print tok

emailText = open('email/ham/6.txt').read()
listOfToken = regEx.split(emailText)
tok = [tok.lower() for tok in listOfToken if len(tok) > 2]
print tok

# test the algorithm
def textSplit(String):
    import re
    listOfToken = re.split(r'\W*', String)
    return [tok.lower() for tok in listOfToken if len(tok) > 2]

def spamTest():
    docList = []; classList = []; fullText = []
    for i in range(1,26):
        wordList = textSplit(open('email/spam/%d.txt' %i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textSplit(open('email/ham/%d.txt' %i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)     
    vocList = createNonRepeatedList(docList)
    trainingSet = range(50); testSet = []
    for i in range(10): # test set
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat = []; trainClass = []
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2VecMN(vocList, docList[docIndex]))
        trainClass.append(classList[docIndex])
    p0, p1, pBase = trainNaiveBayes(array(trainMat), array(trainClass))
    errorCount = 0
    for docIndex in testSet:
        wordVector = bagOfWords2VecMN(vocList, docList[docIndex])
        if naiveBayesClassify(wordVector, p0, p1, pBase) != classList[docIndex]:
            errorCount += 1
    errorRate = float(errorCount)/ len(testSet)
    print "The error rate is: ", errorRate
    return errorRate, fullText

Rate = 0.0
for i in range(100): 
    error, a = spamTest()
    Rate += error
print 'The average error is: ', (Rate / 100)

# import RSS source
def calcFreq(vocList, fullText):
    import operator
    freqDict = {}
    for tok in vocList:
        freqDict[tok] = fullText.count(tok)
    sortedFreq = sorted(freqDict.iteritems(), key = operator.itemgetter(1), reverse = True)
    return sortedFreq[:30]

a, fullText = spamTest()
print calcFreq(vocList, fullText)

def localWords(feed1, feed0):
    import feedparser
    docList = []; classList = []; fullText = []
    minLen = min(len(feed1['entries']), len(feed0['entries']))
    for i in range(minLen):
        wordList = textSplit(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.append(docList)
        classList.append(1)
        wordList = textSplit(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.append(docList)
        classList.append(0)
    vocList = createNonRepeatedList(docList)
    top30Words = calcFreq(vocList, fullText)
    for delWord in top30Words:
        if delWord[0] in vocList:
            vocList.remove(delWord[0])
    trainingSet = range(2 * minLen); testSet = []
    for i in range(20):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat = []; trainClass = []
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2VecMN(vocList, docList[docIndex]))
        trainClass.append(classList[docIndex])
    p0, p1, pBase = trainNaiveBayes(array(trainMat), array(trainClass))
    errorCount = 0
    for docIndex in testSet:  # test
        wordVector = bagOfWords2VecMN(vocList, docList[docIndex])
        if naiveBayesClassify(wordVector, p0, p1, pBase) != classList[docIndex]:
            errorCount += 1
    print 'RSS source...The error rate is: ', float(errorCount) / len(testSet)
    return vocList, p0, p1


def testLocalWords():
    import feedparser
    ny = feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
    sf = feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
    vocList = localWords(ny, sf)
    return ny, sf

ny, sf = testLocalWords()

def getTopWords(ny, sf):
    import operator
    vocList, p0, p1 = localWords(ny, sf)
    topNY = [];topSF = []
    for i in range(len(p0)):
        if p0[i] > -6.0:
            topSF.append((vocList[i], p0[i]))
        if p1[i] > -6.0:
            topNY.append((vocList[i], p1[i]))     
    sortedSF = sorted(topSF, key=lambda pair: pair[1], reverse = True)
    print "SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF"
    for item in sortedSF:
        print item[0]
    sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse = True)
    for item in sortedNY:
        print item[0]
        
getTopWords(ny, sf)