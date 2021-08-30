 # -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 13:20:13 2019

@author: R.S_PC
"""

from AstarGrid31 import AstarGrid
#from AstarGraph3 import AstarGraph
from GridGraphGenerator31 import GridGraphGenerator
import pandas as pd
import numpy as np
#from TransitionCellFinder3 import transitionCellFinder
import psycopg2 as pc
#import math
import timeit
from shower31 import show
import matplotlib.pyplot as plt
def fullStarGrid(mstart, mend):
#    plt.figure()
# generate graph and grid models
    GridGraphGenerator()

# generate the path in graph level
#graph = pd.read_csv('graph.csv', header=None)
#graph = np.asarray(graph)
#nodeCenter = pd.read_csv('nodeCenter.csv', header=None)
#nodeCenter = np.asarray(nodeCenter)
#st1 = time.time()
#path = AstarGraph(graph, nodeCenter, cost, 21, 14)
#ft1 = time.time()

# generate the path in grid level

#transitionCellFinder()
#transitionCell = pd.read_csv('TransitionCellsAtr.csv', header=None)
#transitionCell = np.asarray(transitionCell)
#nodeName = pd.read_csv('nodeName.csv', header=None)
#nodeName = np.array(nodeName)
#edgeName = pd.read_csv('edgeName.csv', header=None)
#edgeName = np.array(edgeName)
#pathPart = []
#translatedPath = []
#for p in path:
#    for item in graphIndex.items():
#        if (item[1] == p) and (item[0] in nodeName) and (p not in edgeName):
#            name = 'node' + str(item[0]) + '.csv'
#            pathPart.append(np.asarray(pd.read_csv(name, header=None)))
#            translatedPath.append(item[0])
#        elif p in edgeName:
#            name = 'edge' + str(p) + '.csv'
#            pathPart.append(np.asarray(pd.read_csv(name, header=None)))
#            translatedPath.append(p)
#            break
#
#def minDist(a, b):
#    a1 = 999
#    conn = pc.connect(host="localhost",database="My Drawing", user="postgres", password="fear3560")
#    cur = conn.cursor()
#    # number of nodes
#    for cell in b:
#        conn.rollback()
#        query = 'select id, centerx, centery from  public."myDeawingFullCellOneDimension" where id='+str(a)
#        cur.execute(query)
#        coordinate = cur.fetchall()
#        coordinate = np.array(coordinate, dtype = float)
#        query = 'select id, centerx, centery from  public."myDeawingFullCellOneDimension" where id='+ str(cell)
#        cur.execute(query)
#        coordinate1 = cur.fetchall()
#        coordinate1 = np.array(coordinate1, dtype = float)
#        coordinate = np.vstack((coordinate,coordinate1))
#        b = math.sqrt((coordinate[0][1]-coordinate[1][1])**2 + (coordinate[0][2]-coordinate[1][2])**2)
#        if b ==  min(a1, b):
#            start = cell
#            a1 = b
#    return start
#st = pathPart[0][start1]
#en = pathPart[-1][end1]
#st2 = time.time()
#for i in range(len(translatedPath)):
#    startCandidate = []
#    endCandidate = []
#    a = transitionCell[:,1:] == translatedPath[i]
#    b = []
#    c = []
#    if i+1<len(translatedPath):
#        b = transitionCell[:,1:] == translatedPath[i+1]
#    if i-1>-1:
#        c = transitionCell[:,1:] == translatedPath[i-1]
#    if len(b)>0:
#        for j in range(len(transitionCell)):
#            if (a[j].any() and b[j].any()) and transitionCell[j, 0] in pathPart[i]:
#                startCandidate.append(transitionCell[j,0])
#        start = minDist(st, startCandidate)
#    if len(c)>0:
#        for j in range(len(transitionCell)):
#            if a[j].any() and c[j].any() and transitionCell[j, 0] in pathPart[i]:
#                endCandidate.append(transitionCell[j,0])
#        end = minDist(start, endCandidate)
#    if i == 0:
#        AstarGrid(pathPart[i],st, start, translatedPath[i])
#    elif i == len(translatedPath)-1:
#        AstarGrid(pathPart[i],end, en, translatedPath[i])
#    else:
#        AstarGrid(pathPart[i], start, end, translatedPath[i])
#    show()
    pathPart = pd.read_csv('node11.csv', header=None)
    pathPart = np.array(pathPart)
    st2 = timeit.default_timer()
    ln = AstarGrid(pathPart, mstart, mend, 1)
    ft2 = timeit.default_timer()
#    mySrt = 'time = '+str(ft2-st2)
#    print(mySrt)
    conn = pc.connect(host="localhost",database="My Drawing", user="postgres", password="fear3560")
    cur = conn.cursor()
    conn.rollback()
    query = 'select centerx, centery from  public."Grid" where id='+str(mstart)+' or id= '+str(mend)
    cur.execute(query)
    coordinate = cur.fetchall()
    coordinate = np.array(coordinate)
#    plt.plot(coordinate[:,0],coordinate[:,1],'bo', label = "Cheked")
#    plt.plot(coordinate[:,0],coordinate[:,1],'r*', label = "Path")
#    plt.plot(coordinate[:,0],coordinate[:,1],'g*', label = "Start/End")
#    plt.legend()
    #plt.axis('off')
    ste = str(mstart)+'_'+str(mend)
    plt.savefig(ste)
    return ln, (ft2-st2)
















