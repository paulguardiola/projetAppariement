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

# Appariement entre deux ensemble de surfaces. Processus inspiré de celui
# defini dans la thèse de Atef Bel Hadj (2001)

def appariementSurfaces(popRef , popComp, param):
    # pre-appariement surfaces
    liensPreApp = preAppariementsSurfaces_avec_index_spatiale(popRef , popComp , param )
    
    # recherche groupes optimaux 
    liensRegroupes = liensPreApp    
    if param["regroupementOptimal"] : 
        liensRegroupes = rechercheRegroupementsOptimaux(liensPreApp, popRef, popComp, param)
    
    # ajout petites surfaces 
    #if param["ajoutPetitesSurfaces"] : 
    #    pass
    #    liensRegroupes = ajoutPetitesSurfaces(liensRegroupes, popRef, popComp, param)
    
    a = time.time()
    # filtres finales  
    liensFiltres = liensRegroupes    
    if param["filtrageFinal"] : 
        liensFiltres = filtresLiens(liensRegroupes, param , popRef , popComp)

    # deja considerer dans writeshapefile 
    #liensFiltres = creerGeometriesDesLiens(liensFiltres, param["persistant"])
    
    return liensFiltres

# 2 surfaces sont pré-appariées si :
# 1) l'intersection des surfaces a une taille supèrieure au seuil " surf_min" ET
# 2) l'intersection fait au moins la taille d'une des surfaces multipliée par le paramètre 
# poucentage min 
# NB 1 par construction : chaque lien pointe vers UN SEUL objet de la population
# de référenes et vers un SEUL objet de la population de comparaison 
# popRef  : population des objets de référence 
# popComp : population des objets de comparaison
# param   : paramètres de l'appariement 
# return lien pré-appariement 

def preAppariementsSurfaces (popRef , popComp , param ):
    preAppLiens = [] 
    
    for i in range(len(popRef)):
        #geomRef = popRef[i].getGeom() 
        geomRef = popRef[i]['geometry']
        
        # test d'association sur tous les objets comp intersectant l'objet ref 
        for j in range(len(popComp)):
            #geomComp = popComp[j].getGeom()
            geomComp = popComp[j]['geometry']
            
            
            # creation eventuelle d'un nouveau lien de pré-appariement
            inter = intersectionRobuste(geomRef , geomComp , param["resolutionMin"],
                                        param["resolutionMax"])
            if (inter == None):
         
                continue 
            surfaceIntersection = inter.area
            
            if surfaceIntersection <= param["surface_min_intersection"]:
           
                continue 
            
            pourcentageRecouvrement = max(surfaceIntersection/ geomRef.area,
                                               surfaceIntersection/ geomComp.area)
            if pourcentageRecouvrement < param["pourcentage_min_intersection"]:
         
                continue #intersection pas suffisante 
                
            Lien = []
            #Lien.append(popRef[i]) #peut etre a revoir 
            #Lien.append(popComp[j])
            """ passe par l'indice spatial """
            
            
            Lien.append(popRef [i]["id_spatial"])
            Lien.append(popComp[j]["id_spatial"])
            Lien.append(pourcentageRecouvrement)
       
            if param["minimiseDistanceSurfacique"]:
                Lien.append(Distances.distanceSurfaciqueRobuste(geomRef , geomComp , param["resolutionMin"],
                                            param["resolutionMax"]) ) # getDistanceSurfacique
                
            else : 
                Lien.append(Distances.exactitude(geomRef , geomComp)) #getExactitude()
                Lien.append(Distances.completude(geomRef , geomComp)) #getCompletude()
            
            preAppLiens.append(Lien)
    return preAppLiens

def preAppariementsSurfaces_avec_index_spatiale (popRef , popComp , param ):

    preAppLiens = [] 
    
    geomRef = [ popRef[i]["geometry"] for i in range(len(popRef)) ]
    geomCom = [ popComp[i]["geometry"] for i in range(len(popComp)) ]
    ref = gpd.GeoSeries( geomRef )
    com = gpd.GeoSeries( geomCom )
    
    # inter = intersectionRobuste_index(geomRef , geomComp , param["resolutionMin"],
    #                            param["resolutionMax"])
    inter = com.sindex.query(ref, predicate="intersects")
    lien = [(inter[0][i] , 
             inter[1][i] , 
             shapely.intersection(geomRef[inter[0][i]] , geomCom[inter[1][i]]).area,
             shapely.intersection(geomRef[inter[0][i]] , geomCom[inter[1][i]]).area / (min(geomRef[inter[0][i]].area , geomCom[inter[1][i]].area)),
             Distances.distanceSurfaciqueRobuste(geomRef[inter[0][i]] , geomCom[inter[1][i]] , param["resolutionMin"],
                                         param["resolutionMax"]) ,
             Distances.exactitude(geomRef[inter[0][i]] , geomCom[inter[1][i]]),
             Distances.completude(geomRef[inter[0][i]] , geomCom[inter[1][i]])
             ) for i in range(len(inter[0]))]
    
    # lien = [ idRef , idCom , inter.area , pourcentageRecouvrement , distSurfaciqueRobuste,  exactitude , completude]
    # verifier si popRef[inter[0][i]]["geometry"] = geomRef[inter[0][i]]
    
    
    for i in range(len(lien)):
        lienFiltre = []
        if lien[i][2] <= param["surface_min_intersection"]:
            continue 
        if lien[i][3] < param["pourcentage_min_intersection"]:
            continue
        if param["minimiseDistanceSurfacique"]:
            lienFiltre = ( lien[i][0] , lien[i][1] , lien[i][3] , lien[i][4] )
        else : 
            lienFiltre = ( lien[i][0] , lien[i][1] , lien[i][3] ,lien[i][5] , lien[i][6] ) 
        preAppLiens.append(lienFiltre)
        
    return preAppLiens

