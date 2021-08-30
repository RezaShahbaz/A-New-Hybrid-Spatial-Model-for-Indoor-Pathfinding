# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 18:22:55 2019

@author: R.S_PC
"""

import psycopg2 as pc
import numpy as np
import re

conn = pc.connect(host="localhost",database="My Drawing", user="postgres", password="fear3560")
    
cur = conn.cursor()
# number of nodes
conn.rollback()


cur.execute('select id, height, width, center  from public."facultyFinal"')
info = np.array(cur.fetchall())


for inf in info:
    splited = re.split("\s", inf[3])
    firstp = re.search('\(', splited[1]).start()
    secondp = first = re.search('\)', splited[2]).start()
    
    centerx = float(splited[1][firstp+1:])
    centery = float(splited[2][:secondp])
    
    left = centerx - float(inf[2])/2
    right = centerx + float(inf[2])/2
    top = centery + float(inf[1])/2
    bottom = centery - float(inf[1])/2
    query = 'update public."facultyFinal" set centerx = %s, centery = %s, bleft =%s,bright = %s,btop = %s,bbottom= %s where id = %s'
    cur.execute(query, (str(centerx), str(centery), str(left),str(right),str(top),str(bottom),str(inf[0])))
    # by commiting all changes save permanently
    conn.commit()
cur.execute('select id, centerx, centery, bleft, bright, btop, bbottom from public."facultyFinal"')
temp = np.array(cur.fetchall())
conn.close()
cur.close()