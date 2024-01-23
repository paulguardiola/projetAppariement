#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from owlready2 import *
import math
import numpy as np

def DistanceWuPalmer(uri , nomRef , nomComp):
    
    onto = get_ontology(uri).load()
    
    fils1 = nomRef
    fils2 = nomComp
    
    listAncestorsCommun = getAncestorsCommun(onto , fils1 , fils2)
    
    num = 2* (len(listAncestorsCommun)-1) 
    
    listAncestors1 = getAncestors(onto , fils1)
    listAncestors2 = getAncestors(onto , fils2)
    
    distAncestors1 = len(listAncestors1) 
    distAncestors2 = len(listAncestors2)
    
    denum = distAncestors1 + distAncestors2
    
    return 1 - num/denum #1 - mesureSimilariteWuPalmer

def CritereSemantique(dist , nomRef, nomComp , seuil): 
    
    tableau = []
    #valTypeRef = nomRef
    #valTypeComp = nomComp
	
    #((DistanceAbstractSemantique) distance).setType(valTypeComp, valTypeRef);
    #double distNorm = distance.getDistance();
    distNorm = dist

    """
    if distNorm < seuil :
        tableau.append((-0.4 / seuil) * distNorm + 0.5)
        tableau.append((0.8 / seuil) * distNorm)
        tableau.append((-0.4 / seuil) * distNorm + 0.5)
    else :
        tableau.append(0.1)
        tableau.append(0.8)
        tableau.append(0.1)
		
	#// Si concept n'est pas dans l'ontologie 
    if np.isnan(distNorm) or abs(distNorm - 2.0) <= 0.000001 :
        tableau.append(0)
        tableau.append(0)
        tableau.append(1)
        
    """
        
    if np.isnan(distNorm) or abs(distNorm - 2.0) <= 0.000001:
        tableau.append(0)
        tableau.append(0)
        tableau.append(1)
    elif distNorm < seuil : 
        tableau.append((-0.7/seuil)*distNorm + 1)
        tableau.append((0.4/seuil)*distNorm)
        tableau.append((0.3/seuil)*distNorm)
    else :
        tableau.append(0.2)
        tableau.append(0.4)
        tableau.append(0.4)


    return tableau;

def getAncestors(onto , fils):
    liste = list(onto[fils].ancestors())
    l = []
    for k in range(len(liste)):
        char = str(liste[k])
        if str(char[0:3]) == 'owl' :
            classe = char[4:len(char)]
            l .append ( (classe , 0 ) )
        
        else : 
            classe = char[7:len(char)]
            l .append ( (classe , len(list(onto[classe].ancestors()))-1 ))
    
    return l 

def getAncestorsCommun(onto , fils1 , fils2):
    
    listAncestors1 = getAncestors(onto , fils1)
    listAncestors2 = getAncestors(onto , fils2)
    
    listAncestorsCommun = []
    
    for k in range(min(len(listAncestors1) , len(listAncestors2))):
        
        Ancestors1 = getClasse(listAncestors1 , k)
        Ancestors2 = getClasse(listAncestors2 , k)
        if  Ancestors2 == Ancestors1 : 
            listAncestorsCommun.append(Ancestors2)
        
    return listAncestorsCommun
    
    
def getClasse(liste , chiffre):
    
    for k in range(len(liste)):
        if liste[k][1] == chiffre : 
            return liste[k][0]
        
    return False 
        


if __name__ == "__main__":
    #onto = get_ontology("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_5/MultiCriteriaMatchingPython/main/GeOnto.owl").load()
    #print(list(onto["île"].subclasses()))
    #print(list(onto["voie_de_service"].subclasses()))
    #print(list(onto["voie_de_service"].ancestors()))
    #print(list(onto["entité_topographique_artificielle"].ancestors()))
    #print(list(onto["entité_topographique_artificielle"].subclasses()))
    
    nomRef = 'sommet'
    nomComp1 = 'habitation'
    nomComp2 = 'construction_ponctuelle'
    nomComp3 = 'col'
    
    
    print(DistanceWuPalmer("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_5/MultiCriteriaMatchingPython/main/GeOnto.owl", nomRef , nomComp1))
    print(DistanceWuPalmer("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_5/MultiCriteriaMatchingPython/main/GeOnto.owl", nomRef , nomComp2))
    print(DistanceWuPalmer("/Users/guardiola/Desktop/ENSG_troisieme_annee/Alternance/semain_5/MultiCriteriaMatchingPython/main/GeOnto.owl", nomRef , nomComp3))
    
    
    
    
    
    