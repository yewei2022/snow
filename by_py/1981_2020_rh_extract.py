# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 22:28:29 2023
1 提取1981-2020 相对湿度
2 提取TC活动日 相对湿度
@author: Lenovo
"""


# 读取40年高原日平均温度，重新存储
import pandas as pd
import numpy as np
import os


#%% branch1 step1 读取日平均温度分别将数据并另存

# # 读取高原站号
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",", usecols = ['station'])
# # print(sta)
# sta1=sta['station'].tolist()
# # print(sta1)

# cols=[0,4,5,6,7]
# colnames=["station","yy","mm","dd","rh"]
# # filename="SURF_CLI_CHN_MUL_DAY-PRE-13011-200810.TXT"
# path_info="F:\\snow_sts_data\\1981-2020-rh\\data\\"
# f_list = os.listdir(path_info)
# for file in f_list:
#     info=pd.read_table(path_info+file,sep = "\s+",header=None, names=colnames,
#                         na_values=32766,usecols=cols)
#     info_tp =info[info.station.isin(sta['station'])].reset_index(drop=True) 
#     # #add 0 before number
#     yy=info_tp['yy'].apply(lambda x : '{:0>4d}'.format(x))
#     mm=info_tp['mm'].apply(lambda x : '{:0>2d}'.format(x))
#     dd=info_tp['dd'].apply(lambda x : '{:0>2d}'.format(x))
#     time=yy+mm+dd
#     info_tp['time'] =time  # or info_tp.loc[:, 'time'] = time
#     info_tp.drop(columns = ['yy','mm','dd'],inplace = True)
#     info_tp['rh']=info_tp['rh']
#     # info_tp['dailypre'] = info_tp['dailypre'].apply(lambda x: format(x, '.1f'))
#     # 这里保留一位小数的话，na_rep命令无效 
#     info_tp.to_csv("F:\\snow_sts_data\\1981-2020-rh-TP\\"+file[31:37]+".txt",
#               index = False,sep='\t',na_rep=32766)



#%%  branch1 step2 组合为一个文件tem1981_2020.txt

# # # #读取tem变成dataframe 
# path_pre="F:\\snow_sts_data\\1981-2020-rh-TP\\"
# f_list = os.listdir(path_pre)  
# info=[]
# for file in f_list:   
#     info.append(pd.read_table(path_pre+file,sep = "\t",na_values=32766))
# pre = pd.concat(info,ignore_index=True)

# pre.to_csv("F:\\snow_sts_data\\1981-2020\\rh1981_2020.txt",index = False,
#                 sep=' ',na_rep=32700)


#%% branch2 提取所有TC活动日站点的地面气温
 
# import xarray as xr
# from metpy.units import units

# #读取40年80个站点的温度
# data0=pd.read_table("F:\\snow_sts_data\\1981-2020\\rh1981_2020.txt",
#                           sep='\s+',na_values=32700)
# #读取需要的时间
# need_time=pd.read_table("F:\\snow_sts_data\\TC\\all_tc_days.txt" ,
#                           sep='\s+')
# need_time.columns=['tc_id','time']
# data1=data0[data0.time.isin(need_time.time)]
# data2=data1.reset_index(drop=True)
# data3=data2.pivot(index='time', columns='station', values='rh')
# #根据站点顺序重新排序
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta_info=pd.read_table(path_sta,sep = ",")
# data4=data3.reindex(columns=sta_info.station)
# data5=data4.values

# ds = xr.Dataset()
# ds['rh'] = (('time','station'),data5*units('%'))
# time2 = pd.to_datetime(need_time['time'],format = '%Y%m%d')

# ds.coords['time'] = ('time',time2)
# ds.coords['station'] = ('station',sta_info['station'].values)
# print('保存的数据: \n{}'.format(ds))
# ds.to_netcdf('F:\\snow_sts_data\\ERA5\\all\\deal\\rh_station.nc') 
