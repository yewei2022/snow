# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 14:00:13 2021

@author: Lenovo
"""

# 根据日期挑选出影响高原降雪的TC个例
# 结果  根据那个半径确实不太能筛出来
#%% 函数
import os
import pandas as pd
from math import sin,radians,cos,asin,sqrt
import numpy as np

path_pre='F:\\daily_data\\origin\\'
path1_save='F:\\daily_data\\test\\'

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
path_tc="F:\\snow_sts_data\\BoB_ymdh_utc_lon_lat.txt"
def ave_dist(station,sta_time,sta_lat,sta_lon,path_tc):
    tc_save = [] #保存影响时刻的台风信息
    dist_info=[] #保存各影响时刻的距离
    tc_info =pd.read_table(path_tc,sep = "\t")
    tc_id=tc_info['tc_id'].tolist()
    yyyymmddhh=tc_info['utc'].tolist()
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

#%%
# #step1 将降水数据时间往前推一天 after run,useless
# import datetime 
# f_list1 = os.listdir(path_pre)
# for file in f_list1:
#     info=pd.read_table(path_pre+file,sep = "\s+",encoding='utf-8',
#                         header=None,names=['station','lon','lat','pre'],
#                         usecols=[0,1,2,4])
#     time0=file[0:10]
#     time1= datetime.datetime.strptime(time0, '%Y%m%d%H') #字符串变时间
#     time2=time1-datetime.timedelta(hours=24) #往前24h,to prep start UTC
#     time3=time2.strftime('%Y%m%d%H')[0:8]#时间变字符串,并提取年月日
#     info['time'] = time3 
#     info.to_csv(path1_save+time3+'.txt',index = False,sep='\t',
#               columns=['station','lon','lat','time','pre'])

#%% 

# 1 读取风暴影响时间信息
path_tc_utc="F:\\snow_sts_data\\BoB_ymd_utc_add.txt"
tc_info =pd.read_table(path_tc_utc,sep = "\t")
tc_time=tc_info['utc'].tolist()

f_list2 = os.listdir(path1_save)
info=[]
for file in f_list2:
    info.append(pd.read_table(path1_save+file,sep = "\t",encoding='utf-8',
                              usecols=['station','lon','lat','time','pre']))
info_frame = pd.concat(info,ignore_index=True)


# 2 挑出tc时间段内的日降水站点
def get_pre(x):
    if x[4]>=0.5: 
        return 1
    else:
        return 0
info_frame.loc[:, 'pre_if'] = info_frame.apply(get_pre, axis=1) 
df    =info_frame[info_frame.time.isin(tc_time)].reset_index(drop=True) 
df_pre_sta =df[df['pre_if']==1]


# 3计算各个站点距离风暴的距离
station=df_pre_sta['station'].tolist()
sta_lat=df_pre_sta['lat'].tolist()
sta_lon=df_pre_sta['lon'].tolist()
sta_time=df_pre_sta['time'].tolist()
npts2=len(station)
dist_list=[]
for i in range(0,npts2):
    dist_list.append(ave_dist(station[i],str(sta_time[i]),sta_lat[i],
                              sta_lon[i],path_tc))
df_pre_sta.loc[:,'dist']=dist_list
df_pre_sta.replace(to_replace='-9999',value=np.nan)
df1 =df_pre_sta[df_pre_sta['dist']<=2236]
# 挑出降水站点大于等于5的日期
df2 =df1.groupby(by=['time'])['pre_if'].sum() #计算每日产生降水的站点数量
pre_day=df2.loc[df2>=5].reset_index() #导出大于等于5个站点的time，and pre_if
# #上面reset....可把Series的index变成dataframe的columns
day_list1=list(pre_day['time']) # 导出目标时间
df_need  =df1[df1.time.isin(day_list1)].reset_index(drop=True)
# df_pre_sta.to_csv(path2_save+'',sep='\t',index=False)
# del df_pre_sta

#找出tc_id
# 根据df_need的时间挑出tc_id
day_list2=list(df_need['time'])
df_tc =tc_info[tc_info.utc.isin(day_list2)].reset_index(drop=True) 
tc_id=set(df_tc['tc_id'].tolist())
tc_list=list(tc_id)
tc_list.sort()
tc_num=len(tc_list)
print("2000-2018个例编号:",tc_list)
print("2000-2018个例数量:",tc_num) #输出个例数
#%%
















