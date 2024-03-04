#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np 
import math

def dempster(liste_critere):
    
    # ajout candidat non app
    
    masseCan = []
    
    
    for i in range(len(liste_critere)):
        masseCan.append(fusionCritereConj(liste_critere[i]))     
        
    # fusion candidat 
    ( resultList , fusCandidat ) = fusionCandidat(masseCan)
    
    # decision 
    deci = decision(resultList , fusCandidat)
    
    return deci 
    

def fusionCritereConj(Candidat) : 
    
    dic = {}
    result = {}
    resultList = []
    transit = {}
    
    
    if len(Candidat) == 1  : 
        Candidat = Candidat[0]
        result["app"] = Candidat[0]
        result["-app"] = Candidat[1]
        result["theta"] = Candidat[2]
        result["phi"] = 0
        return result
        
        
    
    for i in range(len(Candidat)) : 
        dic["app"+str(i+1)] = Candidat[i][0]
        dic["-app"+str(i+1)] = Candidat[i][1]
        dic["theta"+ str(i+1)] = Candidat[i][2]
    result["app"] = 0
    result["-app"] = 0
    result["theta"] = 0
    result["phi"] = 0
    transit["app"] = 0
    transit["-app"] = 0
    transit["theta"] = 0
    transit["phi"] = 0
    
    matrice = [["app" , "phi" , "app"],
               ["phi" , "-app" , "-app"],
               ["app" , "-app" , "theta"]]
    
    for k in range(len(Candidat)-1):
        
        result["app"] = 0
        result["-app"] = 0
        result["theta"] = 0
        result["phi"] = 0
        
        if k == 0 : 
            
            colone = ["app1" , "-app1" , "theta1" ]
            
            ligne = ["app2" , "-app2" , "theta2" ]
            
            matrice = [["app" , "phi" , "app"],
                       ["phi" , "-app" , "-app"],
                       ["app" , "-app" , "theta"]]
        
            for i in range(np.shape(matrice)[0]):
                for j in range(np.shape(matrice)[1]):
                    jeu = matrice[i][j]
                    if dic[colone[j]] * dic[ligne[i]] != 0 :
                        result[jeu] += dic[colone[j]] * dic[ligne[i]]
        
        else : 
            
            ligne = ["app"+str(k+2) , "-app"+str(k+2) , "theta"+str(k+2) ]
            
            colone = ["app" , "-app" , "theta" , "phi" ]
            
            matrice = [["app" , "phi" , "app"],
                       ["phi" , "-app" , "-app"],
                       ["app" , "-app" , "theta"],
                       ["phi" , "phi" , "phi"]]
            
            
            for i in range(np.shape(matrice)[0]):
                for j in range(np.shape(matrice)[1]):
                    
                    jeu = matrice[i][j]
                    
                    
                    if colone[i][0] == 't':
                        result[jeu] += transit['theta'] * dic[ligne[j]]
                    elif colone[i][0] == 'p':
                        result[jeu] += transit['phi'] * dic[ligne[j]]
                    elif colone[i][0] == 'a':
                        result[jeu] += transit['app'] * dic[ligne[j]]
                    elif colone[i][0] == '-':
                        result[jeu] += transit['-app'] * dic[ligne[j]]
                    
                        
        
        transit["app"] = result["app"] 
        transit["-app"] = result["-app"] 
        transit["theta"] = result["theta"]
        transit["phi"] = result["phi"]
        
    return result
        


