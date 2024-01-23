import math 
from Operateurs import intersectionRobuste  
import Distances   
import shapely 
import shapefile
import numpy
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, LineString
import fiona
import pandas as pd
from shapely import wkt
import time 


def readShapefile (url) :
    data  = gpd.read_file(url)
    columns = [data.columns[i] for i in range(len(data.columns)) ]
    popRef = []
    for i in range(len(data)):
        L = {}
        for j in range(len(columns)):
            L[columns[j]] = data[columns[j]][i]
        popRef.append(L) 
    return popRef

def getGeometry(dataset):
    geometry =[]
    for i in range(len(dataset)):
        geometry.append(dataset[i]["geometry"])
    s = gpd.GeoSeries( geometry  )
    return s

def creerLiens_index(ref, comp):
    ref = getGeometry(ref)
    com = getGeometry(comp)
    lien = []
    for i in range(len(ref)):
        if len(ref.sindex.query(com, predicate="intersects")) != 0 : 
            for j in range(len(com)):
                if len(ref.sindex.query(com[i], predicate="intersects")) != 0  :
                    lien.append((i,j))
    return lien
    
def creerLiens(ref, comp):
    lien = []
    for i in range(len(ref)):
        geomRef = ref[i]['geometry']
        for j in range(len(comp)):
            geomCom = comp[j]['geometry']
            inter = shapely.intersection(geomRef , geomCom)
            if inter.is_empty is False  : 
                lien.append((i,j))
                    
    return lien

if __name__ == "__main__" : 
    
    BD1 = readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/Semain_2/qgis/Betton/BettonBD1.shp")
    BD2 = readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/Semain_2/qgis/Betton/BettonBD2.shp")
    BD3 = readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/Semain_2/qgis/Betton/BettonBD3.shp")
    BD4 = readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/Semain_2/qgis/Betton/BettonBD4.shp")
    
    s3 = getGeometry(BD1)
    s4 = getGeometry(BD2)
    
    a = time.time()
    s3 = s4.sindex.query(s3, predicate="intersects")
    lien = [(s3[0][i] , s3[1][i]) for i in range(len(s3[0]))]
    b = time.time()
    print(len(lien))
    print(b-a)

    a = time.time()
    lien = creerLiens_index(BD1, BD2)
    b = time.time()
    print(len(lien))
    print(b-a)


    
    
    