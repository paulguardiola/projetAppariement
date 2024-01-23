#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from shapely.geometry import Point, LineString
from shapely import wkt
import distGeom 
import distText
import distSemantique
import decision 
import distOrientation
import distHaus
import distRadiale
import geopandas as gpd
import numpy as np
import pandas as pd


def main(popRef, popComp):
    
    listeCandidat = SelectionCandidat2(popRef, popComp)
    
    """
    # calcul nombre de candidat 
    a=0
    for k in range(len(listeCandidat[1])) : 
        a+= len(listeCandidat[1][k])
    print(a/len(listeCandidat[0]))
    """
    
    
    listPopRef = listeCandidat[0]
    listPopComp = listeCandidat[1]
    
    listDeci = []
    
    for i in range(len(listPopComp)):
        
        deci = doAppariement(listPopRef[i], listPopComp[i])
        
        if deci == "NA":
            listDeci.append((listPopRef[i][0] , 0))
            continue
        else :
            decision = int(deci[1])
            
            
        
        listDeci.append((listPopRef[i][0] , listPopComp[i][decision-1][0]))
    
        
    return listDeci


def doAppariement(listPopRef, listPopComp):
    
 

    listCritere = []
    
    idRef = listPopRef[0]
    geomRef = listPopRef[1]
    #nomRef  = listPopRef[2]
    #natRef = listPopRef[3]
    
    
    
    for i in range(len(listPopComp)):
        
        
        #print((listPopRef[0] , listPopComp[i][0]))
        listCritere_i = []
        
        idComp = listPopComp[i][0]
        geomComp = listPopComp[i][1]
        #nomComp  = listPopComp[i][2]
        #natComp  = listPopComp[i][3]
   
   
        #Critere géométrique
        dg = distGeom.distanceEuclidienne(geomRef , geomComp)
        cg = distGeom.CritereGeom(dg , 5 , 7)
        #print(cg)
        listCritere_i.append(cg)
        
        dg = distGeom.distanceEuclidienne(geomRef , geomComp)
        cg = distGeom.CritereGeom(dg , 5 , 7)
        #print(cg)
        listCritere_i.append(cg)
        
        if idRef == 182 : 
            print(idComp)
            print(cg)
 
        """
        
        # Critere hausdorff
        dh = distHaus.distanceHausdorff(geomRef, geomComp)
        ct = distHaus.CritereHaus(dh)
        listCritere_i.append(ct)
       
   
        
        # Critere orientation
        orientationRef  = distOrientation.Orientation(geomRef) 
        orientationComp = distOrientation.Orientation(geomComp)
        co = distOrientation.critereOrientation(orientationRef , orientationComp)
        listCritere_i.append(co)
        
    
   
        # Critere radiale
        dr  = distRadiale.distanceRadiale(geomRef, geomComp) 
        cr = distRadiale.critereRadiale(dr)
        listCritere_i.append(cr)
        
 
        
        # Critere toponymique
        ds = distText.distanceSamal(nomRef, nomComp)
        #print((nomRef , nomComp))
        ct = distText.CritereToponymique(ds , nomRef, nomComp , 0.6)
        #print(ct)
        #print(" ")
        listCritere_i.append(ct)
        
        #Critere sémantique
        dwp = distSemantique.DistanceWuPalmer("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_5/MultiCriteriaMatchingPython/main/GeOnto.owl", natRef, natComp)
        cs = distSemantique.CritereSemantique(dwp , natRef, natComp , 0.8)
        listCritere_i.append(cs)
        """
        
        listCritere . append(listCritere_i)
    
    
    lres = decision.dempster(listCritere)

    
    return lres


    #lres = evidenceAlgoFusionCritere.appariementObjet(ref, candidatListe)
    
    
    #TableauResultatFrame tableauPanel = new TableauResultatFrame()
    #tableauPanel.displayEnsFrame("tests", lres)
    #int[] tab = tableauPanel.analyse()
    #System.out.println("NB non-app : " + tab[0]);
    #System.out.println("NB app : " + tab[1]);
    #System.out.println("NB d'indécis : " + tab[2]);
    #System.out.println("NB sans candidat : " + nbSansCandidat);
        
    #ExportToCSV.exportAppariement(listCritere, evidenceAlgoFusionCritere.getSeuilIndecision(), lres, "./data/resu")
      
