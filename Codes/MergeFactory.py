# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 21:34:58 2020

@author: R.S_PC
"""

import shapefile as sf
import shapely.geometry as sg

facA = sf.Reader(r"F:\Stuff\Current_Term\KNTU\papers\ISI\faculty_Areas.shp")
areaGeoms = facA.shapes()

facG = sf.Reader(r"F:\Stuff\Current_Term\KNTU\papers\ISI\ShapeFiles\Grid0.25.shp")
gridGeoms = facG.shapes()

ind = facA.records()
list1 = []

myGrids = sf.Writer(r'F:\Stuff\Current_Term\KNTU\papers\ISI\test\mergeTest.shp', shapeType=5)
myGrids.field('ind', 'C')
for j in range(len(areaGeoms)):
    shp1 = areaGeoms[j]
    bb1 = shp1.bbox
    detector = ind[j][0]
    if detector == 27:
        container = sg.box(bb1[0], bb1[1], bb1[2], bb1[3], ccw = True)
        for i in range(len(gridGeoms)):
            shp2 = gridGeoms[i]
            bb2 = shp2.bbox
            grids = sg.box(bb2[0], bb2[1], bb2[2], bb2[3], ccw = True)
            if container.contains(grids) or container.crosses(grids) or container.intersects(grids):
                list1.append(shp2)
                myGrids.shape(shp2)
                myGrids.record(str(27))   
myGrids.close()
                
            