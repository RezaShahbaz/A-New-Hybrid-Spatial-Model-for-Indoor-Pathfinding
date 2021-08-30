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

myGrids = sf.Writer(r'F:\Stuff\Current_Term\KNTU\papers\ISI\shape2\test3.shp', shapeType=5)
myGrids.field('ind', 'C')
bb1 = grids[80+1260].bbox
bbb = bb1[0]
bb2 = grids[47].bbox
bb = bbb
for i in range(3):
    bb1 = grids[2*i*24+80+1260].bbox
    bb2 = grids[2*(i+1)*24-1+80+1260].bbox
    a = 0.5
    bb = bb + a
    while not(bb1[3] <= bb2[1]):
        bb1[1] = bb1[3] - 0.5
        myGrids.poly([[[bbb, bb1[3]], [bb, bb1[3]], [bb, bb1[1]], [bbb, bb1[1]]]])
        myGrids.record(str(64))
        bb1[3] = bb1[1]
    bbb = bb
myGrids.close()
    