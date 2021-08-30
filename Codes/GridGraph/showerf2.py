# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 14:20:02 2020

@author: R.S_PC
"""

import matplotlib.pyplot as plt
import psycopg2 as pc
#import numpy as np
#from postgis.psycopg import register
#import postgis as pg
import geopandas as geo
import pandas as pd
import shapely as sp
def show():
    conn = pc.connect(host="localhost",database="My Drawing", user="postgres", password="fear3560")
    # number of nodes
    conn.rollback()
    sql = 'select ST_AsText(geom) as geom from public."GridGraph"'
    dat = pd.read_sql_query(sql, conn)
    a = []
    for i in dat['geom']:
            a.append(sp.wkt.loads(i))
    
    b = pd.DataFrame(a,columns=['g'])
    c= geo.GeoDataFrame(b, geometry='g')
    fig, ax = plt.subplots(1)
    c.plot(ax=ax, color='cyan', edgecolor='black')
#geo.plotting.plot_dataframe(ax, c, color = 'cyan', edgecolor = 'black')