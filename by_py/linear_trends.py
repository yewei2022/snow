# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 20:01:10 2022
风暴影响下各量的线性趋势
统计量更改要改三处 35 74 96
@author: YW
"""
import pandas as pd
import numpy as np
from scipy.stats import linregress

#%% TC影响下 降雪频数、站点平均pre、站点平均gss趋势

# need=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_pre_gss.txt",
#                           sep='\s+',na_values=32700)
# #将积雪深度增量负值替换为缺失值
# def fill_existing2(x):
#     if x["gss_inc"] <0:
#         return None
#     else:
#         return x["gss_inc"]
# need.loc[:,'gss_inc']= need.apply(fill_existing2,axis=1)
# need.drop(['lon','lat','gss'],axis=1,inplace=True) #排除lon lat 的nan干扰
# # 但其实这里根本就用不到lon lat

# # 1 各个站点所求统计量的年变化趋势
# need['year']=need['time'].astype(str).str[0:4]
# g1=need.groupby(['station','year'])

# # # 降雪日数
# # g2=g1.agg({'snow':np.sum})

# # # 平均降水量
# # g2=g1.agg({'dailypre':np.mean})

# # 平均gss
# g2=g1.agg({'gss_inc':np.mean})

# g2.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行 不参与回归
# g3=g2.reset_index()

# # #组内排序

# # #测试
# # g5=g3.groupby(by=['station']).count() #分组中非Na值的数量 看多少年是有值的
# # g6=g5[g5['year']==40] #数据连续即40年都有值的是哪些站
# # #站点并不是每年都有值，很多情况只有一个值 不具备统计意义吧？ 91个站点

# # 组内排序并计算趋势
# # # 法一这个不行，不好取出来
# # # g4=g3.groupby('station').apply(lambda x: x.sort_values('year', ascending=False))

# # 法二
# info=[]
# g4=g3.groupby(['station'])
# for group_name, group_eles in g4:
#     group_eles.sort_values(by='year',ascending=True)
#     # print(group_name)
#     newLine = ['station','b','r','p']
#     newLine[0]=group_name
#     #！！！改变统计量时记得改这里哦
#     newLine[1],_,newLine[2],newLine[3],_=linregress(group_eles.year.astype(int),
#                                                       group_eles.gss_inc)
#     info.append(newLine)
# info1=pd.DataFrame(info,columns=['station','b','r','p'])
# info1.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行

# def get_sig(x):
#     if x['p']<0.05: 
#         return 1
#     else:
#         return 0
# info1.loc[:, 'sig'] = info1.apply(get_sig, axis=1) 
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# sta.set_index('station', inplace=True) # column 改为 index
# info1.set_index('station', inplace=True) # column 改为 index
# info2=pd.concat([sta,info1],axis=1)
# info2.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行
# info2.drop(['r','p'],axis=1,inplace=True)

# # # 日数保存
# # info2.to_csv('F:\\snow_sts_data\\trends\\days.txt',sep=' ',na_rep=32700)

# # # 降水量保存
# # info2.to_csv('F:\\snow_sts_data\\trends\\pre.txt',sep=' ',na_rep=32700)

# # gss保存
# # info2.to_csv('F:\\snow_sts_data\\trends\\gss.txt',sep=' ',na_rep=32700)

# # 测试
# print(len(info2[(info2['b']>0)&(info2['sig']==1)]))

# # 测试
# print(len(info2[info2['b']>0]))

# # # 测试某些有snow但p为nan的站点
# # w=need[need['station']==52707]  #因为只有一个样本 只有一年有值



#%% TC影响下 pre极端降雪事件频数变化趋势

# need=pd.read_table("F:\\snow_sts_data\\percentile\\snow_pre_label.txt",
#                           sep='\s+',na_values=32700)

# # 各个站点所求统计量的年变化趋势
# need['year']=need['time'].astype(str).str[0:4]
# g1=need.groupby(['station','year'])

# # # 频数
# g2=g1.agg({'pre_extrm_label':np.sum})

# g2.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行 不参与回归
# g3=g2.reset_index()

# #组内排序

# # #测试
# # g5=g3.groupby(by=['station']).count() #分组中非Na值的数量 看多少年是有值的
# # g6=g5[g5['year']==40] #数据连续即40年都有值的是哪些站
# # #站点并不是每年都有值，很多情况只有一个值 不具备统计意义吧？ 91个站点

# # 组内排序并计算趋势
# # # 法一这个不行，不好取出来
# # # g4=g3.groupby('station').apply(lambda x: x.sort_values('year', ascending=False))

# # 法二
# info=[]
# g4=g3.groupby(['station'])
# for group_name, group_eles in g4:
#     group_eles.sort_values(by='year',ascending=True)
#     # print(group_name)
#     newLine = ['station','b','r','p']
#     newLine[0]=group_name
#     #！！！改变统计量时记得改这里哦
#     newLine[1],_,newLine[2],newLine[3],_=linregress(group_eles.year.astype(int),
#                                                       group_eles.pre_extrm_label)
#     info.append(newLine)
# info1=pd.DataFrame(info,columns=['station','b','r','p'])
# info1.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行

# def get_sig(x):
#     if x['p']<0.05: 
#         return 1
#     else:
#         return 0
# info1.loc[:, 'sig'] = info1.apply(get_sig, axis=1) 
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# sta.set_index('station', inplace=True) # column 改为 index
# info1.set_index('station', inplace=True) # column 改为 index
# info2=pd.concat([sta,info1],axis=1)
# info2.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行
# info2.drop(['r','p'],axis=1,inplace=True)

# # # # 频数保存
# # info2.to_csv('F:\\snow_sts_data\\extrm_events\\trend_pre.txt',sep=' ',na_rep=32700)


# # # 测试
# # print(len(info2[(info2['b']<0)&(info2['sig']==1)]))

# # # 测试
# # print(len(info2[info2['b']<0]))

# # # # 测试某些有snow但p为nan的站点
# # # w=need[need['station']==52707]  #因为只有一个样本 只有一年有值



#%% TC影响下 gss极端降雪事件频数变化趋势

# need=pd.read_table("F:\\snow_sts_data\\percentile\\snow_gss_label.txt",
#                           sep='\s+',na_values=32700)

# # need=extrm_gss[extrm_gss['gss_extrm_label']==1]
# # 如果先把gss_extrm_label=1的样本挑出来
# # 只对挑出来的样本做趋势分析 会导致结果有很大不同
# # 即样本量减少了，个人认为不能这样

# # 各个站点所求统计量的年变化趋势
# need['year']=need['time'].astype(str).str[0:4]
# g1=need.groupby(['station','year'])

# # # 频数
# g2=g1.agg({'gss_extrm_label':np.sum})

# g2.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行 不参与回归
# g3=g2.reset_index()

# #组内排序

# # #测试
# # g5=g3.groupby(by=['station']).count() #分组中非Na值的数量 看多少年是有值的
# # g6=g5[g5['year']==40] #数据连续即40年都有值的是哪些站
# # #站点并不是每年都有值，很多情况只有一个值 不具备统计意义吧？ 91个站点

# # 组内排序并计算趋势
# # # 法一这个不行，不好取出来
# # # g4=g3.groupby('station').apply(lambda x: x.sort_values('year', ascending=False))

# # 法二
# info=[]
# g4=g3.groupby(['station'])
# for group_name, group_eles in g4:
#     group_eles.sort_values(by='year',ascending=True)
#     # print(group_name)
#     newLine = ['station','b','r','p']
#     newLine[0]=group_name
#     #！！！改变统计量时记得改这里哦
#     newLine[1],_,newLine[2],newLine[3],_=linregress(group_eles.year.astype(int),
#                                                       group_eles.gss_extrm_label)
#     info.append(newLine)
# info1=pd.DataFrame(info,columns=['station','b','r','p'])
# info1.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行

# def get_sig(x):
#     if x['p']<0.05: 
#         return 1
#     else:
#         return 0
# info1.loc[:, 'sig'] = info1.apply(get_sig, axis=1) 
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# sta.set_index('station', inplace=True) # column 改为 index
# info1.set_index('station', inplace=True) # column 改为 index
# info2=pd.concat([sta,info1],axis=1)
# info2.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行
# info2.drop(['r','p'],axis=1,inplace=True)

# # # # 频数保存
# # info2.to_csv('F:\\snow_sts_data\\extrm_events\\trend_gss.txt',sep=' ',na_rep=32700)


# # 测试
# print(len(info2[(info2['b']<0)&(info2['sig']==1)]))

# # 测试
# print(len(info2[info2['b']<0]))

# # # # # 测试某些有snow但p为nan的站点
# # # # w=need[need['station']==52707]  #因为只有一个样本 只有一年有值