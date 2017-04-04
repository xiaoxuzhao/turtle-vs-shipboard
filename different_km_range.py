# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 22:15:30 2017
plot the difference of temp  about turtle vs ship  with range of 10 type of day and 15 type of distance
@author: yifan
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from turtleModule import  np_datetime, dist,str2ndlist
from gettopo import gettopo
###################################################################################
def find_range(day,t1,t2,index1,index2,lon1,lat1,lon2,lat2):
    one,two=[],[]
    for r in np.arange(0,30,2):
        ix1,ix2=[],[]
        for i in index1:
            for j in index2:
                
                l = dist(lon1[i], lat1[i],lon2[j],lat2[j])
                if l<r+2 and l>=r:
                    t=abs(t1[i]-t2[j])
                    if t<timedelta(days=day):
                         ix1.append(i)
                         ix2.append(j)
        one.append(ix1)  #have 15 value,each value also have many value
        two.append(ix2)
    return  one,two  
                
day = [1,2,3,4,5,6,7,8,9,10]       # the four range of day to compare the ship vs turtle
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

T=[] #index of turtle
S=[] #index of shipboard
for i in range(10):
    print i
    I=find_range(day[i],obstime,shiptime,tf_index,shipData.index,obslon ,obslat,shiplon,shiplat)
    t_index=I[0]
    s_indx=I[1]
    T.append(t_index)     #turtle index for different range of days
    S.append(s_indx)     #ship index  for different range of days
##  ######### the below compare ship profile with turtle profile that use the whole points of profile
'''
Mean_day=[] # mean difference of temp of turtle vs ship with range of different days and distance
Rms_day=[]
N1,N2,N3=[],[],[]#the number of ship profile,turtle profile,turtle
scales=[]
for d in range(10): # 4 kind of days 
    mean_r=[] # mean difference of temp of turtle vs ship with range of  10 type of distance for one day
    rms_r=[]
    for s in range(15): #each day includes 15 different range of distance
        indx=S[d][s] # ship index
        index=T[d][s]# turtle index
        INDX=pd.Series(indx).unique()
        scales.append(str(day[d])+'day '+str(2*s)+'~'+str(2+2*s)+'km')
        n1=len(INDX)
        n2=len(pd.Series(index).unique())
        n3=len(turtle_id[pd.Series(index).unique()].unique())
        N1.append(n1)
        N2.append(n2)
        N3.append(n3)
        print 'number of ship profile,turtle profile,turtle: ',str(day[d])+'day '+str(2*s)+'~'+str(2+2*s)+'km',n1,n2,n3
        
        Mean_turVSship,Rms_turVSship=[],[]
        for i in range(len(INDX)): 
            diff_turVSship=[] # each ship pofile have many turtle profile to compare the difference of temp
            for j in range(len(indx)):
                if indx[j]==INDX[i]:
                    for k in range(len(obsDepth[index[j]])):
                        for m in range(len(shipdepth[INDX[i]])):
                            if obsDepth[index[j]][k]==shipdepth[INDX[i]][m]:
                                dif_turVSship=abs(obstemp[index[j]][k]-shiptemp[INDX[i]][m])
                                diff_turVSship.append(dif_turVSship)
            if diff_turVSship!=[]: #  some turtle dive on the surface ,but the ship data start from the deeper depth
                mean_turVSship=np.mean(np.array(diff_turVSship))                           
                rms_turVSship=np.sqrt(np.sum(np.array(diff_turVSship)*np.array(diff_turVSship))/len(np.array(diff_turVSship)))
                Mean_turVSship.append(mean_turVSship)
                Rms_turVSship.append(rms_turVSship)
        mean=np.mean(np.array(Mean_turVSship)) #exact value of one day and one distance
        rms=np.mean(np.array(Rms_turVSship))
        mean_r.append(mean) # include 15 values
        rms_r.append(rms)
    Mean_day.append(mean_r) # include 4 values
    Rms_day.append(rms_r)    
data=pd.DataFrame()
data['scales']=pd.Series(scales)
data['number of ship profiles']=pd.Series(N1)
data['number of turtle profiles']=pd.Series(N2)
data['number of turtle']=pd.Series(N3)
data.to_csv('shipVSturtle_scales_big.csv')
'''
##  ######### the below compare ship profile with turtle profile that only use the bottom points of profile
Mean_day=[] # mean difference of temp of turtle vs ship with range of 4 type of day and 15 type of distance
Rms_day=[]
N1,N2,N3=[],[],[]#the number of ship profile,turtle profile,turtle
scales=[]
n_ID=[]
num=0
for d in range(10): # 4 kind of days 
    mean_r=[] # mean difference of temp of turtle vs ship with range of  10 type of distance for one day
    rms_r=[]
    for s in range(15): #each day includes 15 different range of distance
        indx=S[d][s] # ship index
        index=T[d][s]# turtle index
        INDX=pd.Series(indx).unique()
        scales.append(str(day[d])+'day '+str(2*s)+'~'+str(2+2*s)+'km')
        n1=len(INDX)
        n2=len(pd.Series(index).unique())
        n3=len(turtle_id[pd.Series(index).unique()].unique())
        N1.append(n1)
        N2.append(n2)
        N3.append(n3)
        print 'number of ship profile,turtle profile,turtle: ',str(day[d])+'day '+str(2*s)+'~'+str(2+2*s)+'km',n1,n2,n3
        
        Mean_turVSship,Rms_turVSship=[],[]
        ID_turtle=[]
        for i in range(len(INDX)):
            wd1=-gettopo(shiplat[INDX[i]],shiplon[INDX[i]])
            bm1=shipdepth[INDX[i]][-1]
            diff_turVSship=[] # each ship pofile be compared with  many turtle profile in the difference of temp
            if bm1>=wd1*0.9:
                for j in range(len(indx)):
                    if indx[j]==INDX[i]:
                        wd2=-gettopo(obslat[index[j]],obslon[index[j]])
                        bm2=obsDepth[index[j]][-1] # bottom depth of the turtle profile
                        if bm2>=wd2*0.9:
                            dif_turVSship=abs(obstemp[index[j]][-1]-shiptemp[INDX[i]][-1])
                            diff_turVSship.append(dif_turVSship)
                            ID_turtle.append(turtle_id[index[j]])
            if diff_turVSship ==[]:
                num+=1
            if diff_turVSship!=[]: #  some turtle dive on the surface ,but the ship data start from the deeper depth
                mean_turVSship=np.mean(np.array(diff_turVSship))                           
                rms_turVSship=np.sqrt(np.sum(np.array(diff_turVSship)*np.array(diff_turVSship))/len(np.array(diff_turVSship)))
                Mean_turVSship.append(mean_turVSship)
                Rms_turVSship.append(rms_turVSship)       
        mean=np.mean(np.array(Mean_turVSship)) #exact value of one day and one distance
        rms=np.mean(np.array(Rms_turVSship))
        mean_r.append(mean) # include 15 values
        rms_r.append(rms)
        ids=pd.Series(ID_turtle).unique()
        n_ID.append(len(ids))
    Mean_day.append(mean_r) # include 4 values
    Rms_day.append(rms_r)    