# On recherche les regroupements optimaux de liens de pré-traitement, pour
# maximiser la distance surfacique entre les groupes de référence et de 
# comparaison 
# NB l'appariement est symétrique 
# param   : paramètres de l'appariement 
# preAppLiens : liens issus du pré-appariement 
# return liens d'appariement calculés 


def rechercheRegroupementsOptimaux (preAppLiens, popRef , popComp , param):
    
    matrice = np.zeros((len(popRef), len(popComp)))
    for k in range(len(preAppLiens)):
        matrice[preAppLiens[k][0]][preAppLiens[k][1]] = preAppLiens[k][2]
    
    groupesGardes = []
    
    #on parcrous touts les liens n-m créés
    groupesConnexes = []
    for i  in range(len(popRef)):
        groupes = []
        for j in range(len(popComp)): 
            if matrice[i][j] > 0 : 
                groupes.append((i,j,matrice[i][j]))
        
        if len(groupes) != 0 : 
            groupesConnexes.append(groupes)
            
    
    for i in range(len(groupesConnexes)):
        # pour tous les objets isolés ou les liens 1-1, on ne fait rien de plus 
        if len(groupesConnexes[i]) == 1 : 
            groupesGardes.append(groupesConnexes[i])
            continue 
        # pour les groupes n-m on va essayer d'enlever des arcs 
        # mais on garde à coup sûr les liens avec suffisament de recouvrement
    
        arcNonEnlevables = []
        arcEnlevables    = []
        
        for j in range(len(groupesConnexes[i])):
            if groupesConnexes[i][j][2] > param["pourcentage_intersection_sur"]:
                arcNonEnlevables.append(groupesConnexes[i][j])
            else :
                arcEnlevables.append(groupesConnexes[i][j])
                
        if len(arcNonEnlevables) == len(groupesConnexes[i]) : # si on ne peut rien enlever on s'arrête la 
            groupesGardes.append(groupesConnexes[i])
            continue 
        
        
        #on cherche à enlever toutes les combinaisons possibles d'arcs virables
        distSurfMin = 2
        distExacMax = 0
        combinaisons = arcEnlevables
        arcDuGroupeEnlevesFinal = []
        comb = 0
        
        #for j in range(len(arcEnlevables)):
        #    dist = mesureEvaluationGroupe(arcEnlevables[j], popRef, popComp, param)
        #    if param["minimiseDistanceSurfacique"]:
        #        if dist < distSurfMin :
        #            distSurfMin = dist 
        #            arcDuGroupeEnlevesFinal.append(arcEnlevables[j])
        #    else :
        #        if dist > distExacMax : 
        #            distExacMax = dist 
        #            arcDuGroupeEnlevesFinal.append(arcEnlevables[j])
        
        dist = mesureEvaluationGroupe(arcEnlevables, popRef, popComp, param)
        if param["minimiseDistanceSurfacique"]:
            if dist < distSurfMin :
                distSurfMin = dist  # gros problemes de logique 
                arcDuGroupeEnlevesFinal.append(arcEnlevables)
        else :
            if dist > distExacMax : 
                distExacMax = dist 
                arcDuGroupeEnlevesFinal.append(arcEnlevables)
        
        #groupesPreGardes = []
        #for j in range(len(groupesConnexes[i])):
        #    compteur = 0 
        #    if (len(arcDuGroupeEnlevesFinal)) == 0 : 
        #        continue 
        #    for k in range(len(arcDuGroupeEnlevesFinal[0])):
        #        if groupesConnexes[i][j] == arcDuGroupeEnlevesFinal[0][k]:
        #            compteur = 1
        #    if compteur == 0 :
         #       groupesPreGardes.append(groupesConnexes[i][j])
         #groupesGardes.append(GroupesPRegardes)
        
        if (len(arcDuGroupeEnlevesFinal)) == 0 : 
            continue 
        else : 
            for k in range(len(arcDuGroupeEnlevesFinal[0])):
                groupesConnexes[i].remove(arcDuGroupeEnlevesFinal[0][k])
                    
            groupesGardes.append(groupesConnexes[i])
    
    L = []
    for k in range(len(groupesGardes)):
        
        if len(groupesGardes[k]) == 2 : 
            L.append(groupesGardes[k][0])
            L.append(groupesGardes[k][1])
        elif len(groupesGardes[k]) == 0 : 
            continue
        else : 
            L.append(groupesGardes[k][0])
            
    return L
    

