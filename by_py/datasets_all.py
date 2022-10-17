# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 14:11:09 2022
高原40年降雪数据集
@author: Lenovo
"""
import os
import pandas as pd
import numpy as np



#%% branch2 step 1 挑出高原所有有降雪天气的站点存入snow_all1.txt，相当于snow_infl.txt

# snow_df=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_all.txt",sep = "\t")

# need2=snow_df[snow_df['snow']==1]
# # 如何根据行索引取出数据，w和need2相同，包括行索引，这里不用
# # index=need2.index.tolist()
# # w=snow_df.loc[index]

# need3=need2.reset_index(drop=True)

# # 添加位置信息,法一循环添加
# lon_lat=[]
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# for i in need3.station.tolist():
#     ii=int(i)
#     lon_lat.append(sta.loc[sta["station"] == ii,['lon','lat']])
# lon_lat_df = pd.concat(lon_lat,ignore_index=True)
# need4=pd.concat([need3,lon_lat_df],axis=1)

# need4.to_csv("F:\\snow_sts_data\\1981-2020\\snow_all1.txt",index = False,
#                 sep=' ')



#%% branch2 step 2 将日降水量,gss,gssinc赋给snow_all1.txt，存入snow_pre_gss_all.txt

# #读取pre
# pre=pd.read_table("F:\\snow_sts_data\\1981-2020\\pre1981_2020.txt",sep='\s+',na_values=32700)
# #读取gss
# gss=pd.read_table("F:\\snow_sts_data\\1981-2020\\gss1981_2020.txt",sep='\s+',na_values=32700) 
# #读取降雪日
# snow_df=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_all1.txt",sep='\s+')

# #add pre
# pre0=[]
# for i in range(0,len(snow_df)):
#     pre0.append(pre[(pre['time']==snow_df['time'][i]) & \
#                           (pre['station']==snow_df['station'][i])])
# pre1=pd.concat(pre0,ignore_index=True)

# # #add gss
# gss0=[]
# for i in range(0,len(snow_df)):
#     gss0.append(gss[(gss['time']==snow_df['time'][i]) & \
#                           (gss['station']==snow_df['station'][i])])
# gss1=pd.concat(gss0,ignore_index=True)

# # 截止目前gss是对的
# # 但接下来下面这行代码不可用 组合降水和降雪 concat时候出了错  
# #因为在前面循环添加信息的时候，两者index长度不同，同样的index对应的可能不是同样的时间和站点数据
# #因此要么在循环的时候给没有该站点该时刻的位置安上人头 要么就双索引 直接按列连接不行的
# # snow_pre_gss=pd.concat([snow_df,pre1,gss1],axis=1)

# pre11=pre1.set_index(['station','time']) #设置双索引
# gss11=gss1.set_index(['station','time']) #设置双索引
# snow_df1=snow_df.set_index(['station','time']) #设置双索引
# snow_pre_gss = pd.concat([snow_df1,pre11,gss11],axis=1)
# snow_pre_gss.reset_index(inplace=True)

# snow_pre_gss.to_csv("F:\\snow_sts_data\\1981-2020\\snow_pre_gss_all.txt",
#                     index = False,sep=' ',na_rep=32700)


#%% # 降雪日定义为出现降雪且dailypre≥0.1mm 并把gss_inc<0 的值标记为为缺失值

# # 注意snow_pre_gss_all.txt里有某些行的lon lat为nan 
# # 不过只要不随便dropna 'any', 就不会影响计算 
# # 或者计算时候直接drop lon lat 列，反正统计的时候并不需要 后期再加上就是

# need0=pd.read_table("F:\\snow_sts_data\\1981-2020\\包含0mm的\\snow_pre_gss_all.txt",
#                           sep='\s+',na_values=32700)
# need=need0[need0['dailypre']>0]

# def fill_existing2(x):
#     if x["gss_inc"] <0:
#         return None
#     else:
#         return x["gss_inc"]

# need.loc[:,'gss_inc']= need.apply(fill_existing2,axis=1)

# need.to_csv("F:\\snow_sts_data\\1981-2020\\snow_pre_gss_all.txt",index = False,
#                 sep=' ',na_rep=32700)



