#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import shapely
import numpy as np
import math 


"""

distanceSamal("Route de Pressac" , "Route de Brantôme") = 0.31 ou 0.41 l'inverse'

"""

def distanceSamal(string1 , string2):
    
    # mesureRessemblanceToponymie
    tokenLigne = []
    tokenColonne = []

    string1 = process(string1)
    
    string1 = ignorePunctuation(string1)
    
    string2 = process(string2)
    string2 = ignorePunctuation(string2)
    
    st1 = StringTokenizer(string1)
    
    
    st2 = StringTokenizer(string2)
    
    #initialisation matrice
    matriceToken = np.zeros((len(st1), len(st2)))
    
    a=""
    for k in range(len(string1)):
        a+= string1[k]
        if string1[k] == " ":
            tokenLigne.append(a)
            a = ""
            
    b=""
    for k in range(len(string2)):
        b+= string2[k]
        if string2[k] == " ":
            tokenColonne.append(b)
            b = ""
  
    for i in range (len(tokenLigne)) : 
        for j in range (len(tokenColonne)): 
            pass 
            ecart = distance(tokenLigne[i], tokenColonne[j])
            # l'ecart relatif ici est la distance normalisée
            ecartRelatif = 1 - (ecart / max(len(tokenLigne[i]) , len(tokenColonne[j])))
            matriceToken[i][j] = ecartRelatif
            

    
    confidence = 0;
    for i in range(len(matriceToken)):
        max_ = 0;
        for j in range(len(matriceToken[0])):
            if matriceToken[i][j] >= max_ : 
                max_ = matriceToken[i][j]
      
    
        confidence += max_
  
    meanValue = ( len(matriceToken) + len(matriceToken[0]) ) / 2
    confidence /= meanValue
  
    return abs( 1  - confidence ) 



def distance(s1, s2) :
    # Step 1: initialize
    s1Length = len(s1)
    s2Length = len(s2)
    if s1Length == 0 : 
        return s2Length
    if s2Length == 0 : 
        return s1Length
    
    d = np.zeros((s1Length + 1, s2Length + 1))
    # Step 2: initialize first row and column
    for indexS1 in range(0,s1Length+1): 
        d[indexS1][0] = indexS1;
    
    for indexS2 in range(0,s2Length+1): 
        d[0][indexS2] = indexS2;
    

    # Step 3: examine characters from s1
    for indexS1 in range(1,s1Length+1): 
        charS1 = s1[indexS1 - 1]
        # Step 4: examine characters from s2
        for indexS2 in range(1,s2Length+1):
       
            charS2 = s2[indexS2 - 1]
            # Step 5: cost is 0 is characters are the same, 1 otherwise
            if charS1 == charS2 :
                cost = 0
            else : cost = 1
            # Step 6: set the cell cost to the min of its neighbours
            n1 = d[indexS1 - 1][indexS2] + 1
            n2 = d[indexS1][indexS2 - 1] + 1
            n3 = d[indexS1 - 1][indexS2 - 1] + cost
            d[indexS1][indexS2] = min(n1, min(n2, n3))
            
    # Step 7
    return d[s1Length][s2Length]



def process(s) :
    # if no processing required, return the string
    #if (!(this.ignoreAccent || this.ignoreCase || this.ignoreDash || this.ignoreWhitespace)) {
    #  return s;
    #}
    stringBuffer = ""
    # build a new string
    
    if isinstance(s, str) is False : 
        return stringBuffer
    
    for i in range(len(s)):
        c = s[i]
      #if (this.ignoreCase) :
      #        c = Character.toLowerCase(c);
        if verifAccent(s): 
            c = removeAccent(c)
      
        if  c == '_' or c == '-': 
            stringBuffer += ' '
        stringBuffer += c
    
    return stringBuffer

def verifAccent(s):
    if s == 'à' or s == 'â' or s == 'é' or s== 'è' or s == 'ê' or s == 'ë' or s == 'î' or s == 'ô' or s == 'ù' or s == 'ç' : 
        return True 
    else : return False
    
def removeAccent(s):
    if s == 'à' or s == 'â':
        return 'a'
    if s == 'é' or s== 'è' or s == 'ê' or s == 'ë':
        return 'e'
    if s == 'î':
        return 'i'
    if s == 'ô':
        return 'o'
    if s == 'ù':
        return 'u'
    if s == 'ç':
        return 'c'
    
    
