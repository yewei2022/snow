# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 11:27:54 2022
计算并检验TC影响下站点年均降雪频数
@author: Lenovo
"""
from scipy import stats
import numpy as np
import pandas as pd

# 读取高原站点总体均值
popl_avg=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_f_all.txt",
                          sep='\s+',na_values=32700)
popl_avg.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行


# 读取风暴数据
need=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_pre_gss.txt",
                          sep='\s+',na_values=32700)
#将积雪深度增量负值替换为缺失值
def fill_existing2(x):
    if x["gss_inc"] <0:
        return None
    else:
        return x["gss_inc"]
need.loc[:,'gss_inc']= need.apply(fill_existing2,axis=1)

need['year']=need['time'].astype(str).str[0:4]
df1=need.groupby(by=['station','year'])['snow'].sum()
df2=df1.reset_index()

# 40年降雪日数均值的显著性检验
info=[]
g1=df2.groupby(['station'])
for group_name, group_eles in g1:
    # print(group_name)
    newline = ['station','p']
    samp_pick=group_eles.snow
    popl_pick=float(popl_avg[popl_avg['station']==group_name]['mean'])
    # print(popl_pick)
    samp_pick.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行
    _,p = list(stats.ttest_1samp(samp_pick, popl_pick))
    newline[0]=group_name
    newline[1]=float(p)    
    info.append(newline)
info1=pd.DataFrame(info,columns=['station','p'])

def get_sig(x):
    if x['p']<0.05: 
        return 1
    else:
        return 0
info1.loc[:, 'sig'] = info1.apply(get_sig, axis=1) 

#计算各站点年均降雪日数
df3=need.groupby(by=['station'])['snow'].sum() #慎用value_counts计数，索引很难搞
#添加位置信息，法二
path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
#拼接
sta.set_index('station', inplace=True) # column 改为 index
info1.set_index('station', inplace=True) # column 改为 index
info2=pd.concat([sta,df3,info1],axis=1)
info3=info2.reset_index()
info3.loc[:,'mean']=info3['snow']/40

#写入文件
info3.to_csv("F:\\snow_sts_data\\1981-2020\\sta_avg_days.txt",
                    index = False,sep=' ',na_rep=32700)

# 测试 ======================================================================
# # 测试某些有snow但p为nan的站点
# w=df2[df2['station']==52645]  因为只有一个样本 只有一年有值

# # 测试某个值以下占多少百分比
# info4=info3['gss_inc'].dropna(axis=0, inplace=False) #删除任何有nan的行 
# per_nonan=info4.quantile([0,0.25,0.5,0.75,0.8,0.9,0.95,1]) 

# info4=info3['gss_inc']
# per_younan=info4.quantile([0,0.25,0.5,0.75,0.8,0.9,0.95,1]) 

#实测，用dataframe计算百分位时 
# 不管有nan无nan 百分位数计算结果相同 前提是去掉的nan真的是你要计算的那列数据
# 但是用np则需要去掉nan

# w=info3['snow'].dropna(axis=0, how='any') #w=69 对69个站造成影响
# print(len(info3[info3['sig']==1]))


