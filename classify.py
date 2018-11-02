
from numpy import *
import operator


def kNNClassify(newInput, dataSet, labels, k):
    numSamples = dataSet.shape[0]   
    diff = tile(newInput, (numSamples, 1)) - dataSet 
    squaredDiff = diff ** 2  
    squaredDist = sum(squaredDiff, axis = 1)   
    distance = squaredDist ** 0.5  
    sortedDistIndices = argsort(distance)
    classCount = {} # define a dictionary (can be append element)
    for i in xrange(k):
        voteLabel = labels[sortedDistIndices[i]]
        classCount[voteLabel] = classCount.get(voteLabel, 0) + 1
    maxCount = 0
    for key, value in classCount.items():
        if value > maxCount:
            maxCount = value
            maxIndex = key

    return maxIndex
