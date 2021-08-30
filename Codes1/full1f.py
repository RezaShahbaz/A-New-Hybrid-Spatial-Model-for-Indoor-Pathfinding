# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 18:35:18 2019

@author: R.S_PC
"""


import numpy as np
from FullAstarV21f import fullStarMain
#from FullAstarV22 import fullStarGridGraph
#from FullAstarV23 import fullStarGrid

dests1 = [1001, 898, 411, 428, 209,\
         135, 155, 229, 168, 186, 248,\
         7, 27, 108, 124, 281, 300, 41,\
         59, 638, 320, 78, 96]
dests2 = [1001, 898, 411, 428, 209,\
         135, 155, 229, 168, 186, 248,\
         7, 27, 108, 124, 281, 300, 41,\
         59, 638, 320, 78, 96]

numb1 = np.zeros((529,8))
it2 = 0
it1 = 0
for i in dests1:
    for j in dests2:
        if i != j:
            for k in range(5):
                try:
                    a, b = fullStarMain(i,j)
                    numb1[it1, k] = b
                    numb1[it1, 5] = a
                    numb1[it1, 6] = i
                    numb1[it1, 7] = j
                    print(i)
                    print(j)
                except:
                    numb1[it1, 5] = -999
                    numb1[it1, 6] = i
                    numb1[it1, 7] = j
                    print("error")
                    print(i)
                    print(j)
                print("---------------")
                it2 = it2 + 1
            it1 = it1 + 1
np.savetxt('numb1.csv', numb1, delimiter=',', fmt = '%f') 