# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 05:40:25 2020

@author: R.S_PC
"""
import shapefile as sf

facA = sf.Reader(r"F:\Stuff\Current_Term\KNTU\papers\ISI\ShapeFiles\hallway39sq.shp")
grids = facA.shapes()

myGrids = sf.Writer(r'F:\Stuff\Current_Term\KNTU\papers\ISI\test\hallway39final.shp', shapeType=5)
myGrids.field('ind', 'C')
k=1
for j in range(int(len(grids)/20)):
    bb1 = grids[j*20].bbox
    bb2 = grids[(j+1)*20-1].bbox
    print(j*20)
    print((j+1)*20-1)
    print('-----------')
    dif = (bb1[1]-bb2[1])/2+0.25
    dif2 = 0.25/15
    bb2[2] = bb2[2]+dif2*k
    bb1[0] = bb1[0] + dif2*(k-1)
    myGrids.poly([[[bb1[0], bb1[3]], [bb2[2], bb1[3]], [bb2[2], bb2[1]+dif-0.25/2], [bb1[0], bb2[1]+dif-0.25/2]]])
    myGrids.record(str(5)) 
    myGrids.poly([[[bb1[0], bb1[3]-dif+0.25/2], [bb2[2], bb1[3]-dif+0.25/2], [bb2[2], bb2[1]], [bb1[0], bb2[1]]]])
    myGrids.record(str(5))
    k = k+1
myGrids.close()
    