# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 13:47:46 2019

@author: R.S_PC
"""


import psycopg2 as pc
import numpy as np
import shapely.geometry as sg
import matplotlib.pyplot as plt
def transitionCellFinder():
    # Connect to postgres database
    conn = pc.connect(host="localhost",database="My Drawing", user="postgres", password="fear3560")
    
    cur = conn.cursor()
    # number of nodes
    conn.rollback()
    
    cur.execute('select public."grid".id,bleft, bright,\
                btop, bbottom, Node, edge from public."Grid"\
                where node is not null or edge is not null')
    info = cur.fetchall()
    info = np.array(info, dtype = float)
    polyList = []
    plt.figure()
    for i in range(info.shape[0]):
        poly = sg.box(info[i, 1], info[i, 4], info[i, 2], info[i, 3], ccw = True)
        polyList.append((info[i, 0], poly))
        x,y = poly.exterior.xy
        plt.plot(x,y, color = "blue")
    
    
    plt.show()
    arcList = [] 
    j = 0  
    for poly in polyList:
        if str(info[j, 5]) != 'nan':
            temp = [(poly[0], info[j, 5])]
        else:
            temp = [(poly[0], info[j, 6])]
        i = 0
        for poly1 in polyList:
            if poly[1].touches(poly1[1]):
                if str(info[i, 5]) !='nan':
                    temp.append(info[i, 5])
                else:
                    temp.append(info[i, 6])
            i += 1
        j += 1
        arcList.append(temp)
    transitionCellsAtr = [] 
    
    for i in arcList:
    #    if not(all(i[0][1] == j for j in i[1:])):
        for j in i[1:]:
            if i[0][1] != j:
                transitionCellsAtr.append([i[0][0], i[0][1], j])
    #                query = 'update public."multiSize" set bfrom = %s, bto = %s where id = %s'
    #                cur.execute(query, (int(i[0][1]), int(j), int(i[0][0])))
    #                conn.commit()
    #transitionCellsAtr = set(transitionCellsAtr)
    transitionCellsAtr = np.asarray(transitionCellsAtr)
    conn.close()
    cur.close()
    np.savetxt('TransitionCellsAtr.csv', transitionCellsAtr, delimiter=',', fmt='%d')
            




