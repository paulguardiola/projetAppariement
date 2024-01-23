#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np 
import math

def dempster(liste_critere):
    
    Candidat1 = liste_critere[0] # [Critere1 , Critere2 , Critere3]
    Candidat2 = liste_critere[1] #[Critere1 , Critere2 , Critere3]
    Candidat3 = liste_critere[2] #[Critere1 , Critere2 , Critere3]
    
    # fusion Critere 
    masseCandidat1 = fusionCritere (Candidat1)
    masseCandidat2 = fusionCritere (Candidat2)
    masseCandidat3 = fusionCritere (Candidat3)
    
    # fusion candidat 
    fusCandidat = fusionCandidat(masseCandidat1 , masseCandidat2 , masseCandidat3)
    
    # decision 
    deci = decision(fusCandidat)
    
    return deci 

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
        
    return source




def fusionCandidat(c1 , c2 , c3) : 
    # c1[2] = c2[2] = c3[2] = m12 ( omega ) ?
    
    # c1 = candidat 1
    # c2 = candidat 2
    # c3 = candidat 3
    
    # c[0] = masse app
    # c[1] = masse non app
    # c[2] = masse nsp
    
    liste = {}
    
    print(c1)
    print(c2)
    
    
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
    

    
def decision(l):
    
    
    masseC1 = l["masseC1"]
    masseC2 = l["masseC2"]
    masseC3 = l["masseC3"]
    masseC1barre = l["masseC1barre"]
    masseC2barre = l["masseC1barre"]
    masseC3barre = l["masseC1barre"]
    masseNA = l["masseNA"]
    masseOm = l["masseOm"]
    massevide = l["massevide"]
    
    liste = {}
    
    liste["PC1"] = masseC1 + masseC2barre/3 + masseC3barre/3 + masseOm/6
    liste["PC2"] = masseC2 + masseC1barre/3 + masseC3barre/3 + masseOm/6
    liste["PC3"] = masseC3 + masseC1barre/3 + masseC2barre/3 + masseOm/6
    liste["PC1barre"] = masseC1barre + masseC2/3 + masseC3/3 + masseOm/6
    liste["PC2barre"] = masseC2barre + masseC1/3 + masseC3/3 + masseOm/6
    liste["PC3barre"] = masseC3barre + masseC1/3 + masseC2/3 + masseOm/6
    liste["POm"] = masseOm 
    liste["Pvide"] = massevide
    
    return liste 







    
if __name__ == "__main__" : 
    
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
    
    #print(dempster(( Candidat1 , Candidat2 , Candidat3)))
    print(fusionCandidat(c1 , c2 , c3))
    print(" ")
    
    print(resultat)
    
    