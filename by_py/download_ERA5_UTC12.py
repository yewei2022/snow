# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 15:44:28 2021
# https://cds.climate.copernicus.eu/cdsapp#!/software/
# app-c3s-daily-era5-statistics?tab=app
# https://confluence.ecmwf.int/display/CKB/
# ERA5%3A+How+to+calculate+daily+total+precipitation
@author: Lenovo
"""


import cdsapi
import requests
import pandas as pd

# CDS API script to use CDS service to retrieve daily ERA5* variables and iterate over
# all months in the specified years.

# Requires:
# 1) the CDS API to be installed and working on your system
# 2) You have agreed to the ERA5 Licence (via the CDS web page)
# 3) Selection of required variable, daily statistic, etc

# Output:
# 1) separate netCDF file for chosen daily statistic/variable for each month

c = cdsapi.Client(timeout=300)

file_date="F:\\snow_sts_data\\1981-2020\\snow_date.txt"
date=pd.read_csv(file_date,sep="\s+",usecols=['time'])
date['years']=date['time'].astype(str).str[0:4]
date['months']=date['time'].astype(str).str[4:6]
date1=date.drop_duplicates(['years','months'], keep='first').reset_index(drop=True)
years=date1.years.tolist()
months=date1.months.tolist()


# For valid keywords, see Table 2 of:
# https://datastore.copernicus-climate.eu/documents/app-c3s-daily-era5-statistics/
# C3S_Application-Documentation_ERA5-daily-statistics-v2.pdf

# select your variable; name must be a valid ERA5 CDS API name.
var = ['geopotential', 'u_component_of_wind', 'v_component_of_wind',
        'Temperature','Specific humidity']

# Select the required statistic, valid names given in link above
stat = "daily_mean"

# Loop over years and months

for yr in years:
    for mn in months:
        result = c.service(
        "tool.toolbox.orchestrator.workflow",
        params={
              "realm": "c3s",
              "project": "app-c3s-daily-era5-statistics",
              "version": "master",
              "kwargs": {
                  "dataset": "reanalysis-era5-pressure-levels",
                  "product_type": "reanalysis",
                  "variable": var,
                  'pressure_level': ['100','200','500','700','750'],
                  "statistic": stat,
                  "year": yr,
                  "month": mn,
                  "time_zone": "UTC+12:0",
                  "frequency": "1-hourly",
                  "area":{"lat": [0, 60], "lon": [50, 130]}
#
# Users can change the output grid resolution and selected area
#
#                "grid": "1.0/1.0",
#                "area":{"lat": [10, 60], "lon": [65, 140]}

                  },
        "workflow_name": "application"
        })

# set name of output file for each month (statistic, variable, year, month

        file_name = "F:\\snow_sts_data\ERA5\\UTC12\\" +yr+mn+".nc"

        location=result[0]['location']
        res = requests.get(location, stream = True)
        print("Writing data to " + file_name)
        with open(file_name,'wb') as fh:
            for r in res.iter_content(chunk_size = 1024):
                fh.write(r)
        fh.close()
