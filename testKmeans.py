#!C:\Users\eric\PycharmProjects\TestDemo
# -*- coding: utf-8 -*-
# @Time    : 2018/12/20 20:18
# @Author  : Eric
# @Site    : 
# @File    : testKmeans.py
# @Software: PyCharm

from numpy import *
from kmeans import kmeans, showCluster

## step 1: load data
print "step 1: load data..."
dataSet = []
fileIn = open('C:\\Users\\eric\\Desktop\\kmean\\testSet.txt')
for line in fileIn.readlines():
    lineArr = line.strip().split('\t')
    dataSet.append([float(lineArr[0]), float(lineArr[1])])

## step 2: clustering...
print "step 2: clustering..."
dataSet = mat(dataSet)
k = 4
centroids, clusterAssment = kmeans(dataSet, k)

## step 3: show the result
print "step 3: show the result..."
showCluster(dataSet, k, centroids, clusterAssment)
