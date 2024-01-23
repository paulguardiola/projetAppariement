import Operateurs 
import shapely

def distanceSurfaciqueRobuste(geomA , geomB, minRes, maxRes ) :
    inter = Operateurs.intersectionRobuste(geomA, geomB, minRes, maxRes)
    # en cas de problème d'intersection avec JTS, la methode retourne 2 
    if inter == None : return 2 
    union = shapely.union(geomA,geomB)
    if union == None : return 1
    return 1 - inter.area / union.area



# exactitude = surface( A inter B) / Surface (A)
def exactitude(geomA, geomB):
    inter = shapely.intersection(geomA , geomB)
    if inter.is_empty is True : return 0
    return inter.area / geomA.area
    
# completude = surface( A inter B) / Surface (B) 
def completude(geomA , geomB): 
    return exactitude(geomB, geomA)