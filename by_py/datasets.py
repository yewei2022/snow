# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 14:11:09 2022
风暴影响下的高原40年降雪数据集
@author: Lenovo
"""
import os
import pandas as pd
import numpy as np
from matplotlib.path import Path


#%% branch1 step # 根据云系覆盖区域筛选出各个时次影响到的高原站点 另存

# infl_area =pd.read_table("F:\\snow_sts_data\\infl_area.txt",sep = "\t")
# tp_sta_dir="F:\\snow_sts_data\\after_quality_control\\"
# sta_info=pd.read_table(tp_sta_dir+"tp_sta_info_by2014.txt",sep = ",",
#                       usecols=[0,1,2])
# for i in range(len(infl_area)):
#     lonmin1=infl_area['minlon1'][i]
#     lonmax1=infl_area['maxlon1'][i]
#     latmin1=infl_area['minlat1'][i]
#     latmax1=infl_area['maxlat1'][i]
#     lonmin2=infl_area['minlon2'][i]
#     lonmax2=infl_area['maxlon2'][i]
#     latmin2=infl_area['minlat2'][i]
#     latmax2=infl_area['maxlat2'][i]
#     p1= Path([(lonmin1,latmin1),(lonmax1,latmin1),(lonmax1,latmax1),
#               (lonmin1, latmax1)])
#     p2= Path([(lonmin2,latmin2),(lonmax2,latmin2),(lonmax2,latmax2),
#               (lonmin2, latmax2)])
    
#     sta=[]
#     tc_id=[]
#     date=[]
#     lon=[]
#     lat=[]
#     for j in range(len(sta_info)):
#         if p1.contains_point((sta_info['lon'][j],sta_info['lat'][j])) \
#             or p2.contains_point((sta_info['lon'][j],sta_info['lat'][j])):
#             sta.append(sta_info['station'][j])
#             lon.append(sta_info['lon'][j])
#             lat.append(sta_info['lat'][j])
#             tc_id.append(infl_area['tc_id'][i])
#             date.append(infl_area['infl_date'][i])
#     df=pd.DataFrame(zip(tc_id,date,sta,lon,lat),columns=['tc_id','date',
#                                                             'station','lon','lat'])
#     if len(df)>0:
#         df.to_csv("F:\\snow_sts_data\\sta_by_tc_infl_area\\"+infl_area['infl_date']\
#               .astype(str)[i]+'.txt',index = False,sep='\t',encoding = "utf-8")



#%% branch2 step 1 找出风暴云系影响下的高原降雪站点 时间，存入snow_infl.txt

# path_tc_cloud="F:\\snow_sts_data\\sta_by_tc_infl_area\\"
# f_list1 = os.listdir(path_tc_cloud)
# info=[]
# for file in f_list1:
#     info.append(pd.read_table(path_tc_cloud+file,sep = "\t",encoding='utf-8'))
# info_df = pd.concat(info,ignore_index=True) #变成dataframe

# snow_df=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_all.txt",sep = "\t")
# need1=[]

# #对每个日期下的站点（即可能被影响的站点）添加是否降雪的信息 法一 循环添加
# for i in range(0,len(info_df)):
#     need1.append(snow_df[(snow_df['time']==info_df['date'][i]) & \
#                           (snow_df['station']==info_df['station'][i])])
# need11=pd.concat(need1,ignore_index=True)

# #提取降雪日，重要
# need2=need11[need11['snow']==1] 
# # 如何根据行索引取出数据，w和need2相同，包括行索引
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

# need4.to_csv("F:\\snow_sts_data\\1981-2020\\snow_infl.txt",index = False,
#                 sep=' ')



#%% branch2 step 2 将对应的pre,gss,gssinc tc_id赋给snow_infl.txt，存为snow_pre_gss.txt

# #读取pre
# pre=pd.read_table("F:\\snow_sts_data\\1981-2020\\pre1981_2020.txt",sep='\s+',
#                   na_values=32700)
# #读取gss
# gss=pd.read_table("F:\\snow_sts_data\\1981-2020\\gss1981_2020.txt",sep='\s+',
#                   na_values=32700)
# #读取降雪日和站点
# snow_df=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_infl.txt",sep='\s+')

# #add pre
# pre0=[]
# for i in range(0,len(snow_df)):
#     pre0.append(pre[(pre['time']==snow_df['time'][i]) & \
#                           (pre['station']==snow_df['station'][i])])
# pre1=pd.concat(pre0,ignore_index=True)

# #add gss
# gss0=[]
# for i in range(0,len(snow_df)):
#     gss0.append(gss[(gss['time']==snow_df['time'][i]) & \
#                           (gss['station']==snow_df['station'][i])])
# gss1=pd.concat(gss0,ignore_index=True)

# pre11=pre1.set_index(['station','time']) #设置双索引
# gss11=gss1.set_index(['station','time']) #设置双索引
# snow_df1=snow_df.set_index(['station','time']) #设置双索引
# snow_pre_gss = pd.concat([snow_df1,pre11,gss11],axis=1)
# snow_pre_gss.reset_index(inplace=True)

# # 添加tc_id
# infl_area =pd.read_table("F:\\snow_sts_data\\infl_area.txt",sep = "\t")
# tc_id0=[]
# for i in range(0,len(snow_pre_gss)):
#     tc_id0.append(infl_area.loc[infl_area['infl_date']==snow_pre_gss['time'][i],['tc_id']])
# tc_id1=pd.concat(tc_id0,ignore_index=True)
# tc_id1.reset_index(drop=True,inplace=True)
# snow_pre_gss['tc_id']=tc_id1

# snow_pre_gss.to_csv("F:\\snow_sts_data\\1981-2020\\snow_pre_gss.txt",index = False,
#                 sep=' ',na_rep=32700)



#%% # 降雪日定义为出现降雪且dailypre≥0.1mm 并把gss_inc<0 的值标记为为缺失值

# # 注意snow_pre_gss_all.txt里有某些行的lon lat为nan 
# # 不过只要不随便dropna 'any', 就不会影响计算 
# # 或者计算时候直接drop lon lat 列，反正统计的时候并不需要 后期再加上就是

# need0=pd.read_table("F:\\snow_sts_data\\1981-2020\\包含0mm的\\snow_pre_gss.txt",
#                           sep='\s+',na_values=32700)
# need=need0[need0['dailypre']>0]

# def fill_existing2(x):
#     if x["gss_inc"] <0:
#         return None
#     else:
#         return x["gss_inc"]

# need.loc[:,'gss_inc']= need.apply(fill_existing2,axis=1)

# need.to_csv("F:\\snow_sts_data\\1981-2020\\snow_pre_gss.txt",index = False,
#                 sep=' ',na_rep=32700)


