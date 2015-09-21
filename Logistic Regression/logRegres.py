# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 22:53:07 2015

@author: Herbert
"""

from numpy import *
sys.setrecursionlimit(1500)

def loadData():
    dataMat = []; labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineSplit = line.strip().split()
        dataMat.append([1.0, float(lineSplit[0]), float(lineSplit[1])])
        labelMat.append(int(lineSplit[2]))
    return dataMat, labelMat

def sigmoid(x):
    return 1.0 / (1 + exp(-x))
    
def gradAscent(data, label):
    dataMat = mat(data)
    labelMat = mat(label).transpose()
    m, n = shape(dataMat)
    alpha = 0.001
    maxCycles = 500
    w = ones((n, 1))
    for k in range(maxCycles):
        p = sigmoid(dataMat * w)
        error = labelMat - p
        w = w + alpha * dataMat.transpose() * error
    return dataMat, labelMat, w

data, label = loadData()
dataMat, labelMat, w = gradAscent(data, label)
print labelMat

def plotBestSplit(w):
    import matplotlib.pyplot as plt
    dataMat, labelMat = loadData()
    dataArr = array(dataMat)
    n = shape(dataArr)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        if int(labelMat[i]) == 1:
            xcord1.append(dataArr[i, 1]) # array only
            ycord1.append(dataArr[i, 2])
        else:
            xcord2.append(dataArr[i, 1])
            ycord2.append(dataArr[i, 2])            
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s = 30, c = 'red', marker = 's')
    ax.scatter(xcord2, ycord2, s = 30, c = 'blue')
    x = arange(-3.0, 3.0, 0.1)
    y = (-w[0] - w[1] * x) / w[2]
    ax.plot(x, y)
    plt.xlabel('x1'); plt.ylabel('x2');
    plt.show()

plotBestSplit(w.getA()) # ?

def stocGradAscent(data, label):
    m,n = shape(data)
    alpha = 0.01
    w = ones(n)
    for i in range(m):
        h = sigmoid(sum(data[i]) * w)
        error = label[i] - h
        w = w + alpha * error *data[i]
    return w

wNew = stocGradAscent(data, label)
plotBestSplit(wNew)

def stocGradAscentAdvanced(data, label, numIter = 150):
    m,n = shape(data)
    w = ones(n)
    for i in range(numIter):
        dataIndex = range(m)
        for j in range(m):
            alpha = 4 / (1.0 + i + j) + 0.01
            randIndex = int(random.uniform(0, len(dataIndex)))
            h = sigmoid(sum(data[randIndex] * w))
            error = label[randIndex] - h
            w = w + alpha * error* array(data[randIndex])
            del(dataIndex[randIndex])
    return w
    
wNewAdv = stocGradAscentAdvanced(data, label, numIter = 150)
plotBestSplit(wNewAdv)

def classifyVector(x, w):
    prob = sigmoid(sum(x * w))
    if prob > 0.5: return 1.0
    else: return 0.0
    
def horseColicTest():
    frTrain = open('horseColicTraining.txt')
    frTest = open('horseColicTest.txt')
    trainingData = []; trainingLabel = []
    for line in frTrain.readlines():
        currLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(currLine[i]))
        trainingData.append(lineArr)
        trainingLabel.append(float(currLine[21]))
    w = stocGradAscentAdvanced(array(trainingData), trainingLabel, numIter = 500)
    errorCount = 0.0; numOfTest = 0.0
    for line in frTest.readlines():
        numOfTest += 1.0
        currLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(currLine[i]))
        if int(classifyVector(array(lineArr), w)) != int(currLine[21]):
            errorCount += 1
    errorRate = float(errorCount) / numOfTest
    print "The error rate of this test is: %f" % errorRate
    return errorRate
    
def finalTest():
    numOfTest = 10; errorSum = 0.0
    for i in range(numOfTest):
        errorSum += horseColicTest()
    print "After %d iterations the average error rate is: %f" \
    % (numOfTest, errorSum / float(numOfTest))
          
finalTest()
        