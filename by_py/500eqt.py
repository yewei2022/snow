# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 13:57:32 2022
1.提取并计算TC日均值 成功
2.计算eqt 失败
@author: Lenovo
"""
import xarray as xr
import datetime
import pandas as pd

#%% #读取格点数据

data1 = xr.open_dataset('F:\\snow_sts_data\\ERA5\\all\\pick\\rh500_6h.nc') 
# print(data1)
data2 = xr.open_dataset('F:\\snow_sts_data\\ERA5\\all\\pick\\tmp500_6h.nc')
level = data1.level
lon = data1.longitude
lat = data1.latitude
time0=data1.time
time1 = pd.to_datetime(time0,format = '%Y-%m-%d %H:%M:%S')
time2 = (time1 + datetime.timedelta(hours=12))#.strftime("%Y-%m-%d %H:%M:%S")
rh = data1.r
tmp = data2.t
rh.coords['time'] = time2
tmp.coords['time'] = time2

# # test resample
# # https://blog.csdn.net/m0_52118763/article/details/121441124
# w=pd.date_range(start = '2021/2/1', periods=49,freq='6H')
# y = pd.Series(np.arange(49),index=w)
# print(y)
# yy=y.resample('1D',closed='left',label='left').mean() 
# print(yy)

daily_rh = rh.resample(time='1D',closed='left',label='left').mean()
daily_tmp = tmp.resample(time='1D',closed='left',label='left').mean()

# 这个函数代表连续采样 从初始到结尾一直有时间 和 NCL不同
# print(rh.shape)
# print(daily_rh.shape)

# # 常数扩展至四维 这里好像没啥用
# # https://zhuanlan.zhihu.com/p/425885524
# level1=np.tile(level,(1025,1,161,161))
# print(level1.shape)


#%% # 挑选风暴活动日的时间 
# 参考 https://www.thinbug.com/q/57781130

import metpy.calc as mpcalc
from metpy.units import units
import pandas as pd
import numpy as np

need_time=pd.read_table("F:\\snow_sts_data\\TC\\all_tc_days.txt",
                          sep='\s+')
sel_date = pd.to_datetime(need_time['bjt'],format = '%Y%m%d')
rh_sel = daily_rh.sel(time=sel_date.values)
tmp_sel = daily_tmp.sel(time=sel_date.values)

ds = xr.Dataset()
ds['rh'] = (('time','level','lat','lon'),rh_sel.values*units.percent)
ds['tmp'] = (('time','level','lat','lon'),tmp_sel.values*units.K)
ds.coords['time'] = ('time',sel_date.values)
ds.coords['level'] = ('level',level.values)
ds.coords['lat'] = ('lat',lat.values)
ds.coords['lon'] = ('lon',lon.values)
ds.to_netcdf('F:\\snow_sts_data\\ERA5\\all\\pick\\rh_tmp500.nc')


#%% 计算eqt 失败

# tmp_sel1 =tmp_sel-273.15
# tmp_sel1.attrs['units'] = 'degC'
# # 露点温度 tmp C rh %
# td = mpcalc.dewpoint_from_relative_humidity(tmp_sel1, rh_sel.values)
# # print(td)
# # 相当位温
# theta_e1=[]
# for i in range(0,len(sel_date.values)):
#     theta_e = mpcalc.equivalent_potential_temperature(level*units.hPa, 
#                                                       tmp_sel1[i,:,:,:],
#                                                       td[i,:,:,:])
#     theta_e1.append(theta_e)

# import numpy as np
# import xarray as xr

# theta_e2=np.array(theta_e1)
# print(theta_e2)
# ds1 = xr.Dataset()
# ds1['theta_e'] = (('time','level','lat','lon'),theta_e2*units.K)
# ds1.coords['time'] = ('time',sel_date.values)
# ds1.coords['level'] = ('level',level.values)
# ds1.coords['lat'] = ('lat',lat.values)
# ds1.coords['lon'] = ('lon',lon.values)
# ds1.to_netcdf('F:\\snow_sts_data\\ERA5\\all\\pick\\eqt500.nc')

