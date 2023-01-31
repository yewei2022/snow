# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 11:15:47 2022
所有TC活动日站点的地面气温
@author: Lenovo
"""

import xarray as xr
import datetime
import pandas as pd
from metpy.units import units

    
#%% step 1 风暴影响半径计算函数

# from math import sin,radians,cos,asin,sqrt
# import numpy as np

# def SphereDistance(lon1, lat1, lon2, lat2):
#     radius = 6371.0 # radius of Earth, unit:KM
#     # degree to radians
#     lon1, lat1,lon2, lat2 = map(radians,[lon1, lat1,lon2, lat2])
#     dlon = lon2 -lon1
#     dlat = lat2 -lat1
#     arg  = sin(dlat*0.5)**2 +  \
#             cos(lat1)*cos(lat2)*sin(dlon*0.5)**2
#     dist = 2.0 * radius * asin(sqrt(arg))
#     return dist

# # 函数：根据站点经纬度，时间，返回当天各个时次距离的平均值
# def ave_dist(sta_id,sta_time,sta_lat,sta_lon,sta_tc_id,path_tc):
#     tc_save = [] #保存影响时刻的台风信息
#     dist_info=[] #保存各影响时刻的距离
#     tc_info =pd.read_table(path_tc,sep = "\t")
#     tc_id=tc_info['tc_id'].tolist()
#     yyyymmddhh=tc_info['bjt'].tolist()
#     lat_tc=tc_info['lat_tc'].tolist()
#     lon_tc=tc_info['lon_tc'].tolist()
#     N=len(lon_tc)
#     for i in range(0,N):
#         newLine = ['station','sta_lat','sta_lon','tc_id', 'time', 
#                     'tc_lat', 'tc_lon']
#         if (str(yyyymmddhh[i])[0:8]==sta_time) & (tc_id[i]==sta_tc_id):
#             dist_tc2sta = SphereDistance(lon_tc[i],lat_tc[i],sta_lon,sta_lat)                    
#             newLine[0] = sta_id
#             newLine[1] = sta_lat
#             newLine[2] = sta_lon                
#             newLine[3] = tc_id[i]
#             newLine[4] = str(yyyymmddhh[i])
#             newLine[5] = lat_tc[i]
#             newLine[6] = lon_tc[i]
#             # print(newLine)
#             if newLine not in tc_save:
#                 tc_save.append(newLine)
#                 dist_info.append(dist_tc2sta)
#     if len(tc_save)>0:
#         dist_ave=np.mean(dist_info)
#         print(tc_save)
#         print(dist_info)
#         print(dist_ave)
#     else:
#         dist_ave=32700
#         print(str(sta_id)+'在'+str(sta_time)+'期间无风暴记录！')
#     return dist_ave




#%% 挑选所有TC活动日距离

# path_save="F:\\snow_sts_data\\TC\\"
# path_tc="F:\\snow_sts_data\\TC\\BoB_ymdh_bjt_lon_lat.txt"

# time_info=pd.read_table("F:\\snow_sts_data\\TC\\all_tc_days.txt" ,
#                           sep='\s+')
# time_info.columns=['tc_id','time']
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta_info=pd.read_table(path_sta,sep = ",")

# sta_id=sta_info['station'].tolist()
# sta_lat=sta_info['lat'].tolist()
# sta_lon=sta_info['lon'].tolist()
# sta_time=time_info['time'].tolist()
# sta_tc_id=time_info['tc_id'].tolist()
# data=[]
# for i in range(0,len(sta_info)):
#     for j in range(0,len(time_info)):
#         newline1 = ['station','time','tcdist'] #必须放在内层循环
#         #不然每次data存的都是最新的一条数据 而没有全部存下来
#         newline1[0]=sta_id[i]
#         newline1[1]=sta_time[j]
#         newline1[2]=ave_dist(sta_id[i],str(sta_time[j]),sta_lat[i],
#                                   sta_lon[i],sta_tc_id[j],path_tc)
#         data.append(newline1)
        
# data1=pd.DataFrame(data,columns=['station','time','tcdist'])

# #保存为txt文件
# data1.to_csv(path_save+'tcdist1981_2020.txt',sep=' ',index=False,na_rep=32700)


#%% # 将数据列为矩阵保存为nc文件

# data0=pd.read_table("F:\\snow_sts_data\\TC\\tcdist1981_2020.txt",
#                           sep='\s+',na_values=32700)

# data1=data0.pivot(index='time', columns='station', values='tcdist')
# #根据站点顺序重新排序
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta_info=pd.read_table(path_sta,sep = ",")
# data2=data1.reindex(columns=sta_info.station)
# data3=data2.values

# ds = xr.Dataset()
# ds['tcdist'] = (('time','station'),data3*units('km'))
# #时间维
# time0=data2.index 
# time1 = pd.to_datetime(time0,format = '%Y%m%d')

# ds.coords['time'] = ('time',time1)
# ds.coords['station'] = ('station',sta_info['station'].values)
# print('保存的数据: \n{}'.format(ds))
# ds.to_netcdf('F:\\snow_sts_data\\ERA5\\regress\\tcdist_station.nc') 




