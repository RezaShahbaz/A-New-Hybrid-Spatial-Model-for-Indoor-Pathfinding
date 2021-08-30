# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 17:20:13 2019

@author: R.S_PC
"""

import psycopg2 as pc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
def GridGraphGenerator():
    # Connect to postgres database
    conn = pc.connect(host="localhost",database="My Drawing", user="postgres", password="fear3560")
    
    cur = conn.cursor()
    # number of nodes
    conn.rollback()
    
    cur.execute('select distinct node from public."facultyFinal"\
                    where node is not null')
    nodeName = cur.fetchall()
    nodeCenter = []
    # number of nodes
    for node in nodeName:
        conn.rollback()
        
        cur.execute('select id ,centerx, centery from public."facultyFinal"\
                    where node = '+str(node[0])+' \
                    order by centerX desc, centery asc')
        data = cur.fetchall()
    
        # each row is a tuple of 3 data base columns that we quered of
        data = np.asarray(data)   # break down each tuple to 3 numpy array component
        data = np.array(data, dtype = float)
        nodeGrid = np.zeros([np.unique(data[:,2]).shape[0],np.unique(data[:,1]).shape[0]])
        nodeCenter.append((np.average(data[:,1]),np.average(data[:,2])))
        # according to cell coordinate the number of row and column in matrix are calculated
        tupleX = {}
        tupleY = {}
        j = np.unique(data[:,2]).shape[0]-1
        for i in np.unique(data[:,2]):
            tupleX.update({i:j})
            j = j-1
        j = 0
        for i in np.unique(data[:,1]):
            tupleY.update({i:j})
            j = j+1        
        
        for i in range(data.shape[0]):
            nodeGrid[tupleX[data[i,2]], tupleY[data[i,1]]] = data[i,0]
        name = 'node'+  str(node[0])+'.csv'     
        np.savetxt(name, nodeGrid, delimiter=',', fmt='%d')
#        plt.figure(1)
        #plt.plot(data[:,1], data[:,2], 'co')
        
        
    #####################################################################################
    #####################################################################################
    # Start of Graph Builder Part
    
    #        #Caculate Center Of each node with averag of its cells
    #        nodeCenter.append((np.average(data[:,1]),np.average(data[:,2])))
    #        # save node number and its transition cells tr1 and tr2 attributes in tuple => all node in a list
    #        transitionCells = np.where(data2[:,3]==6)
    #        for cell in transitionCells[0]:
    #           nodesTransitionCells.append((data2[cell,0], data2[cell,1], data2[cell,2]))
    #        for trCell in nodesTransitionCells:
    #            if ',' in trCell[1]:
    #                splited = trCell[1].split(',')
    #                for j in splited:
    #                    new = (trCell[0] ,j, trCell[2])
    #                    nodesTransitionCells.append(new)
    #                nodesTransitionCells.remove(trCell)
    #            if ',' in trCell[2]:
    #                splited = trCell[2].split(',')
    #                for j in splited:
    #                    new = (trCell[0], trCell[1], j)
    #                    nodesTransitionCells.append(new)   
    #                nodesTransitionCells.remove(trCell)
    #    for trCell1 in nodesTransitionCells:
    #        for trCell2 in nodesTransitionCells:
    #            if trCell1[1] == trCell2[2] and trCell1[2] == trCell2[1]:
    #                nodesTransitionCells.remove(trCell1)
    #    nodesTransitionCells = set(nodesTransitionCells)
    #    nodesTransitionCells = list(nodesTransitionCells)
    graphIndex = {nodeName[i][0]:i for i in range(len(nodeName))}
    graph = np.zeros([len(nodeName), len(nodeName)])
    nodeName1 = graphIndex.keys()
    nodesTransitionCells = pd.read_csv('TransitionCellsAtr3.csv', header=None)
    nodesTransitionCells = np.array(nodesTransitionCells)
    transitionCells = []
    for i in range(len(nodesTransitionCells)):
        transitionCells.append(tuple(nodesTransitionCells[i,:]))
    for trCell1 in transitionCells:
        for trCell2 in transitionCells:
            if trCell1 != trCell2:
                if trCell1[1] == trCell2[2] and int(trCell1[2]) in nodeName1 and int(trCell2[1]) in nodeName1:
                    graph[graphIndex[int(trCell1[2])],graphIndex[int(trCell2[1])]] = trCell2[2]
    
                elif trCell1[2] == trCell2[1] and int(trCell1[1]) in nodeName1 and int(trCell2[2]) in nodeName1:
                    graph[graphIndex[int(trCell1[1])],graphIndex[int(trCell2[2])]] = trCell1[2]
    
                elif trCell1[2] == trCell2[2] and int(trCell1[1]) in nodeName1 and int(trCell2[1]) in nodeName1:
                    graph[graphIndex[int(trCell1[1])],graphIndex[int(trCell2[1])]] = trCell1[2]
    
                elif trCell1[1] == trCell2[1] and int(trCell1[2]) in nodeName1 and int(trCell2[2]) in nodeName1:
                    graph[graphIndex[int(trCell1[2])],graphIndex[int(trCell2[2])]] = trCell1[1]
    
                elif int(trCell1[1]) in nodeName1 and int(trCell1[2]) in nodeName1:
                    graph[graphIndex[int(trCell1[1])],graphIndex[int(trCell1[2])]] = 999
    #    transitionCells = np.array([-999, -999, -999])
    #    for cell in nodesTransitionCells:
    #        a = [cell[0], int(cell[1]), int(cell[2])]
    #        transitionCells = np.vstack((transitionCells, a)) 
    np.fill_diagonal(graph, 0)
    np.savetxt('graph.csv', graph, delimiter=',', fmt='%d')
    np.savetxt('nodeName.csv', nodeName, delimiter=',', fmt='%d')
    np.savetxt('nodeCenter.csv', nodeCenter, delimiter=',', fmt='%d')
    #    np.savetxt('TransitionCells.csv', transitionCells, delimiter=',', fmt='%s')
    ######################################################################################
    ######################################################################################
    # End of Graoh Builder Part
    
    # edges
    conn.rollback()
    
    cur.execute('select distinct edge from public."facultyFinal"\
                    where edge is not null')
    edgeName = cur.fetchall()
    counter = 0
    cost = {}
    for edge in edgeName:
        conn.rollback()
        
        cur.execute('select id ,centerx, centery from public."facultyFinal"\
                    where edge = '+str(edge[0])+' \
                    order by centerX desc, centery asc')
        data = cur.fetchall()
        # each row is a tuple of 3 data base columns that we quered of
        data = np.asarray(data)   # break down each tuple to 3 numpy array component
        
        edgeGrid = np.zeros([np.unique(data[:,2]).shape[0],np.unique(data[:,1]).shape[0]])
        # according to cell coordinate the number of row and column in matrix are calculated
        tupleX = {}
    
        tupleY = {}
        j = np.unique(data[:,2]).shape[0]-1
        for i in np.unique(data[:,2]):
            tupleX.update({i:j})
            j = j-1
        j = 0
        for i in np.unique(data[:,1]):
            tupleY.update({i:j})
            j = j+1        
        
        for i in range(data.shape[0]):
            edgeGrid[tupleX[data[i,2]], tupleY[data[i,1]]] = data[i,0]
        name = 'edge'+  str(edge[0])+'.csv'     
        np.savetxt(name, edgeGrid, delimiter=',', fmt='%d')
        #plt.plot(data[:,1], data[:,2], 'bo')
        counter = counter+1
        if len(np.where(graph == edge[0])[0]) > 0:
            node1 = np.where(graph == edge[0])[0][0]
            node2 = np.where(graph == edge[0])[1][0]
            dx = (nodeCenter[node1][0]-nodeCenter[node2][0])**2
            dy = (nodeCenter[node1][1]-nodeCenter[node2][1])**2
            cost.update({edge[0]:math.sqrt(dx+dy)})
    #plt.show()
    conn.close()
    
#    plt.figure(2)
#    plt.plot([i[0] for i in nodeCenter], [i[1] for i in nodeCenter], 'bo')
    #plt.show()
    np.savetxt('edgeName.csv', edgeName, delimiter=',', fmt='%d')
    return graphIndex, cost