def fusionCandidat(candidat):
    
    # Changer pa rapport au fait que masseCan est un dictionnaire 
    
    # intialisation des dictionnaires
    
    
    if len(candidat) > 9 : 
        result = {}
        resultList = []
        result["C1"] = 0
        result["-C1"] = 0
        result["theta"] = 0
        result["phi"] = 0
        resultList.append("C1")
        resultList.append("-C1")
        resultList.append("theta")
        resultList.append("phi")
        return (resultList , result)
    

    
    
    dic = {}
    transit = {}
    result = {}
    resultList = []
    for i in range(len(candidat)) : 
        dic["C"+str(i+1)] = candidat[i]["app"]
        dic["-C"+str(i+1)] = candidat[i]["-app"]
        dic["theta"+ str(i+1)] = candidat[i]["theta"]
        dic["phi"+ str(i+1)] = candidat[i]["phi"]
        transit["C"+str(i+1)] = 0
        transit["-C"+str(i+1)] = 0
        result["C"+str(i+1)] = 0
        result["-C"+str(i+1)] = 0
        resultList.append("C"+str(i+1))
        resultList.append("-C"+str(i+1))
    transit["theta"] = 0
    transit["phi"] = 0
    result["theta"] = 0
    result["phi"] = 0
    #result["NA"] = 0
    resultList.append("theta")
    resultList.append("phi")
    #resultList.append("NA")
    
    
    if len(candidat) == 1 : 
        
        result["C1"] = candidat[i]["app"]
        result["-C1"] = candidat[i]["-app"]
        result["theta"] = candidat[i]["theta"]
        result["phi"] = candidat[i]["phi"]
    
    for k in range(len(candidat)-1):
        
        (ligne , colone , matrice) =  mat( k + 2 , len(candidat))
        
        listmodif = []
        
        
        for i in range(len(resultList)):
            result[resultList[i]] = 0
        
        
        for i in range(np.shape(matrice)[0]):
            for j in range(np.shape(matrice)[1]):
                jeu = str(matrice[i][j])[2:len(str(matrice[i][j]))-1]
                listmodif.append(jeu)
                #if dic[colone[j]] * dic[ligne[i]] != 0 :
                if k == 0 : 
                    coeff = dic[colone[j]] * dic[ligne[i]]
                else : 
                    if ligne[i][0] == 't':
                        coeff = transit['theta'] * dic[colone[j]]
                    elif ligne[i][0] == 'p':
                        coeff = transit['phi'] * dic[colone[j]]
                    else :
                        coeff = transit[ligne[i]] * dic[colone[j]]
                             
                # ajout NA
                if jeu == "NA":
                    lis = [k+1 for k in range(len(candidat))]
                    a = int(colone[j][::-1][0])
                    b = int(ligne[i][::-1][0])
                    reste= []
                    for n in range(len(lis)):
                        if lis[n]  in (a,b) : 
                            pass
                        else :
                            reste.append(lis[n])
                    
                    
                    if reste == [] : 
                        result[jeu] = coeff
                    else : 
                        string = 'NA'
                        string += str(reste) 
                        result[string] = coeff
                    
                else : 
                   result[jeu] += coeff


        for i in range(len(listmodif)):
            if listmodif[i] != "phi" and listmodif[i] != "theta" and listmodif[i] != "NA":
                transit[listmodif[i]] = result[listmodif[i]] 
        transit["theta"] = result["theta"] 
        transit["phi"] = result["phi"] 
        
    
    
    a = result['phi']
    if a != 1:
        for i in range(len(result)):
            result[list(result.keys())[i]] = result[list(result.keys())[i]] / ( 1 - a )
      
    result['phi'] = 0
    
    """
    sum_ = 0
    for i in range(len(result)):
        string = str(list(result.keys())[i])
        sum_ += result[string]
    """
    
    return ( resultList , result )
        

def mat( index , nbCandidat):
    
    colone = ("C"+ str(index) , "-C"+ str(index)  , "theta"+ str(index) , "phi"+ str(index))
    
    ligne = []
    
    for i in range(index-1):
        
        ligne.append("C"+str(i+1))
        ligne.append("-C"+str(i+1))
    
            
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
        
        if x[0] == 'C' :
            if y[0] == 'C' : 
                return "phi"
            if y[0] == '-' :
                return x
        
    
    if len(y) > 2:
        if y[0:3] == "phi" : 
            return "phi"
        if y[0:5] == "theta":
            return x
        
        if y[0] == 'C' :
            if x[0] == 'C' : 
                return "phi"
            if x[0] == '-' :
                return y
                

    
    if x[0] == "C" : 
        
        if y[0] == "C" :    
            if x[1] != y[1] : 
                return "phi"
            
        if y[0] == "-" : 
            
            if x[1] != y[2] : 
                return x
            elif len(x) == len(y) - 2 :
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
    

