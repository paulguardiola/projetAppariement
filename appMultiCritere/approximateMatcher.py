#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shapely
import numpy as np
import math
import /Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_5/MultiCriteriaMatchingPython/util/text/approximateMatcher.py 

def distance(s1, s2) :
    # Step 1: initialize
    s1Length = len(s1)
    s2Length = len(s2)
    if s1Length == 0 : 
        return s2Length
    if s2Length == 0 : 
        return s1Length
    
    d = np.zeros((s1Length + 1, s2Length + 1))
    # Step 2: initialize first row and column
    for indexS1 in range(0,s1Length+1): 
        d[indexS1][0] = indexS1;
    
    for indexS2 in range(0,s2Length+1): 
        d[0][indexS2] = indexS2;
    

    # Step 3: examine characters from s1
    for indexS1 in range(1,s1Length+1): 
        charS1 = s1[indexS1 - 1]
        # Step 4: examine characters from s2
        for indexS2 in range(1,s2Length+1):
       
            charS2 = s2[indexS2 - 1]
            # Step 5: cost is 0 is characters are the same, 1 otherwise
            if charS1 == charS2 :
                cost = 0
            else : cost = 1
            # Step 6: set the cell cost to the min of its neighbours
            n1 = d[indexS1 - 1][indexS2] + 1
            n2 = d[indexS1][indexS2 - 1] + 1
            n3 = d[indexS1 - 1][indexS2 - 1] + cost
            d[indexS1][indexS2] = min(n1, min(n2, n3))
            
    # Step 7
    print(d)
    return d[s1Length][s2Length]


    
  