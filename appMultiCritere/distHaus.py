#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shapely

def distanceHausdorff(geomRef, geomComp):
    
    distance = shapely.hausdorff_distance(geomRef, geomComp)
    
    return distance 

def CritereHaus (dist):
    
    # même que critereGeom attends de voir le scipt d'ibrahim 
    
    distNorm = dist
    seuilT1 = 7
    seuilT2 = 13
    
    tableau = []
    if distNorm < seuilT1 : 
        tableau.append ( (-0.9/seuilT2) * distNorm + 1 )
        tableau.append(0 )
        tableau.append((0.9/seuilT2) * distNorm )
    elif distNorm < seuilT2 : 
        tableau.append((-0.9/seuilT2) * distNorm + 1)
        tableau.append(0.8 / (seuilT2 - seuilT1) * distNorm - 0.8 * seuilT1 / (seuilT2 - seuilT1) )
        tableau.append((0.1*seuilT2 - 0.9*seuilT1) / (seuilT2*(seuilT2 - seuilT1)) * distNorm +  0.8 * seuilT1  / (seuilT2 - seuilT1))
    else :
        tableau.append( 0.1)
        tableau.append(0.8)
        tableau.append(0.1)
    
	#Return 3 masses sous forme de tableau
    return tableau;




