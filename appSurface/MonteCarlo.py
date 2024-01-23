#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import AppariementSurfaces 
import geopandas as gpd
import shapely
from shapely import wkt
from shapely.geometry import Polygon
 
def calcul_index(lien , popComp , popRef ):
    PP = 0 
    PN = 0 
    NP = 0 
    NN = 0  
    
    geomRef = [ popRef[i]["geometry"] for i in range(len(popRef)) ]
    geomCom = [ popComp[i]["geometry"] for i in range(len(popComp)) ]
    ref = gpd.GeoSeries( geomRef )
    com = gpd.GeoSeries( geomCom )
    inter = com.sindex.query(ref, predicate="intersects")
    
    lienSimple = [(inter[0][i] ,inter[1][i] ) for i in range(len(inter[0]))]
    
    PP += len(popRef)
    
    lien = [ (lien[k][0] , lien[k][1]) for k in range(len(lien))]
    lienNonApp = []
    lienApp    = []
    
    for i in range(len(lienSimple)):
        if lienSimple[i] not in lien : 
            lienNonApp.append(lienSimple[i])
        else :
            lienApp.append(lienSimple[i])
            idRef = lienSimple[i][0]
            idLie = lienSimple[i][1]
            geomRef = AppariementSurfaces.getGeom(idRef , popRef)
            geomLie = AppariementSurfaces.getGeom(idLie , popComp)
            inter = shapely.intersection(geomRef, geomLie)
            
            if inter.area / geomLie.area < 0.1 : 
                PN += 1
    
    lien_1 = [  lien[k][1]  for k in range(len(lien))]
    
    
    for i in range(len(lienNonApp)):
        
        idRef = lienNonApp[i][0]
        
        idLie = lienNonApp[i][1]
        geomRef = AppariementSurfaces.getGeom(idRef , popRef)
        geomLie = AppariementSurfaces.getGeom(idLie , popComp)
        inter = shapely.intersection(geomRef, geomLie)
        
        if inter.area / geomRef.area > 0.7 : 

            if idLie in lien_1 : 
                
                NP += 1
            else : 
                NN += 1
                
    PP = PP - NN - NP - PN
    
    index = {}
    
    precision = PP / ( PP + NP ) 
    recall = PP / ( PP + PN )
    F = 2*precision*recall / (precision + recall)
    
    index['precision'] = PP / ( PP + NP ) 
    index['recall'] = PP / ( PP + PN )
    #index['True negative rate'] = NN / ( NN + NP )
    index['F score'] = F
                
    return index
    
    
def getId(pop, indice):
    return pop[indice]['ID']
    
def ajoutLigne(param , url , index ):
    
    f = open(url,'a')  
    f.write('\n')
    f.write(str(param["surface_min_intersection"]))
    f.write(";")
    f.write(str(param["pourcentage_min_intersection"]))
    f.write(";")
    f.write(str(param["pourcentage_intersection_sur"]))
    f.write(";")
    f.write(str(param["distSurfMaxFinal"]))
    f.write(";")
    f.write(str(param["completudeExactitudeMinFinal"]))
    f.write(";")
    f.write(str(index["F score"]))
    f.write(";")
    f.write(str(index["recall"]))
    f.close()
    
def variationParam(popRef, popComp , url , param ):
    
    #f = open(url,'w')
    #f.write('AnneeBD1;AnneeBD2;SurfMinInter;PourMinInter;PourInterSurf;MinDistSurf;DistSurfMax;CompExacMax;RegrOpti;FiltFinal;ResoMin;ResoMax;Prec:Rec;RateNeg;F')
    #f.close()
    #a = param[parametre]
    for i in range(0,240):
        param = randomParam(param)
        
        lienFiltres = AppariementSurfaces.appariementSurfaces(popRef , popComp, param)
        
        index = calcul_index(lienFiltres, popComp, popRef)
        
        ajoutLigne(param , url , index)
        
def readTXT(url):
    data = []
    fil = open(url, "r")
    lignes = fil.readlines()
    for ligne in lignes:
        dataLigne = []
        a=0
        for i in range(1, len(ligne)):
            if ligne[i] == '"':
                dataLigne.append(ligne[a+1:i])
                a = i+1
        dataLigne.append(ligne[a+1:len(ligne)])
        data.append(dataLigne)
    data.pop(0)
    for p in range(len(data)):
        a = 0
        polygon=[]
        for k in range(len(data[p][0])):
            if data[p][0][k] == ",":
                polygon.append(data[p][0][a:k-2])
                a = k+1
        polygon[0] = polygon[0][12:len(polygon[0])]
        lat_long = []
        for i in range(len(polygon)):
            for j in range(len(polygon[i])):
                if polygon[i][j] == " ":
                    lat_long .append((float(polygon[i][0:j])
                                      ,float(polygon[i][j:len(polygon[i])])))
                    
        data[p][0] = Polygon(lat_long)
    
    dataset = []
    for k in range(len(data)):
        dataLigne = [data[k][0]]
        a=0
        for i in range(1, len(data[k][1])):
            if data[k][1][i] == ',':
                dataLigne.append(float(data[k][1][a:i]))
                a = i+1
        dataset.append(dataLigne)
    
    shape =[]
    for i in range(len(dataset)):
        pop = {}
        pop['id_spatial'] = dataset[i][1]
        pop['geometry'] = dataset[i][0]
        shape.append(pop)   
    
    return shape

