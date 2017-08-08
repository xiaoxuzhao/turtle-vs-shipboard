# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 15:18:57 2017
draw the good positions of turtle and 70m contour line 
@author: yifan
"""
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import pandas as pd
from turtleModule import draw_basemap
from gettopo import gettopo
ship = pd.read_csv('ship06-08_MODELtemp.csv')
lonship, latship = ship['LON'], ship['LAT']

ctd = pd.read_csv('ctd_extract_good.csv', index_col=0)
TF = ctd['TF']              # If True, data is good, if False, data is bad.
latGoodCTD, lonGoodCTD = ctd['LAT'][TF==True], ctd['LON'][TF==True]

contour_lon,contour_lat,contour_depth=[],[],[]
for i in ship.index:
    contour_lon.append(lonship[i])
    contour_lat.append(latship[i])
    wd=-gettopo(latship[i],lonship[i])
    contour_depth.append(wd)
for i in latGoodCTD.index:
    contour_lon.append(lonGoodCTD[i])
    contour_lat.append(latGoodCTD[i])
    wd=-gettopo(latGoodCTD[i],lonGoodCTD[i])
    contour_depth.append(wd)

'''obsData = pd.read_csv('ctdWithdepthofbottom_roms.csv')
obsLon, obsLat = obsData['LON'], obsData['LAT']     #use for plotting depth line
depthBottom = pd.Series(obsData['depth_bottom'],index=obsData.index)
for i in obsData.index:
    if depthBottom[i]>200:
        depthBottom[i]=200
'''
lonsize = [-79.5, -64]
latsize = [33, 46]
#lonsize = [np.amin(lonGoodCTD), np.amax(lonGoodCTD)]
#latsize = [np.amin(latGoodCTD), np.amax(latGoodCTD)]
fig =plt.figure()
ax = fig.add_subplot(111)
plt.scatter(lonGoodCTD, latGoodCTD, color='g',s=1, label='Turtle(good position)')
plt.scatter(lonship, latship, color='y',s=1, label='Ship')
draw_basemap(fig, ax, lonsize, latsize, interval_lon=4, interval_lat=4)

lon_is = np.linspace(lonsize[0],lonsize[1],150)
lat_is = np.linspace(latsize[0],latsize[1],150)  #use for depth line
depth_i=griddata(np.array(contour_lon),np.array(contour_lat),np.array(contour_depth),lon_is,lat_is,interp='linear')
cs=plt.contour(lon_is, lat_is,depth_i,levels=[100],colors = 'r',linewidths=1.5,linestyles='--')
ax.annotate('100m water depth',color='r',fontsize=6,xy=(-75.2089,34.9195),xytext=(-75.0034,34.0842),arrowprops=dict(color='r',
            arrowstyle="->",connectionstyle="arc3"))
#plt.clabel(cs,'%.0f'%70.000,fmt='%s %m',inline=True,colors='k',fontsize=10)#fmt='%2.1d'
plt.title('Positions of turtle and ship', fontsize=10)
plt.legend(loc='lower right',fontsize = 'x-small')
plt.savefig('turtleVSship_map',dpi=200)
plt.show()
