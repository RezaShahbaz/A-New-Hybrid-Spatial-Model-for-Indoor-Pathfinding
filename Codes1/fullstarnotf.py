# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 13:20:13 2019

@author: R.S_PC
"""

from AstarGrid1f import AstarGrid
from AstarGraph1f import AstarGraph
from GridGraphGenerator1f import GridGraphGenerator
from showerf import show
import pandas as pd
import numpy as np
#from TransitionCellFinder1 import transitionCellFinder
import psycopg2 as pc
import math
import timeit
import matplotlib.pyplot as plt

mstart = 143
mend = 899
# generate graph and grid models
graphIndex, cost = GridGraphGenerator()

# generate the path in graph level
graph = pd.read_csv('graph.csv', header=None)
graph = np.asarray(graph)
nodeCenter = pd.read_csv('nodeCenter.csv', header=None)
nodeCenter = np.asarray(nodeCenter)
conn = pc.connect(host="localhost",database="My Drawing", user="postgres", password="fear3560")
cur = conn.cursor()
cur.execute('select Node from  public."facultyFinal" where id='+str(mstart))
sm = cur.fetchall()
conn.rollback()
cur.execute('select Node from  public."facultyFinal" where id='+str(mend))
em = cur.fetchall()
st0 = timeit.default_timer()
path = AstarGraph(graph, nodeCenter, cost, sm[0][0], em[0][0])
ft0 = timeit.default_timer()
show()
#transitionCellFinder()
# generate the path in grid level
transitionCell = pd.read_csv('TransitionCellsAtr3.csv', header=None)
transitionCell = np.asarray(transitionCell)
nodeName = pd.read_csv('nodeName.csv', header=None)
nodeName = np.array(nodeName)
edgeName = pd.read_csv('edgeName.csv', header=None)
edgeName = np.array(edgeName)
pathPart = []
translatedPath = []
tempp = 0
for p in path:
    for item in graphIndex.items():
        if (item[1] == p) and (item[0] in nodeName):
            name = 'node' + str(item[0]) + '.csv'
            pathPart.append(np.asarray(pd.read_csv(name, header=None)))
            translatedPath.append(item[0])
            print("node = " + str(item[0]))
            tempp = 0
            break
        elif (p in edgeName) and (tempp < 1):
            name = 'edge' + str(p) + '.csv'
            pathPart.append(np.asarray(pd.read_csv(name, header=None)))
            translatedPath.append(p)
            print("edge = " + str(p))
            tempp = tempp + 1
            break

def minDist(a, b):
    a1 = 999
    conn = pc.connect(host="localhost",database="My Drawing", user="postgres", password="fear3560")
    cur = conn.cursor()
    # number of nodes
    for cell in b:
        conn.rollback()
        query = 'select id, centerx, centery from  public."facultyFinal" where id='+str(a)
        cur.execute(query)
        coordinate = cur.fetchall()
        coordinate = np.array(coordinate, dtype = float)
        query = 'select id, centerx, centery from  public."facultyFinal" where id='+ str(cell)
        cur.execute(query)
        coordinate1 = cur.fetchall()
        coordinate1 = np.array(coordinate1, dtype = float)
        coordinate = np.vstack((coordinate,coordinate1))
        b = math.sqrt((coordinate[0][1]-coordinate[1][1])**2 + (coordinate[0][2]-coordinate[1][2])**2)
        if b ==  min(a1, b):
            start = cell
            a1 = b
    return start
st = mstart
en = mend
ln11 = 0
ln22 = 0
ln33 = 0
aaa = 0
it = 1 
it2 = 1
for i in range(len(translatedPath)):
    startCandidate = []
    endCandidate = []
    a = transitionCell[:,1:] == translatedPath[i]
    b = []
    c = []
    if i+1<len(translatedPath):
        b = transitionCell[:,1:] == translatedPath[i+1]
    if i-1>-1:
        c = transitionCell[:,1:] == translatedPath[i-1]
    if len(b)>0:
        for j in range(len(transitionCell)):
            if (a[j].any() and b[j].any()) and transitionCell[j, 0] in pathPart[i]:
                startCandidate.append(transitionCell[j,0])
        start = minDist(st, startCandidate)
    if len(c)>0:
        for j in range(len(transitionCell)):
            if a[j].any() and c[j].any() and transitionCell[j, 0] in pathPart[i]:
                endCandidate.append(transitionCell[j,0])
        end = minDist(start, endCandidate)
    if i == 0:
        st1 = timeit.default_timer()
        ln1, it = AstarGrid(pathPart[i],st, start, translatedPath[i], 1)
        ft1 = timeit.default_timer()
        ln11 = ln11+ln1

    elif i == len(translatedPath)-1:
        st2 = timeit.default_timer()
        ln2, it1 = AstarGrid(pathPart[i],end, en, translatedPath[i], it)
        ft2 = timeit.default_timer()
        ln22 = ln22+ln2
    else:
        st3 = timeit.default_timer()
        ln3, it2 = AstarGrid(pathPart[i], start, end, translatedPath[i], it+1)
        it = it2
        ft3 = timeit.default_timer()
        ln33 = ln33+ln3
        aaa = (ft3-st3) + aaa
conn.rollback()
query = 'select centerx, centery from  public."facultyFinal" where id='+str(mstart)+' or id= '+str(mend)
cur.execute(query)
coordinate = cur.fetchall()
coordinate = np.array(coordinate)
plt.plot(coordinate[:,0],coordinate[:,1],'bo', label = "Cheked")
plt.plot(coordinate[:,0],coordinate[:,1],'r*', label = "Path")
plt.plot(coordinate[:,0],coordinate[:,1],'g*', label = "Start/End")
#plt.plot(obs[0],obs[1],'ko', markersize=2, label = "Obstacle")
#plt.plot(obs[2],obs[3],'rs', markersize=3, label = "Exit")
plt.legend()
#ste = str(mstart)+'_'+str(mend)
#plt.savefig(ste)
#plt.savefig("dng.png",format="png", dpi=500,bbox_inches="tight")
















