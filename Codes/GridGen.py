# -*- coding: utf-8 -*-
"""
Created on Tue May 26 07:30:42 2020

@author: R.S_PC
"""

import shapefile as sf
hallways = [8, 70, 4, 16, 53, 23, 39, 34]
stairs = [26, 24, 42, 40, 54, 56, 19, 17, 12, 10, 71, 72, 7, 5, 30, 32]
sites = [35, 27, 20, 15, 14, 13, 3, 2, 1]
elevator = [57]
test = [33, 36, 38, 45, 43, 47, 62, 69]
fac = sf.Reader(r"F:\Stuff\Current_Term\KNTU\papers\ISI\faculty_Areas.shp")
geomfac = fac.shapes()
myGrids = sf.Writer(r'F:\Stuff\Current_Term\KNTU\papers\ISI\test\all12.shp', shapeType=5)
myGrids.field('ind', 'C')
ind = fac.records()
h = 1
w = 1
def horiz():
    global w, h
    stepx = (bb[2]-bb[0])/int((bb[2]-bb[0])/h)
    if (bb[3]-bb[1]) < w:
        w = (bb[3]-bb[1])
    if (bb[2]-bb[0]) < h:
        h = (bb[2]-bb[0])
    stepy = (bb[3]-bb[1])/int((bb[3]-bb[1])/w)
    for i in range(0,int((bb[2]-bb[0])/h)):
        for j in range(0,int((bb[3]-bb[1])/w)):
            myGrids.poly([[[bb[0]+i*stepx,bb[1]+j*stepy],[bb[0]+i*stepx,bb[1]+(j+1)*stepy],[bb[0]+(i+1)*stepx,bb[1]+(j+1)*stepy],[bb[0]+(i+1)*stepx,bb[1]+j*stepy]]])
            myGrids.record(str(1))   
                
def vert():
    global w, h
    h = w
    w = h
    stepx = (bb[3]-bb[1])/int((bb[3]-bb[1])/h)
    if (bb[3]-bb[1]) < h:
        h = (bb[3]-bb[1])
    if (bb[2]-bb[0]) < w:
        w = (bb[2]-bb[0])
    stepy = (bb[3]-bb[1])/int((bb[3]-bb[1])/w)
    for i in range(0,int((bb[3]-bb[1])/h)):
        for j in range(0,int((bb[3]-bb[1])/w)):
            myGrids.poly([[[bb[0]+i*stepx,bb[1]+j*stepy],[bb[0]+i*stepx,bb[1]+(j+1)*stepy],[bb[0]+(i+1)*stepx,bb[1]+(j+1)*stepy],[bb[0]+(i+1)*stepx,bb[1]+j*stepy]]])
            myGrids.record(str(2))
def squre():
    stepx = (bb[2]-bb[0])/int((bb[2]-bb[0])/h)
    stepy = (bb[3]-bb[1])/int((bb[3]-bb[1])/h) 
    for i in range(0,int((bb[2]-bb[0])/h)):
        for j in range(0,int((bb[3]-bb[1])/h)):
            myGrids.poly([[[bb[0]+i*stepx,bb[1]+j*stepy],[bb[0]+i*stepx,bb[1]+(j+1)*stepy],[bb[0]+(i+1)*stepx,bb[1]+(j+1)*stepy],[bb[0]+(i+1)*stepx,bb[1]+j*stepy]]])
            myGrids.record(str(3))             
for j in range(len(geomfac)):
    shp1 = geomfac[j]
    bb = shp1.bbox
    detector = ind[j][0]
    if detector in hallways:
        #horiz()
        print("hi")
    elif detector in stairs:
        #vert()
        print("hi")
    elif detector in test:
        squre()
        print("hi")
    elif detector in sites:
        #squre()
        print("hi")
    else:
        #squre()
        print("hi")
myGrids.close()