def readTXT2(url):
    data = []
    fil = open(url, "r")
    lignes = fil.readlines()
    for ligne in lignes:
        dataLigne = []
        a=0
        for i in range(1, len(ligne)):
            if ligne[i] == '"':
                dataLigne.append(ligne[a+1:i])
                a = i+1
        dataLigne.append(ligne[a+1:len(ligne)])
        data.append(dataLigne)
    
    data.pop(0)        
    for p in range(len(data)):
        a = 0
        polygon=[]
        
        for k in range(len(data[p][0])):
            if data[p][0][k] == ",":
                polygon.append(data[p][0][a:k-2])
                a = k+1
            
        

        polygon[0] = polygon[0][12:len(polygon[0])]
        lat_long = []
        for i in range(len(polygon)):
            a = 0
            index = 0
            for j in range(len(polygon[i])):
                
                
                if polygon[i][j] == " " and a == 1:
                    lat_long .append((float(polygon[i][0:index])
                                      ,float(polygon[i][index:j])))
                    a = 0
            
                elif polygon[i][j] == " ":
                    a = 1
                    index = j
                    
        data[p][0] = Polygon(lat_long)
    
    dataset = []
    for k in range(len(data)):
        dataLigne = [data[k][0]]
        a=0
        for i in range(1, len(data[k][1])):
            if data[k][1][i] == ',':
                dataLigne.append(data[k][1][a:i])
                a = i+1
        dataset.append(dataLigne)
    
    shape =[]
    for i in range(len(dataset)):
        pop = {}
        pop['id_spatial'] = dataset[i][1]
        pop['geometry'] = dataset[i][0]
        shape.append(pop)   
    
    return shape


import random 
def randomParam (param):
    
    surface_min_intersection = random.random()
    pourcentage_min_intersection = random.random()
    pourcentage_intersection_sur = random.random()
    distSurfMaxFinal = random.random()
    completudeExactitudeMinFinal = random.random()
    
    param["surface_min_intersection"] = surface_min_intersection
    param["pourcentage_min_intersection"] = pourcentage_min_intersection
    param["pourcentage_intersection_sur"] = pourcentage_intersection_sur
    param["distSurfMaxFinal"] = distSurfMaxFinal
    param["completudeExactitudeMinFinal"] = completudeExactitudeMinFinal
    
    return param 


if __name__ == '__main__' : 
    
    param = {}
    param["surface_min_intersection"] = 1;        # a faire 
    param["pourcentage_min_intersection"] = 0.0;  # a faire 
    param["pourcentage_intersection_sur"] = 0.8;  # a faire 
    param["minimiseDistanceSurfacique"] = True;
    param["distSurfMaxFinal"] = 0.6;              # a faire 
    param["completudeExactitudeMinFinal"] = 0.3;  # a faire 
    param["regroupementOptimal"] = True;
    param["filtrageFinal"] = True;
    #param["ajoutPetitesSurfaces"] = True;
    #param["seuilPourcentageTaillePetitesSurfaces"] = 0.1;
    #param["persistant"] = False;
    param["resolutionMin"] = 1;
    param["resolutionMax"] = 11;
    
    #f = open('data.txt','w')
    #f.write('#;AnneeBD1;AnneeBD2;SurfMinInter;PourMinInter;PourInterSurf;MinDistSurf;DistSurfMax;CompExacMax;RegrOpti;FiltFinal;ResoMin;ResoMax;Prec:Rec;RateNeg;F')
    #f.close()
    
    #popRef = readTXT("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_4/testVT/bati_osm.txt")
    #popComp= readTXT2("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_4/testVT/bati_bdtopo.txt")
    

    
    popRef = AppariementSurfaces.readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_3/CentreUrbain/BD2023.shp")
    popComp = AppariementSurfaces.readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_3/CentreUrbain/BD2010.shp")
    #popRef = AppariementSurfaces.readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_3/CentreUrbain/BD2023.shp")
    #popComp = AppariementSurfaces.readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_3/CentreUrbain/BD2010.shp")
    #popRef = AppariementSurfaces.readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_3/Campagne/BD2023.shp")
    #popComp = AppariementSurfaces.readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_3/Campagne/BD2010.shp")
    #popRef = AppariementSurfaces.readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_4/Combourg/Pavillon/BD2023.shp")
    #popComp = AppariementSurfaces.readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_4/Combourg/Pavillon/BD2010.shp")
    
    #lienFiltres = AppariementSurfaces.appariementSurfaces(popRef , popComp, param)
    #index = calcul_index(lienFiltres, popComp, popRef)

    variationParam(popRef, popComp , 'data.txt' , param )
    
    
    
    
    
    
    



