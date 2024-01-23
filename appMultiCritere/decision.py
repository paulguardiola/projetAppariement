#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np 
import math

def dempster(liste_critere):
    
    masseCan = []
    
    for i in range(len(liste_critere)):
        masseCan.append(fusionCritereConj(liste_critere[i]))
        
    #print(masseCan)
    #print(" ")
    # fusion candidat 
    ( resultList , fusCandidat ) = fusionCandidat(masseCan)

    
    print(fusCandidat)
    
    # decision 
    deci = decision(resultList , fusCandidat)
    
    return deci 
    
"""
def masse(c1 , c2):
    
    # c1 = critere 1 
    # c2 = critere 2 

    m1_A  = c1[0]
    m1_B  = c1[1]
    m1_Om = c1[2]
    m2_A  = c2[0]
    m2_B  = c2[1]
    m2_Om = c2[2]
    
    m12A = m1_A * m2_A + m1_A * m2_Om + m2_A * m1_Om
    m12B = m1_B * m2_B + m1_B * m2_Om + m2_B * m1_Om
    m12Om = m1_Om * m2_Om
    m12vide = m1_A * m2_B + m1_B * m2_A
    
    return [m12A , m12B , m12Om , m12vide ]
    
    
def fusionCritere(Candidat) : 
    
    #print("candidat =", Candidat)
    
    source1 = Candidat[0]
    
    if len(Candidat) == 1 : 
        source2 = Candidat[1]
        source = masse(source1 , source2)
        source1 = source
    else : 
        for k in range(len(Candidat) - 1 ):
            source2 = Candidat[k+1]
            source = masse(source1 , source2)
            source1 = source
        
    return source1
"""

def fusionCritereConj(Candidat) : 
    
    dic = {}
    result = {}
    resultList = []
    for i in range(len(Candidat)) : 
        dic["app"+str(i+1)] = Candidat[i][0]
        dic["-app"+str(i+1)] = Candidat[i][1]
        dic["theta"+ str(i+1)] = Candidat[i][2]
    result["app"] = 0
    result["-app"] = 0
    result["theta"] = 0
    result["phi"] = 0
    
    matrice = [["app" , "phi" , "app"],
               ["phi" , "-app" , "-app"],
               ["app" , "-app" , "theta"]]
    
    ligne = ["app1" , "-app1" , "theta1" ]
    
    for k in range(len(Candidat)-1):
        
        result["app"] = 0
        result["-app"] = 0
        result["theta"] = 0
        result["phi"] = 0
        
        colone = ["app"+str(k+2) , "-app"+str(k+2) , "theta"+str(k+2) ]
        
        
        for i in range(np.shape(matrice)[0]):
            for j in range(np.shape(matrice)[1]):
                jeu = matrice[i][j]
                #print(jeu)
                #print(colone[j])
                #print(dic[colone[j]])
                #print(ligne[i])
                #print(dic[ligne[i]])
                #print(dic[colone[j]] * dic[ligne[i]] )
                if dic[colone[j]] * dic[ligne[i]] != 0 :
                    result[jeu] += dic[colone[j]] * dic[ligne[i]]
                    
        dic["app1"]   = result["app"]
        dic["-app1"]  = result["-app"]
        dic["theta1"] = result["theta"]
        
    return result
        
    


