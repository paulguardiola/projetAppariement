#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shapely

def distanceEuclidienne(geomRef, geomComp):
    centroidRef = geomRef.centroid
    centroidComp = geomComp.centroid
    distance = ((centroidRef.x - centroidComp.x)**2 + (centroidRef.y - centroidComp.y)**2)**.5
    return distance 

def CritereGeom (dist , seuilT1 , seuilT2):

    distNorm = dist
    
    tableau = []
    if distNorm < seuilT1 : 
        tableau.append((-0.9/seuilT2) * distNorm + 1)
        tableau.append(0)
        tableau.append((0.9/seuilT2) * distNorm)
    elif distNorm < seuilT2 : 
        tableau.append((-0.9/seuilT2) * distNorm + 1)
        tableau.append(0.8 / (seuilT2 - seuilT1) * distNorm - 0.8 * seuilT1 / (seuilT2 - seuilT1) )
        tableau.append((0.1*seuilT2 - 0.9*seuilT1) / (seuilT2*(seuilT2 - seuilT1)) * distNorm +  0.8 * seuilT1  / (seuilT2 - seuilT1))
    else :
        tableau.append(0.1)
        tableau.append(0.8)
        tableau.append(0.1)
    
	#Return 3 masses sous forme de tableau
    return tableau;
	