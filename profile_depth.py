# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 10:27:13 2016
calculate the number of profiles in each  depth 
@author: yifan
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd        
obsData = pd.read_csv('ctd_good.csv') # From nearestIndexInMod.py
tf_index = np.where(obsData['TF'].notnull())[0] # Get  index of good data.
depth = obsData['MAX_DBAR'][tf_index] # get deepest data file depth
obsID = obsData['PTT'][tf_index]           # Get ID of turtle.

index1 = depth[depth>200].index
id = obsID[index1]
print 'ID of observations that depth>200:', id.drop_duplicates().values

depth.sort()
y=depth.unique()
x=depth.value_counts()
x=x.sort_index()

ynew,xnew=[],[]
for i in range(11):
    sum=0
    for j in range(len(y)):
        if y[j]>i*8 and y[j]<i*8+8:
            sum+=x[y[j]]
    xnew.append(sum)
    ynew.append(i*8)

fig = plt.figure()            
plt.barh(ynew, xnew,height=6)
plt.ylim(88,0)
plt.ylabel('profile Depth', fontsize=12)
plt.xlabel('Quantity', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(np.arange(0,88,8),fontsize=10)
plt.title('Profile  Depth ', fontsize=14)
plt.savefig('profile_depth.png', dpi=200)
plt.show()
