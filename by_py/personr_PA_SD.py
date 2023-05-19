# -*- coding: utf-8 -*-
"""
Created on Sat May 13 21:22:40 2023
各站点PA和SD的相关系数
@author: Lenovo
"""



from scipy.stats import pearsonr
import pandas as pd

# 读取风暴数据
need0=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_pre_gss_all.txt",
                          sep='\s+',na_values=32700)
path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
station_tp=pd.read_table(path_sta,sep = ",")
need = need0[need0.station.isin(station_tp.station)]
need.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行

# 均值的显著性检验
info=[]
g1=need.groupby(['station'])
for group_name, group_eles in g1:
    # print(group_name)
    newline = ['station','r','p']
    a=group_eles.dailypre
    b=group_eles.gss
    r,p = pearsonr(a,b)
    newline[0]=group_name
    newline[1]=float(r)    
    newline[2]=float(p)    
    info.append(newline)
info1 = pd.DataFrame(info,columns=['station','r','p'])

def get_sig(x):
    if x['p']<0.05: 
        return 1
    else:
        return 0
info1.loc[:, 'sig'] = info1.apply(get_sig, axis=1) 

# 测试为何55569站点的相关系数为nan
test=need[need['station']==55569]
# 因为该站的gss全为0值，从来不积雪？不可能啊？海拔4km