def SelectionCandidat(popRef, popComp):
    
    idRef   = [ popRef[i]["id"] for i in range(len(popRef)) ]
    idComp   = [ popComp[i]["id"] for i in range(len(popComp)) ]
    geomCom = [ popComp[i]["geometry"] for i in range(len(popComp)) ]
    infoCom = [ ( popComp[i]["NOM"] , popComp[i]["NATURE"] ) for i in range(len(popComp)) ]
    geomRef = [ popRef[i]["geometry"] for i in range(len(popRef)) ]
    infoRef = [ ( popRef[i]["NOM"] , popRef[i]["NATURE"] ) for i in range(len(popRef)) ]
    
    ref = gpd.GeoSeries( geomRef )
    ref_buffer = ref.buffer(30)
    com = gpd.GeoSeries( geomCom )
    
    inter = com.sindex.query(ref_buffer, predicate="intersects")
    
    # creation liste popRef 
    listeRef = [(idRef[inter[0][0]] , geomRef[inter[0][0]], infoRef[inter[0][0]][0] , infoRef[inter[0][0]][1])]
    for i in range(len(inter[0])-1):
        if inter[0][i] == inter[0][i+1]:
            continue 
        else :
            listeRef.append((idRef[inter[0][i+1]] , geomRef[inter[0][i+1]], infoRef[inter[0][i+1]][0] , infoRef[inter[0][i+1]][1]))
    
    # creation liste popComp 
    listeComp   = []
    listeComp_i = [(idComp[inter[1][0]] , geomCom[inter[1][0]], infoCom[inter[1][0]][0] , infoCom[inter[1][0]][1])]
    
    for i in range(len(inter[0])-1):
        if inter[0][i] == inter[0][i+1]:
            listeComp_i . append((idComp[inter[1][i+1]] , geomCom[inter[1][i+1]], infoCom[inter[1][i+1]][0] , infoCom[inter[1][i+1]][1]))
        else :
            listeComp . append(listeComp_i)
            listeComp_i = [(idComp[inter[1][i+1]] , geomCom[inter[1][i+1]], infoCom[inter[1][i+1]][0] , infoCom[inter[1][i+1]][1])]
    listeComp . append(listeComp_i)
    
    
    return (listeRef , listeComp)

def SelectionCandidat2(popRef, popComp):
    
    idRef   = [ popRef[i]["FID"] for i in range(len(popRef)) ]
    idComp   = [ popComp[i]["FID"] for i in range(len(popComp)) ]
    geomCom = [ popComp[i]["geometry"] for i in range(len(popComp)) ]
    geomRef = [ popRef[i]["geometry"] for i in range(len(popRef)) ]
    
    ref = gpd.GeoSeries( geomRef )
    ref_buffer = ref.buffer(3)
    com = gpd.GeoSeries( geomCom )
    
    inter = com.sindex.query(ref_buffer, predicate="intersects")
    
    # creation liste popRef 
    listeRef = [(idRef[inter[0][0]] , geomRef[inter[0][0]])]
    for i in range(len(inter[0])-1):
        if inter[0][i] == inter[0][i+1]:
            continue 
        else :
            listeRef.append((idRef[inter[0][i+1]] , geomRef[inter[0][i+1]]))
    
    # creation liste popComp 
    listeComp   = []
    listeComp_i = [(idComp[inter[1][0]] , geomCom[inter[1][0]])]
    
    for i in range(len(inter[0])-1):
        if inter[0][i] == inter[0][i+1]:
            listeComp_i . append((idComp[inter[1][i+1]] , geomCom[inter[1][i+1]]))
        else :
            listeComp . append(listeComp_i)
            listeComp_i = [(idComp[inter[1][i+1]] , geomCom[inter[1][i+1]])]
    listeComp . append(listeComp_i)
    
    
    return (listeRef , listeComp)
    
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
    
def writeShapefile (data, url) :
    """
    data = [ idRef, idComp , Evaluation , ...]
    """
    shape = []
    for i in range(len(data)):
        lien = {}
        sourcePosition = data[i][0].centroid
        targetPosition = data[i][0].centroid
        linestring = LineString([sourcePosition, targetPosition]).wkt
        lien["geometry"] = linestring
        shape.append(lien)
    
    listeLinestring = []
    for k in range(len(shape)):
        listeLinestring.append(shape[k]["geometry"])
    

    df = pd.DataFrame(
    {
        "geometry" : listeLinestring
    })
    
    df['geometry'] = df['geometry'].apply(wkt.loads)
    #print(df.centroidSource[0])
    #line = LineString([df.centroidSource, df.centroidTarget])
    gdf = gpd.GeoDataFrame(
    df, geometry="geometry", crs="EPSG:2154"
    )

    gdf.to_file(url)  
    
