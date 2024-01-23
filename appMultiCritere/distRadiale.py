#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from shapely.geometry import Point, LineString
from shapely import wkt
import distGeom 
import distText
import distSemantique
import decision 
import geopandas as gpd
import numpy as np
import pandas as pd

def signature(geom):
    
    linestring = geom.boundary
    listCharPoint = str(linestring)[12:len(str(linestring))-1]
    
    listCharPoint = enleveVirgule(listCharPoint)
    
    lat , lon = '' , ''
    coord = 'lat'
    Point = []
    
    for i in range(len(listCharPoint)):
        #lat 
        if coord == 'lat' : 
            lat += listCharPoint[i]
            if listCharPoint[i] == " ": 
                coord = 'lon'
        else : 
            lon += listCharPoint[i]
            if listCharPoint[i] == " ": 
                coord = 'lat'
                Point.append((float(lat), float(lon)))
                lat = ''
                lon = ''
                
   
    centroid = geom.centroid
    liste = []
    
    liste.append((0,
                  ((centroid.x - Point[0][0])**2 + (centroid.y - Point[0][1])**2)**.5))
    
    dist = 0
    
    for k in range(1, len(Point)): 
        
        x = Point[k][0]
        y = Point[k][1]
        
        ordon = ((centroid.x - x)**2 + (centroid.y - y)**2)**.5
        absci = ((Point[k-1][0] - x)**2 + (Point[k-1][1] - y)**2)**.5
        
        liste.append((absci + dist , ordon))
        
        dist += absci
        
    a = liste[len(liste)-1][0]
    
    liste_norm = []
        
    for k in range(len(liste)):
        
        liste_norm.append((liste[k][0]/a , liste[k][1]))
    return liste_norm 

def enleveVirgule(string):
    char = ''
    for i in range(len(string)):
        if string[i] != ',':
            char += string[i]
    return char

def distanceRadiale(geomRef, geomComp):
    
    signRef = signature(geomRef)
    signComp= signature(geomComp)
            
    diff = abs(aire(signRef) - aire(signComp))
        
    return diff 


def aire(signature):
    ai = 0
    for k in range(len(signature)-1):
        dist = signature[k+1][0] - signature[k][0]
        if signature[k][1] < signature[k+1][0]:
            ai += dist * signature[k][1]
            ai += dist * ( signature[k+1][1] - signature[k][1] )/2
        else : 
            ai += dist * signature[k+1][1]
            ai += dist * ( signature[k][1] - signature[k+1][1] ) /2
            
    return ai
    

def critereRadiale (distance):
    
    seuil = 6
    
    tableau = []
    
    
    if distance < seuil : 
        tableau.append( 0.8 - (0.8/seuil) * distance )
        tableau.append( (0.8/seuil) * distance )
        tableau.append( 0.2 )
    else : 
        tableau.append( 0.1 )
        tableau.append( 0.8 )
        tableau.append( 0.1 )
        
    
	#Return 3 masses sous forme de tableau
    return tableau

if __name__ == "__main__" : 
    
    def readShapefile (url) :
        data  = gpd.read_file(url)
        columns = [data.columns[i] for i in range(len(data.columns)) ]
        popRef = []
        for i in range(len(data)):
            L = {}
            for j in range(len(columns)):
                L[columns[j]] = data[columns[j]][i]
            L['id_spatial'] = i
            popRef.append(L) 
        return popRef
    
    popRef = readShapefile("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/testMultiCritere/batiement/popRef.shp")
    popComp = readShapefile("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/testMultiCritere/batiement/popComp.shp")
    
    import matplotlib.pyplot as plt
    
    """
    x,y = [] , []
    for k in range(len(signature(popRef[0]['geometry']))):
        x .append(signature(popRef[0]['geometry'])[k][0])
        y. append(signature(popRef[0]['geometry'])[k][1])
   
    plt.plot(x,y)
    
    """
    
    
    print(aire(signature(popRef[0]['geometry'])))
    print(aire(signature(popRef[1]['geometry'])))
    
    for i in range(len(popRef)):
        for j in range(len(popComp)):
            a = abs(aire(signature(popRef[i]['geometry'])) - aire(signature(popComp[j]['geometry'])))
            print((i,j,a))
            print(distanceRadiale(popRef[i]['geometry'], popComp[j]['geometry']))
            
            
    display(popRef[2]['geometry'])
    display(popComp[8]['geometry'])


    
    
    