# Il me semble qu'on ajoute la zone petite à la zone plus grande pour en 
# faire une nouvelle entité 
def mesureEvaluationGroupe(groupe , popRef , popComp , param):
    
    if param["minimiseDistanceSurfacique"]:
        result = 2 
    else : result = -1
    
    # groupe = [(1, 10, 0.9558426479762911), (1, 26, 0.9999474003823016)]
    
    listRef = []
    listComp = []

    for j in range(len(groupe)):
        listRef.append(groupe[j][0])
        listComp.append(groupe[j][1])
    unionRef  = unionListe(listRef,popRef)  
    unionComp = unionListe(listComp,popComp)
        
    #if len(groupe) == 3 : # A changer si on change le nombre dans groupe 
    #    unionRef  = popRef[groupe[0]]["geometry"]
    #    unionComp = popComp[groupe[1]]["geometry"]

    #else :
    #    for j in range(len(groupe)):
    #        print("groupe =", groupe)
    #        listRef.append(groupe[j][0])
    #        listComp.append(groupe[j][1])
    #    unionRef  = unionListe(listRef,popRef)  
    #    unionComp = unionListe(listComp,popComp) 
        
        
    geomRef = unionRef # peut etre que il y a un pb de type 
    geomComp = unionComp

    #on combine les mesures des parties connexes 
    if param["minimiseDistanceSurfacique"]:
        value= Distances.distanceSurfaciqueRobuste(geomRef, geomComp, param["resolutionMin"], param["resolutionMax"])
        result = min(value, result)
    else : 
        value = Distances.exactitude(geomRef , geomComp) + Distances.completude(geomRef , geomComp)
        result = max(value, result)       
    
    return result 
        
def filtresLiens(liensRegroupes, param , popRef , popComp):
    # liensRegroupes = [ [ idRef, idCom, dsi]]
    
    liensFiltres = []
    
    for i in range(len(liensRegroupes)):
        lien = []
        if param["minimiseDistanceSurfacique"] : 
            distSurf = liensRegroupes[i][2]
            if distSurf < param["distSurfMaxFinal"]:
                lien.append(liensRegroupes[i][0])
                lien.append(liensRegroupes[i][1])
                lien.append(distSurf)
                #liens.append(getArcs)
            else : 
                exactitude = Distances.exactitude(popRef[liensRegroupes[i][0]]["geometry"] , popComp[liensRegroupes[i][1]]["geometry"] )
                completude = Distances.completude(popRef[liensRegroupes[i][0]]["geometry"] , popComp[liensRegroupes[i][1]]["geometry"] )
                #exactitude = liensRegroupes[2]
                #completude = liensRegroupes[3]
                if exactitude > param["completudeExactitudeMinFinal"] and completude > param["completudeExactitudeMinFinal"]: 
                    lien.append(liensRegroupes[i][0])
                    lien.append(liensRegroupes[i][1])
                    lien.append(exactitude + completude)
                    #liens.append(getArcs)
        if len(lien) != 0 :
            liensFiltres.append(lien)
    return liensFiltres 



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
   
    
    
