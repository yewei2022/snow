# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 22:23:51 2023
算好所有TC活动日的副高西脊点指数和印缅槽指数
一日一值
然后再分配成站点的形式
@author: Lenovo
"""

import xarray as xr
import datetime
import pandas as pd
from scipy import interpolate
import numpy as np
import metpy.calc as mpcalc
from metpy.units import units



#%% branch1 step1 读取数据 转化为北京时 做平均

# file_path="F:\\snow_sts_data\\ERA5\\all\\pick\\geo500_6h_large.nc"
# data0 = xr.open_dataset(file_path)
# var0=data0.z.loc[:, 500,:,:]
# time0=data0.time
# lon = data0.longitude
# lat = data0.latitude
# # 时间转换为可处理的格式
# time1 = pd.to_datetime(time0,format = '%Y-%m-%d %H:%M:%S')
# #再赋给var0
# time2 = (time1 + datetime.timedelta(hours=8))#.strftime("%Y-%m-%d %H:%M:%S")
# # 不用.strftime("%Y-%m-%d %H:%M:%S")  不然还要再转回原来时间格式
# var0.coords['time'] = time2
# daily_var = var0.resample(time='1D',closed='left',label='left').mean()
# print(daily_var)


#%% branch1 step2 挑选TC活动日时间 写入文件 
# 参考 https://www.thinbug.com/q/57781130

# import pandas as pd

# need_time=pd.read_table("F:\\snow_sts_data\\TC\\all_tc_days.txt" ,
#                           sep='\s+')
# need_time.columns=['tc_id','time']
# sel_date = pd.to_datetime(need_time['time'],format = '%Y%m%d')
# var_sel = daily_var.sel(time=sel_date.values)
# print('变量维度: \n{}'.format(var_sel.shape))
# print(var_sel)

# var_sel.to_netcdf('F:\\snow_sts_data\\ERA5\\all\\pick\\geo500_alltcdays.nc')


#%% branch2 step1 python计算副高西脊点指数 WRPI 不对 未找出原因

# import numpy.ma as ma

# # 读取前面生成的格点数据
# file_path1='F:\\snow_sts_data\\ERA5\\all\\pick\\geo500_alltcdays.nc'
# data1 = xr.open_dataset(file_path1)
# var1=data1.z.loc[:,50:10,90:140]
# lon = data1.longitude.loc[90:140]
# lat = data1.latitude.loc[50:10]
# var1 = var1/98.
# # print(var1)

# # 挑选588线
# def WRPI(value_min, value_max,var1):
#     var11 = var1.where((var1>=value_min) * (var1<value_max), drop=False)
#     #drop=True可以看出哪些日子没有586线 但经纬度格点也会drop掉 所以还是得设为False
#     # print(var11.values)
    
#     time1 = var1.time
#     time2 = pd.to_datetime(time1,format = '%Y-%m-%d %H:%M:%S')
#     # 经度扩展成和 dw 同样大小的数组 在右轴
#     arr_lon=np.broadcast_to(lon,(len(time2),len(lat),len(lon)))
#     # 经度数组与dw同位置 nan一致
#     arr_lon_mask = ma.masked_where(np.isnan(var11), arr_lon)
#     # print(arr_lon_mask.shape)
    
#     # # 法一 用xarray
#     # #填充缺测值 便于变成dataarray 求最小值
#     arr1 = arr_lon_mask.filled(32700)
#     #!!!? 注意 填充32700后 后面算出的最小值 会是32700
#     # print(arr1.shape)
#     ds = xr.Dataset()
#     ds['WRPI'] = (('time','lat','lon'),arr1.data)
#     ds.coords['time'] = ('time',time2)
#     ds.coords['lat'] = ('lat',lat.data)
#     ds.coords['lon'] = ('lon',lon.data)
#     # print(ds)
#     #计算每日所有空间格点最小值 并降到时间维
#     ds1 = ds.reduce(np.min,dim=['lat','lon'])
#     ds2 = ds1.WRPI
#     print('经度size: \n{}'.format(ds2.shape))
#     print('经度为90E的日数: \n{}'.format(len(ds2[ds2==90.]))) 
#     print('经度为Nan的日数: \n{}'.format(len(ds2[ds2==32700]))) # 376 90E +109 nan
    
#     # # 法二 用numpy 两种方法结果相同
#     # idx = np.argmin(arr_lon_mask, axis=2)
#     # num_days=len(time2)
#     # k,i = np.ogrid[:num_days,:len(lat)]
#     # arr_lon_mask1=arr_lon_mask[k,i,idx[k,i]]
#     # ds2 = arr_lon_mask1.min(axis=1)
#     # print('经度: \n{}'.format(ds2.shape)) 
#     # print('经度为90E的日数: \n{}'.format(len(ds2[ds2==90.]))) 
#     # ds3 = ds2.filled(np.nan)
#     # print('经度为Nan的日数: \n{}'.format(len(ds3[np.isnan(ds3)==True]))) 
#     # 376 90E +109 nan
    
#     return ds2


# var_588 = WRPI(587.5, 588.5,var1) #109无588线 的日子
# data_588 = var_588.data
# # print(ds1)

    
# # # 选取原数据中 没有588线的日子 即为32700的日子
# var_no588 = var1.where(var_588==32700, drop=True) #19 无587线
# var_587 = WRPI(586.5, 587.5,var_no588) # 找587线

# # # 选取原数据中 没有587线的日子 即为32700的日子
# var_no587 = var1.where(var_587==32700, drop=True) #1 无586线
# var_586 = WRPI(585.5, 586.5,var_no587) #找586线

# # # 选取原数据中 没有586线的日子 即为32700的日子
# var_no586 = var1.where(var_586==32700, drop=True) #1 无586线
# var_585 = WRPI(584.5, 585.5,var_no586) #找585
# # print(var_585)

# file_new=[]
# var_588_only = var_588.where(var_588!=32700, drop=True)
# var_587_only = var_587.where(var_587!=32700, drop=True)
# var_586_only = var_586.where(var_586!=32700, drop=True)
# var_585_only = var_585.where(var_585!=32700, drop=True)

# # print(var_588_only.shape)

# file_new.append(var_588_only)
# file_new.append(var_587_only)  
# file_new.append(var_586_only)  
# file_new.append(var_585_only)   
# new_file=xr.concat(file_new,dim='time')#合并 
# time1 = new_file.time
# time2 = pd.to_datetime(time1,format = '%Y-%m-%d %H:%M:%S')
# print('组合后文件时间维: \n{}'.format(time2))
# time_orgin = var1.time
# time_orgin1 = pd.to_datetime(time_orgin,format = '%Y-%m-%d %H:%M:%S')
# ds = new_file.reindex(time = time_orgin1)
# time11 = ds.time
# time22 = pd.to_datetime(time11,format = '%Y-%m-%d %H:%M:%S')
# print('组合后文件 调整后时间维: \n{}'.format(time22))

# ds2 = ds.data
# print('WRPI: \n{}'.format(ds2))
# print('WRPI 经度为90E的日数: \n{}'.format(len(ds2[ds2==90.])))





#%% branch2 step2  把一维1025 变成二维（1025,80）增加站点属性 保存文件 

# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# station=pd.read_table(path_sta,sep = ",")
# sta_lat=station['lat']
# sta_lon=station['lon']
# time_index=np.arange(0,len(time2))
# # broadcast 必须在最右维
# var_sta=np.broadcast_to(ds2,(len(station),len(time2)))
# var_sta1=np.swapaxes(var_sta, 0, 1)
# print(var_sta1.shape)


# ds3 = xr.Dataset()
# ds3['WRPI'] = (('time','station'),var_sta1)
# ds3.coords['time'] = ('time',time2)
# ds3.coords['station'] = ('station',station['station'].values)
# # print('保存的数据: \n{}'.format(ds3))
# print('测试: \n{}'.format(ds3.WRPI[12,:])) #看和ds2同一天的值是否一样
# ds3.to_netcdf('F:\\snow_sts_data\\regress\\variable\\WRPI_station.nc')


#%% branch3 step1 计算印缅槽指数 IBTI 

# # 读取前面生成的格点数据
# file_path1='F:\\snow_sts_data\\ERA5\\all\\pick\\geo500_alltcdays.nc'
# data1 = xr.open_dataset(file_path1)
# var1=data1.z.loc[:,20:15,80:100] 
# time1=data1.time
# time2 = pd.to_datetime(time1,format = '%Y-%m-%d %H:%M:%S')
# lon = data1.longitude.loc[90:140]
# lat = data1.latitude.loc[50:10]
# var1 = var1/98.
# # print(var1)
# var2 = var1-580.
# print(var2)
# var3 = var2.reduce(np.sum,dim=['latitude','longitude'])
# print(var3)


#%% branch3 step2  把一维1025 变成二维（1025,80）增加站点属性 保存文件 

# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# station=pd.read_table(path_sta,sep = ",")
# sta_lat=station['lat']
# sta_lon=station['lon']
# time_index=np.arange(0,len(time2))
# # broadcast 必须在最右维
# var_sta=np.broadcast_to(var3,(len(station),len(time2)))
# var_sta1=np.swapaxes(var_sta, 0, 1)
# print(var_sta1.shape)


# ds3 = xr.Dataset()
# ds3['IBTI'] = (('time','station'),var_sta1)
# ds3.coords['time'] = ('time',time2)
# ds3.coords['station'] = ('station',station['station'].values)
# # print('保存的数据: \n{}'.format(ds3))
# print('测试: \n{}'.format(ds3.IBTI[12,:])) #看和ds2同一天的值是否一样
# ds3.to_netcdf('F:\\snow_sts_data\\regress\\variable\\IBTI_station.nc')


#%% branch4 ncl计算WRPI 读取一维1025 变成二维（1025,80）增加站点属性 保存文件

# #读取wf
# var = pd.read_table("F:\\snow_sts_data\\\ERA5\\\deal\\WRPI_alltcdays.txt",
#                     header = None)
# # print(var)
# var3 = var.values.flatten() #变为1维
# print('测试看和同一天的值是否一样: \n{}'.format(var3[12]))

# # 读取时间
# need_time=pd.read_table("F:\\snow_sts_data\\TC\\all_tc_days.txt" ,
#                           sep='\s+')
# need_time.columns=['tc_id','time']
# time2 = pd.to_datetime(need_time['time'],format = '%Y%m%d')


# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# station=pd.read_table(path_sta,sep = ",")
# sta_lat=station['lat']
# sta_lon=station['lon']
# # time_index=np.arange(0,len(time2))
# # broadcast 必须在最右维
# var_sta=np.broadcast_to(var3,(len(station),len(time2)))
# var_sta1=np.swapaxes(var_sta, 0, 1)
# # print(var_sta1.shape)


# ds3 = xr.Dataset()
# ds3['WRPI'] = (('time','station'),var_sta1)
# ds3.coords['time'] = ('time',time2)
# ds3.coords['station'] = ('station',station['station'].values)

# ds3.to_netcdf('F:\\snow_sts_data\\regress\\variable\\WRPI_station.nc')

