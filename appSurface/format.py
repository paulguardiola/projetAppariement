#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import AppariementSurfaces 
import geopandas as gpd
import shapely

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
    
def ajoutLigne(param , url , index, parametre):
    
    f = open(url,'a')  
    f.write('\n')
    f.write(str(param[parametre]))
    f.write(";")
    f.write(str(index["F score"]))
    #f.write(";")
    #f.write("t0.95")
    f.write(";")
    f.write(parametre)
            
    f.close()
    
def variationParam(popRef, popComp , url , param , parametre ):
    
    #f = open(url,'w')
    #f.write('AnneeBD1;AnneeBD2;SurfMinInter;PourMinInter;PourInterSurf;MinDistSurf;DistSurfMax;CompExacMax;RegrOpti;FiltFinal;ResoMin;ResoMax;Prec:Rec;RateNeg;F')
    #f.close()
    #a = param[parametre]
    #for i in range(0,100,5):
    #    param[parametre] =  i/100  
    
    for i in range(0,100):
        
        param[parametre] =  i /10
        
        lienFiltres = AppariementSurfaces.appariementSurfaces(popRef , popComp, param)
        
        index = calcul_index(lienFiltres, popComp, popRef)
        
        ajoutLigne(param , url , index , parametre)
        
    
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
    param["resolutionMin"] = 1;
    param["resolutionMax"] = 11;
    
    popRef = AppariementSurfaces.readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/batimentTest/pavillon1/bati.shp")
    popComp = AppariementSurfaces.readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/batimentTest/pavillon1/batiIndiff.shp")
    #popRef = AppariementSurfaces.readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_4/Combourg/Pavillon/BD2023.shp")
    #popComp = AppariementSurfaces.readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_4/Combourg/Pavillon/BD2010.shp")
    #lienFiltres = AppariementSurfaces.appariementSurfaces(popRef , popComp, param)
    #index = calcul_index(lienFiltres, popComp, popRef)


    variationParam(popRef, popComp , '/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/batimentTest/pavillon1/variableCont.txt' , param , "surface_min_intersection")
    
    param = {}
    param["surface_min_intersection"] = 1;        # a faire 
    param["pourcentage_min_intersection"] = 0.0;  # a faire 
    param["pourcentage_intersection_sur"] = 0.8;  # a faire 
    param["minimiseDistanceSurfacique"] = True;
    param["distSurfMaxFinal"] = 0.6;              # a faire 
    param["completudeExactitudeMinFinal"] = 0.3;  # a faire 
    param["regroupementOptimal"] = True;
    param["filtrageFinal"] = True;
    param["resolutionMin"] = 1;
    param["resolutionMax"] = 11;
    
    # remettre les param 
    variationParam(popRef, popComp , '/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/batimentTest/pavillon1/variableCont.txt' , param , "distSurfMaxFinal")
    
    param = {}
    param["surface_min_intersection"] = 1;        # a faire 
    param["pourcentage_min_intersection"] = 0.0;  # a faire 
    param["pourcentage_intersection_sur"] = 0.8;  # a faire 
    param["minimiseDistanceSurfacique"] = True;
    param["distSurfMaxFinal"] = 0.6;              # a faire 
    param["completudeExactitudeMinFinal"] = 0.3;  # a faire 
    param["regroupementOptimal"] = True;
    param["filtrageFinal"] = True;
    param["resolutionMin"] = 1;
    param["resolutionMax"] = 11;
    
    popRef = AppariementSurfaces.readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/batimentTest/pavillon2/bati.shp")
    popComp = AppariementSurfaces.readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/batimentTest/pavillon2/batiIndiff.shp")

    variationParam(popRef, popComp , '/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/batimentTest/pavillon2/variableCont.txt' , param , "surface_min_intersection")
    
    param = {}
    param["surface_min_intersection"] = 1;        # a faire 
    param["pourcentage_min_intersection"] = 0.0;  # a faire 
    param["pourcentage_intersection_sur"] = 0.8;  # a faire 
    param["minimiseDistanceSurfacique"] = True;
    param["distSurfMaxFinal"] = 0.6;              # a faire 
    param["completudeExactitudeMinFinal"] = 0.3;  # a faire 
    param["regroupementOptimal"] = True;
    param["filtrageFinal"] = True;
    param["resolutionMin"] = 1;
    param["resolutionMax"] = 11;
    
    # remettre les param 
    variationParam(popRef, popComp , '/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/batimentTest/pavillon2/variableCont.txt' , param , "distSurfMaxFinal")
    
    param = {}
    param["surface_min_intersection"] = 1;        # a faire 
    param["pourcentage_min_intersection"] = 0.0;  # a faire 
    param["pourcentage_intersection_sur"] = 0.8;  # a faire 
    param["minimiseDistanceSurfacique"] = True;
    param["distSurfMaxFinal"] = 0.6;              # a faire 
    param["completudeExactitudeMinFinal"] = 0.3;  # a faire 
    param["regroupementOptimal"] = True;
    param["filtrageFinal"] = True;
    param["resolutionMin"] = 1;
    param["resolutionMax"] = 11;

    popRef = AppariementSurfaces.readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/batimentTest/pavillon3/bati.shp")
    popComp = AppariementSurfaces.readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/batimentTest/pavillon3/batiIndiff.shp")

    variationParam(popRef, popComp , '/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/batimentTest/pavillon3/variableCont.txt' , param , "surface_min_intersection")
    
    param = {}
    param["surface_min_intersection"] = 1;        # a faire 
    param["pourcentage_min_intersection"] = 0.0;  # a faire 
    param["pourcentage_intersection_sur"] = 0.8;  # a faire 
    param["minimiseDistanceSurfacique"] = True;
    param["distSurfMaxFinal"] = 0.6;              # a faire 
    param["completudeExactitudeMinFinal"] = 0.3;  # a faire 
    param["regroupementOptimal"] = True;
    param["filtrageFinal"] = True;
    param["resolutionMin"] = 1;
    param["resolutionMax"] = 11;
    
    # remettre les param 
    variationParam(popRef, popComp , '/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/batimentTest/pavillon3/variableCont.txt' , param , "distSurfMaxFinal")
    
    param = {}
    param["surface_min_intersection"] = 1;        # a faire 
    param["pourcentage_min_intersection"] = 0.0;  # a faire 
    param["pourcentage_intersection_sur"] = 0.8;  # a faire 
    param["minimiseDistanceSurfacique"] = True;
    param["distSurfMaxFinal"] = 0.6;              # a faire 
    param["completudeExactitudeMinFinal"] = 0.3;  # a faire 
    param["regroupementOptimal"] = True;
    param["filtrageFinal"] = True;
    param["resolutionMin"] = 1;
    param["resolutionMax"] = 11;    

    popRef = AppariementSurfaces.readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/batimentTest/pavillon4/bati.shp")
    popComp = AppariementSurfaces.readShapefile ("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/batimentTest/pavillon4/batiIndiff.shp")

    variationParam(popRef, popComp , '/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/batimentTest/pavillon4/variableCont.txt' , param , "surface_min_intersection")
    
    param = {}
    param["surface_min_intersection"] = 1;        # a faire 
    param["pourcentage_min_intersection"] = 0.0;  # a faire 
    param["pourcentage_intersection_sur"] = 0.8;  # a faire 
    param["minimiseDistanceSurfacique"] = True;
    param["distSurfMaxFinal"] = 0.6;              # a faire 
    param["completudeExactitudeMinFinal"] = 0.3;  # a faire 
    param["regroupementOptimal"] = True;
    param["filtrageFinal"] = True;
    param["resolutionMin"] = 1;
    param["resolutionMax"] = 11;
    
    # remettre les param 
    variationParam(popRef, popComp , '/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_6/batimentTest/pavillon4/variableCont.txt' , param , "distSurfMaxFinal")
    

    
    
    
    



