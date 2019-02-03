#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 00:34:41 2019

@author: zbit12
"""

import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

with open("cbcModel.pk","rb") as cbc:
    cbc = pickle.load(cbc)
    
ID = cbc[2][4]

#First, find best cluster
pos = np.inf
for idx, artID in enumerate(cbc[2]):
    if artID == ID:
        pos = idx
        break

vector = cbc[0][pos].todense()

bestSim = -np.inf
bestCentroidPosition = -np.inf

for idx, centroid in enumerate(cbc[1]):
    sim = cosine_similarity(centroid.reshape(1,-1), vector)
    if sim > bestSim:
        bestSim = sim
        bestCentroidPosition = idx
        
itemsInSameCluster = []

for idx, pos in enumerate(cbc[3]):
    if pos == bestCentroidPosition:
        itemsInSameCluster.append(idx)
    
vectorsToCompare = []
for i in itemsInSameCluster:
    vectorsToCompare.append((cbc[0][i], i))

similarities = [(cosine_similarity(vectorsToCompare[i][0], vector),vectorsToCompare[i][1])
                         for i in range(len(vectorsToCompare))]
similarities = sorted(similarities, reverse=True)[:5]

bestRecommendationIds = []
indices = [similarities[i][1] for i in range(len(similarities))]

for i in indices:
    bestRecommendationIds.append(cbc[2][i])
    
print(bestRecommendationIds)
