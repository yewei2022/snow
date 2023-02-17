# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 19:31:34 2023
TC活动日80个站点的海拔高度[1028,80]
*将一维数组扩展为二维
@author: Lenovo
"""
import pandas as pd
import numpy as np
import xarray as xr
from metpy.units import units

# 读取高原站号和海拔
path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
sta0=pd.read_table(path_sta,sep = ",", usecols = ['station','alti'])
sta=sta0.set_index('station') # column 改为 index
sta1=sta.values
sta2 = np.repeat(sta1,1025, 1) #将数据复制为二维，第二维在最右边
sta3=sta2.T #转置

# #读取需要的时间
need_time=pd.read_table("F:\\snow_sts_data\\TC\\all_tc_days.txt" ,
                          sep='\s+')
need_time.columns=['tc_id','time']

sta4= pd.DataFrame(sta3, columns=sta0['station'], index=need_time['time'])

ds = xr.Dataset()
ds['alti'] = (('time','station'),sta4.values*units('m'))
time2 = pd.to_datetime(need_time['time'],format = '%Y%m%d')

ds.coords['time'] = ('time',time2)
ds.coords['station'] = ('station',sta0['station'].values)
print('保存的数据: \n{}'.format(ds))
ds.to_netcdf('F:\\snow_sts_data\\ERA5\\all\\regress\\alti_station.nc') 
