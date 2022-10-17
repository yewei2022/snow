# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 14:11:09 2022
高原40年降雪数据 统计
@author: Lenovo
"""
import os
import pandas as pd
import numpy as np

# 以下必须分块做，不能顺序做，否则变量名重复

need=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_pre_gss_all.txt",
                          sep='\s+',na_values=32700)


#%% branch3 计算 step 2.1 各站点pre的25 50 75 90 95 百分位值

# # 预处理
# # per_younan=info4.quantile([0,0.25,0.5,0.75,0.8,0.9,0.95,1]) 
# # 实测上句命令不管有nan无nan 百分位数计算结果相同 前提是去掉的nan真的是你要计算的那列数据
# # 但是这里用的np.percentile会受到nan值影响 导致算不出来

# def fill_existing3(x):
#     if x["dailypre"] >0:
#         return x["dailypre"]
#     else:
#         return None
# need.loc[:,'dailypre']= need.apply(fill_existing3,axis=1)

# # 排除干扰 便于后面除去gss_inc nan值行
# need.drop(['lon','lat','snow','gss','gss_inc'],axis=1,inplace=True)
# # 删掉gss_inc 缺测行
# need.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行

# # # 将数据按照站点、年份分组计算百分位数
# need['year']=need['time'].astype(str).str[0:4]
# need1=need[['station','year','time','dailypre']]
# per25 = need1.groupby(by=['station','year'])['dailypre'].\
#     apply(lambda x: np.percentile(x, 25))
# per25_reset=per25.reset_index()
# per25_ave=per25_reset.groupby(by=['station'])['dailypre'].mean()

# per50 = need1.groupby(by=['station','year'])['dailypre'].\
#     apply(lambda x: np.percentile(x, 50))
# per50_reset=per50.reset_index()
# per50_ave=per50_reset.groupby(by=['station'])['dailypre'].mean()

# per75 = need1.groupby(by=['station','year'])['dailypre'].\
#     apply(lambda x: np.percentile(x, 75))
# per75_reset=per75.reset_index()
# per75_ave=per75_reset.groupby(by=['station'])['dailypre'].mean()

# per90 = need1.groupby(by=['station','year'])['dailypre'].\
#     apply(lambda x: np.percentile(x, 90))
# per90_reset=per90.reset_index()
# per90_ave=per90_reset.groupby(by=['station'])['dailypre'].mean()

# per95 = need1.groupby(by=['station','year'])['dailypre'].\
#     apply(lambda x: np.percentile(x, 95))
# per95_reset=per95.reset_index()
# per95_ave=per95_reset.groupby(by=['station'])['dailypre'].mean()


# #添加位置信息，法二  
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# sta.set_index('station', inplace=True) # column 改为 index

# per=pd.concat([sta,per25_ave,per50_ave,per75_ave,per90_ave,per95_ave],axis=1)
# per_save=per.reset_index()
# per_save.columns=['station','lon','lat','25th','50th','75th','90th','95th']

# per_save.to_csv("F:\\snow_sts_data\\percentile\\pre_pecentile_all.txt",
#                   index = False,sep=' ',na_rep=32700)



#%% branch3 计算 step 2.2 各站点gssinc的25 50 75 90 95 百分位值

# # 预处理
# # per_younan=info4.quantile([0,0.25,0.5,0.75,0.8,0.9,0.95,1]) 
# # 实测上句命令不管有nan无nan 百分位数计算结果相同 前提是去掉的nan真的是你要计算的那列数据
# # 但是这里用的np.percentile会受到nan值影响

# def fill_existing4(x):
#     if x["gss_inc"] >0:
#         return x["gss_inc"]
#     else:
#         return None
# need.loc[:,'gss_inc']= need.apply(fill_existing4,axis=1)

# # 排除干扰 便于后面除去gss_inc nan值行
# need.drop(['lon','lat','snow','dailypre','gss'],axis=1,inplace=True)
# # 删掉gss_inc 缺测行
# need.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行

# # # # 将数据按照站点、年份分组计算百分位数
# need['year']=need['time'].astype(str).str[0:4]
# need1=need[['station','year','time','gss_inc']]
# per25 = need1.groupby(by=['station','year'])['gss_inc'].\
#     apply(lambda x: np.percentile(x, 25))
# per25_reset=per25.reset_index()
# per25_ave=per25_reset.groupby(by=['station'])['gss_inc'].mean()

# per50 = need1.groupby(by=['station','year'])['gss_inc'].\
#     apply(lambda x: np.percentile(x, 50))
# per50_reset=per50.reset_index()
# per50_ave=per50_reset.groupby(by=['station'])['gss_inc'].mean()

# per75 = need1.groupby(by=['station','year'])['gss_inc'].\
#     apply(lambda x: np.percentile(x, 75))
# per75_reset=per75.reset_index()
# per75_ave=per75_reset.groupby(by=['station'])['gss_inc'].mean()

# per90 = need1.groupby(by=['station','year'])['gss_inc'].\
#     apply(lambda x: np.percentile(x, 90))
# per90_reset=per90.reset_index()
# per90_ave=per90_reset.groupby(by=['station'])['gss_inc'].mean()

# per95 = need1.groupby(by=['station','year'])['gss_inc'].\
#     apply(lambda x: np.percentile(x, 95))
# per95_reset=per95.reset_index()
# per95_ave=per95_reset.groupby(by=['station'])['gss_inc'].mean()


# #添加位置信息，法二  
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# sta.set_index('station', inplace=True) # column 改为 index

# per=pd.concat([sta,per25_ave,per50_ave,per75_ave,per90_ave,per95_ave],axis=1)
# per_save=per.reset_index()
# per_save.columns=['station','lon','lat','25th','50th','75th','90th','95th']

# per_save.to_csv("F:\\snow_sts_data\\percentile\\gssinc_pecentile_all.txt",
#                   index = False,sep=' ',na_rep=32700)

    

#%% branch3 计算 step 2.3 各站点gss的25 50 75 90 95 百分位值

# # 预处理
# # per_younan=info4.quantile([0,0.25,0.5,0.75,0.8,0.9,0.95,1]) 
# # 实测上句命令不管有nan无nan 百分位数计算结果相同 前提是去掉的nan真的是你要计算的那列数据
# # 但是这里用的np.percentile会受到nan值影响

# def fill_existing4(x):
#     if x["gss"] >0:
#         return x["gss"]
#     else:
#         return None
# need.loc[:,'gss']= need.apply(fill_existing4,axis=1)

# # 排除干扰 便于后面除去gss_inc nan值行
# need.drop(['lon','lat','snow','dailypre','gss_inc'],axis=1,inplace=True)
# # 删掉gss_inc 缺测行
# need.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行

# # # # 将数据按照站点、年份分组计算百分位数
# need['year']=need['time'].astype(str).str[0:4]
# need1=need[['station','year','time','gss']]
# per25 = need1.groupby(by=['station','year'])['gss'].\
#     apply(lambda x: np.percentile(x, 25))
# per25_reset=per25.reset_index()
# per25_ave=per25_reset.groupby(by=['station'])['gss'].mean()

# per50 = need1.groupby(by=['station','year'])['gss'].\
#     apply(lambda x: np.percentile(x, 50))
# per50_reset=per50.reset_index()
# per50_ave=per50_reset.groupby(by=['station'])['gss'].mean()

# per75 = need1.groupby(by=['station','year'])['gss'].\
#     apply(lambda x: np.percentile(x, 75))
# per75_reset=per75.reset_index()
# per75_ave=per75_reset.groupby(by=['station'])['gss'].mean()

# per90 = need1.groupby(by=['station','year'])['gss'].\
#     apply(lambda x: np.percentile(x, 90))
# per90_reset=per90.reset_index()
# per90_ave=per90_reset.groupby(by=['station'])['gss'].mean()

# per95 = need1.groupby(by=['station','year'])['gss'].\
#     apply(lambda x: np.percentile(x, 95))
# per95_reset=per95.reset_index()
# per95_ave=per95_reset.groupby(by=['station'])['gss'].mean()


# #添加位置信息，法二  
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# sta.set_index('station', inplace=True) # column 改为 index

# per=pd.concat([sta,per25_ave,per50_ave,per75_ave,per90_ave,per95_ave],axis=1)
# per_save=per.reset_index()
# per_save.columns=['station','lon','lat','25th','50th','75th','90th','95th']

# per_save.to_csv("F:\\snow_sts_data\\percentile\\gss_pecentile_all.txt",
#                   index = False,sep=' ',na_rep=32700)



#%% branch3 计算 step 3.1 根据各个站点的百分位对pre 进行降雪强度标记 

# need1=need[['station','time','snow','dailypre']]

# #先根据pre
# thresh=pd.read_table("F:\\snow_sts_data\\percentile\\pre_pecentile_all.txt",
#                       sep='\s+',usecols=['station','25th','50th','75th',
#                                         '95th'],na_values=32700)

# # # 测试某个值以下占多少百分比
# # info1=thresh[thresh['95th']<10]
# # info4=thresh['95th']
# # per_younan=info4.quantile([0,0.25,0.5,0.75,0.8,0.9,0.95,1]) 

# thresh.columns=['thresh_sta','25th','50th','75th','95th']
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

# need_thresh.drop(['thresh_sta','25th','50th','75th','95th'],axis=1,inplace=True)

# need_thresh.to_csv("F:\\snow_sts_data\\percentile\\snow_pre_label_all.txt",
#                     index = False,sep=' ',na_rep=32700)



#%% branch3 计算 step 3.2 根据各个站点的百分位对gssinc 进行降雪强度标记 

# need1=need[['station','time','snow','gss_inc']]

# #根据gssinc
# thresh=pd.read_table("F:\\snow_sts_data\\percentile\\gssinc_pecentile_all.txt",
#                       sep='\s+',usecols=['station','25th','50th','75th',
#                                         '95th'],na_values=32700)


# # # 测试某个值以下占多少百分比
# # info1=thresh[thresh['95th']<8]
# # info4=thresh['95th']
# # per_younan=info4.quantile([0,0.25,0.5,0.75,0.8,0.9,0.95,1]) 


# thresh.columns=['thresh_sta','25th','50th','75th','95th']
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

# need_thresh.drop(['thresh_sta','25th','50th','75th','95th'],axis=1,inplace=True)

# need_thresh.to_csv("F:\\snow_sts_data\\percentile\\snow_gssinc_label_all.txt",
#                     index = False,sep=' ',na_rep=32700)



#%% branch3 计算 step 3.3 根据各个站点的百分位对gss 进行降雪强度标记 

# need1=need[['station','time','snow','gss']]

# #根据gss
# thresh=pd.read_table("F:\\snow_sts_data\\percentile\\gss_pecentile_all.txt",
#                       sep='\s+',usecols=['station','25th','50th','75th',
#                                         '95th'],na_values=32700)


# # # 测试某个值以下占多少百分比
# # info1=thresh[thresh['95th']<8]
# # info4=thresh['95th']
# # per_younan=info4.quantile([0,0.25,0.5,0.75,0.8,0.9,0.95,1]) 


# thresh.columns=['thresh_sta','25th','50th','75th','95th']
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

# need_thresh.drop(['thresh_sta','25th','50th','75th','95th'],axis=1,inplace=True)

# need_thresh.to_csv("F:\\snow_sts_data\\percentile\\snow_gss_label_all.txt",
#                     index = False,sep=' ',na_rep=32700)



#%% branch3 计算 step # 各站点年均降雪频数空间分布

# need['year']=need['time'].astype(str).str[0:4]
# # 降雪日
# d1=need[['year','time','snow','station']]
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
# d5.to_csv("F:\\snow_sts_data\\1981-2020\\snow_f_all.txt",index = False,
#                 sep=' ',na_rep=32700)


#%% branch3 计算 step # 各站点平均降水量

# pre=need.groupby(by=['station'])['dailypre'].mean()
# #添加位置信息，法二
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# sta.set_index('station', inplace=True) # column 改为 index

# pre1=pd.concat([sta,pre],axis=1)
# pre2=pre1.reset_index()

# #写入文件
# pre2.to_csv("F:\\snow_sts_data\\1981-2020\\sta_avg_pre_all.txt",
#                     index = False,sep=' ',na_rep=32700)

# # 测试某个值以下占多少百分比
# pre3=pre2['dailypre'].dropna(axis=0, how='any',inplace=False) #删除任何有nan的行 便于后面进行缺测的计数
# per=pre3.quantile([0,0.25,0.5,0.75,0.8,0.9,0.95,1])   



#%% branch3 计算 step # 各站点平均积雪深度及其增量

# gssinc=need.groupby(by=['station'])['gss_inc'].mean()
# gss=need.groupby(by=['station'])['gss'].mean()

# #添加位置信息，法二
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# sta.set_index('station', inplace=True) # column 改为 index

# gss1=pd.concat([sta,gssinc,gss],axis=1)
# gss2=gss1.reset_index()

# #将各个站点平均降雪强度写入文件
# gss2.to_csv("F:\\snow_sts_data\\1981-2020\\sta_avg_gss_all.txt",
#                     index = False,sep=' ',na_rep=32700)

# # 测试某个值以下占多少百分比
# gss3=gss2['gss_inc'].dropna(axis=0, how='any',inplace=False) #删除任何有nan的行 便于后面进行缺测的计数
# per=gss3.quantile([0,0.25,0.5,0.75,0.8,0.9,0.95,1])  



#%% branch3 计算 step # 降雪频数、平均降水量，平均积雪深度及其增量的年变化

# need['year']=need['time'].astype(str).str[0:4]
# # 降雪日
# days=need.groupby(by=['year'])['snow'].sum() #慎用value_counts计数，索引很难搞
# #降水量
# pre=need.groupby(by=['year'])['dailypre'].mean() #慎用value_counts计数，索引很难搞
# #gss_inc
# gss_inc=need.groupby(by=['year'])['gss_inc'].mean() #慎用value_counts计数，索引很难搞
# #gss
# gss=need.groupby(by=['year'])['gss'].mean() #慎用value_counts计数，索引很难搞


# # 拉长为40年，填充缺失值
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

# days_pre_gss1=days_pre_gss1.fillna(0) #替换nan值为0 可不需要 因为无nan
# print(days_pre_gss1['days'].mean())
# print(days_pre_gss1['dailypre'].mean())
# print(days_pre_gss1['gss'].mean())
# print(days_pre_gss1['gss_inc'].mean())

# # 3232.575
# # 2.620300179245999
# # 1.535654041488014
# # 0.6588257518582766

# days_pre_gss1.to_csv("F:\\snow_sts_data\\1981-2020\\days_pre_gss_annual_all.txt",
#                     index = False,sep=' ',na_rep=0) 



#%% branch3 计算 step # 降雪频数，平均pre 平均gss月变化

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
# snow1.to_csv("F:\\snow_sts_data\\1981-2020\\days_pre_gss_mon_all.txt",
#                     index = False,sep=' ',na_rep=0)



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

# snow0.to_csv("F:\\snow_sts_data\\1981-2020\\days_pre_gss_season_all.txt",
#                     index = False,sep=' ',na_rep=0) 



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

# need1.to_csv("F:\\snow_sts_data\\1981-2020\\snow_alti_all.txt",
#                     index = False,sep=' ',columns=['alti'],na_rep=32700) 




