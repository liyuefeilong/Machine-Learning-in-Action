# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 14:36:02 2015

Input:   data: vector of test sample (1xN)
         sample: size m data set of known vectors (NxM)
         labels: labels of the sample (1xM vector)
         k: number of neighbors
            
Output:  the class label

@author: peng__000
"""

from numpy import *
import numpy as np
import operator
from os import listdir

# training samples
sample = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])

# the labels of samples
label = ['A', 'A', 'B', 'B']

def classify(data, sample, label, k):
    SampleSize = sample.shape[0]
    DataMat = tile(data, (SampleSize, 1))
    delta = (DataMat - sample)**2
    distance = (delta.sum(axis = 1))**0.5 # 
    sortedDist = distance.argsort()
    classCount = {}
    
    for i in range(k):
        votedLabel = label[sortedDist[i]]
        classCount[votedLabel] = classCount.get(votedLabel, 0) + 1    
    result = sorted(classCount.iteritems(), key = operator.itemgetter(1), reverse = True)
    return result[0][0]

#print classify([10,0], sample, label, 3)

def file2matrix(filename):
    fil = open(filename)
    fileLines = fil.readlines() # Convert the contents of a file into a list
    lenOfLines = len(fileLines)
    Mat = zeros((lenOfLines, 3))
    classLabel = []
    index = 0
    for line in fileLines:
        line = line.strip()
        listFromLine = line.split('\t')
        Mat[index,: ] = listFromLine[0:3]
        classLabel.append(int(listFromLine[-1])) # the last one of listFromLine is Label
        index += 1
    return Mat, classLabel

mat,label = file2matrix('datingTestSet2.txt')

print mat, label

# draw 

import matplotlib
import matplotlib.pyplot as plt

fil = open('datingTestSet2.txt')
fileLines = fil.readlines() # Convert the contents of a file into a list
lenOfLines = len(fileLines)

figure = plt.figure()
axis = figure.add_subplot(111)
lab = ['didntLike', 'smallDoses', 'largeDoses']

for i in range(3):
    n = []
    l = []
    for j in range(lenOfLines):
        if label[j] == i + 1:
            n.append(list(mat[j,0:3]))
            l.append(label[j])
    n = np.array(n)   # list to numpy.adarray
    #reshape(n, (3,k))
    axis.scatter(n[:,1], n[:,2], 15.0*array(l), 15.0*array(l), label = lab[i])
print type(mat)
print type(n)
plt.legend()
plt.show()

def Normalize(data):
    minValue = data.min(0)
    maxValue = data.max(0)
    ValueRange = maxValue - minValue
    norm_data = zeros(shape(data))
    k = data.shape[0]
    norm_data = data - tile(minValue, (k, 1))
    norm_data = norm_data / tile(ValueRange, (k, 1))
    return norm_data, ValueRange, minValue

def WebClassTest():
    ratio = 0.1
    dataMat, dataLabels = file2matrix('datingTestSet2.txt') 
    normMat, ValueRange, minValue = Normalize(dataMat)
    k = normMat.shape[0]
    num = int(k * ratio) # test sample : 10%
    errorCount = 0.0
    for i in range(num):
        result = classify(normMat[i,:], normMat[num:k,:],\
                          dataLabels[num:k], 7) # k = 3
        print "The classifier came back with: %d, the real answer is %d"\
                % (result, dataLabels[i])
        if (result != dataLabels[i]): errorCount += 1
    print "The total error rate is %f " % (errorCount / float(num))

WebClassTest()

# Test 2

def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect

def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('trainingDigits')    #load the training set
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]     # take off .txt
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)
    testFileList = listdir('testDigits')        # iterate through the test set
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]     # take off .txt
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classify(vectorUnderTest, trainingMat, hwLabels, 7) # k = 3
        print "The classifier came back with: %d, the real answer is: %d"\
        % (classifierResult, classNumStr)
        if (classifierResult != classNumStr): errorCount = errorCount + 1.0
    print "\nThe total number of errors is: %d" % errorCount
    print "\nThe total error rate is: %f" % (errorCount/float(mTest))
    
#handwritingClassTest()