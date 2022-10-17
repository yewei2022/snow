# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 11:28:35 2022

@author: Lenovo
"""

import cdsapi

c = cdsapi.Client()

var =  ['geopotential', 'u_component_of_wind', 'v_component_of_wind']
for var in var:
    c.retrieve(
        'reanalysis-era5-pressure-levels',
        {
            'product_type': 'reanalysis',
            'variable':var,
            'pressure_level': [
                '100','150', '200',
                '250', '300',
                '350', '400', '450',
                '500', '550', '600',
                '650', '700', '750',
                '800', '850', '900',
                '950', '1000'],
            'year': [
                '2020',
            ],
            'month': '11',
            'day': '28',
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
                60, 70, 0,
                140,
            ],
        },
        'F:\\snow_sts_data\\ERA5\\snow\\'+'era5.'+var+'.20201128.nc')