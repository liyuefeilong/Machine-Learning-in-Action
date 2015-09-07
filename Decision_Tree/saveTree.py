# -*- coding: utf-8 -*-
"""
Created on Sun Sep 06 01:56:04 2015

@author: Herbert
"""

import pickle

def storeTree(tree, filename):
    fw = open(filename, 'w')
    pickle.dump(tree, fw)
    fw.close()

def getTree(filename):
    fr = open(filename)
    return pickle.load(fr)