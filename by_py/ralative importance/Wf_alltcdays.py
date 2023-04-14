# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 20:16:35 2023
所有TC活动日的u100 v100
@author: Lenovo
"""

import xarray as xr
import datetime
import pandas as pd
from scipy import interpolate
import numpy as np
import metpy.calc as mpcalc
from metpy.units import units



#%% branch1 读取u100 v100数据 转化为北京时 做日平均 挑选TC活动日时间 写入文件

# count = 1
# varname = ["u100","v100"]
# file_path="F:\\snow_sts_data\\ERA5\\pick\\"+varname[count]+"_6h_selbox.nc"
# data0 = xr.open_dataset(file_path)
# var0=data0[varname[count]].loc[:,40:25,70:105]
# time0=data0.time
# lon = data0.longitude.loc[70:105]
# lat = data0.latitude.loc[40:25]
# # 时间转换为可处理的格式
# time1 = pd.to_datetime(time0,format = '%Y-%m-%d %H:%M:%S')
# #再赋给var0
# time2 = (time1 + datetime.timedelta(hours=8))#.strftime("%Y-%m-%d %H:%M:%S")
# # 不用.strftime("%Y-%m-%d %H:%M:%S")  不然还要再转回原来时间格式
# var0.coords['time'] = time2
# daily_var = var0.resample(time='1D',closed='left',label='left').mean() #日平均
# print(daily_var)


# # 挑选TC活动日时间 写入文件 
# # 参考 https://www.thinbug.com/q/57781130

# import pandas as pd

# need_time=pd.read_table("F:\\snow_sts_data\\TC\\all_tc_days.txt" ,
#                           sep='\s+')
# need_time.columns=['tc_id','time']
# sel_date = pd.to_datetime(need_time['time'],format = '%Y%m%d')
# var_sel = daily_var.sel(time=sel_date.values)
# print('变量维度: \n{}'.format(var_sel.shape))
# print(var_sel)

# var_sel.to_netcdf("F:\\snow_sts_data\\ERA5\\deal\\"+varname[count]+"_alltcdays.nc")



#%% branch2 读取地形高度 算Wf 这一步用NCL做

#######

#%% branch3 step1 读取Wf二进制文件 插值到站点

# #读取wf
# wf = np.fromfile("F:\\snow_sts_data\\\ERA5\\\deal\\wf_alltcdays.bin")
# print(wf)
# #转换
# wf1 = np.reshape(wf,(1025,450,1050))
# print(wf1[0,1,2]) #测试python读取的输出文件数据是否保真

# # 读取经纬度信息
# topo = xr.open_dataset("D:\\case\\data\\other\\ETOPO2v2c_f4.nc")
# # elev = topo.z.loc[70:105,25:40]
# lon = topo.x.loc[70:105]
# lat = topo.y.loc[25:40]
# print(lon)
# print(lat)


# # 读取时间
# need_time=pd.read_table("F:\\snow_sts_data\\TC\\all_tc_days.txt" ,
#                           sep='\s+')
# need_time.columns=['tc_id','time']
# time2 = pd.to_datetime(need_time['time'],format = '%Y%m%d')


# # 插值到站点

# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# station=pd.read_table(path_sta,sep = ",")
# sta_lat=station['lat']
# sta_lon=station['lon']
# time_index=np.arange(0,len(time2))
# #插值要求输出纬度该维递增
# wf2 = np.zeros((len(time2),len(sta_lat)))
# for i in range(len(time2)):
#     for j in range(len(sta_lat)):
#         xi=np.array([time_index[i], sta_lat[j], sta_lon[j]])
#         # print(xi)
#         interp_value=interpolate.interpn((time_index, lat, lon), wf1,xi,
#                                           method='linear')
#         wf2[i,j]=interp_value


#%% branch3 step2 保存文件

# ds = xr.Dataset()
# ds['Wf'] = (('time','station'),wf2)
# ds.coords['time'] = ('time',time2)
# ds.coords['station'] = ('station',station['station'].values)
# ds.to_netcdf('F:\\snow_sts_data\\regress\\variable\\wf_station.nc') 


#%% branch3 step3 测试保存的文件

# data = xr.open_dataset("F:\\snow_sts_data\\regress\\variable\\wf_station.nc")
# ds = data.Wf
# print(ds)
