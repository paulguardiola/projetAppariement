#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shapely
from shapely.geometry import Polygon, MultiPolygon
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import LineString
import pyproj
from pyproj import CRS
import math

def Orientation(geom):
    
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
    
    Point.append(Point[0])

    Point1 = 0
    Point2 = 0
    dist = 0 
    
    for i in range(len(Point)-1):
        if distanceEucl(Point[i],Point[i+1]) > dist :
            Point1 = Point[i] 
            Point2 = Point[i+1] 
            dist = distanceEucl(Point[i],Point[i+1])
       
    if Point1[1] < Point2[1] : 
        PointBas , PointHaut = Point1 , Point2
    else : 
        PointBas , PointHaut = Point2 , Point1
        
    PointCreer = (PointBas[0] + 1 , PointBas[1])
    
    distBasHaut  = distanceEucl(PointBas,PointHaut)
    distBasCree  = distanceEucl(PointBas,PointCreer)
    distHautCree = distanceEucl(PointCreer,PointHaut)
    
    if distBasHaut > distBasCree and distBasHaut > distHautCree : 
        cos_gamma = (distBasCree**2 + distHautCree**2 - distBasHaut**2) / (2*distHautCree*distBasCree)   
    elif distBasCree > distBasHaut and distBasCree > distHautCree : 
        cos_gamma = (distBasHaut**2 + distHautCree**2 - distBasCree**2) / (2*distHautCree*distBasHaut)
    else : 
        cos_gamma = (distBasHaut**2 + distBasCree**2 - distHautCree**2) / (2*distBasCree*distBasHaut)

    gamma = math.acos(cos_gamma)
    
    return math.pi - gamma

def enleveVirgule(string):
    char = ''
    for i in range(len(string)):
        if string[i] != ',':
            char += string[i]
    return char

def distanceEucl(Point1, Point2):
    distance = ((Point1[0] - Point2[0] )**2 + (Point1[1]  - Point2[1] )**2)**.5
    return distance 

def critereOrientation (orientationRef , orientationComp ):
    
    seuil = math.pi/2
    
    distance = abs(orientationComp - orientationRef)
    
    tableau = []
    
    
    if distance < seuil : 
        tableau.append( 0.8 - (0.8/seuil) * distance )
        tableau.append( (0.8/seuil) * distance )
        tableau.append( 0.2 )
    else : 
        distance = distance - seuil
        tableau.append( (0.8/seuil) * distance )
        tableau.append( 0.8 - (0.8/seuil) * distance  )
        tableau.append( 0.2 )
        
    
	#Return 3 masses sous forme de tableau
    return tableau

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

if __name__ == "__main__" : 
    
    popRef = readShapefile("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/testMultiCritere/batiReconstruit/popRef.shp")
    
    
    geomRef = popRef[2]['geometry']
    geomComp = popRef[1]['geometry']
    
    orientationRef = Orientation(geomRef)
    orientationComp = Orientation(geomComp)
    
    
    display(geomRef)
    display(geomComp)
    
    print(orientationRef)
    print(orientationComp)
    print(abs(orientationComp - orientationRef))
    
    
    print(critereOrientation(orientationRef, orientationComp))
    #print(geom)
    #display(geom)




