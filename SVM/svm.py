# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 00:24:47 2015

@author: Herbert
"""

from numpy import *
from time import sleep

def loadData(fileName):
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMat.append([float(lineArr[0]), float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat, labelMat

def seleteJrand(i, m):
    j = i
    while (j == i):
        j = int(random.uniform(0, m))
    return j
    
def keepAlphaValue(aj, H, L):
    if aj > H:
        aj = H
    if aj < L:
        aj = L
    return aj

def SMOsimple(data, classLabel, C, toler, maxIter):
    dataMat = mat(data); labelMat = mat(classLabel).transpose()
    m, n = shape(dataMat)
    b = 0, iter = 0
    alpha = mat(zeros(m, 1))
    while (iter < maxIter):
        alphaPairsChanged = 0
        for i in range(m):
            fi = float(multiply(alpha, labelMat).T*\
                       (dataMat * dataMat[i, :].T)) + b
            Errori = fi - float(classLabel[i])
            if ((labelMat[i] * Errori < -toler) and (alpha[i] < C)) or \
               ((labelMat[i] * Errori > toler) and (alpha[i] > 0)):
                   j = seleteJrand(i, m)  # the second alpha
                   fj = float(multiply(alpha, labelMat).T*\
                              (dataMat * dataMat[j ,:].T)) + b
                   Errorj = fj = float(classLabel[j])
                   alphaIold = alpha[i].copy()
                   laphaJold = alpha[j].copy()
                   if (labelMat[i] != labelMat[j]):
                       H = min(C, C + alpha[j] - alpha[i])
                       L = max(0, alpha[j] - alpha[i])
                   else:
                       H = min(C, alpha[j] + alpha[i])
                       L = max(0, alpha[j] + alpha[i] - C)
                   if (H == L):
                       print "H == L"
                       continue
                   eta = 2.0 * dataMat[i, :] * dataMat[j, :].T - \
                         dataMat[i, :] * dataMat[i, :].T - \
                         dataMat[j, :] * dataMat[j, :].T