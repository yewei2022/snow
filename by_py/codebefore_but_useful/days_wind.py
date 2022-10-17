# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 14:11:09 2022
将降雪数据按照TC强度分类
@author: Lenovo
"""
import os
import pandas as pd
import numpy as np
from matplotlib.path import Path

#%% branch1  读数据 根据tc强度贴上不同的标签 

# #读取tc
# tc=pd.read_table("F:\\snow_sts_data\\TC\\tc_date_infl.txt",sep='\s+',
#                  usecols=['tc_id','wind','infl_date'],na_values=32700)

# # 将TC按照强度分为两类
# def fill_wind_label(x):
#     if x["wind"] <=63:
#         return 1
#     elif x["wind"] >=64:
#         return 2
# tc.loc[:,'wind_label']= tc.apply(fill_wind_label,axis=1)
# # a=tc[tc['wind_label']==1]

# # 读取降雪数据
# need=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_pre_gss.txt",
#                           sep='\s+',na_values=32700)
# # #将gss_inc<0 的值标记为为缺失值
# def fill_existing2(x):
#     if x["gss_inc"] <0:
#         return None
#     else:
#         return x["gss_inc"]
# need.loc[:,'gss_inc']= need.apply(fill_existing2,axis=1)

# # #add wind_label

# wind0=[]
# for i in range(0,len(need)):
#     wind0.append(tc.loc[tc['tc_id']==need['tc_id'][i],['wind_label']])
# wind1=pd.concat(wind0,ignore_index=True)
# need_wind=pd.concat([need,wind1],axis=1)

# need_wind.to_csv("F:\\snow_sts_data\\1981-2020\\wind\\snow_pre_gss_wind.txt",
#                  index = False,sep=' ',na_rep=32700)



#%% branch2 计算 step # 各站点年均降雪频数空间分布

# need=pd.read_table("F:\\snow_sts_data\\1981-2020\\wind\\snow_pre_gss_wind.txt",
#                           sep='\s+',na_values=32700)

# d0=need[need['wind_label']==2]
# d1=d0[['time','snow','station']]
# d2=d1.groupby(by=['station'])['snow'].sum() #慎用value_counts计数，索引很难搞
# d3=d2.reset_index()
# d3.loc[:,'mean']=d3['snow']/40
# # #添加位置信息，法二
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# sta.set_index('station', inplace=True) # column 改为 index
# d3.set_index('station', inplace=True)
# d4=pd.concat([sta,d3],axis=1)
# d5=d4.reset_index()
# d5.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行
# d5.to_csv("F:\\snow_sts_data\\1981-2020\\wind\\snow_f2.txt",index = False,
#                 sep=' ',na_rep=32700)



#%% branch3 计算 step # 各站点平均降水量 

# need0=pd.read_table("F:\\snow_sts_data\\1981-2020\\wind\\snow_pre_gss_wind.txt",
#                           sep='\s+',na_values=32700)

# need=need0[need0['wind_label']==2]

# snow_grade=need.groupby(by=['station'])['dailypre'].mean()
# #添加位置信息，法二
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# sta.set_index('station', inplace=True) # column 改为 index

# snow_grade1=pd.concat([sta,snow_grade],axis=1)
# snow_grade2=snow_grade1.reset_index()

# snow_grade2.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行

# #将各个站点平均降雪强度写入文件
# snow_grade2.to_csv("F:\\snow_sts_data\\1981-2020\\wind\\sta_avg_pre2.txt",
#                     index = False,sep=' ',na_rep=32700)


#%% branch3 计算 step # 各站点平均积雪深度 

# need0=pd.read_table("F:\\snow_sts_data\\1981-2020\\wind\\snow_pre_gss_wind.txt",
#                           sep='\s+',na_values=32700)

# need=need0[need0['wind_label']==2]

# gss_grade=need.groupby(by=['station'])['gss_inc'].mean()
# #添加位置信息，法二
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# sta.set_index('station', inplace=True) # column 改为 index

# gss_grade1=pd.concat([sta,gss_grade],axis=1)
# gss_grade2=gss_grade1.reset_index()
# gss_grade2.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行

# #将各个站点平均降雪强度写入文件
# gss_grade2.to_csv("F:\\snow_sts_data\\1981-2020\\wind\\sta_avg_gss2.txt",
#                     index = False,sep=' ',na_rep=32700)

#%% branch3 计算 step # 比较各站点平均积雪深度 

gss1=pd.read_table("F:\\snow_sts_data\\1981-2020\\wind\\sta_avg_gss1.txt",
                          sep='\s+',na_values=32700)

gss2=pd.read_table("F:\\snow_sts_data\\1981-2020\\wind\\sta_avg_gss2.txt",
                          sep='\s+',na_values=32700)
a1=gss1['gss_inc'].mean()
a2=gss2['gss_inc'].mean()

gss11=gss1.set_index(['station']) #设置双索引
gss22=gss2.set_index(['station']) #设置双索引
gss = pd.concat([gss11,gss22],axis=1)
gss.reset_index(inplace=True)

gss.drop(['lat','lon'],axis=1,inplace=True)
gss.columns=['station','gss1','gss2']

def fill_label(x):
    if x["gss1"]>x["gss2"]:
        return 1
    else:
        return 0
gss.loc[:,'count']= gss.apply(fill_label,axis=1)
gss.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行
w=gss['count'].sum()

# w=32 ,gss57 说明较低强度的TC影响的降雪量有32个大于较高强度的，而有25个小于较高强度的
# 但是a1小于a2 上述结论不成立


