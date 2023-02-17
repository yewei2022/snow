# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 11:28:35 2022

@author: Lenovo
"""

#%% 下载指定日期的数据 自己扩大范围下载的

import pandas as pd
import cdsapi

c = cdsapi.Client()

file_date="F:\\snow_sts_data\\1981-2020\\snow_date.txt"
date=pd.read_csv(file_date,sep="\s+",usecols=['time'])


#下载当天的数据
# y4=date['time'].astype(str).str[0:4].tolist()
# m2=date['time'].astype(str).str[4:6].tolist()
# d2=date['time'].astype(str).str[6:8].tolist()
# npts=len(y4)

#下载前一天的数据
date.loc[:,'time']=pd.to_datetime(date['time'].astype(str)) 
date1=date.set_index('time') # Datetime 列改为 index
date2=date1.shift(periods=-1, freq="D") #时间前移一天
date3=date2.reset_index(drop=False)
date3.loc[:,'time']=date3['time'].dt.strftime("%Y%m%d")
date4 = date3.sort_values(by='time', ascending=True)
y4=date['time'].astype(str).str[0:4].tolist()
m2=date['time'].astype(str).str[4:6].tolist()
d2=date['time'].astype(str).str[6:8].tolist()
npts=len(y4)

filename =  ['geopotential', 'u', 'v','q']
var_name =  ['geopotential', 'u_component_of_wind', 'v_component_of_wind','Specific humidity']
for j in range(0,4):
    for i in range(0,npts):
        c.retrieve(
            'reanalysis-era5-pressure-levels',
            {
                'product_type': 'reanalysis',
                'variable':var_name[j],
                'pressure_level': ['200','500','700','750'],
                'year': y4[i],
                'month': m2[i],
                'day': d2[i],
                'time': [
                    '00:00', '01:00', '02:00',
                    '03:00', '04:00', '05:00',
                    '06:00', '07:00', '08:00',
                    '09:00', '10:00', '11:00',
                    '12:00', '13:00', '14:00',
                    '15:00', '16:00', '17:00',
                    '18:00', '19:00', '20:00',
                    '21:00', '22:00', '23:00',
                ],
                'format': 'netcdf',
                'area': [
                    60, 50, 0,
                    130,
                ],
            },
            'F:\\snow_sts_data\\ERA5\\snow_mydown\\'+filename[j]+'\\'+
            var_name[j]+'_'+y4[i]+m2[i]+d2[i]+'.nc')
        
        

#%% 只下载最后一天的和组内数据一致的geopotential

# import pandas as pd
# import cdsapi
# import numpy as np

# c = cdsapi.Client()
# pressure0=np.linspace(100,1000,19)
# pressure1=pressure0.astype(int)
# pressure2=[]
# for pres in pressure1:
#     pressure2.append(str(pres))
# c.retrieve(
#     'reanalysis-era5-pressure-levels',
#     {
#         'product_type': 'reanalysis',
#         'variable':'geopotential',
#         'pressure_level': pressure2,
#         'year': ['2020'],
#         'month': ['11'],
#         'day': '27',
#         'time': [
#             '00:00', '01:00', '02:00',
#             '03:00', '04:00', '05:00',
#             '06:00', '07:00', '08:00',
#             '09:00', '10:00', '11:00',
#             '12:00', '13:00', '14:00',
#             '15:00', '16:00', '17:00',
#             '18:00', '19:00', '20:00',
#             '21:00', '22:00', '23:00',
#         ],
#         'format': 'netcdf',
#         'area': [
#             60, 70, 0,
#             140,
#         ],
#     },
#     'F:\\snow_sts_data\\ERA5\\snow_group\\geopotential20201127.nc')