print num
N3_1=n_ID[0:15]      #N3[0:15]
N3_10=n_ID[-15:]      #N3[-15:]
color=['g','orange','r','k','c','m','y','violet','peru','b'] 
xlabes=['0~2','2~4','4~6','6~8','8~10','10~12','12~14','14~16','16~18','18~20','20~22','22~24','24~26','26~28','28~30']
fig=plt.figure()
ax=fig.add_subplot(111)
M,R=[],[]
for i in range(10):
    m_day=pd.Series.dropna(pd.Series(Mean_day[i]))
    r_day=pd.Series.dropna(pd.Series(Rms_day[i]))
    M.append(np.mean(m_day))
    R.append(np.mean(r_day))
    ax.plot(np.arange(0,15,1),Mean_day[i],color[i],label=str(i+1)+': '+str(round(np.mean(m_day),2)))
for i in range(15):
    if i==1:
       ax.text(i, 2.3, N3_10[i],
           color='b', fontsize=10)
    else:
       ax.text(i, Mean_day[9][i]+0.08, N3_10[i],
           #va='bottom', ha='right',
           #transform=ax.transAxes,
           color='b', fontsize=10)
for i in np.arange(2,15,1):
    ax.text(i, Mean_day[0][i]-0.2, N3_1[i],
           #va='bottom', ha='right',
           #transform=ax.transAxes,
           color='g', fontsize=10)
ax.set_ylim([0,2.4])
ax.set_xticks(range(15))
ax.set_xticklabels(xlabes,rotation=45)
ax.set_yticks(np.arange(0,2.4,0.2))
plt.title('turtle vs ship',fontsize=16)
plt.xlabel('range of distance(km)',fontsize=12)
plt.ylabel('temperature difference('+u'°C'+')',fontsize=12)  
plt.legend(loc='lower right',ncol=2,fontsize = 'x-small')
plt.text(11,0.73,'range of day',fontsize=8)
fig.tight_layout() # I use it to be sure that the labels can show up on the picture.
plt.savefig('different_km_range_bottom',dpi=200)       # different_km_range'
plt.show()
print 'mean(mean ship-turtle)',np.mean(np.array(M))#Mean_day
print 'mean(rms ship-turtle)',np.mean(np.array(R))#Rms_day

