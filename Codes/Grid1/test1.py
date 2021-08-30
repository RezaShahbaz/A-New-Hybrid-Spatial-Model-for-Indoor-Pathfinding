# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 16:08:39 2019

@author: R.S_PC
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 22:14:51 2019

@author: R.S_PC
"""

import numpy as np
from matplotlib import pyplot as plt
import psycopg2 as pc
import pandas as pd
#import owlready2
#import re
import math
#def AstarGrid(grid, s, e, gridNum):
e = 4086
s = 124
pathPart = pd.read_csv('node1.csv', header=None)
data1 = pd.read_csv('data.csv', header=None)
data1 = np.array(data1)
plt.figure(2)
plt.plot(data1[:,1], data1[:,2], 'co')
grid = np.array(pathPart)
gridNum = 1
dest1 = np.where(grid == s)
dest2 = np.where(grid == e)
start = (dest1[0][0], dest1[1][0])
end = (dest2[0][0], dest2[1][0])
#    # load OWL file
#    my_world = owlready2.World()
#    my_world.get_ontology(r"F:\Stuff\Current_Term\KNTU\Thesis\ProtegeModels\My Drawing\FNormalNormal.owl").load()
#    
#    # Convert OWL axioms to RDF graph
#    graph = my_world.as_rdflib_graph()
#    
#    # query
#    # last space in each line is necessary
#    query = "PREFIX : <http://www.semanticweb.org/r.s_pc/ontologies/2019/11/NormalNormal#> " \
#                "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> " \
#                "SELECT ?s " \
#                "WHERE {?s rdf:type :Obstacle }"
#    resultlist = graph.query(query)
#    
#    # convert results to list of integers
#    response = []
#    for item in resultlist:
#        s = str(item['s'].toPython())
#        s = re.sub(r'.*#',"",s)
#    
#        response.append(int(s))
#    

gridMat = np.zeros(grid.shape)

for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        if grid[i, j]==0:
            gridMat[i, j] = 1
    
global shape
shape = gridMat.shape
conn = pc.connect(host="localhost",database="My Drawing", user="postgres", password="fear3560")
cur = conn.cursor()
conn.rollback()

#    cur.execute('select distinct width, height from public."myDrawingfullGraphSameCell"\
#                where node = 1')
global dim
dim = np.array([[1, 1]])

def hvalue(point):
    global dim
    dx = abs(point[1] - end[1])*dim[0,0]
    dy = abs(point[0] - end[0])*dim[0,1]
    return math.sqrt(dx**2 + dy**2)


def VerNeigh(point1, point2):
    if (point2[0], point2[1]) in [(point1[0],point1[1]+1),(point1[0],point1[1]-1)]:
        return True
    else:
        return False
    
def HorNeigh(point1, point2):
    if (point2[0], point2[1]) in [(point1[0]+1,point1[1]),(point1[0]-1,point1[1])]:
        return True
    else:
        return False

def diagNeigh(point1, point2):
    if (point2[0], point2[1]) in [(point1[0]-1,point1[1]+1),(point1[0]+1,point1[1]-1),(point1[0]-1,point1[1]-1),(point1[0]+1,point1[1]+1)]:
        return True
    else:
        return False    
    
def gvalue(point1, point2):
    global dim
    if diagNeigh(point1, point2):
        return math.sqrt(dim[0,0]**2 + dim[0,1]**2)
    elif HorNeigh(point1, point2):
        return dim[0,0]
    elif VerNeigh(point1, point2):
        return dim[0,1]
    else:
        print("its not neighbour")
        
def neighbours(point):
    global shape
    neighbours = []
    for dx, dy in [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]:
        neighX = point[0]+dx
        neighy = point[1]+dy
        if not (neighX<0 or neighX>shape[0]-1 or neighy<0 or neighy>shape[1]-1) and gridMat[neighX, neighy] != 1:
            neighbours.append((neighX, neighy))
    return neighbours
        
#    for i in range(shape[0]):
#        for j in range(shape[1]):
#            if gridMat[i,j] == 0:
#                plt.plot(j, shape[0]-i,'bo')
#            elif gridMat[i,j] == 1:
#                plt.plot(j, shape[0]-i,'ko')     
    
        
openList = {}
closeList = [start]
currentLocation = start
score = np.zeros(gridMat.shape)
iterator = 0
parent = {}
while currentLocation != end:
    for point in neighbours(currentLocation):
        if point not in closeList:
            if score[point]>gvalue(currentLocation, point)+score[currentLocation] or score[point]==0:
                score[point] = gvalue(currentLocation, point)+score[currentLocation]
                parent.update({point:currentLocation})
            gscore = score[point]#gvalue(currentLocation, point) + score[currentLocation]
            hscore = hvalue(point)
            totalScore = gscore + hscore
            openList.update({point:totalScore})
            #ttt=openList
    maxScore = min(openList.values())
    for candidate in openList.keys():
        if openList[candidate] ==  maxScore:
            #if candidate in neighbours(currentLocation):
            currentLocation = candidate      
    closeList.append(currentLocation)
    del openList[currentLocation] 
    iterator += 1
path = [end]   
while currentLocation in parent:
    currentLocation = parent[currentLocation]
    #plt.plot(currentLocation[1], shape[0]-currentLocation[0], 'ro') 
    path.append(currentLocation)
path.reverse()
pathIds = []
for p in path:
    pathIds.append(grid[p])
#plt.plot([end[1],start[1]], [shape[0]-end[0],shape[0]-start[0]], 'go')

conn.rollback()
plt.figure(2)
for p in pathIds:
    cur.execute('select centerx, centery from public."myDeawingFullCellOneDimension"\
                where id = '+str(p))
    data = cur.fetchall()
    # each row is a tuple of 3 data base columns that we quered of
    data = np.asarray(data)   # break down each tuple to 3 numpy array component
    plt.plot(data[0,0], data[0,1], 'r*')
conn.close()
plt.show()         
        