def ignorePunctuation(chaine) :
    ponctuations = ".,;!#$/:?'()[]_-&{}"
    chaineStrippee = chaine
    chaineStrippee1 = ""
    chaineStrippee2 = ""

    
    for j in range(len(chaineStrippee)):
        lettre = chaineStrippee[j]
        a = 0
        for i in range (len(ponctuations)): 
            caracter = ponctuations[i]
            
            if lettre == caracter : 
                a = 1

        if a != 1 : 
            chaineStrippee1 += lettre

    st =  StringTokenizer(chaineStrippee1)
    #// Méthode qui va éliminer les mots contenant maximum 2 caractères
    for i in range(len(st)) : 
        mot = st[i];
        if len(mot) > 2 : 
            chaineStrippee2 += mot 
            chaineStrippee2 += " "
    
    return chaineStrippee2;

def StringTokenizer(chaine):
    l = []
    index = 0
    for i in range(len(chaine)):
        if chaine[i] == " ":
            l.append(chaine[index:i])
            index = i +1
    
    if index != len(chaine) : 
        l.append(chaine[index:len(chaine)])
    return l 

def CritereToponymique (dist , nomRef, nomComp , seuil): 
    
    tableau = []
    
    nomTopoComp = "" 
    if isinstance(nomComp, str) is False : 
        tableau.append(0)
        tableau.append(0)
        tableau.append(1)
        return tableau
    elif nomComp != "" :
        nomTopoComp = nomComp
        nomTopoComp = nomTopoComp.lower()
    else :
        tableau.append(0)
        tableau.append(0)
        tableau.append(1)
        return tableau
    
    nomTopoRef = ""
    if nomRef != "" :
        nomTopoRef = nomRef
        nomTopoRef = nomTopoRef.lower()
    else :
        tableau.append(0)
        tableau.append(0)
        tableau.append(1)
        return tableau

    distNorm = dist
    
    """
    
    featureRef = getGraphie(popRef)
    featureComp = getGraphie(popComp)
     
    if len(featureRef) > 0 : 
        if len(featureComp) > 0 : 
            for i in len(featureRef) :
                graphieRef = featureRef[i]
                graphieRef = graphieRef.lower()
                d = distance(graphieRef , nomTopoComp)
					
                if d < distNorm :
                    distNorm = d
				
                for j in range(len(featureComp)) : 
                    graphieComp = featureComp[j]
                    graphieComp = graphieComp.lower();
                    d = distance(graphieRef, graphieComp)
                    if d < distNorm :
                        distNorm = d		
				
        else :
            for i in len(featureRef) :
                graphieRef = featureRef[i]
                graphieRef = graphieRef.lower()
                d = distance(graphieRef , nomTopoComp)
					
                if d < distNorm :
                    distNorm = d 
				
			
    else :
        for j in range(len(graphieComp)) : 
            graphieComp = featureComp[j]
            graphieComp = graphieComp.lower();
            d = distance(nomTopoRef, graphieComp)
            if d < distNorm :
                distNorm = d	

    """
    if np.isnan(distNorm) :
        tableau.append(0)
        tableau.append(0)
        tableau.append(1)
    elif distNorm < seuil : 
        tableau.append((-0.70/seuil)*distNorm + 1)
        tableau.append((0.40/seuil)*distNorm)
        tableau.append((0.30/seuil)*distNorm)
    else :
        tableau.append(0.2)
        tableau.append(0.4)
        tableau.append(0.4)
    
	#// 	Return 3 masses sous forme de tableau
    return tableau

def getGraphie(pop):
    l = []
    l.append(pop["NOM"])
    return l

if __name__ == "__main__":
    
    chaine = 'Pressac'
    chaine1 = 'Brantôme'
    chaine2 = 'Point observation'
    chaine3 = 'Col de la Siberie'
    
    chaine = 'Point observation'
    chaine1 = 'Col de la Siberie'
    
    print(distanceSamal(chaine1 , chaine))
    
    
    
    """
    print(CritereToponymique (distanceSamal(chaine , chaine1) , chaine , chaine1))
    print(distanceSamal(chaine , chaine2))
    print(CritereToponymique (distanceSamal(chaine , chaine2) , chaine , chaine2))
    print(distanceSamal(chaine , chaine3))
    print(CritereToponymique (distanceSamal(chaine , chaine3) , chaine , chaine3))
    """
  