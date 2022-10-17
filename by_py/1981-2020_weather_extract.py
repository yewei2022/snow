# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 16:05:22 2022
提取1981-2020所有是否降雪的信息(不管风暴)，分别读取，并连接
@author: Lenovo
"""

import os
import pandas as pd

# 提取1981-2020所有是否降雪的信息(不管风暴)，分别读取，并连接

path_snow1="F:\\snow_sts_data\\1981-2015\\weather_snow\\"
snow_list1 = os.listdir(path_snow1)
snow1=[]
for file in snow_list1:
    snow1.append(pd.read_table(path_snow1+file,sep = "\t",encoding='utf-8',
                              na_values='9999'))
snow_df1 = pd.concat(snow1,ignore_index=True)
# #add 0 before number
yy=snow_df1['yy'].apply(lambda x : '{:0>4d}'.format(x))
mm=snow_df1['mm'].apply(lambda x : '{:0>2d}'.format(x))
dd=snow_df1['dd'].apply(lambda x : '{:0>2d}'.format(x))
time=yy+mm+dd
snow_df1['time'] =time  # or snow_df1.loc[:, 'time'] = time 
snow_df1.drop(columns = ['yy','mm','dd'],inplace = True)

path_snow2="F:\\snow_sts_data\\2016-2020\\weather_snow\\out2\\"
snow_list2 = os.listdir(path_snow2)
info=[]
for file in snow_list2:
    info.append(pd.read_table(path_snow2+file,sep = "\t",encoding='utf-8',
                              usecols=['station','time','snow'],
                              na_values='9999'))
snow_df2 = pd.concat(info,ignore_index=True) #变成dataframe
snow_df =pd.concat([snow_df1,snow_df2],ignore_index=True)
snow_df.to_csv("F:\\snow_sts_data\\1981-2020\\snow_all.txt",index = False,
                sep='\t')