# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 07:28:14 2020

@author: R.S_PC
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 05:40:25 2020

@author: R.S_PC
"""
import shapefile as sf

facA = sf.Reader(r"F:\Stuff\Current_Term\KNTU\papers\ISI\ShapeFiles\mergeTest.shp")
grids = facA.shapes()

myGrids = sf.Writer(r'F:\Stuff\Current_Term\KNTU\papers\ISI\test\stair12final.shp', shapeType=5)
myGrids.field('ind', 'C')
bb1 = grids[0].bbox
bb2 = grids[-1].bbox
while not(bb1[3] <= bb2[1]):
    bb1[1] = bb1[3] - 0.5
    myGrids.poly([[[bb1[0], bb1[3]], [bb2[2], bb1[3]], [bb2[2], bb1[1]], [bb1[0], bb1[1]]]])
    myGrids.record(str(63))
    bb1[3] = bb1[1]
    print(bb1[1])
    print(bb1[3])
    print('--------')
#    myGrids.poly([[[bb1[0], bb1[3]], [bb2[2], bb1[3]], [bb2[2], bb2[1]], [bb1[0], bb2[1]]]])
#    myGrids.record(str(5))
myGrids.close()
    