# -*- coding: utf-8 -*-
"""
Created on Wed Sep 02 23:29:46 2015

@author: Herbert
"""

from math import log 
import operator

def Entropy(data):  
    dataNum = len(data)    
    LabelsCounts = {}    
    for feature in data:    
        Labels = feature[-1]
        if Labels not in LabelsCounts.keys():
            LabelsCounts[Labels] = 0
        LabelsCounts[Labels] += 1
    
    ent = 0.0
    for key in LabelsCounts:
        p = float(LabelsCounts[key]) / dataNum
        ent -= p * log(p, 2)

    return ent

# test the Rntropy function
def CreateDate():
    data = [[1,1,'yes'], [1,1,'yes'], [1,0,'no'], [0,1,'no'],[0,1,'no']]
    labels = ['no surfacing', 'flippers']
    return data, labels

data, labels = CreateDate()
# print data
print Entropy(data)

def splitData(data, k, value): # selete the kth feature , return the value of the feature
    result = []
    for feature in data:
        if feature[k] == value:
            reducedFeature = feature[:k]
            reducedFeature.extend(feature[k + 1:])
            result.append(reducedFeature)
    return result

print splitData(data, 1, 1)

# choose the best feature to split the data
def bestFeature(data):
    featureNum = len(data[0]) - 1 
    baseEntropy = Entropy(data)
    infoGain = 0.0; LargestGain = 0.0; bestFeature = -1
    for i in range(featureNum):
        featList = [example[i] for example in data]
        featList = set(featList) # Remove duplicate labels
        ent = 0.0
        for value in featList:
            splitResult = splitData(data, i, value)
            p = float(len(splitResult)) / len(data)
            ent -= p * Entropy(splitResult)
        infoGain = baseEntropy + ent
        if infoGain > LargestGain:
            LargestGain = infoGain
            bestFeature = i
    return bestFeature
        
print bestFeature(data)

def DefineLeafNodes(classList):
    classCount = {}
    for vote in classCount:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted()
    return sortedClassCount[0][0]
    
def buildTree(data, labels):
    classList = [example[-1] for example in data]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(data[0]) == 1:
        return DefineLeafNodes(classList)
    bestFeat = bestFeature(data)
    FeatureLabel = labels[bestFeat]
    tree = {FeatureLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in data]
    featValues = set(featValues)  # Remove duplicate values
    for value in featValues:
        newLabels = labels[:]
        tree[FeatureLabel][value] = buildTree(splitData(data, bestFeat,\
                                        value), newLabels)
    return tree

# use date & labels
tree = buildTree(data, labels)
print tree

import plotTree
plotTree.createPlot(tree)

def classify(tree, featLabels, test):
    firstKey = tree.keys()[0]
    secondDict = tree[firstKey]
    featIndex = featLabels.index(firstKey)
    for key in secondDict.keys():
        if test[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, test)
            else: classLabel = secondDict[key]
    return classLabel

