# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 16:33:36 2023
计算理查森数 用theta
@author: Lenovo
"""
import xarray as xr
import datetime
import pandas as pd
from scipy import interpolate
import numpy as np
import metpy
import metpy.calc as mpcalc
from metpy.units import units


#%% branch1 step1 读取所有高度层 uv 数据转化为北京时 做日平均 并挑选出TC活动日

# var_name = ['u','v']
# for name in var_name:
#     file_path='F:\\snow_sts_data\\ERA5\\pick\\'+name+'_selbox.nc'
#     data0 = xr.open_dataset(file_path)
#     var0=data0[name].loc[:, 400:1000,40:25,70:105] #和tmp_alltcdays.nc一致
#     time0=data0.time
#     level0=data0.level.loc[400:1000]
#     lon = data0.longitude.loc[70:105]
#     lat = data0.latitude.loc[40:25]
#     # 时间转换为可处理的格式
#     time1 = pd.to_datetime(time0,format = '%Y-%m-%d %H:%M:%S')
#     #再赋给var0
#     time2 = (time1 + datetime.timedelta(hours=8))#.strftime("%Y-%m-%d %H:%M:%S")
#     # 不用.strftime("%Y-%m-%d %H:%M:%S")  不然还要再转回原来时间格式
#     var0.coords['time'] = time2
#     daily_var = var0.resample(time='1D',closed='left',label='left').mean()
#     print(daily_var)
    
#     need_time=pd.read_table("F:\\snow_sts_data\\TC\\all_tc_days.txt" ,
#                               sep='\s+')
#     need_time.columns=['tc_id','time']
#     sel_date = pd.to_datetime(need_time['time'],format = '%Y%m%d')
#     var_sel = daily_var.sel(time=sel_date.values)
#     print('变量维度: \n{}'.format(var_sel.shape))
#     print(var_sel)
    
#     var_sel.to_netcdf('F:\\snow_sts_data\\ERA5\\deal\\'+name+'_alltcdays.nc')



#%% branch2 step1 读取数据

# file_path0 = "F:\\snow_sts_data\\ERA5\\deal\\tmp\\tmp_alltcdays.nc"
# data0 = xr.open_dataset(file_path0)
# tmp0 = data0.t
# file_path1 = "F:\\snow_sts_data\\ERA5\\deal\\u_alltcdays.nc"
# data1 = xr.open_dataset(file_path1)
# u0 = data1.u
# file_path2 = "F:\\snow_sts_data\\ERA5\\deal\\v_alltcdays.nc"
# data2 = xr.open_dataset(file_path2)
# v0 = data2.v

# level0 = data0.level
# # print(tmp0)
# # print(level0)
# hgt0 = mpcalc.pressure_to_height_std(level0)
# print(hgt0)

# theta = mpcalc.potential_temperature(level0, tmp0)
# print(theta)


#%% branch2 step2 计算

# # 看 u v属性
# # file_path3 = "F:\\snow_sts_data\\ERA5\\u\\era5.u_component_of_wind.20201206.nc"
# # data3 = xr.open_dataset(file_path3)
# # u_units = data3.u
# # print(u_units) # 看属性

# u1 = u0.transpose('level', 'time', 'latitude', 'longitude')
# v1 = v0.transpose('level', 'time', 'latitude', 'longitude')

# # 赋予属性
# u1.attrs['units'] = 'm s**-1'
# u1.attrs['long_name'] = 'U component of wind'
# u1.attrs['standard_name'] = 'eastward_wind'

# v1.attrs['units'] = 'm s**-1'
# v1.attrs['long_name'] = 'V component of wind'
# v1.attrs['standard_name'] = 'northward_wind'

# hgt0 = hgt0*1000.
# hgt0.attrs['units'] = 'meter'
# Ri = mpcalc.gradient_richardson_number(hgt0,  theta, u1, v1, vertical_dim=0)
# print(Ri)


#%% branch2 step3 挑选 存入文件

# var_sel = Ri.loc[500,:,:,:] #400和500hPa值是一样的 可认为算的就是400-500层的值
# print(var_sel[0,1,2]) #测试单个 
# #注意这里print 单位 km/m 
# #因为前面用的hgt0单位是km 单位好像没被我转换过来 不过自己知道这里m已经抵消了就行

# ds = xr.Dataset()
# time0=data0.time
# lon = data0.longitude.loc[70:105]
# lat = data0.latitude.loc[40:25]
# ds['Ri'] = (('time','lat','lon'),var_sel.values)
# ds.coords['time'] = ('time',time0.values)
# ds.coords['lon'] = ('lon',lon.data)
# ds.coords['lat'] = ('lat',lat.data)

# ds.to_netcdf("F:\\snow_sts_data\\ERA5\\deal\\Ri_alltcdays.nc")


#%% branch3  插值到站点 保存文件

# file_dir = "F:\\snow_sts_data\\ERA5\\deal\\Ri_alltcdays.nc"
# data = xr.open_dataset(file_dir)
# var = data.Ri.loc[:,40:25,70:105]
# time0 = data.time
# lon = data.lon.loc[70:105]
# lat = data.lat.loc[40:25]
# # 时间转换为可处理的格式
# time2 = pd.to_datetime(time0,format = '%Y-%m-%d %H:%M:%S')

# print(var)
# # print(var[0,1,2]) #测试单个

# # # 插值到站点

# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# station=pd.read_table(path_sta,sep = ",")
# sta_lat=station['lat']
# sta_lon=station['lon']
# time_index=np.arange(0,len(time2))
# #插值要求输出纬度该维递增
# lat1 = lat[::-1]
# var1 = var[:,::-1,:]
# var2 = np.zeros((len(time2),len(sta_lat)))
# for i in range(len(time2)):
#     for j in range(len(sta_lat)):
#         xi=np.array([time_index[i], sta_lat[j], sta_lon[j]])
#         # print(xi)
#         interp_value=interpolate.interpn((time_index, lat1, lon), var1,xi,
#                                           method='linear')
#         var2[i,j]=interp_value


# ds = xr.Dataset()
# ds['Ri'] = (('time','station'),var2)
# ds.coords['time'] = ('time',time2)
# ds.coords['station'] = ('station',station['station'].values)
# ds.to_netcdf('F:\\snow_sts_data\\regress\\variable\\Ri_station.nc') 


