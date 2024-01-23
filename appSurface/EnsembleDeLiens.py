
import networkx as nwx


def transformeEnCarteTopo(popRef, popComp, appariement):
    
    G = nwx.Graph()
    
    #creation des noeuds 
    noeudRef  = [popRef[i] for i in range(len(popRef))]
    noeudComp = [popComp[i] for i in range(len(popComp))]
    
    #creation des arcs du graphe = lien d'appariement 
    