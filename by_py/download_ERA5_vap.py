# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 21:44:03 2022
整层水汽通量
@author: Lenovo
"""

import pandas as pd
import cdsapi

c = cdsapi.Client()

file_date="F:\\snow_sts_data\\1981-2020\\snow_date.txt"
date=pd.read_csv(file_date,sep="\s+",usecols=['time'])
y4=date['time'].astype(str).str[0:4].tolist()
m2=date['time'].astype(str).str[4:6].tolist()
d2=date['time'].astype(str).str[6:8].tolist()
npts=len(y4)

var_name =['vertical_integral_of_eastward_water_vapour_flux',
      'vertical_integral_of_northward_water_vapour_flux']
for i in range(1,npts):
    for var in var_name:
        c.retrieve(
            'reanalysis-era5-single-levels',
            {
                'product_type': 'reanalysis',
                'variable':var,
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
            'F:\\snow_sts_data\\ERA5\\snow_mydown\\vap\\'+var+'_'+
            y4[i]+m2[i]+d2[i]+'.nc')