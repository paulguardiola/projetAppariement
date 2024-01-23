#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shapely

def distanceEuclidienne(geomRef, geomComp):
    centroidRef = geomRef.centroid
    centroidComp = geomComp.centroid
    distance = ((centroidRef[0] - centroidComp[0])**2 + (centroidRef[1] - centroidComp[1])**2)**.5
    return distance 