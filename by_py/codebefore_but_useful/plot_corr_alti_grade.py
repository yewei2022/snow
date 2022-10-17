# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 19:50:52 2022
积雪深度增量与站点海拔高度相关系数热力图
没啥用相关性
@author: Lenovo
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

need=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_pre_gss.txt",
                          sep='\s+',na_values=32700)
#将积雪深度增量为负的，其他30000以上的标记替换为缺失值
def fill_existing1(x):
    if (x["gss"] <= -30000 or x["gss"]>=30000):
        return None
    else:
        return x["gss"]
need.loc[:,'gss']= need.apply(fill_existing1,axis=1)

def fill_existing2(x):
    if (x["gss_inc"] <0 or x["gss_inc"]>=30000):
        return None
    else:
        return x["gss_inc"]
need.loc[:,'gss_inc']= need.apply(fill_existing2,axis=1)
need.loc[:,'gss']=need['gss'].replace(32766,0) #将某值替换

need1=need[['station','time','gss_inc']]

#添加海拔
path_sta='F:\\snow_sts_data\\tp_sta_info.txt'
sta=pd.read_table(path_sta,sep = ",",usecols=['station','alti'])
# 添加海拔信息 法一  循环添加  海拔，因为index不唯一，不能通过index直接concat
alti=[]
for i in need1.station.tolist():
    ii=int(i)
    alti.append(sta.loc[sta["station"] == ii,['alti']])
alti_df = pd.concat(alti,ignore_index=True)
dd=pd.concat([need1,alti_df],axis=1)

df = dd[['gss_inc','alti']]

# 设置大小
plt.subplots(figsize=(8, 8))
# 热力图
# annot=True 显示数值
# round(2) 小数点2位
sns.heatmap(df.corr().round(2),annot=True)
