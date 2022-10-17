# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 21:34:48 2022
风暴影响下各降雪日TC中心位置
极端降雪日的TC中心位置
影响高原降雪的tc时间，强度统计，存入tc_date_infl.txt 
@author: Lenovo
"""

import pandas as pd


#%% 降雪日的TC点位置 存入TC_dot.txt

# # #找出前后不一致的时间
# # import os
# # date_id=pd.read_csv('F:\\snow_sts_data\\1981-2020\\snow_date.txt',sep="\s+")
# # date_id_list=date_id.time.astype(str).tolist()
# # ERA5_dir='F:\\snow_sts_data\\ERA5\\snow_mydown\\geopotential\\'
# # f_list = os.listdir(ERA5_dir)  # 得到文件夹下的所有文件名称 na_values='32700'
# # str_f_date=[]
# # for file in f_list:
# #     str_f_date.append(file[13:21])  
# # print(set(date_id_list)^set(str_f_date))
    
# import pandas as pd
 
# # 读取降雪日日期

# date_id=pd.read_csv('F:\\snow_sts_data\\1981-2020\\snow_date.txt',sep="\s+")
# tc_info=pd.read_csv("F:\\snow_sts_data\\TC\\BoB_ymdh_bjt_lon_lat.txt",sep="\t")
# tc_info.loc[:,"y4m2d2"]=tc_info['bjt'].astype(str).str[0:8]
# tc1=[]
# for i in range(0,len(date_id)):
#     tc1.append(tc_info[(tc_info['y4m2d2']==date_id['time'][i].astype(str))&\
#                         (tc_info['tc_id']==date_id['tc_id'][i])])
# tc2=pd.concat(tc1,ignore_index=True)

# tc2.to_csv("F:\\snow_sts_data\\TC\\TC_dot.txt",index = False,sep=' ')


#%% 产生影响 的TC最大强度频数百分比 降雪期间TC强度频数百分比 存入TC_intensity_freq.txt

 
# # 读取降雪期间TC强度
# tc_dot=pd.read_csv("F:\\snow_sts_data\\TC\\TC_dot.txt",sep="\s+")
# # 产生影响TC的最大强度
# tc_max=pd.read_csv("F:\\snow_sts_data\\TC\\tc_date_infl.txt",sep="\s+")


# def tc_intensity(x):    
#     if x['wind']<34: 
#         return "1TD"
#     elif (34<=x['wind']<64):
#         return "2TS"
#     elif (64<=x['wind']<83):
#         return "3H1"   
#     elif(83<=x['wind']<96):
#         return "4H2"
#     elif(96<=x['wind']<113):
#         return "5H3"
#     elif(113<=x['wind']<136):
#         return "6H4"
#     else:
#         return "7H5"
# tc_dot.loc[:, 'tc_intensity']=tc_dot.apply(tc_intensity, axis=1) 
# tc_max.loc[:, 'tc_intensity']=tc_max.apply(tc_intensity, axis=1) 


# tc_dot.loc[:,'count_dot']=1
# tc_max.loc[:,'count_max']=1

# dot_freq=tc_dot.groupby(by=['tc_intensity'])['count_dot'].sum() 
# max_freq=tc_max.groupby(by=['tc_intensity'])['count_max'].sum() 

# freq = pd.concat([max_freq,dot_freq],axis=1)

# tc=freq.reset_index()

# tc.loc[:,'per_max']=tc['count_max']/len(tc_max)
# tc.loc[:,'per_dot']=tc['count_dot']/len(tc_dot)


# tc.to_csv("F:\\snow_sts_data\\TC\\TC_intensity_freq.txt",index = False,sep=' ')



#%% 极端降雪日的TC位置 存入TC_dot_extrm.txt 暂时不需要

# # 读取极端降雪日日期
# date_id0=pd.read_csv('F:\\snow_sts_data\\extrm_events\\extrm_info.txt',sep="\s+")
# date_id=date_id0.drop_duplicates(["time"], keep='first').reset_index(drop=True)

# tc_info=pd.read_csv("F:\\snow_sts_data\\TC\\BoB_ymdh_bjt_lon_lat.txt",sep="\t")
# tc_info.loc[:,"y4m2d2"]=tc_info['bjt'].astype(str).str[0:8]
# tc1=[]
# for i in range(0,len(date_id)):
#     tc1.append(tc_info[(tc_info['y4m2d2']==date_id['time'][i].astype(str))&\
#                         (tc_info['tc_id']==date_id['tc_id'][i])])
# tc2=pd.concat(tc1,ignore_index=True)

# tc2.to_csv("F:\\snow_sts_data\\TC\\TC_dot_extrm.txt",index = False,sep=' ')


#%% 影响高原降雪的tc_id 生成时间，最大强度统计，存入tc_date.txt
# tc_date2 是影响日和对应的tc_id


# import pandas as pd

# snow_date=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_date.txt",
#                         sep = "\s+")

# # 现在只需要tc_id
# tc_date3=snow_date.drop_duplicates(["tc_id"], keep='first').reset_index(drop=True)
# tc_id=tc_date3['tc_id'].tolist()

# # 添加tc强度
# bob_tc=pd.read_table('F:\\snow_sts_data\\TC\\BoB_ymdh_bjt_lon_lat.txt',sep = "\t")
# bob_tc['tctime']=bob_tc['bjt'].astype(str).str[0:8]
# maxwind=bob_tc.groupby(by=['tc_id'])['wind'].max()
# maxwind1= maxwind.reset_index()
# maxwind_need=[]
# tc_time=[]

# for i in tc_id:
#     ii=int(i)
#     maxwind_need.append(maxwind1.loc[maxwind1["tc_id"]== ii,['tc_id','wind']])
#     tc_time.append(bob_tc.loc[bob_tc["tc_id"]== i,['tc_id','tctime']])   
# maxwind_need_df = pd.concat(maxwind_need,ignore_index=True)

# tc_time_df = pd.concat(tc_time)
# tc_time_start=tc_time_df.drop_duplicates(["tc_id"], keep='first').reset_index(drop=True)

# tc_time_start.loc[:,'y4']=tc_time_start['tctime'].astype(str).str[0:4]
# tc_time_start.loc[:,'m2']=tc_time_start['tctime'].astype(str).str[4:6]
# tc_time_start.loc[:,'d2']=tc_time_start['tctime'].astype(str).str[6:8]

# maxwind_need_df.set_index('tc_id',inplace=True) # column 改为 index
# tc_time_start.set_index('tc_id',inplace=True) # column 改为 index
# tc_date4=pd.concat([maxwind_need_df,tc_time_start],axis=1)
# tc_date4.reset_index(inplace=True)

# # 归纳各个量的个数
# # tc_date4['count']=1
# # m=tc_date4['count'].sum()
# # w=tc_date4.groupby(by=['y4'])['count'].sum()/m

# tc_date4.to_csv("F:\\snow_sts_data\\TC\\tc_date.txt",index = False,
#                 columns=['tc_id','y4','m2','d2','wind'],sep=' ')




#%% 根据tc_date_infl.txt 的tc_id 生成影响高原降雪的文件目录 tc_file_list.txt

# catalog=pd.read_table("F:\\snow_sts_data\\TC\\tc_date_infl.txt",
#                         usecols=['tc_id'], sep='\s+')
# catalog.sort_values(by='tc_id', ascending=True,inplace=True)

# catalog['prefix']='/mnt/f/snow_sts_data/BOB/bio'
# catalog['suffix']='.txt'
# catalog['filename']=catalog['prefix']+catalog['tc_id'].astype(str)\
#     +catalog['suffix']
# catalog.to_csv("F:\\snow_sts_data\\TC\\tc_file_list.txt",index=False,
#                 header=False,columns = ['filename'])


#%% 影响高原降雪的tc_id  影响时间，最大强度统计，存入tc_date_infl.txt
# tc_date2 是影响日和对应的tc_id

# =============================================================================
# snow_date=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_date.txt",
#                         sep = "\s+")
# 
# 
# # 添加tc强度
# bob_tc=pd.read_table('F:\\snow_sts_data\\TC\\BoB_ymdh_bjt_lon_lat.txt',sep = "\t")
# maxwind=bob_tc.groupby(by=['tc_id'])['wind'].max()
# maxwind1= maxwind.reset_index()
# 
# tc_date3=snow_date.drop_duplicates(["tc_id"], keep='first').reset_index(drop=True)
# 
# maxwind_need=[]
# for tc_id in tc_date3.tc_id:
#     maxwind_need.append(maxwind1.loc[maxwind1["tc_id"]== tc_id,['wind']])
# maxwind_need_df = pd.concat(maxwind_need,ignore_index=True)
# maxwind_need_df.reset_index(drop=True,inplace=True)
# tc_date3['wind']=maxwind_need_df
# 
# tc_date3.loc[:,'y4']=tc_date3['time'].astype(str).str[0:4]
# tc_date3.loc[:,'m2']=tc_date3['time'].astype(str).str[4:6]
# tc_date3.loc[:,'d2']=tc_date3['time'].astype(str).str[6:8]
# tc_date3.columns=['infl_date','tc_id','wind','y4','m2','d2']
# 
# 
# # 归纳各个量的个数
# # tc_date4['count']=1
# # m=tc_date4['count'].sum()
# # w=tc_date4.groupby(by=['y4'])['count'].sum()/m
# # a=tc_date3['wind'].mean()
# 
# tc_date3.to_csv("F:\\snow_sts_data\\TC\\tc_date_infl.txt",index = False,
#                 columns=['infl_date','tc_id','wind','y4','m2','d2'],sep=' ')
# =============================================================================



#%% 根据 tc_infl_date.txt 将影响TC路径按季节 月份分类 得到文件目录track_in_season.txt 

# import pandas as pd

# df1=pd.read_table("F:\\snow_sts_data\\TC\\tc_date_infl.txt",
#                         sep = "\s+")
# def fill_season(x):
#     if 1<=x["m2"] <=2:
#         return "winter"
#     elif 2<x["m2"] <=5:
#         return "premon"
#     elif 5<x["m2"] <=9:
#         return "monsoon"
#     elif 9<x["m2"] <=12:
#         return "postmon"
# df1.loc[:,'season']= df1.apply(fill_season,axis=1)
# df1.drop(['infl_date','d2','y4'],axis=1,inplace=True)
# df1['path']='/mnt/f/snow_sts_data/BOB/bio'+df1['tc_id'].astype(str)\
#     +'.txt'

# a=df1[df1['m2']==9]

# df1['m2']=df1['m2'].apply(lambda x : '{:0>2d}'.format(x))

# df1.to_csv("F:\\snow_sts_data\\TC\\track_in_season.txt",index=False,sep=" ")



#%% 根据 TC_dot.txt 将dot按季节分类 得到TC_dot_season.txt
#根据 TC_dot_extrm.txt 将dot按季节分类 得到TC_dot_extrm_season.txt 暂时不需要

# import pandas as pd

# df1=pd.read_table("F:\\snow_sts_data\\TC\\TC_dot.txt",
#                         sep = "\s+")
# df1.loc[:,'m2']=df1['y4m2d2'].astype(str).str[4:6]
# df1.loc[:,'m2']=df1['m2'].astype(int)

# def fill_season(x):
#     if 1<=x["m2"] <=2:
#         return "winter"
#     elif 2<x["m2"] <=5:
#         return "premon"
#     elif 5<x["m2"] <=9:
#         return "monsoon"
#     elif 9<x["m2"] <=12:
#         return "postmon"
# df1.loc[:,'season']= df1.apply(fill_season,axis=1)
# df1.drop(['bjt'],axis=1,inplace=True)

# a=df1[df1['m2']==4]

# df1['m2']=df1['m2'].apply(lambda x : '{:0>2d}'.format(x))

# df1.to_csv("F:\\snow_sts_data\\TC\\TC_dot_season.txt",index=False,sep=" ",
#             columns=['tc_id', 'lon_tc' ,'lat_tc' ,'y4m2d2', 'm2', 'season','wind'])



#%% 影响高原极端的tc_id  影响时间，最大强度统计，存入tc_infl_date_extrm.txt
# tc_date2 是影响日和对应的tc_id

# import pandas as pd

# date_id=pd.read_csv('F:\\snow_sts_data\\extrm_events\\extrm_info.txt',sep="\s+")
# # #读取影响时间和对应的tc_id
# tc_date2=date_id[['time','tc_id']]


# # 添加tc强度
# bob_tc=pd.read_table('F:\\snow_sts_data\\TC\\BoB_ymdh_bjt_lon_lat.txt',sep = "\t")
# maxwind=bob_tc.groupby(by=['tc_id'])['wind'].max()
# maxwind1= maxwind.reset_index()

# # 只要影响的tc_id,和第一次影响时间
# tc_date3=tc_date2.drop_duplicates(["tc_id"], keep='first').reset_index(drop=True)

# maxwind_need=[]
# for tc_id in tc_date3.tc_id:
#     maxwind_need.append(maxwind1.loc[maxwind1["tc_id"]== tc_id,['wind']])
# maxwind_need_df = pd.concat(maxwind_need,ignore_index=True)
# maxwind_need_df.reset_index(drop=True,inplace=True)
# tc_date3['wind']=maxwind_need_df

# tc_date3.loc[:,'y4']=tc_date3['time'].astype(str).str[0:4]
# tc_date3.loc[:,'m2']=tc_date3['time'].astype(str).str[4:6]
# tc_date3.loc[:,'d2']=tc_date3['time'].astype(str).str[6:8]


# # 归纳各量的个数
# tc_date3['count']=1
# m=tc_date3['count'].sum()
# w=tc_date3.groupby(by=['y4'])['count'].sum()

# # tc_date3.to_csv("F:\\snow_sts_data\\TC\\tc_date_infl_extrm.txt",index = False,
# #                 columns=['tc_id','y4','m2','d2','wind','time'],sep=' ')


#%% 根据tc_infl_date_extrm.txt 的tc_id 生成影响高原极端降雪的tc文件目录 extrm_tc_file_list

# import pandas as pd
   
# catalog=pd.read_table("F:\\snow_sts_data\\TC\\tc_date_infl_extrm.txt",
#                         usecols=['tc_id'], sep='\s+')
# catalog.sort_values(by='tc_id', ascending=True,inplace=True)
# catalog['prefix']='/mnt/f/snow_sts_data/BOB/bio'
# catalog['suffix']='.txt'
# catalog['filename']=catalog['prefix']+catalog['tc_id'].astype(str)\
#     +catalog['suffix']
# catalog.to_csv("F:\\snow_sts_data\\TC\\extrm_tc_file_list.txt",index=False,
#                 header=False,columns = ['filename'])



#%% 计算影响降雪的tc个数 活动日数 降雪日数 后者占前者比例年变化 存入TC_snowdays_annual.txt

# import pandas as pd

# # 活动日数
# tc_info=pd.read_table("F:\\snow_sts_data\\TC\\BoB_ymd_bjt_add.txt",sep='\s+')
# tc_infl=pd.read_table("F:\\snow_sts_data\\TC\\tc_date.txt",sep='\s+')
# tc_info1 =tc_info[tc_info.tc_id.isin(tc_infl.tc_id)]
# tc_info1.loc[:,'count']=1
# tc_info1.loc[:,'year']=tc_info1['bjt'].astype(str).str[0:4]
# tc_info1.loc[:,'ymd']=tc_info1['bjt'].astype(str).str[0:8]
# # 去除重复活动日数
# tc_info2=tc_info1.drop_duplicates(["ymd","tc_id"], keep='first').reset_index(drop=True)
# tc_days=tc_info2.groupby(by=['year'])['count'].sum() 


# # 影响降雪的TC 个数
# tc_num=tc_info1.drop_duplicates(["tc_id"],
#                                 keep='first').reset_index(drop=True)
# tc_num1=tc_num.groupby(by=['year'])['count'].sum() #慎用value_counts计数，索引很难搞

# # TC影响下的降雪日数
# date=pd.read_csv('F:\\snow_sts_data\\1981-2020\\snow_date.txt',sep="\s+")
# date.loc[:,'year']=date['time'].astype(str).str[0:4]
# date.loc[:,'count']=1
# # 去除重复降雪日
# snow_days=date.drop_duplicates(["time"],
#                                 keep='first').reset_index(drop=True)
# snow_days1=snow_days.groupby(by=['year'])['count'].sum() #慎用value_counts计数，索引很难搞

# # 拉长为40年，填充缺失值
# tim_list = pd.date_range("1981-01-01 00:00","2020-12-31 23:00",
#                               freq="Y").strftime("%Y").to_list()
# add = list(range(40))
# add_table=pd.DataFrame(list(zip(tim_list,add)),columns=['year','daysadd'])
# add_table.set_index('year', inplace=True) # column 改为 index #inplace 改变原数据

# tc_info3 = pd.concat([tc_days,tc_num1,snow_days1,add_table],axis=1)
# tc_info4 = tc_info3.sort_values(by='year', ascending=True)
# tc_info4.drop('daysadd',axis=1,inplace=True)
# tc_info4.reset_index(inplace=True)
# tc_info4.columns=['year','tc_days','tc_num','snow_days']
# tc_info4.loc[:,'snow/tc']=tc_info4['snow_days']/tc_info4['tc_days']
# # 不行啊，198602这个TC的活动日数比降雪日数少

# a=tc_info4['snow_days'].mean()
# b=tc_info4['tc_days'].mean()
# c=tc_info4['snow/tc'].mean()


# tc_info4.to_csv("F:\\snow_sts_data\\TC\\TC_snowdays_annual.txt",
#                     index = False,sep=' ',na_rep=0) 


#%% 计算影响降雪的tc个数 强度 影响个数占总个数比例 年变化 存入TC_annual.txt

# import pandas as pd

# # 强度
# tc_info1=pd.read_table("F:\\snow_sts_data\\TC\\tc_date.txt",sep='\s+')
# tc_info1.loc[:,'y4']=tc_info1['y4'].astype(str)
# tc_wind=tc_info1.groupby(by=['y4'])['wind'].mean() 

# # 影响降雪的TC 个数
# tc_info1['count']=1
# tc1=tc_info1.groupby(by=['y4'])['count'].sum() #慎用value_counts计数，索引很难搞

# # TC总个数
# tc_all=pd.read_csv("F:\\snow_sts_data\\TC\\BoB_ymdh_bjt_lon_lat.txt",sep="\t")
# tc_all.loc[:,'y4']=tc_all['bjt'].astype(str).str[0:4]
# # # 去除重复tc
# tc_all0=tc_all.drop_duplicates(["tc_id"],
#                                 keep='first').reset_index(drop=True)
# tc_all0.loc[:,'count']=1
# tc_all1=tc_all0.groupby(by=['y4'])['count'].sum() #慎用value_counts计数，索引很难搞

# # 拉长为40年，填充缺失值
# tim_list = pd.date_range("1981-01-01 00:00","2020-12-31 23:00",
#                               freq="Y").strftime("%Y").to_list()
# add = list(range(40))
# add_table=pd.DataFrame(list(zip(tim_list,add)),columns=['y4','daysadd'])
# add_table.set_index('y4', inplace=True) # column 改为 index #inplace 改变原数据

# tc_info3 = pd.concat([tc1,tc_wind,tc_all1,add_table],axis=1)
# tc_info4 = tc_info3.sort_values(by='y4', ascending=True)
# tc_info4.drop('daysadd',axis=1,inplace=True)
# tc_info4.reset_index(inplace=True)
# tc_info4.columns=['year','tc','wind','tc_all']
# tc_info4['rate']=tc_info4['tc']/tc_info4['tc_all']

# # # a=tc_info4['tc'].mean()
# # # b=tc_info4['wind'].mean()
# # # c=tc_info4['snow'].mean()


# tc_info4.to_csv("F:\\snow_sts_data\\TC\\TC_annual.txt",
#                     index = False,sep=' ',na_rep=0)


#%% 相关性 结论是弱相关 0.3-0.8之间

# import pandas as pd
# from scipy.stats import pearsonr
# import numpy as np

# #读取TC个数和强度的年变化，以及降雪频数，pre，gss年变化
# tc=pd.read_table("F:\\snow_sts_data\\TC\\TC_wind_snow_annual.txt",sep='\s+')
# snow=pd.read_table("F:\\snow_sts_data\\1981-2020\\days_pre_gss_annual.txt",sep='\s+')

# a = tc['wind']
# b = snow['gss_inc']
# r,p = pearsonr(a,b)
# print('r={},p={}'.format(np.round(r,2),np.round(p,2))) 

#%% 计算所有TC的活动日数 

# # 活动日数
# tc_info1=pd.read_table("F:\\snow_sts_data\\TC\\BoB_ymd_bjt_add.txt",sep='\s+')
# # 去除重复活动日数
# tc_info2=tc_info1.drop_duplicates(["bjt"], keep='first').reset_index(drop=True)
# tc_info2.to_csv("F:\\snow_sts_data\\TC\\all_tc_days.txt",index = False,sep=' ')