# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 15:44:28 2021

@author: Lenovo
"""


import cdsapi
import requests

# CDS API script to use CDS service to retrieve daily ERA5* variables and iterate over
# all months in the specified years.

# Requires:
# 1) the CDS API to be installed and working on your system
# 2) You have agreed to the ERA5 Licence (via the CDS web page)
# 3) Selection of required variable, daily statistic, etc

# Output:
# 1) separate netCDF file for chosen daily statistic/variable for each month

c = cdsapi.Client(timeout=300)

# Uncomment years as required

years =  ['1977','1994','1995']


# Retrieve all months for a given year.

months = ['01', '02', '03',
          '04', '05', '06',
          '07', '08', '09',
          '10', '11', '12']

# For valid keywords, see Table 2 of:
# https://datastore.copernicus-climate.eu/documents/app-c3s-daily-era5-statistics/C3S_Application-Documentation_ERA5-daily-statistics-v2.pdf

# select your variable; name must be a valid ERA5 CDS API name.
var = "Total precipitation"

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
                 "dataset": "reanalysis-era5-single-levels",
                 "product_type": "reanalysis",
                 "variable": var,
                 "statistic": stat,
                 "year": yr,
                 "month": mn,
                 "time_zone": "UTC+12:0",
                 "frequency": "1-hourly",
                 "area":{"lat": [15, 55], "lon": [70, 140]}
#
# Users can change the output grid resolution and selected area
#
#                "grid": "1.0/1.0",
#                "area":{"lat": [10, 60], "lon": [65, 140]}

                 },
        "workflow_name": "application"
        })

# set name of output file for each month (statistic, variable, year, month

        file_name = "D:/data/ERA5_pre/ERA5_total_precipitation_" + yr + "_" + mn + ".nc"

        location=result[0]['location']
        res = requests.get(location, stream = True)
        print("Writing data to " + file_name)
        with open(file_name,'wb') as fh:
            for r in res.iter_content(chunk_size = 1024):
                fh.write(r)
        fh.close()
