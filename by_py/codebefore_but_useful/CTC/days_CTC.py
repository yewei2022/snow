# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 14:11:09 2022
影响期间不同环流形势的降雪统计
@author: Lenovo
"""

import pandas as pd

#%% 降雪日数月变化

# import pandas as pd

# file="F:\\snow_sts_data\\CTC\\snow\\snow_CTC_group.txt"
# date=pd.read_csv(file,sep="\s+")
# date.loc[:,"mon"]=date['time'].astype(str).str[4:6]
# date.loc[:,"count"]=1

# type_mon=date.groupby(by=['type','mon'])['count'].sum()
# type_mon1=type_mon.reset_index()

# tim_list = ['02','04','05','06','09','10','11','12']
# add = list(range(8))
# add_table=pd.DataFrame(list(zip(tim_list,add)),columns=['mon','useless'])
# add_table.set_index('mon', inplace=True) # column 改为 index #inplace 改变原数据

# type1=type_mon1[type_mon1['type']==3] #!!!!改这里
# type1.set_index('mon', inplace=True) 
# snow0 = pd.concat([type1,add_table],axis=1)
# snow1 = snow0.sort_values(by='mon', ascending=True)
# snow1.drop(['useless','type'],axis=1,inplace=True)
# snow1.reset_index(inplace=True)

# #!!!改这里
# snow1.to_csv("F:\\snow_sts_data\\CTC\\analysis\\mon_days_type3.txt",
#                     index = False,sep=' ',na_rep=0) 



#%% branch1  读数据 根据环流形势贴上不同的标签 

# #读取标签
# file="F:\\snow_sts_data\\CTC\\snow\\snow_CTC_group.txt"
# CTC=pd.read_csv(file,sep="\s+")

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

# # #add CTC_label

# wind0=[]
# for i in range(0,len(need)):
#     wind0.append(CTC.loc[CTC['time']==need['time'][i],['type']])
# wind1=pd.concat(wind0,ignore_index=True)
# need_wind=pd.concat([need,wind1],axis=1)

# need_wind.to_csv("F:\\snow_sts_data\\CTC\\analysis\\snow_pre_gss_CTC.txt",
#                   index = False,sep=' ',na_rep=32700)



#%% branch2 计算 step # SF月变化

# # import pandas as pd

# date=pd.read_csv("F:\\snow_sts_data\\CTC\\analysis\\snow_pre_gss_CTC.txt",
#                   sep="\s+",na_values=32700)
# date.loc[:,"mon"]=date['time'].astype(str).str[4:6]

# type_mon=date.groupby(by=['type','mon'])['snow'].sum()
# type_mon1=type_mon.reset_index()

# tim_list = ['02','04','05','06','09','10','11','12']
# add = list(range(8))
# add_table=pd.DataFrame(list(zip(tim_list,add)),columns=['mon','useless'])
# add_table.set_index('mon', inplace=True) # column 改为 index #inplace 改变原数据

# type1=type_mon1[type_mon1['type']==3] #!!!!改这里
# type1.set_index('mon', inplace=True) 
# snow0 = pd.concat([type1,add_table],axis=1)
# snow1 = snow0.sort_values(by='mon', ascending=True)
# snow1.drop(['useless','type'],axis=1,inplace=True)
# snow1.reset_index(inplace=True)

# #!!!改这里
# snow1.to_csv("F:\\snow_sts_data\\CTC\\analysis\\mon_SF_type3.txt",
#                     index = False,sep=' ',na_rep=0) 



#%% branch2 计算 step # pre月变化

# import pandas as pd

# date=pd.read_csv("F:\\snow_sts_data\\CTC\\analysis\\snow_pre_gss_CTC.txt",
#                   sep="\s+",na_values=32700)
# date.loc[:,"mon"]=date['time'].astype(str).str[4:6]

# type_mon=date.groupby(by=['type','mon'])['dailypre'].mean()
# type_mon1=type_mon.reset_index()

# tim_list = ['02','04','05','06','09','10','11','12']
# add = list(range(8))
# add_table=pd.DataFrame(list(zip(tim_list,add)),columns=['mon','useless'])
# add_table.set_index('mon', inplace=True) # column 改为 index #inplace 改变原数据

# type1=type_mon1[type_mon1['type']==3] #!!!!改这里
# type1.set_index('mon', inplace=True) 
# snow0 = pd.concat([type1,add_table],axis=1)
# snow1 = snow0.sort_values(by='mon', ascending=True)
# snow1.drop(['useless','type'],axis=1,inplace=True)
# snow1.reset_index(inplace=True)

# #!!!改这里
# snow1.to_csv("F:\\snow_sts_data\\CTC\\analysis\\mon_PA_type3.txt",
#                     index = False,sep=' ',na_rep=0) 


#%% branch2 计算 step # SDI月变化

# import pandas as pd

# date=pd.read_csv("F:\\snow_sts_data\\CTC\\analysis\\snow_pre_gss_CTC.txt",
#                   sep="\s+",na_values=32700)
# date.loc[:,"mon"]=date['time'].astype(str).str[4:6]

# type_mon=date.groupby(by=['type','mon'])['gss_inc'].mean()
# type_mon1=type_mon.reset_index()

# tim_list = ['02','04','05','06','09','10','11','12']
# add = list(range(8))
# add_table=pd.DataFrame(list(zip(tim_list,add)),columns=['mon','useless'])
# add_table.set_index('mon', inplace=True) # column 改为 index #inplace 改变原数据

# type1=type_mon1[type_mon1['type']==3] #!!!!改这里
# type1.set_index('mon', inplace=True) 
# snow0 = pd.concat([type1,add_table],axis=1)
# snow1 = snow0.sort_values(by='mon', ascending=True)
# snow1.drop(['useless','type'],axis=1,inplace=True)
# snow1.reset_index(inplace=True)

# #!!!改这里
# snow1.to_csv("F:\\snow_sts_data\\CTC\\analysis\\mon_SDI_type3.txt",
#                     index = False,sep=' ',na_rep=0) 



#%% branch2 计算 step # SD月变化

# import pandas as pd

# date=pd.read_csv("F:\\snow_sts_data\\CTC\\analysis\\snow_pre_gss_CTC.txt",
#                   sep="\s+",na_values=32700)
# date.loc[:,"mon"]=date['time'].astype(str).str[4:6]

# type_mon=date.groupby(by=['type','mon'])['gss'].mean()
# type_mon1=type_mon.reset_index()

# tim_list = ['02','04','05','06','09','10','11','12']
# add = list(range(8))
# add_table=pd.DataFrame(list(zip(tim_list,add)),columns=['mon','useless'])
# add_table.set_index('mon', inplace=True) # column 改为 index #inplace 改变原数据

# type1=type_mon1[type_mon1['type']==3] #!!!!改这里
# type1.set_index('mon', inplace=True) 
# snow0 = pd.concat([type1,add_table],axis=1)
# snow1 = snow0.sort_values(by='mon', ascending=True)
# snow1.drop(['useless','type'],axis=1,inplace=True)
# snow1.reset_index(inplace=True)

# #!!!改这里
# snow1.to_csv("F:\\snow_sts_data\\CTC\\analysis\\mon_SD_type3.txt",
#                     index = False,sep=' ',na_rep=0) 



#%% branch2 计算 step # 不同type下各站点年均降雪频数和其对TC影响下总量的贡献

# need=pd.read_table("F:\\snow_sts_data\\CTC\\analysis\\snow_pre_gss_CTC.txt",
#                           sep='\s+',na_values=32700)

# # 总数
# a1=need[['time','snow','station']]
# a2=a1.groupby(by=['station'])['snow'].sum() #慎用value_counts计数，索引很难搞

# # type
# d0=need[need['type']==3] #!!!
# d1=d0[['time','snow','station']]
# d2=d1.groupby(by=['station'])['snow'].sum() #慎用value_counts计数，索引很难搞
# d3=d2.reset_index()
# d3.loc[:,'mean']=d3['snow']/40

# # #添加位置信息，法二
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# sta.set_index('station', inplace=True) # column 改为 index
# d3.set_index('station', inplace=True)

# d4=pd.concat([sta,d3,a2],axis=1)
# d5=d4.reset_index()
# d5.columns=['station','lon','lat','snow_type','snow_type_mean','snow_all']
# d5.loc[:,'contrib']=d5['snow_type']/d5['snow_all']

# d5.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行
# d5.to_csv("F:\\snow_sts_data\\CTC\\analysis\\snow_f3.txt",index = False,#!!!
#                 sep=' ',na_rep=32700) 



#%% branch3 计算 step # 不同type下各站点平均降水量 和其对TC影响下总量的贡献

# import pandas as pd
# need0=pd.read_table("F:\\snow_sts_data\\CTC\\analysis\\snow_pre_gss_CTC.txt",
#                           sep='\s+',na_values=32700)

# # 总数
# a1=need0.groupby(by=['station'])['dailypre'].sum() #总量

# # type
# need=need0[need0['type']==2]#!!!

# snow_mean=need.groupby(by=['station'])['dailypre'].mean() #平均
# snow_sum=need.groupby(by=['station'])['dailypre'].sum() #总量

# #添加位置信息，法二
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# sta.set_index('station', inplace=True) # column 改为 index

# snow1=pd.concat([sta,snow_mean,snow_sum,a1],axis=1)
# snow2=snow1.reset_index()

# snow2.columns=['station','lon','lat','type_pre_mean','type_pre_sum','all_pre_sum']
# snow2.loc[:,'contrib']=snow2['type_pre_sum']/snow2['all_pre_sum']

# snow2.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行
# aaa=snow2[snow2['contrib']>=0.7]

# # #写入文件
# snow2.to_csv("F:\\snow_sts_data\\CTC\\analysis\\sta_avg_pre2.txt",#!!!
#                     index = False,sep=' ',na_rep=32700)


#%% branch3 计算 step # 不同type下各站点平均积雪深度增量 和其对TC影响下总量的贡献

# import pandas as pd
# need0=pd.read_table("F:\\snow_sts_data\\CTC\\analysis\\snow_pre_gss_CTC.txt",
#                           sep='\s+',na_values=32700)

# # 总数
# a1=need0.groupby(by=['station'])['gss_inc'].sum() #总量

# # type
# need=need0[need0['type']==1]#!!!

# snow_mean=need.groupby(by=['station'])['gss_inc'].mean() #平均
# snow_sum=need.groupby(by=['station'])['gss_inc'].sum() #总量

# # aaa1=need[need['station']==56374] #只有一个值 还缺测
# #一个站点，只有一条数据且为nan，求平均是nan，求和为0

# #添加位置信息，法二
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# sta.set_index('station', inplace=True) # column 改为 index

# snow1=pd.concat([sta,snow_mean,snow_sum,a1],axis=1)
# snow2=snow1.reset_index()

# snow2.columns=['station','lon','lat','type_gssinc_mean','type_gssinc_sum',\
#                'all_gssinc_sum']
# snow2.loc[:,'contrib']=snow2['type_gssinc_sum']/snow2['all_gssinc_sum']

# # # #条件替换 np.where也可
# # snow2['contrib']=snow2['contrib'].mask((snow2['type_gss_mean']==0)&
# #                                        (snow2['type_gss_sum']==0)&(snow2['all_gss_sum']==0),0)
# # #替换为0的原因是想把被影响的位置都画出来，占一个坑位
# # #因为画图时会画等于0 
# # #算了没有必要 有人问解释清楚就行

# snow2.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行

# # aaa=snow2[snow2['contrib']>=0.7]

# # #写入文件
# # snow2.to_csv("F:\\snow_sts_data\\CTC\\analysis\\sta_avg_gssinc1.txt",#!!!
# #                     index = False,sep=' ',na_rep=32700)


#%% branch3 计算 step # 不同type下各站点平均积雪深度 和其对TC影响下总量的贡献

# import pandas as pd
# need0=pd.read_table("F:\\snow_sts_data\\CTC\\analysis\\snow_pre_gss_CTC.txt",
#                           sep='\s+',na_values=32700)

# # 总数
# a1=need0.groupby(by=['station'])['gss'].sum() #总量

# # type
# need=need0[need0['type']==3]#!!!

# snow_mean=need.groupby(by=['station'])['gss'].mean() #平均
# snow_sum=need.groupby(by=['station'])['gss'].sum() #总量

# # aaa1=need[need['station']==56374] #只有一个值 还缺测
# #一个站点，只有一条数据且为nan，求平均是nan，求和为0

# #添加位置信息，法二
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# sta.set_index('station', inplace=True) # column 改为 index

# snow1=pd.concat([sta,snow_mean,snow_sum,a1],axis=1)
# snow2=snow1.reset_index()

# snow2.columns=['station','lon','lat','type_gss_mean','type_gss_sum','all_gss_sum']
# snow2.loc[:,'contrib']=snow2['type_gss_sum']/snow2['all_gss_sum']

# # # #条件替换 np.where也可
# # snow2['contrib']=snow2['contrib'].mask((snow2['type_gss_mean']==0)&
# #                                        (snow2['type_gss_sum']==0)&(snow2['all_gss_sum']==0),0)
# # #替换为0的原因是想把被影响的位置都画出来，占一个坑位
# # #因为画图时会画等于0 
# # #算了没有必要 有人问解释清楚就行

# snow2.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行

# # aaa=snow2[snow2['contrib']>=0.7]

# #写入文件
# snow2.to_csv("F:\\snow_sts_data\\CTC\\analysis\\sta_avg_gss3.txt",#!!!
#                     index = False,sep=' ',na_rep=32700)

