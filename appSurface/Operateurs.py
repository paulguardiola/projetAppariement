import shapely
import numpy as np



def intersectionRobuste(geomA, geomB, minRes , maxRes):
    inter = shapely.intersection(geomA , geomB)
    if inter.is_empty is False  : 
        return inter 
    for i in range(0,10):
        seuilDouglas = minRes + i * (maxRes - minRes)/10
        Amodif = DouglasPeucker(geomA , seuilDouglas)
        Bmodif = DouglasPeucker(geomB , seuilDouglas)
        inter = shapely.intersection( Amodif.buffer(0) , Bmodif.buffer(0))
        if inter.is_empty is False  : 
            return inter
    return None 
            
# methode Douglas-Peucker sur un polygon cf B Xiong et alt 2016
def DouglasPeucker(geom, seuil):
    
    geom_mapped = shapely.geometry.mapping(geom)
    geom = geom_mapped['coordinates'][0]
    
    
    #recherche de la diagonale la plus grande par rapport au point initiale
    dmax = 0 
    A = geom[0]
    noeudFin = 1
    for j in range(1, len(geom)): 
        B = geom[j]
        dist = ((A[0] - B[0])**2 + (A[1] - B[1])**2)**.5
        if dist > dmax:
            noeudFin = j
            dmax = dist 
    
    #creation des listes
    listA, listB = [], []
    for i in range(len(geom)):
        if i<=noeudFin : listA.append(geom[i])
        else :           listB.append(geom[i])
            
    #DouglasPeucker sur une ligne 
    ligneA = DouglasPeuckerLigne(listA, seuil)
    ligneB = DouglasPeuckerLigne(listB, seuil)
    
    ligne = ligneA + ligneB

    if len(ligne) <3 : 
        return shapely.geometry.Polygon(geom)
    geom = shapely.geometry.Polygon(ligne)
    return geom
    
def DouglasPeuckerLigne(geom, seuil): 
    listFinal = [geom[0]]
    A = geom[0]
    C = geom[len(geom)-1]
    for j in range(1, len(geom)): 
        B = geom[j]
        if A[0] == B[0] : 
            continue
        dist = projete(A, B, C)
        if dist > seuil :
            listFinal.append(B)
            A = B
        
    return listFinal

def projete(A, B , C) : 
    a = ( B[1] - A[1] )/ ( B[0] - A[0] )
    #b = A[1] - a*A[0]

    # calcul du point othoganl de objet_interre sur la droite y :-> ax + b
    vect = ( B[0] - A[0] , B[1] - A[1])
    AH = ( ( C[0] - A[0] )*vect[0] + ( C[1] - A[1] )*vect[1] ) / ((vect[0]**2 + vect[1]**2 )**.5)
    xH = A[0] + (AH*vect[0])/((vect[0]**2 + vect[1]**2 )**.5)
    yH = A[1] + (AH*vect[1])/((vect[0]**2 + vect[1]**2 )**.5)
    
    return ((C[0] - xH)**2 + (C[1] - yH)**2)**.5
        
        
    
    