import numpy
def decision(resultList , fusion):
    
    proba = {}
    
    
        
    a = int((len(resultList) - 2 )/ 2)
    
    if a == 1 :
        if fusion["C1"] > fusion["-C1"] or fusion["C1"] > fusion["theta"] :
            return "C1"
        else : return "NA"
    
    app  = []
    _app = []
    
    for i in range(a):
        app.append(fusion['C' + str(i+1)])
        _app.append(fusion['-C' + str(i+1)])
        
    result  = np.array(app) @ numpy.eye(a)
    result += np.array(_app) @ (1/(a) * ( numpy.ones(a) - numpy.eye(a) ))
    
    
    
    ligneNA = []
    matrice = []
    
    
    for i in range(len(fusion)):
        if list(fusion.keys())[i][0:2] == 'NA': 
            ligneNA.append(fusion[list(fusion.keys())[i]])
            ligne = [0 for i in range(a)]
            for j in range(int( (len(list(fusion.keys())[i]) ) /3  ) ):
                """
                if 3*j + 3 == 24 : 
                    chiffre = 10
                    ligne[int(chiffre) - 1] = 1/(a - 1)
                """
                chiffre = list(fusion.keys())[i][3*j +3]
                ligne[int(chiffre) - 1] = 1/(a - 1)
                
            
            matrice.append(ligne)
    
    
                
    result +=   np.array(ligneNA) @ matrice
    
    
    resultNA = np.array(ligneNA) @ ( 1/(a - 1) * np.ones(len(ligneNA)))
    resultNA += np.array(_app) @ (1/(a) * np.ones(a))

    
    
    for i in range(a):
        proba['C' + str(i+1)] = result[i]
        proba['C' + str(i+1)] += fusion['theta']/(a+1)
    proba['NA'] = resultNA
    proba['NA'] += fusion['theta']/(a+1)
    
    
    sum_ = 0
    for i in range(len(proba)):
        string = str(list(proba.keys())[i])
        sum_ += proba[string]
    
    max_ = 0
    for i in range(len(list(proba.keys()))):
        if proba[str(list(proba.keys())[i])] > max_ : 
            max_ = proba[str(list(proba.keys())[i])]
            result = str(list(proba.keys())[i])
        
    
    if result == 'NA' : 
        return 'NA'
    
    epsilon = 0.01
    if proba['NA'] - epsilon < max_ and max_ < proba['NA'] + epsilon :
        return "NA"
    
    
    return result
                    
              
                
if __name__ == "__main__" : 
    
    Candidat1 = [[0.5511923335630442, 0.13274213314042746, 0.3160655332965283], [0.01, 0.29000000000000004, 0.7]]
    Candidat2 = [[0.01, 0.29000000000000004, 0.7], [0.01, 0.29000000000000004, 0.7]]
    Candidat3 = [[0.4992905470434321, 0.14754996651777896, 0.3531594864387889], [0.01, 0.29000000000000004, 0.7]]
    Candidat4 = [[0.4992905470434321, 0.14754996651777896, 0.3531594864387889], [0.01, 0.29000000000000004, 0.7]]
    
    
    
    print(mat( 10 , 10)[2])
    
    
    """
    # 2077
    Candidat1 = [[0.5511923335630442, 0.13274213314042746, 0.3160655332965283], [0.01, 0.29000000000000004, 0.7]]
    Candidat2 = [[0.01, 0.29000000000000004, 0.7], [0.01, 0.29000000000000004, 0.7]]
    Candidat3 = [[0.4992905470434321, 0.14754996651777896, 0.3531594864387889], [0.01, 0.29000000000000004, 0.7]]

    
    c1 = fusionCritereConj(Candidat1)
    print("fusionCritereC1 = ",c1)
    print(" ")
    c2 = fusionCritereConj(Candidat2)
    print("fusionCritereC2 = ",c2)
    print(" ")
    c3 = fusionCritereConj(Candidat3)
    print("fusionCritereC3 = ",c3)
    print(" ")
    
    d = dempster(( Candidat1 , Candidat2 , Candidat3))
    print(" ")
    print(d)
    
    d = dempster(( Candidat2 , Candidat3 , Candidat1))
    print(" ")
    print(d)
    
    Candidat1 = [[ 0.4 , 0 , 0.6 ] , [0.3 , 0 , 0.7]]
    Candidat2 = [[ 0.1 , 0.9 , 0 ] , [0 , 1 , 0]]
    Candidat3 = [[ 0.35 , 0 , 0.65 ] , [0.3 , 0 , 0.7]]
    
    c1 = [ 0.58 , 0 , 0.42 , 0 ]
    c2 = [ 0, 0.9 , 0 , 0.1 ]
    c3 = [ 0.54 , 0 , 0.46 , 0 ]
    
    print(dempster((Candidat1 , Candidat2 , Candidat3)))
    
    
    resultat = {'masseC1': 0.24, 'masseC1barre': 0.0,
                'masseC2': 0.0,  'masseC2barre': 0.17, 
                'masseC3': 0.20, 'masseC3barre': 0.0, 
                'masseNA': 0.0, 'masseOm': 0.0, 'massevide': 0.39}
    
    """
    

    
    
    