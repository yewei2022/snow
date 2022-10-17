# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 22:16:41 2022
以数据连续性为原则（缺测率不超过10%），挑选高原站点
用到的文件：snow_all.txt -记录是否降雪
pre1981_2020.txt gss1981_2020.txt 40年所有站点的雨雪
最终目的：得到确定的研究站点 tp_sta_info_by2014.txt
用于days.py 中筛选
@author: Lenovo
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime

# 获取40年的日数
time1 = pd.to_datetime('1981-01-01')
time2 = pd.to_datetime('2020-12-31')
# Timedelta类型
delta_time = time2 - time1
# 转换为int
delta_time = delta_time.days

#%% 天气现象数据的站点筛选

#读取天气现象数据 没有缺测值标记
weather=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_all.txt",sep = "\t")
weather.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行 便于后面缺测值计数 
weather.loc[:,'count']=1
weath1=weather.groupby(by=['station'])['count'].sum()

weath1=weath1/delta_time
weath1.where(weath1 > 0.9, inplace=True)#cond为True，则保留原值，否则默认替换为nan
#``df1.where(m, df2)``等于``np.where(m, df1, df2)``等于''df1.mask(~m, df2)''
weath1.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行 
# weather无异常值 可不做异常值剔除

weath2=weath1.reset_index(drop=False)
weath_sta=weath2.station.tolist()

#%% 日降水量数据的站点筛选

#读取pre
pre=pd.read_table("F:\\snow_sts_data\\1981-2020\\pre1981_2020.txt",sep='\s+',
                  na_values=32700)
pre.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行 便于后面进行缺测的计数

pre.loc[:,'count']=1
pre1=pre.groupby(by=['station'])['count'].sum()

pre1=pre1/delta_time
pre1.where(pre1 > 0.9, inplace=True)#cond为True，则保留原值，否则默认替换为nan
pre1.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行 
pre2=pre1.reset_index(drop=False)
pre_sta=pre2.station.tolist()

#%% 日积雪深度数据的站点筛选

#读取gss
gss=pd.read_table("F:\\snow_sts_data\\1981-2020\\gss1981_2020.txt",sep='\s+',
                  na_values=32700)
gss.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行 便于后面进行缺测的计数

gss.loc[:,'count']=1 #count用于计数
gss1=gss.groupby(by=['station'])['count'].sum()

gss1=gss1/delta_time
gss1.where(gss1 > 0.9, inplace=True)#cond为True，则保留原值，否则默认替换为nan
gss1.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行 
gss2=gss1.reset_index(drop=False)
gss_sta=gss2.station.tolist()


#%% 合并共同站点 挑出三个数据的共同站点 从中提取高原站点  【剔除异常值 可能不合适】

com_sta=set(weath_sta)&set(pre_sta)&set(gss_sta)
TP_sta_df=pd.read_table("F:\\snow_sts_data\\station_pick\\TP_sta_id_by2014.txt",
                        header=None,names=['station'])
TP_sta=TP_sta_df.station.tolist()
#站点连续 并在高原上
final_sta=list(com_sta&set(TP_sta))
sta_info=pd.read_table("F:\\snow_sts_data\\station_pick\\sta_info.txt",sep=',')

# 添加位置信息 法一 循环添加
pos=[]
for sta in final_sta:
    pos.append(sta_info.loc[sta_info["station"] == sta,:])
pos_df = pd.concat(pos,ignore_index=True)

# 筛选出了最终的高原站点
pos_df.to_csv("F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt",
              index = False,sep=',')


#%% 这块其实可以不用做了

weath3=weather[weather.station.isin(final_sta)]
pre3=pre[pre.station.isin(final_sta)]
gss3=gss[gss.station.isin(final_sta)]
weath3.drop(columns = ['count'],inplace = True)
pre3.drop(columns = ['count'],inplace = True)
gss3.drop(columns = ['count'],inplace = True)

weath3.to_csv("F:\\snow_sts_data\\after_quality_control\\snow_1981_2020.txt",
              index = False,sep=' ',na_rep=32700)
pre3.to_csv("F:\\snow_sts_data\\after_quality_control\\pre_1981_2020.txt",
              index = False,sep=' ',na_rep=32700)
gss3.to_csv("F:\\snow_sts_data\\after_quality_control\\gss_1981_2020.txt",
              index = False,sep=' ',na_rep=32700)