if __name__ == "__main__" : 
    
    
    popRef = readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_4/popRef.shp")
    popComp = readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_4/popComp.shp")
    
    data = main(popRef, popComp)
    
    #writeShapefile (data , "/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_8/appariement.shp")
    
    
    PP = 0
    FP = 0
    for i in range(len(data)):
        if data[i][0] == data[i][1] : 
            PP += 1
        else : 
            FP += 1
            #print(data[i][0])
    print("nombre app vrai = ", PP)
    print("nombre app faux = ", FP)
    print("ratio = ", (PP - FP) / PP)
    
    
    """
    popRef = {}
    popRef["NOM"] = "col de Sibérie"
    #popRef["NATURE"] = "http://www.owl-ontologies.com/Ontology1176999717.owl#col"
    popRef["NATURE"] = "col"
    popRef["geometry"] = Point(826910.2, 6574293.6)
    popRef["X"] = 826910.2
    popRef["Y"] = 6574293.6
    
    pop = []
    popComp = {}
    popComp["NOM"] = "tête du pis"
    #popComp["NATURE"] = "http://www.owl-ontologies.com/Ontology1176999717.owl#sommet"
    popComp["NATURE"] = "sommet"
    popComp["geometry"] = Point(826665.2, 6574272.7)
    popComp["X"] = 826665.2
    popComp["Y"] = 6574272.7
    pop.append(popComp)
    popComp = {}
    popComp["NOM"] = "grande montagne"
    #popComp["NATURE"] = "http://www.owl-ontologies.com/Ontology1176999717.owl#sommet"
    popComp["NATURE"] = "sommet"
    popComp["geometry"] = Point(827361.1, 6574327.7)
    popComp["X"] = 827361.1
    popComp["Y"] = 6574327.7
    pop.append(popComp)
    popComp = {}
    popComp["NOM"] = "col de la sibérie"
    #popComp["NATURE"] = "http://www.owl-ontologies.com/Ontology1176999717.owl#col"
    popComp["NATURE"] = "col"
    popComp["geometry"] = Point(826596.7, 6574083.4)
    popComp["X"] = 826596.7
    popComp["Y"] = 6574083.4
    pop.append(popComp)
    popComp = pop 
    
    # A terme le popComp et le popRef devront etre les shapefiles 
    #popRef = readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_3/betton/BD2023.shp")
    #popComp = readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_3/betton/BD2010.shp")
    
    """
    #popRef = readShapefile("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/testMultiCritere/popRef.shp")
    #popComp = readShapefile("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/testMultiCritere/popComp.shp")
    
    #popRef = readShapefile("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/testMultiCritere/batiement/popRef.shp")
    #popComp = readShapefile("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/testMultiCritere/batiement/popComp.shp")

    #popRef = readShapefile("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/testMultiCritere/batiReconstruit/popRef.shp")
    #popComp = readShapefile("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/testMultiCritere/batiReconstruit/popComp.shp")
    
    """
    popRef = readShapefile("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/batimentTest/point/popRef.shp")
    popComp = readShapefile("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/batimentTest/point/popComp.shp")
    
    resultat = [ (1,3) , (2,7) , (3,8) , (4,9) , (5,10) , (6,11) , (7,0) , (8,12) , (9,13) ,
                (10 , 14) , (11,15) , (12,16) , (13,17) , (14,18) , (15,19) , (16,20) , (17,23) ,
                (18,24) , (19,25) , (20,26) , (21, 27) , (22, 0)]
    
    
    data = main(popRef, popComp)
    
    #print(data)
    
    
    PP= 0
    for i in range(len(data)):
        if data[i] in resultat : 
            PP+=1
            
    #print(PP)
    
    #print(len(data))
    
    """
    
    


    
    #writeShapefile (data , "/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/appariement3.shp")
    
    
    #print(doAppariement(popRef, popComp))
    

        
        
        