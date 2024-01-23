#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 09:52:30 2024

@author: guardiola
"""

import numpy as np


def fusionCandidat(candidat):
    
    # intialisation des dictionnaires
    dic = {}
    result = {}
    resultList = []
    for i in range(len(candidat)) : 
        dic["C"+str(i+1)] = candidat[i][0]
        dic["-C"+str(i+1)] = candidat[i][1]
        dic["theta"+ str(i+1)] = candidat[i][2]
        dic["phi"+ str(i+1)] = candidat[i][3]
        result["C"+str(i+1)] = 0
        result["-C"+str(i+1)] = 0
        resultList.append("C"+str(i+1))
        resultList.append("-C"+str(i+1))
    result["theta"] = 0
    result["phi"] = 0
    result["NA"] = 0
    resultList.append("theta")
    resultList.append("phi")
    resultList.append("NA")
    
    transit = dic
    
    
    
    for k in range(len(candidat)-1):
        (ligne , colone , matrice) =  mat( k + 2 )
        
        listmodif = []
        
        for i in range(len(resultList)):
            result[resultList[i]] = 0
        
        
        for i in range(np.shape(matrice)[0]):
            for j in range(np.shape(matrice)[1]):
                
                jeu = str(matrice[i][j])[2:len(str(matrice[i][j]))-1]
                listmodif.append(jeu)
                if dic[colone[j]] * dic[ligne[i]] != 0 :
                    result[jeu] += transit[colone[j]] * transit[ligne[i]]
                

        for i in range(len(listmodif)):
            if listmodif[i] != "phi" and listmodif[i] != "theta" and listmodif[i] != "NA":
                transit[listmodif[i]] = result[listmodif[i]] 
        transit["theta1"] = result["theta"] 
        transit["phi1"] = result["phi"] 
        
    
    for i in range(len(resultList)):
        result[resultList[i]] = result[resultList[i]] / ( 1 - result['phi'] )
    
    return result
        

def mat( index ):
    
    colone = ("C"+ str(index) , "-C"+ str(index)  , "theta"+ str(index) , "phi"+ str(index))
    
    ligne = []
    
    for i in range(index-1):
        
        ligne.append("C"+str(i+1))
        ligne.append("-C"+str(i+1))
        
    if index > 2 : 
        #ligne.append("C"+str(index))
        pass
    ligne.append("theta"+ str(1))
    ligne.append("phi"+ str(1))
        
    matrice = np.chararray((len(ligne),len(colone)), 5)
    for i in range(len(colone)):
        for j in range(len(ligne)):
            matrice[j][i] = loi(ligne[j] , colone[i])
            
    return (ligne , colone , matrice)


def loi(x,y):
    
    # x = Cx , -Cx , theta , phi 
    
    if x == y : 
        return x
    
    if len(x) > 2 :
        if x[0:3] == "phi" :
                return "phi"
        
        if x[0:5] == "theta":
            if len(y) >2 and y[0:3] == "phi" : 
                return "phi"
            else : 
                return y
    
    if len(y) > 2:
        if y[0:3] == "phi" : 
            return "phi"
        if y[0:5] == "theta":
            return x

    
    if x[0] == "C" : 
        
        if y[0] == "C" :    
            if x[1] != y[1] : 
                return "phi"
            
        if y[0] == "-" : 
            
            if x[1] != y[2] : 
                return x
            else : 
                return "NA"
        
        
    if x[0] == "-" : 
        
        if y[0] == "C" :    
            if x[2] != y[1] : 
                return y
            else : 
                return "NA"
            
        if y[0] == "-" : 
            return "NA"
    

if __name__ == "__main__" : 
    
    c1 = [ 0.58 , 0 , 0.42 , 0 ]
    c2 = [ 0, 0.9 , 0 , 0.1 ]
    c3 = [ 0.54 , 0 , 0.46 , 0 ]
    
    candidat = (c1 , c2 , c3)
    print(fusionCandidat(candidat))
    

