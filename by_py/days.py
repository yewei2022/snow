# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 14:11:09 2022
风暴影响下的降雪数据 统计
@author: Lenovo
"""
import os
import pandas as pd
import numpy as np
from matplotlib.path import Path


# # 计算分块做，不能顺序做，否则变量名重复

need=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_pre_gss.txt",
                          sep='\s+',na_values=32700)

# a = need[need['tc_id']==200804]
# a1=a.drop_duplicates(['station'],
#                               keep='first').reset_index(drop=True)



# # ========================================================
# # need.loc[:,'gss']=need['gss'].replace(32766,None) #替换特定值
# # info['station']=info['station'].fillna(0) #替换nan值为0 可不需要
# # ====================================================================


#%% branch3 计算 step # 根据pre percentile 对样本进行降雪强度标记 另存

# need1=need[['station','time','snow','dailypre','tc_id']]

# #根据pre
# thresh=pd.read_table("F:\\snow_sts_data\\percentile\\pre_pecentile_all.txt",
#                       sep='\s+',usecols=['station','25th','50th','75th','90th',
#                                           '95th'],na_values=32700)

# thresh.columns=['thresh_sta','25th','50th','75th','90th','95th']
# #到时候方便删掉thresh_sta列

# #把thresh扩充成need同长度的列
# # #添加阈值 法一 循环添加
# thresh1=[]
# for i in range(0,len(need1)):
#     thresh1.append(thresh[(thresh['thresh_sta']==need1['station'][i])])
# thresh2=pd.concat(thresh1,ignore_index=True)
# need_thresh=pd.concat([need1,thresh2],axis=1)
# def pre_grd_label(x):    
#     if 0<x['dailypre']<x['25th']: 
#         return 1
#     elif (x['25th']<=x['dailypre']<x['50th']):
#         return 2
#     elif (x['50th']<=x['dailypre']<x['75th']):
#         return 3    
#     elif x['dailypre']>=x['75th']:
#         return 4
#     else:
#         return 0
# need_thresh.loc[:, 'pre_grd_label']=need_thresh.apply(pre_grd_label, axis=1) 

# def pre_extrm_label(x):    
#     if x['dailypre']>x['95th']: 
#         return 1
#     else:
#         return 0
# need_thresh.loc[:, 'pre_extrm_label']=need_thresh.apply(pre_extrm_label, axis=1) 

# need_thresh.drop(['thresh_sta','25th','50th','75th','90th','95th'],axis=1,inplace=True)

# need_thresh.to_csv("F:\\snow_sts_data\\percentile\\snow_pre_label.txt",
#                     index = False,sep=' ',na_rep=32700)



#%% branch3 计算 step # 根据gssinc percentile 对样本进行降雪强度标记 另存

# need1=need[['station','time','snow','gss_inc','tc_id']]

# #根据gss
# thresh=pd.read_table("F:\\snow_sts_data\\percentile\\gssinc_pecentile_all.txt",
#                       sep='\s+',usecols=['station','25th','50th','75th','90th',
#                                           '95th'],na_values=32700)

# thresh.columns=['thresh_sta','25th','50th','75th','90th','95th']
# #到时候方便删掉thresh_sta列

# #把thresh扩充成need同长度的列
# # #添加阈值 法一 循环添加
# thresh1=[]
# for i in range(0,len(need1)):
#     thresh1.append(thresh[(thresh['thresh_sta']==need1['station'][i])])
# thresh2=pd.concat(thresh1,ignore_index=True)
# need_thresh=pd.concat([need1,thresh2],axis=1)
# def gss_grd_label(x):    
#     if 0<x['gss_inc']<x['25th']: 
#         return 1
#     elif (x['25th']<=x['gss_inc']<x['50th']):
#         return 2
#     elif (x['50th']<=x['gss_inc']<x['75th']):
#         return 3    
#     elif x['gss_inc']>=x['75th']:
#         return 4
#     else:
#         return 0
# need_thresh.loc[:, 'gssinc_grd_label']=need_thresh.apply(gss_grd_label, axis=1) 

# def gss_extrm_label(x):    
#     if x['gss_inc']>x['95th']: 
#         return 1
#     else:
#         return 0
# need_thresh.loc[:, 'gssinc_extrm_label']=need_thresh.apply(gss_extrm_label, axis=1) 

# need_thresh.drop(['thresh_sta','25th','50th','75th','90th','95th'],axis=1,inplace=True)

# need_thresh.to_csv("F:\\snow_sts_data\\percentile\\snow_gssinc_label.txt",
#                     index = False,sep=' ',na_rep=32700)



#%% branch3 计算 step # 根据gss percentile 对样本进行降雪强度标记 另存

# need1=need[['station','time','snow','gss','tc_id']]

# #根据gss
# thresh=pd.read_table("F:\\snow_sts_data\\percentile\\gss_pecentile_all.txt",
#                       sep='\s+',usecols=['station','25th','50th','75th','90th',
#                                         '95th'],na_values=32700)

# thresh.columns=['thresh_sta','25th','50th','75th','90th','95th']
# #到时候方便删掉thresh_sta列

# #把thresh扩充成need同长度的列
# # #添加阈值 法一 循环添加
# thresh1=[]
# for i in range(0,len(need1)):
#     thresh1.append(thresh[(thresh['thresh_sta']==need1['station'][i])])
# thresh2=pd.concat(thresh1,ignore_index=True)
# need_thresh=pd.concat([need1,thresh2],axis=1)
# def gss_grd_label(x):    
#     if 0<x['gss']<x['25th']: 
#         return 1
#     elif (x['25th']<=x['gss']<x['50th']):
#         return 2
#     elif (x['50th']<=x['gss']<x['75th']):
#         return 3    
#     elif x['gss']>=x['75th']:
#         return 4
#     else:
#         return 0
# need_thresh.loc[:, 'gss_grd_label']=need_thresh.apply(gss_grd_label, axis=1) 

# def gss_extrm_label(x):    
#     if x['gss']>x['95th']: 
#         return 1
#     else:
#         return 0
# need_thresh.loc[:, 'gss_extrm_label']=need_thresh.apply(gss_extrm_label, axis=1) 

# need_thresh.drop(['thresh_sta','25th','50th','75th','90th','95th'],axis=1,inplace=True)

# need_thresh.to_csv("F:\\snow_sts_data\\percentile\\snow_gss_label.txt",
#                     index = False,sep=' ',na_rep=32700)



#%% branch3 计算 step # TC影响下站点累积的pre极端事件频数年变化 不用打开step1

# extrm=pd.read_table("F:\\snow_sts_data\\percentile\\snow_pre_label.txt",
#                           sep='\s+',na_values=32700)
# extrm['year']=extrm['time'].astype(str).str[0:4]
# #站点累积的降雪日数，没有去掉重复日
# prefreq=extrm.groupby(by=['year'])['pre_extrm_label'].sum()
# # 总降雪日
# days=extrm.groupby(by=['year'])['snow'].sum() #慎用value_counts计数，索引很难搞
# # 极端占总降雪日比例
# per_pre=prefreq/days


# # # # 拉长年限
# days0 = pd.concat([prefreq,per_pre,add_table],axis=1)
# days1 = days0.sort_values(by='year', ascending=True)
# days1.drop('daysadd',axis=1,inplace=True)
# days1.reset_index(inplace=True)
# days1.columns=['year','prefreq','per_pre']

# days1.to_csv("F:\\snow_sts_data\\extrm_events\\pre_f_annual.txt",index = False,
#                 sep=' ',na_rep=0)



#%% branch3 计算 step # TC影响下站点累积的gss极端事件频数年变化 不用打开step1

# extrm=pd.read_table("F:\\snow_sts_data\\percentile\\snow_gss_label.txt",
#                           sep='\s+',na_values=32700)
# extrm['year']=extrm['time'].astype(str).str[0:4]
# #站点累积的降雪日数，没有去掉重复日
# gssfreq=extrm.groupby(by=['year'])['gss_extrm_label'].sum()
# # 总降雪日
# days=extrm.groupby(by=['year'])['snow'].sum() #慎用value_counts计数，索引很难搞
# # 极端占总降雪日比例
# per_gss=gssfreq/days


# # # # 拉长年限
# days0 = pd.concat([gssfreq,per_gss,add_table],axis=1)
# days1 = days0.sort_values(by='year', ascending=True)
# days1.drop('daysadd',axis=1,inplace=True)
# days1.reset_index(inplace=True)
# days1.columns=['year','gssfreq','per_gss']

# days1.to_csv("F:\\snow_sts_data\\extrm_events\\gss_f_annual.txt",index = False,
#                 sep=' ',na_rep=0)

#%% branch3 计算 step # 各站点累计pre极端事件频数空间分布 不用打开step1

# need1=pd.read_table("F:\\snow_sts_data\\percentile\\snow_pre_label.txt",
#                             sep='\s+',na_values=32700)
# # 极端日
# d1=need1[['station','time','pre_extrm_label']]
# pre=d1.groupby(by=['station'])['pre_extrm_label'].sum()
# a=pre[pre>0]

# # # #添加位置信息，法二
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# sta.set_index('station', inplace=True) # column 改为 index
# d3=pd.concat([sta,pre],axis=1)
# d4=d3.reset_index()
# d4.columns=['station','lon','lat','pre_extrm_f']

# d4.to_csv("F:\\snow_sts_data\\extrm_events\\pre_f.txt",index = False,
#                 sep=' ',na_rep=32700)



#%% branch3 计算 step # 各站点累计gss极端事件频数空间分布 不用打开step1

# need1=pd.read_table("F:\\snow_sts_data\\percentile\\snow_gss_label.txt",
#                             sep='\s+',na_values=32700)
# # 极端日
# d1=need1[['station','time','gss_extrm_label']]
# gss=d1.groupby(by=['station'])['gss_extrm_label'].sum()
# a=gss[gss>0]

# # # #添加位置信息，法二
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# sta.set_index('station', inplace=True) # column 改为 index
# d3=pd.concat([sta,gss],axis=1)
# d4=d3.reset_index()
# d4.columns=['station','lon','lat','gss_extrm_f']
# b=d4[d4['gss_extrm_f']>0]

# # d4.to_csv("F:\\snow_sts_data\\extrm_events\\gss_f.txt",index = False,
# #                 sep=' ',na_rep=32700)



#%% branch3 计算 step # TC影响下极端降雪数据 另存 不用打开step1

# pre=pd.read_table("F:\\snow_sts_data\\percentile\\snow_pre_label.txt",
#                             sep='\s+',na_values=32700)
# pre.drop(['dailypre','pre_grd_label'],axis=1,inplace=True)
# pre1=pre[pre['pre_extrm_label']==1]
# gss=pd.read_table("F:\\snow_sts_data\\percentile\\snow_gss_label.txt",
#                             sep='\s+',na_values=32700)
# gss.drop(['gss_inc','gss_grd_label'],axis=1,inplace=True)
# gss1=gss[gss['gss_extrm_label']==1]

# extrm=pd.concat([pre1,gss1],axis=0,ignore_index=True)
# extrm1=extrm.drop_duplicates(['station','time','tc_id'],
#                               keep='first').reset_index(drop=True)
# extrm1.drop(['pre_extrm_label','gss_extrm_label'],axis=1,inplace=True)

# # 添加位置信息,法一循环添加
# lon_lat=[]
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# for i in extrm1.station.tolist():
#     lon_lat.append(sta.loc[sta["station"] == i,['lon','lat']])
# lon_lat_df = pd.concat(lon_lat,ignore_index=True)
# extrm2=pd.concat([extrm1,lon_lat_df],axis=1)

# extrm2.to_csv("F:\\snow_sts_data\\extrm_events\\extrm_info.txt",index = False,
#               sep=' ',na_rep=32700)

# # 读取极端降雪日日期
# date0=pd.read_csv('F:\\snow_sts_data\\extrm_events\\extrm_info.txt',sep="\s+")
# date1=date0.drop_duplicates(["time"], keep='first').reset_index(drop=True)
# date1.sort_values(by='time', ascending=True,inplace=True)
# date1.to_csv("F:\\snow_sts_data\\extrm_events\\extrm_date.txt",index = False,
#               columns = ['time'],sep=' ',na_rep=0)





#%% branch3 计算 step # TC影响下的降雪日(一个站点就算）日期  以及对应的tc_id

# need1=need.drop_duplicates(['time','tc_id'],
#                               keep='first').reset_index(drop=True)
# need1.sort_values(by='time', ascending=True,inplace=True)
# need1.to_csv("F:\\snow_sts_data\\1981-2020\\snow_date.txt",index = False,
#               columns = ['time','tc_id'],sep=' ',na_rep=0)



#%% branch3 计算 step # 风暴引起的降水/雪占 当月 高原总降水/雪的百分比

# #1 计算风暴影响下的
# need['yymm']=need['time'].astype(str).str[0:6]
# pre_mon=need.groupby(by=['yymm'])['dailypre'].sum() 
# gssinc_mon=need.groupby(by=['yymm'])['gss_inc'].sum() 
# gss_mon=need.groupby(by=['yymm'])['gss'].sum() 

# #2 计算高原总体的
# need_all=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_pre_gss_all.txt",
#                           sep='\s+',na_values=32700)
# need_all['yymm']=need_all['time'].astype(str).str[0:6]
# pre_mon_all=need_all.groupby(by=['yymm'])['dailypre'].sum() 
# gssinc_mon_all=need_all.groupby(by=['yymm'])['gss_inc'].sum() 
# gss_mon_all=need_all.groupby(by=['yymm'])['gss'].sum() 

# pre_mon.replace([0],pd.NA,inplace=True) #将0替换为Nan
# gssinc_mon.replace([0],pd.NA,inplace=True) #可剔除无降水或降雪的月份
# gss_mon.replace([0],pd.NA,inplace=True) #可剔除无降水或降雪的月份

# comp=pd.concat([pre_mon,pre_mon_all,gssinc_mon,gssinc_mon_all,\
#                 gss_mon,gss_mon_all],axis=1)
# comp.columns=['pre_mon','pre_mon_all','gssinc_mon','gssinc_mon_all',\
#               'gss_mon','gss_mon_all']
# comp.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行 可排除非风暴影响的年月
# comp.loc[:,'per_pre']=comp['pre_mon']/comp['pre_mon_all']
# comp.loc[:,'per_gssinc']=comp['gssinc_mon']/comp['gssinc_mon_all']
# comp.loc[:,'per_gss']=comp['gss_mon']/comp['gss_mon_all']

# comp.reset_index(inplace=True)
# comp['mm']=comp['yymm'].astype(str).str[4:6]
# per_pre_mon=comp.groupby(by=['mm'])['per_pre'].mean()
# per_gssinc_mon=comp.groupby(by=['mm'])['per_gssinc'].mean()
# per_gss_mon=comp.groupby(by=['mm'])['per_gss'].mean()
# per_pre_gss_mon=pd.concat([per_pre_mon,per_gssinc_mon,per_gss_mon],axis=1)
# per_pre_gss_mon.reset_index(drop=False,inplace=True)

# per_pre_gss_mon.to_csv("F:\\snow_sts_data\\1981-2020\\per_pre_gss_mon.txt",
#                         index = False,sep=' ')



#%% branch3 计算 step # 风暴引起的降水/雪占 当季 高原总降水/雪的百分比

# #1 计算风暴影响下的
# need['yymm']=need['time'].astype(str).str[0:6]
# pre_mon=need.groupby(by=['yymm'])['dailypre'].sum() 
# gss_mon=need.groupby(by=['yymm'])['gss_inc'].sum() 

# #2 计算高原总体的
# need_all=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_pre_gss_all.txt",
#                           sep='\s+',na_values=32700)
# need_all.loc[:,'gss_inc']= need_all.apply(fill_existing2,axis=1)
# need_all['yymm']=need_all['time'].astype(str).str[0:6]
# pre_mon_all=need_all.groupby(by=['yymm'])['dailypre'].sum() 
# gss_mon_all=need_all.groupby(by=['yymm'])['gss_inc'].sum() 

# pre_mon.replace([0],pd.NA,inplace=True) #将0替换为Nan
# gss_mon.replace([0],pd.NA,inplace=True) #可剔除无降水或降雪的月份

# comp=pd.concat([pre_mon,pre_mon_all,gss_mon,gss_mon_all],axis=1)
# comp.columns=['pre_mon','pre_mon_all','gss_mon','gss_mon_all']
# comp.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行 可排除非风暴影响的年月
# comp.loc[:,'per_pre']=comp['pre_mon']/comp['pre_mon_all']
# comp.loc[:,'per_gss']=comp['gss_mon']/comp['gss_mon_all']
# comp.reset_index(inplace=True)

# comp['m2']=comp['yymm'].astype(str).str[4:6]
# comp.loc[:,'m2']=comp['m2'].astype(int)

# def fill_season(x):
#     if 1<=x["m2"] <=2:
#         return "1winter"
#     elif 2<x["m2"] <=5:
#         return "2premon"
#     elif 5<x["m2"] <=9:
#         return "3monsoon"
#     elif 9<x["m2"] <=12:
#         return "4postmon"
# comp.loc[:,'season']= comp.apply(fill_season,axis=1)

# per_pre_season=comp.groupby(by=['season'])['per_pre'].mean()
# per_gss_season=comp.groupby(by=['season'])['per_gss'].mean()
# per_pre_gss_season=pd.concat([per_pre_season,per_gss_season],axis=1)
# per_pre_gss_season.reset_index(drop=False,inplace=True)

# per_pre_gss_season.to_csv("F:\\snow_sts_data\\1981-2020\\per_pre_gss_season.txt",
#                         index = False,sep=' ')


#%% branch3 计算 step # 各站点年均降雪频数空间分布  转路sta_avg_days_and_test.py

# d1=need[['time','snow','station']]
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
# d5.to_csv("F:\\snow_sts_data\\1981-2020\\sta_avg_days.txt",index = False,
#                 sep=' ',na_rep=32700)

# # 有na_rep其实就是说明风暴影响下的该站点无降雪日


#%% branch3 计算 step # 各站点平均降水量 转路 sta_avg_pre_and_test.py

# snow_grade=need.groupby(by=['station'])['dailypre'].mean()
# #添加位置信息，法二
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# sta.set_index('station', inplace=True) # column 改为 index

# snow_grade1=pd.concat([sta,snow_grade],axis=1)
# snow_grade2=snow_grade1.reset_index()
# #将各个站点平均降雪强度写入文件
# snow_grade2.to_csv(r"F:\\snow_sts_data\\1981-2020\\sta_avg_pre.txt",
#                     index = False,sep=' ',na_rep=32700)


#%% branch3 计算 step # 各站点平均积雪深度 转路 sta_avg_gss_and_test.py

# gss_grade=need.groupby(by=['station'])['gss_inc'].mean()
# #添加位置信息，法二
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# sta.set_index('station', inplace=True) # column 改为 index

# gss_grade1=pd.concat([sta,gss_grade],axis=1)
# gss_grade2=gss_grade1.reset_index()
# #将各个站点平均降雪强度写入文件
# gss_grade2.to_csv(r"F:\\snow_sts_data\\1981-2020\\sta_avg_gss.txt",
#                     index = False,sep=' ',na_rep=32700)



#%% branch3 计算 step # 降雪频数、平均降水量、平均积雪深度及其增量的年变化

# need['year']=need['time'].astype(str).str[0:4]
# # 降雪频数
# days=need.groupby(by=['year'])['snow'].sum() #慎用value_counts计数，索引很难搞
# #降水量
# pre=need.groupby(by=['year'])['dailypre'].mean() #慎用value_counts计数，索引很难搞
# #gss_inc
# gss_inc=need.groupby(by=['year'])['gss_inc'].mean() #慎用value_counts计数，索引很难搞

# #gss
# gss=need.groupby(by=['year'])['gss'].mean() #慎用value_counts计数，索引很难搞

# # # 拉长为40年，填充缺失值
# tim_list = pd.date_range("1981-01-01 00:00","2020-12-31 23:00",
#                               freq="Y").strftime("%Y").to_list()
# add = list(range(40))
# add_table=pd.DataFrame(list(zip(tim_list,add)),columns=['year','daysadd'])
# add_table.set_index('year', inplace=True) # column 改为 index #inplace 改变原数据

# days_pre_gss = pd.concat([days,pre,gss,gss_inc,add_table],axis=1)
# days_pre_gss1 = days_pre_gss.sort_values(by='year', ascending=True)
# days_pre_gss1.drop('daysadd',axis=1,inplace=True)
# days_pre_gss1.columns=["days","dailypre","gss","gss_inc"]
# days_pre_gss1.reset_index(inplace=True)

# days_pre_gss1=days_pre_gss1.fillna(0) #替换nan值为0 可不需要
# print(days_pre_gss1['days'].mean())
# print(days_pre_gss1['dailypre'].mean())
# print(days_pre_gss1['gss'].mean())
# print(days_pre_gss1['gss_inc'].mean())

# # 20.95
# # 5.410863219514697
# # 1.441558593292148
# # 1.447934422408006

# days_pre_gss1.to_csv("F:\\snow_sts_data\\1981-2020\\days_pre_gss_annual.txt",
#                     index = False,sep=' ',na_rep=0) 

# # na_rep设置为0的原因，若当年没有降雪日，其实就是说明风暴影响下的降雪日为0



#%% 相关性讨论  基本不相关

# import pandas as pd
# from scipy.stats import pearsonr
# import numpy as np

# #读取降雪频数，pre，gss年变化
# snow1=pd.read_table("F:\\snow_sts_data\\1981-2020\\days_pre_gss_annual_all.txt",sep='\s+')
# snow2=pd.read_table("F:\\snow_sts_data\\1981-2020\\days_pre_gss_annual.txt",sep='\s+')

# a = snow1['gss']
# b = snow2['gss']
# r,p = pearsonr(a,b)
# print('r={},p={}'.format(np.round(r,2),np.round(p,2))) 


#%% branch3 计算 step # 降雪频数，平均降水量 平均积雪深度及其增量的月变化

# need['mon']=need['time'].astype(str).str[4:6]
# # 降雪日
# days=need.groupby(by=['mon'])['snow'].sum()/40 #慎用value_counts计数，索引很难搞
# # pre
# pre=need.groupby(by=['mon'])['dailypre'].mean() 
# # gss_inc
# gss_inc=need.groupby(by=['mon'])['gss_inc'].mean() 
# # gss
# gss=need.groupby(by=['mon'])['gss'].mean() 

# tim_list = ['01','02','03','04','05','06','07','08','09','10','11','12']
# add = list(range(12))
# add_table=pd.DataFrame(list(zip(tim_list,add)),columns=['mon','useless'])
# add_table.set_index('mon', inplace=True) # column 改为 index #inplace 改变原数据

# snow0 = pd.concat([days,pre,gss_inc,gss,add_table],axis=1)
# snow1 = snow0.sort_values(by='mon', ascending=True)
# snow1.drop('useless',axis=1,inplace=True)
# snow1.columns=['days','dailypre','gss_inc','gss']
# snow1.reset_index(inplace=True)
# snow1.to_csv("F:\\snow_sts_data\\1981-2020\\days_pre_gss_mon.txt",
#                     index = False,sep=' ',na_rep=0) 

# # # na_rep设置为0的原因，若当年没有降雪日，其实就是说明风暴影响下的降雪日为0



#%% branch3 计算 step # 降雪频数，平均pre 平均gss季节变化

# need['m2']=need['time'].astype(str).str[4:6]
# need.loc[:,'m2']=need['m2'].astype(int)
# def fill_season(x):
#     if 1<=x["m2"] <=2:
#         return "1winter"
#     elif 2<x["m2"] <=5:
#         return "2premon"
#     elif 5<x["m2"] <=9:
#         return "3monsoon"
#     elif 9<x["m2"] <=12:
#         return "4postmon"
# need.loc[:,'season']= need.apply(fill_season,axis=1)

# # 降雪日
# days=need.groupby(by=['season'])['snow'].sum()/40 #慎用value_counts计数，索引很难搞
# # pre
# pre=need.groupby(by=['season'])['dailypre'].mean() 
# # gss
# gss=need.groupby(by=['season'])['gss_inc'].mean() 

# snow0 = pd.concat([days,pre,gss],axis=1)
# snow0.columns=['days','dailypre','gss_inc']
# snow0.reset_index(inplace=True)

# snow0.to_csv("F:\\snow_sts_data\\1981-2020\\days_pre_gss_season.txt",
#                     index = False,sep=' ',na_rep=0) 

# # na_rep设置为0的原因，若当年没有降雪日，其实就是说明风暴影响下的降雪日为0

#%% branch3 计算 step # 为所有降雪站点添加海拔高度  

# #添加海拔
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','alti'])
# # 添加海拔信息 法一  循环添加  海拔，因为index不唯一，不能通过index直接concat
# alti=[]
# for i in need.station.tolist():
#     alti.append(sta.loc[sta["station"] == i,['alti']])
# alti_df = pd.concat(alti,ignore_index=True)
# need1=pd.concat([need,alti_df],axis=1)

# need1.to_csv("F:\\snow_sts_data\\1981-2020\\snow_alti.txt",
#                     index = False,sep=' ',columns=['alti'],na_rep=32700) 



#%%  每个风暴影响的站点数 和 降水量 积雪深度 统计

# snow_f=need.groupby(by=['tc_id'])['snow'].sum()
# pre_avg=need.groupby(by=['tc_id'])['dailypre'].sum()
# gss_avg=need.groupby(by=['tc_id'])['gss'].sum()

# a=pd.concat([snow_f,pre_avg,gss_avg],axis=1)
# a1=a.reset_index()


# per_younan=a1['dailypre'].quantile([0,0.25,0.5,0.75,0.9,1]) 
# print('百分位数: \n{}'.format(per_younan))

# a1.to_csv("F:\\snow_sts_data\\1981-2020\\TC_snow_pre_gss.txt",
#                     index = False,sep=' ') 
