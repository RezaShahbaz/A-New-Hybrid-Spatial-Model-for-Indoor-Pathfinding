# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 18:59:25 2020

@author: R.S_PC
"""
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import owlready2
import re
import psycopg2 as pc
from GridGraphGenerator1f import GridGraphGenerator
graphIndex, cost = GridGraphGenerator()
mstart = 1000
mend = 628
conn = pc.connect(host="localhost",database="My Drawing", user="postgres", password="fear3560")
cur = conn.cursor()
graph11 = pd.read_csv('graph.csv', header=None)
graph11 = np.asarray(graph11)
nodeCenter = pd.read_csv('nodeCenter.csv', header=None)
nodeCenter = np.asarray(nodeCenter)
conn = pc.connect(host="localhost",database="My Drawing", user="postgres", password="fear3560")
cur = conn.cursor()
cur.execute('select Node from  public."GridGraph" where id='+str(mstart))
sm = cur.fetchall()
conn.rollback()
cur.execute('select Node from  public."GridGraph" where id='+str(mend))
em = cur.fetchall()
  #   load OWL file
#my_world = owlready2.World()
#my_world.get_ontology(r"F:\Stuff\Current_Term\KNTU\Thesis\ProtegeModels\My Drawing\FDisableNormal.owl").load()
s = sm[0][0]
e = em[0][0]
# Convert OWL axioms to RDF graph
#graph = my_world.as_rdflib_graph()
#
## query
## last space in each line is necessary
#query = "PREFIX : <http://www.semanticweb.org/r.s_pc/ontologies/2019/11/NormalNormal#> " \
#            "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> " \
#            "SELECT ?s " \
#            "WHERE {?s rdf:type :Obstacle }"
#resultlist = graph.query(query)
graphC = nodeCenter
# convert results to list of integers
response = []
#for item in resultlist:
#    s1 = str(item['s'].toPython())
#    s1 = re.sub(r'.*#',"",s1)
#    response.append(int(s1))   
graphTest = graph11
conn.rollback()
for i in response:
    cur.execute('select edge from public."GridGraph"\
                where id = '+str(i))
    edName = cur.fetchall()
    #print(edName[0][0])
    graphTest[np.where(graphTest==edName[0][0])] = 0
    #print(graphTest[np.where(graphTest==edName[0][0])])
#np.savetxt('graphtest.csv', graphTest, delimiter = ',')    
global graphTest1
global cost1
graphTest1 = graphTest
cost1 = cost
xIndices = []
yIndices = []
for i in graphC:
    xIndices.append(i[0])
    yIndices.append(i[1])

plt.figure(1)
temp = np.where(graphTest != 0)
for i in range(temp[0].shape[0]):
    edgeX1=xIndices[temp[0][i]]
    edgeY1=yIndices[temp[0][i]]
    edgeX2=xIndices[temp[1][i]]
    edgeY2=yIndices[temp[1][i]]
    plt.plot([edgeX1, edgeX2], [edgeY1, edgeY2], color = 'blue')
    plt.annotate(str(graphTest[temp[0][i], temp[1][i]]), xy=((edgeX1+edgeX2)/2,(edgeY1+edgeY2)/2))

plt.plot(xIndices, yIndices,'yo')
plt.show()
nodeName = pd.read_csv('nodeName.csv', header=None)
nodeName = np.array(nodeName)
graphIndex = {nodeName[i][0]:i for i in range(len(nodeName))}
start = graphIndex[s]
end = graphIndex[e]
def hValue(pointNum):
    dist = math.sqrt(((xIndices[pointNum]-xIndices[end])**2)+((yIndices[pointNum]-yIndices[end])**2))
    return dist
def gValue(parentNum,pointNum):
    global graphTest1
    global cost1
    return cost[graphTest[parentNum, pointNum]]  

openList = []   # all the squares that are being considered to find the shortest path
closeList = [] # squares that does not have to consider them again
currentLocation = start
parent = start
closeList.append(start)
score = np.zeros(graphTest.shape)
gValueMat = np.zeros(graphTest.shape[0])
score = score + 999
iterator = 0
path = []
while currentLocation != end:
    adjPoints = np.where(graphTest[currentLocation,:]!=0)[0]
    for i in adjPoints:
        if i not in closeList:
            openList.append(i)
            heuristicCost = hValue(i)
            thisStep = gValue(currentLocation,i)        
            if currentLocation != start:
                gValueMat[currentLocation] = gValueMat[parent]+ thisStep
                moveCost = gValueMat[currentLocation]+ thisStep
            else:
                moveCost = thisStep
            score[currentLocation, i] = moveCost + heuristicCost
#                print(str(parent+1)+"-->"+str(currentLocation+1)+"=>"+str(i+1) + "---"+ str(moveCost) + "  +  " + str(heuristicCost))
    openList = np.unique(openList)
    openList = list(openList)
    parent = np.where(score == np.min(score[:,openList]))[0][-1]
    currentLocation = np.where(score == np.min(score[:,openList]))[1][-1]
    try:
        openList.remove(currentLocation)
        closeList.append(currentLocation)
    except:
        currentLocation = parent
    iterator = iterator+1
    
index = currentLocation
while index != start:
    path.append(index)
    index = np.where(score[:,path[-1]]==np.min(score[:,path[-1]]))[0][0]
path.append(start)
path.reverse()
finalPath = []
i = 1
while i != len(path)+1:
    finalPath.append(path[i-1])
    if i < len(path):
        if graphTest[path[i-1],path[i]] != 0:
            finalPath.append(graphTest[path[i-1],path[i]])
    i += 1
xIndices = np.array(xIndices)
yIndices = np.array(yIndices)
plt.plot(xIndices[path], yIndices[path],'r*')
plt.plot(xIndices[path],yIndices[path], color='red')
plt.show()