# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 14:00:13 2021

@author: Lenovo
"""

# 根据风暴影响日期以及距离挑选出影响高原降雪的TC个例
# 某日发生降雪的站点数大于等于N=5,15,20
# 已弃 原因是根据距离挑选个例不科学

import os
import pandas as pd
from math import sin,radians,cos,asin,sqrt
import numpy as np

# 函数：计算距离
def SphereDistance(lon1, lat1, lon2, lat2):
    radius = 6371.0 # radius of Earth, unit:KM
    # degree to radians
    lon1, lat1,lon2, lat2 = map(radians,[lon1, lat1,lon2, lat2])
    dlon = lon2 -lon1
    dlat = lat2 -lat1
    arg  = sin(dlat*0.5)**2 +  \
            cos(lat1)*cos(lat2)*sin(dlon*0.5)**2
    dist = 2.0 * radius * asin(sqrt(arg))
    return dist

# 函数：根据站点经纬度，时间，返回当天各个时次距离的平均值
path_tc="F:\\snow_sts_data\\BoB_ymdh_bjt_lon_lat.txt"
def ave_dist(station,sta_time,sta_lat,sta_lon,path_tc):
    tc_save = [] #保存影响时刻的台风信息
    dist_info=[] #保存各影响时刻的距离
    tc_info =pd.read_table(path_tc,sep = "\t")
    tc_id=tc_info['tc_id'].tolist()
    yyyymmddhh=tc_info['bjt'].tolist()
    lat_tc=tc_info['lat_tc'].tolist()
    lon_tc=tc_info['lon_tc'].tolist()
    N=len(lon_tc)
    newLine = ['station','sta_lat','sta_lon','tc_id', 'time', 
                'tc_lat', 'tc_lon']
    for i in range(0,N):
        if str(yyyymmddhh[i])[0:8]==sta_time:
            dist_tc2sta = SphereDistance(lon_tc[i],lat_tc[i],sta_lon,sta_lat)                    
            newLine[0] = station
            newLine[1] = sta_lat
            newLine[2] = sta_lon                
            newLine[3] = tc_id[i]
            newLine[4] = str(yyyymmddhh[i])
            newLine[5] = lat_tc[i]
            newLine[6] = lon_tc[i]
            # print(newLine)
            if newLine not in tc_save:
                tc_save.append(newLine)
                dist_info.append(dist_tc2sta)
    if len(tc_save)>0:
        dist_ave=np.mean(dist_info)
        # print(tc_save)
        # print(dist_info)
        # print(dist_ave)
    else:
        dist_ave=-9999.
        # print(str(station)+'在'+str(sta_time)+'期间无风暴记录！')
    return dist_ave

#%% 2016-2020

# 1 读取风暴影响时间信息
path_tc_bjt="F:\\snow_sts_data\\BoB_ymd_bjt_add.txt"
tc_info =pd.read_table(path_tc_bjt,sep = "\t")
tc_time=tc_info['bjt'].tolist()

path_snow="F:\\snow_sts_data\\2016-2020\\snow\\test_out2\\"
f_list = os.listdir(path_snow)
info=[]
for file in f_list:
    info.append(pd.read_table(path_snow+file,sep = "\t",encoding='utf-8',
                              usecols=['station','time','snow'],na_values='9999'))
info_frame = pd.concat(info,ignore_index=True) #变成dataframe


# 2 挑出日降雪站点数>=3的tc时间段内，的降雪站点
df =info_frame[info_frame.time.isin(tc_time)].reset_index(drop=True) 
df1=df.groupby(by=['time'])['snow'].sum() 
snow_day=df1.loc[df1>=5].reset_index()
# #上面reset....可把Series的index变成dataframe的columns
day_list1=list(snow_day['time'])
df_snowday=df[df.time.isin(day_list1)].reset_index(drop=True)
df_snow_sta=df_snowday[df_snowday['snow']==1]

# 给df_snow_sta 添加经纬度
path_sta='F:\\snow_sts_data\\tp_sta_info.txt'
tp_sta_info=pd.read_table(path_sta,sep = ",")
tp_sta=tp_sta_info['station'].tolist()
tp_lat=tp_sta_info['lat'].tolist()
tp_lon=tp_sta_info['lon'].tolist()
npts1=len(tp_sta)
def get_lon(x):
    for i in range(0,npts1): 
        if x['station']==tp_sta[i]:
            return tp_lon[i]
def get_lat(x):
    for i in range(0,npts1): 
        if x['station']==tp_sta[i]:
            return tp_lat[i]
df_snow_sta.loc[:, 'lon'] = df_snow_sta.apply(get_lon, axis=1) 
df_snow_sta.loc[:, 'lat'] = df_snow_sta.apply(get_lat, axis=1) 

# 2计算各个站点距离风暴的距离
station=df_snow_sta['station'].tolist()
sta_lat=df_snow_sta['lat'].tolist()
sta_lon=df_snow_sta['lon'].tolist()
sta_time=df_snow_sta['time'].tolist()
npts2=len(station)
dist_list=[]
for i in range(0,npts2):
    dist_list.append(ave_dist(station[i],str(sta_time[i]),sta_lat[i],
                              sta_lon[i],path_tc))
df_snow_sta.loc[:,'dist']=dist_list
df_snow_sta.replace(to_replace='-9999',value=np.nan)
df_need=df_snow_sta[df_snow_sta['dist']<=2236]
# df_snow_sta.to_csv(path2_save+'',sep='\t',index=False)
# del df_snow_sta

#找出tc_id
day_list2=list(df_need['time'])
df_tc =tc_info[tc_info.bjt.isin(day_list2)].reset_index(drop=True) 
tc_id=set(df_tc['tc_id'].tolist())
tc_list=list(tc_id)
tc_list.sort()
tc_num=len(tc_list)
print("2016-2020个例编号:",tc_list)
print("2026-2020个例数量:",tc_num) #输出个例数


#%% 1981-2015

# # read tc information
# path_tc_bjt="F:\\snow_sts_data\\BoB_ymd_bjt_add.txt"
# tc_info =pd.read_table(path_tc_bjt,sep = "\t")
# tc_time=tc_info['bjt'].tolist()

# path_snow="F:\\snow_sts_data\\1981-2015\\weather_snow\\"
# f_list = os.listdir(path_snow)
# info=[]
# for file in f_list:
#     info.append(pd.read_table(path_snow+file,sep = "\t",encoding='utf-8',
#                               na_values='9999'))
# info_frame = pd.concat(info,ignore_index=True)
# # #add 0 before number
# yy=info_frame['yy'].apply(lambda x : '{:0>4d}'.format(x))
# mm=info_frame['mm'].apply(lambda x : '{:0>2d}'.format(x))
# dd=info_frame['dd'].apply(lambda x : '{:0>2d}'.format(x))
# time=yy+mm+dd
# info_frame['time'] =time  # or info_frame.loc[:, 'time'] = time 

# # pick time
# info_frame.to_csv('F:\\snow_sts_data\\info_frame.txt',index = False,na_rep='9999')
# del info_frame
# info_frame=pd.read_table('F:\\snow_sts_data\\info_frame.txt',sep = ",",
#                     encoding='utf-8',na_values='9999')
# # pick snow information during TCs 
# df =info_frame[info_frame.time.isin(tc_time)].reset_index(drop=True)
# # calculate station number of each day
# ds=df.groupby(by=['time'])['snow'].sum() 
# df_day=ds.loc[ds>=20].reset_index()
# #上面reset....可把Series的index变成dataframe的columns
# day_list=list(df_day['time'])
# df_tc =tc_info[tc_info.bjt.isin(day_list)].reset_index(drop=True) 
# # df_tc.sort_values(by='tc_id', ascending=True)
# tc_id=set(df_tc['tc_id'].tolist())
# tc_list=list(tc_id)
# tc_list.sort()
# tc_num=len(tc_list)
# print("1981-2015个例编号:",tc_list)
# print("1981-2015个例数量:",tc_num) #输出个例数














