# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 08:27:24 2020

@author: R.S_PC
"""

import pandas as pd
import numpy as np
tr = pd.read_csv('TransitionCellsAtr.csv', header=None)
tr = np.asarray(tr)

nn = pd.read_csv('nodeName.csv', header=None)
nn = np.asarray(nn)

en = pd.read_csv('edgeName.csv', header=None)
en = np.asarray(en)

for i in range(tr.shape[0]):
    if tr[i, 1] in nn and tr[i, 2] in nn:
        np.delete(tr, i, 0)
np.savetxt('F:\Stuff\Current_Term\KNTU\papers\ISI\csvs\TransitionCellsAtr2.csv', tr, delimiter=',', fmt='%d')
