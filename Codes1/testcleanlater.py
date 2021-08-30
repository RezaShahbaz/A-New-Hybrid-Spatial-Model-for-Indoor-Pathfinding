# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 17:27:55 2020

@author: R.S_PC
"""
p = 12
for item in graphIndex.items():
    if (item[1] == p) and (item[0] in nodeName):
        name = 'node' + str(item[0]) + '.csv'
        pathPart.append(np.asarray(pd.read_csv(name, header=None)))
        translatedPath.append(item[0])
        print("this")
        print(p)
        print(item[0])
        break
    if p in edgeName:
        print(p)
        name = 'edge' + str(p) + '.csv'
        pathPart.append(np.asarray(pd.read_csv(name, header=None)))
        translatedPath.append(p)
        break