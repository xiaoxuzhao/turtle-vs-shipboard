# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 22:15:30 2017
different scales of distance and days for comparing ship with turtle
@author: yifan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from turtleModule import mon_alpha2num, np_datetime, dist,str2ndlist,colors,str2list
###################################################################################
r1,r2 = 10,15                # the obs position that has shipboard position within (r) kilometers might be considered as good data.
day = 1                # the obs time that has shipboard time within (day) days might be considered as good data.
obsData=pd.read_csv('ctdWithModTempByDepth.csv',index_col=0)
tf_index=np.where(obsData['TF'].notnull())[0]
obslat = pd.Series(obsData['LAT'][tf_index],index=tf_index)
obslon = pd.Series(obsData['LON'][tf_index],index=tf_index)
obstime = pd.Series(np_datetime(obsData['END_DATE'][tf_index]),index=tf_index)
obsDepth=pd.Series(str2ndlist(obsData['TEMP_DBAR'][tf_index]),index=tf_index)
obstemp=pd.Series(str2ndlist(obsData['TEMP_VALS'][tf_index]),index=tf_index)
turtle_id=obsData['PTT'][tf_index]

shipData=pd.read_csv('ship06-08_MODELtemp.csv',index_col=0)
shiplat=pd.Series(shipData['LAT'],index=shipData.index)
shiplon=pd.Series(shipData['LON'],index=shipData.index)
shiptime=pd.Series(shipData['time'],index=shipData.index)
shipdepth=pd.Series(str2ndlist(shipData['depth'],bracket=True),index=shipData.index)
shiptemp=pd.Series(str2ndlist(shipData['temperature'],bracket=True),index=shipData.index)
for i in range(len(shiptime)):
    shiptime[i]=datetime.strptime(shiptime[i], "%Y-%m-%d %H:%M:%S")  # change str to datatime


index = []     #index of turtle
indx=[]        #index of shipboard 
for i in tf_index:
    for j in shipData.index:
        l = dist(obslon[i], obslat[i],shiplon[j],shiplat[j])
        if l<r2 and l>=r1:
            #print l        #distance
            maxtime = obstime[i]+timedelta(days=day)
            mintime = obstime[i]-timedelta(days=day)
            mx = shiptime[j]<maxtime
            mn = shiptime[j]>mintime
            TF = mx*mn  
            if TF==1:      #time
                index.append(i)     #turtle index
                indx.append(j)      #ship index

INDX=pd.Series(indx).unique()      
Mean_turVSship,Rms_turVSship=[],[]
color=color=['k','g','y','b','c','m','k','g','y','b','c','m']
for i in range(len(INDX)):
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.plot(shiptemp[INDX[i]],shipdepth[INDX[i]],color='red' ,linewidth=2,label='shipindex'+str(INDX[i])) 
    diff_turVSship=[]
    t_index=[] # index of turtle
    for j in range(len(indx)):
        if indx[j]==INDX[i]:
            t_index.append(index[j])
            for k in range(len(obsDepth[index[j]])):
                for m in range(len(shipdepth[INDX[i]])):
                    if obsDepth[index[j]][k]==shipdepth[INDX[i]][m]:
                        dif_turVSship=obstemp[index[j]][k]-shiptemp[INDX[i]][m]
                        diff_turVSship.append(dif_turVSship)
    ax.plot(obstemp[t_index[0]],obsDepth[t_index[0]],color='black' ,linewidth=1,label='id: '+str(turtle_id[t_index[0]]))
    s=turtle_id[t_index[0]]
    c=color[0]
    for j in range(1,len(t_index)):
        if s==turtle_id[t_index[j]]:
            ax.plot(obstemp[t_index[j]],obsDepth[t_index[j]],color=c,linewidth=1)
        else:
            c=color[j]
            s=turtle_id[t_index[j]]
            ax.plot(obstemp[t_index[j]],obsDepth[t_index[j]],color=c,linewidth=1,label='id: '+str(s))

    mean_turVSship=np.mean(np.array(diff_turVSship))                           
    rms_turVSship=np.sqrt(np.sum(np.array(diff_turVSship)*np.array(diff_turVSship))/len(np.array(diff_turVSship)))
    Mean_turVSship.append(mean_turVSship)
    Rms_turVSship.append(rms_turVSship)                                                                           

    ax.set_xlim([0,30])
    ax.set_ylim([45,0])
    ax.set_xticks(np.arange(0,30,5))
    ax.set_yticks(np.arange(45,0,-5))
    plt.text(22,39,'mean: '+str(round(mean_turVSship,2))+u'°C',fontsize=10)
    plt.text(22,44,'RMS: '+str(round(rms_turVSship,2))+u'°C',fontsize=10)  
    ax.set_title('1day10~15km '+'('+str(shiptime[INDX[i]].date())+')',fontsize=14)

    plt.legend(loc='upper left')
    plt.savefig('1day10~15km  '+str(INDX[i]))        
    plt.show()
print 'mean(mean ship-turtle)',np.mean(np.array(Mean_turVSship))
print 'mean(rms ship-turtle)',np.mean(np.array(Rms_turVSship))
print 'number of ship profile: ',len(INDX)
print 'number of turtle profile: ',len(pd.Series(index).unique())
print 'number of turtle: ',len(turtle_id[pd.Series(index).unique()].unique())