def fusionCandidat(candidat):
    
    # Changer pa rapport au fait que masseCan est un dictionnaire 
    
    # intialisation des dictionnaires
    dic = {}
    result = {}
    resultList = []
    for i in range(len(candidat)) : 
        #dic["C"+str(i+1)] = candidat[i][0]
        #dic["-C"+str(i+1)] = candidat[i][1]
        #dic["theta"+ str(i+1)] = candidat[i][2]
        #dic["phi"+ str(i+1)] = candidat[i][3]
        dic["C"+str(i+1)] = candidat[i]["app"]
        dic["-C"+str(i+1)] = candidat[i]["-app"]
        dic["theta"+ str(i+1)] = candidat[i]["theta"]
        dic["phi"+ str(i+1)] = candidat[i]["phi"]
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
    
    if len(candidat) == 1 : 
        
        result["C1"] = candidat[i]["app"]
        result["-C1"] = candidat[i]["-app"]
        result["C"] = candidat[i]["theta"]
        result["phi"] = candidat[i]["phi"]
    
    for k in range(len(candidat)-1):
        (ligne , colone , matrice) =  mat( k + 2 )
        
        listmodif = []
        
        print(matrice)
        
        for i in range(len(resultList)):
            result[resultList[i]] = 0
        
        
        for i in range(np.shape(matrice)[0]):
            for j in range(np.shape(matrice)[1]):
                
                jeu = str(matrice[i][j])[2:len(str(matrice[i][j]))-1]
                listmodif.append(jeu)
                if dic[colone[j]] * dic[ligne[i]] != 0 :
                    #print(jeu)
                    #print((colone[j] , ligne[i]))
                    #print((transit[colone[j]] , transit[ligne[i]]))
                    #print(transit[colone[j]] * transit[ligne[i]])
                    result[jeu] += transit[colone[j]] * transit[ligne[i]]
                

        for i in range(len(listmodif)):
            if listmodif[i] != "phi" and listmodif[i] != "theta" and listmodif[i] != "NA":
                transit[listmodif[i]] = result[listmodif[i]] 
        transit["theta1"] = result["theta"] 
        transit["phi1"] = result["phi"] 
        
        #print(result)
        
    
        
    
    a = result['phi']
    for i in range(len(resultList)):
        result[resultList[i]] = result[resultList[i]] / ( 1 - a )
    
    return ( resultList , result )
        

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
    

    
def decision(resultList , fusion):
    
    fusion["phi"] = 0 
    result = "NA"
    max_ = 0
    for i in range(len(resultList)):
        if fusion[resultList[i]] > max_ : 
            max_ = fusion[resultList[i]]
            result = resultList[i]
        
    if result[0] == "-":
        return "NA"
    return result

    
if __name__ == "__main__" : 
    """
    
    list_tableau = []
    
    list_tableau .append ([0.6 , 0.2 , 0.2])
    list_tableau .append ([0.5 , 0.5 , 0.0])
    list_tableau .append ([0.5 , 0.1 , 0.4])
    
    Candidat1 = [[ 0.4 , 0 , 0.6 ] , [0.3 , 0 , 0.7]]
    Candidat2 = [[ 0.1 , 0.9 , 0 ] , [0 , 1 , 0]]
    Candidat3 = [[ 0.35 , 0 , 0.65 ] , [0.3 , 0 , 0.7]]
    
    
    c1 = [ 0.58 , 0 , 0.42 , 0 ]
    c2 = [ 0, 0.9 , 0 , 0.1 ]
    c3 = [ 0.54 , 0 , 0.46 , 0 ]
    
    resultat = {'masseC1': 0.24, 'masseC2': 0.0, 
                'masseC3': 0.20, 'masseC1barre': 0.0, 
                'masseC2barre': 0.17, 'masseC3barre': 0.0, 
                'masseNA': 0.0, 'masseOm': 0.0, 'massevide': 0.39}
    
    #print(dempster((Candidat1 , Candidat2 , Candidat3)))
    """
    """
    #(13, 15)
    Candidat1 = [[0.13284131941161248, 0.7416154321571335, 0.12554324843125408]
    ,[0.3, 0.4, 0.3]]
    #(13, 16)
    Candidat2 = [[0.19671093300279918, 0.6280694524394681, 0.17521961455773272]
    ,[0.3, 0.4, 0.3]]
    #(13, 18)
    Candidat3 = [[0.2707458396920056, 0.49645184054754554, 0.23280231976044874]
    ,[0.3, 0.4, 0.3]]
    #(13, 17)
    Candidat4 = [[0.5656474715455644, 0, 0.4343525284544356]
    ,[0.8, 0.11428571428571424, 0.08571428571428567]]
    #(13, 19)
    Candidat5 = [[0.1, 0.8, 0.1]
    ,[0.3, 0.4, 0.3]]
    #(13, 22)
    Candidat6 = [[0.176637617014758, 0.6637553475293192, 0.15960703545592292]
    ,[0.3, 0.4, 0.3]]
    
    
    
    
    (7, 14)
    Candidat1 = [[0.1, 0.8, 0.1],
    [0.2, 0.3, 0.5]]
    (7, 11)
    Candidat2 = [[0.5674521093202527, 0, 0.43254789067974736],
    [0.2, 0.3, 0.5]]
    (7, 13)
    Candidat3 = [[0.3002662149610662, 0.4439711734025491, 0.2557626116363848],
    [0.2, 0.3, 0.5]]
    (7, 12)
    Candidat4 = [[0.6025559252809549, 0, 0.39744407471904514],
    [0.2, 0.3, 0.5]]
    
    
    print(dempster((Candidat1 , Candidat2 , Candidat3 ,
                    Candidat4 )))
    
    #print(fusionCandidat( (c1 , c2 , c3)))
    """
    
    Candidat1 = [[ 0.4 , 0 , 0.6 ] , [0.3 , 0 , 0.7] ]
    Candidat11 = [[ 0.4 , 0 , 0.6 ] , [0.3 , 0 , 0.7] , [0 , 1 , 0]]
    Candidat2 = [[ 0.4 , 0 , 0.6 ] , [0.3 , 0 , 0.7] , [0.5 , 0 , 0.5] , [0.5 , 0.1 , 0.4]]
    #Candidat2 = [[ 0.4 , 0 , 0.6 ] , [0.3 , 0 , 0.7] , [0.5 , 0 , 0.5] , [0.3 , 0.1 , 0.6]]
    
    
    c1 = fusionCritereConj(Candidat1)
    c11= fusionCritereConj(Candidat11)
    c2 = fusionCritereConj(Candidat2)
    
    #print(c1)
    #print(c11)
    #print(c2)
    
    Candidat1 = [[ 0.4 , 0 , 0.6 ] , [0.3 , 0 , 0.7] , [0.3 , 0.3 , 0.4]]
    c1 = fusionCritereConj(Candidat1)
    #print(c1)
    
    
    Candidat1 = [[0.1, 0.8, 0.1] , [0.1, 0.8, 0.1]]
    c1 = fusionCritereConj(Candidat1)
    print(c1)
    Candidat2 = [[0.1, 0.8, 0.1] , [0.1, 0.8, 0.1]]
    c2 = fusionCritereConj(Candidat2)
    print(c2)
    Candidat3 = [[0.1, 0.8, 0.1] , [0.1, 0.8, 0.1]]
    c3 = fusionCritereConj(Candidat3)
    print(c3)
    Candidat4 = [[0.8820518115462805, 0, 0.11794818845371949] , [0.8820518115462805, 0, 0.11794818845371949]]
    c4 = fusionCritereConj(Candidat4)
    print(c4)
    print(dempster((Candidat1 , Candidat2 , Candidat1 ,Candidat4  )))
    