def writeShapefile (popRef, popComp, data, url) :
    """
    data = [ idRef, idComp , Evaluation , ...]
    """
    shape = []
    for i in range(len(data)):
        lien = {}
        idSource = data[i][0]
        idTarget = data[i][1]
        source = popRef[idSource]
        target = popComp[idTarget]
        sourcePosition = popRef[idSource]["geometry"].centroid
        targetPosition = popComp[idTarget]["geometry"].centroid
        linestring = LineString([sourcePosition, targetPosition]).wkt
        lien["centroidSource"] = sourcePosition
        lien["centroidTarget"] = targetPosition
        lien["idLien"] = i
        #lien["edgeId"] = i
        lien["sourceID"] = source["ID"]
        lien["targetID"] = target["ID"]
        lien["Evaluation"] = data[i][2]
        lien["DistanceSurfacique"] = Distances.distanceSurfaciqueRobuste(popRef[idSource]["geometry"] , popComp[idTarget]["geometry"] , param["resolutionMin"],
                                    param["resolutionMax"])
        lien["Exactitude"] = Distances.exactitude(popRef[idSource]["geometry"] , popComp[idTarget]["geometry"] )
        lien["Completude"] = Distances.completude(popRef[idSource]["geometry"] , popComp[idTarget]["geometry"] )
        lien["geometry"] = linestring
        shape.append(lien)
    
    listeidLien=[]
    listesourceID=[]
    listetargetID=[]
    listeEvaluation=[]
    listeDistance=[]
    listeExactitude=[]
    listeCompletude=[]
    listeSourcePos=[]
    listeTargetPos=[]
    listeLinestring = []
    for k in range(len(shape)):
        listeidLien.append(shape[k]["idLien"])
        listesourceID.append(shape[k]["sourceID"])
        listetargetID.append(shape[k]["targetID"])
        listeEvaluation.append(shape[k]["Evaluation"])
        listeDistance.append(shape[k]["DistanceSurfacique"])
        listeExactitude.append(shape[k]["Exactitude"])
        listeCompletude.append(shape[k]["Completude"])
        listeSourcePos.append(shape[k]["centroidSource"])
        listeTargetPos.append(shape[k]["centroidTarget"])
        listeLinestring.append(shape[k]["geometry"])
    

    df = pd.DataFrame(
    {
        "idLien": listeidLien,
        "sourceID": listesourceID,
        "targetID": listetargetID,
        "Evaluation": listeEvaluation,
        "DistanceSurfacique" : listeDistance,
        "Exactitude": listeExactitude,
        "Completude" : listeCompletude,
        #"centroidSource" : listeSourcePos,
        #"centroidTarget" : listeTargetPos,
        "geometry" : listeLinestring
        
    })
    
    df['geometry'] = df['geometry'].apply(wkt.loads)
    #print(df.centroidSource[0])
    #line = LineString([df.centroidSource, df.centroidTarget])
    gdf = gpd.GeoDataFrame(
    df, geometry="geometry", crs="EPSG:2154"
    )

    gdf.to_file(url)
    

def unionListe(liste,pop):
    union = getGeom(liste[0],pop)
    for k in range(1, len(liste)):
        union = shapely.union(union , getGeom(liste[k],pop))
    
    return union

def getGeom(indice,pop):
    return pop[indice]['geometry']
    
if __name__ == "__main__" : 
    param = {}
    param["surface_min_intersection"] = 1;
    param["pourcentage_min_intersection"] = 0.0;
    param["pourcentage_intersection_sur"] = 0.8;
    param["minimiseDistanceSurfacique"] = True;
    param["distSurfMaxFinal"] = 0.6;
    param["completudeExactitudeMinFinal"] = 0.3;
    param["regroupementOptimal"] = True;
    param["filtrageFinal"] = True;
    param["ajoutPetitesSurfaces"] = True;
    param["seuilPourcentageTaillePetitesSurfaces"] = 0.1;
    param["persistant"] = False;
    param["resolutionMin"] = 1;
    param["resolutionMax"] = 11;
    
    """

    popRef = readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_3/CentreUrbain/BD2023.shp")
    popComp = readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_3/CentreUrbain/BD2010.shp")
    
    #preAppLiens = preAppariementsSurfaces_avec_index_spatiale(popRef, popComp, param)
    
    
    lienFiltres = appariementSurfaces(popRef , popComp, param)
    
    
    
    
    
    
    #lien = readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/Semain_2/qgis/Betton/lien.shp")
    #print(lien[0]["geometry"])
    
    
    writeShapefile (popRef, popComp, lienFiltres, "/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_5/appariement.shp")
    
    #print(shapely.intersection(popRef[0]['geometry'], popComp[21]['geometry']).is_empty)
    #print (preAppLiens)
    
    #print(shapely.intersection(popComp[0]['geometry'] , popComp[0]['geometry']).area)

    #a = popRef[0]['geometry']
    #print(a)
    #poly_mapped = shapely.geometry.mapping(a)
    #poly_coordinates = poly_mapped['coordinates'][0]
    #print(poly_coordinates)
    #print(shapely.geometry.Polygon(poly_coordinates))
    
    """
    
    popRef = readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_4/popRef.shp")
    popComp = readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_4/popComp.shp")
    
    lienFiltres = appariementSurfaces(popRef , popComp, param)
    
    print(lienFiltres)
    
    PP = 0
    FP = 0
    for i in range(len(lienFiltres)):
        if lienFiltres[i][0] == lienFiltres[i][1] : 
            PP += 1
        else : 
            FP += 1
    print("nombre app vrai = ", PP)
    print("nombre app faux = ", FP)
    print("ratio = ", (PP - FP) / PP)
    

   

                