# -*- coding: utf-8 -*-
"""
Created on Fri Sep 04 01:15:01 2015

@author: Herbert
"""

import matplotlib.pyplot as plt

nonLeafNodes = dict(boxstyle = "sawtooth", fc = "0.8")
leafNodes = dict(boxstyle = "round4", fc = "0.8")
line = dict(arrowstyle = "<-")

def getLeafNum(tree):
    num = 0
    firstKey = tree.keys()[0]
    secondDict = tree[firstKey]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            num += getLeafNum(secondDict[key])
        else:
            num += 1
    return num
    
def getTreeDepth(tree):
    maxDepth = 0
    firstKey = tree.keys()[0]
    secondDict = tree[firstKey]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            depth = getTreeDepth(secondDict[key]) + 1
        else:
            depth = 1
        if depth > maxDepth:
            maxDepth = depth
    return maxDepth

def plotNode(nodeName, targetPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeName, xy = parentPt, xycoords = \
                            'axes fraction', xytext = targetPt, \
                            textcoords = 'axes fraction', va = \
                            "center", ha = "center", bbox = nodeType, \
                            arrowprops = line)
                            
def insertText(targetPt, parentPt, info):
    xCoord = (parentPt[0] - targetPt[0]) / 2.0 + targetPt[0]
    yCoord = (parentPt[1] - targetPt[1]) / 2.0 + targetPt[1]
    createPlot.ax1.text(xCoord, yCoord, info)
    
def plotTree(tree, parentPt, info):
    leafNum = getLeafNum(tree)
    treeDepth = getTreeDepth(tree)
    firstKey = tree.keys()[0]
    firstPt = (plotTree.xOff + (1.0 + float(leafNum)) / 2.0/plotTree.totalW,\
                plotTree.yOff)
    insertText(firstPt, parentPt, info)
    plotNode(firstKey, firstPt, parentPt, nonLeafNodes)
    secondDict = tree[firstKey]
    plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            plotTree(secondDict[key], firstPt, str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), \
                    firstPt, leafNodes)
            insertText((plotTree.xOff, plotTree.yOff), firstPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD

def createPlot(inTree):
    fig = plt.figure(1, facecolor = 'white')
    fig.clf()
    createPlot.ax1 = plt.subplot(111, frameon = False) #, **axprops)
    plotTree.totalW = float(getLeafNum(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5 / plotTree.totalW
    plotTree.yOff = 1.0
    plotTree(inTree, (0.5, 1.0), ' ')
    #plotNode(U'决策节点', (0.5, 0.1), (0.1, 0.5), nonLeafNodes)
    #plotNode(U'叶节点', (0.8, 0.1), (0.3, 0.8), leafNodes)
    plt.show()

def retrieveTree(i):
    listOfTrees = [{'no surfacing':{0: 'no', 1:{'flippers':{0:'no', 1:'yes'}}}},\
                    {'no surfacing':{0: 'no', 1:{'flippers':{0:{'head':{0:'no', \
                    1:'yes'}}, 1:'no'}}}}]
    return listOfTrees[i]
    
createPlot(retrieveTree(1))
