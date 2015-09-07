# -*- coding: utf-8 -*-
"""
Created on Sun Sep 06 14:21:43 2015

@author: Herbert
"""
import tree
import plotTree
import saveTree

fr = open('lenses.txt')
lensesData = [data.strip().split('\t') for data in fr.readlines()]
lensesLabel = ['age', 'prescript', 'astigmatic', 'tearRate']
lensesTree = tree.buildTree(lensesData, lensesLabel)
#print lensesData
print lensesTree

print plotTree.createPlot(lensesTree)