"""
def fusionCandidat(c1 , c2 , c3) : 
    # c1[2] = c2[2] = c3[2] = m12 ( omega ) ?
    
    # c1 = candidat 1
    # c2 = candidat 2
    # c3 = candidat 3
    
    # c[0] = masse app
    # c[1] = masse non app
    # c[2] = masse nsp
    
    liste = {}
    
    masseVide = c1[0]*c2[1]*c3[1] + c1[1]*c2[0]*c3[1] + c1[1]*c2[1]*c3[0] + \
                c1[1]*c2[0]*c3[0] + c1[0]*c2[1]*c3[0] + c1[0]*c2[0]*c3[1] + \
                c1[3] + c2[3] + c3[3]
    
    liste["masseC1"] = c1[0] * (c2[1] + c2[2]) * (c3[1] + c3[2]) # sûr
    liste["masseC2"] = c2[0] * (c1[1] + c1[2]) * (c3[1] + c3[2]) # sûr
    liste["masseC3"] = c3[0] * (c1[1] + c1[2]) * (c2[1] + c2[2]) # sûr
    liste["masseC1barre"] = c1[1] * (c2[0] + c2[2]) * (c3[0] + c3[2]) # non 
    liste["masseC2barre"] = c2[1] * (c1[0] + c1[2]) * (c3[0] + c3[2]) # non 
    liste["masseC3barre"] = c3[1] * (c1[0] + c1[2]) * (c2[0] + c2[2]) # non 
    liste["masseNA"] = c1[1] * c2[1] * c3[1] # sûr
    liste["masseOm"] = c1[2] * c2[2] * c3[2] # quasi- sûr
    #liste["massevide"] = c1[3] * c2[3] * c3[3] # non 
    liste["massevide"] = masseVide
    
    return liste
"""

    
    
    