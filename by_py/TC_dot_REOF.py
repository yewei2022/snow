# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 23:04:43 2022
不同空间型下的TC中心位置
@author: Lenovo
"""

import pandas as pd


tc_info=pd.read_csv("F:\\snow_sts_data\\TC\\BoB_ymdh_bjt_lon_lat.txt",sep="\t")
tc_info.loc[:,"time"]=tc_info['bjt'].astype(str).str[0:8]

# 读取降雪日日期和分类
file_dir="F:\\snow_sts_data\\REOF\\spa_index.txt"
date_id=pd.read_csv(file_dir,sep="\s+")
# 添加降雪日对应的tc_id
date_tc=pd.read_csv("F:\\snow_sts_data\\1981-2020\\snow_date.txt",sep="\s+")
date_tc1=[]
for i in range(0,len(date_id)):
    # print(date_id['time'][i].astype(str))
    date_tc1.append(date_tc[(date_tc['time']==date_id['time'][i])])
date_tc2=pd.concat(date_tc1,ignore_index=True)

tc1=[]
for i in range(0,len(date_tc2)):
    tc1.append(tc_info[(tc_info['time']==date_tc2['time'][i].astype(str))&
                       (tc_info['tc_id']==date_tc2['tc_id'][i])])
tc2=pd.concat(tc1,ignore_index=True)

label1=[]
for time in tc2.time:
    label1.append(date_id.loc[date_id.time.astype(str) == time,['type']])
label2=pd.concat(label1,ignore_index=True)
df=pd.concat([tc2,label2],axis=1)



# =============================================================================
# # 199605和199606有重叠日期，但实际有影响的只有199606
## 199806和199807 都在19981116 19981117 生命史内 但这两天产生影响的是199806
# df['tc_id'].replace([199605],pd.NA,inplace=True) #替换为Nan
# # 同198204
# df['tc_id'].replace([198204],pd.NA,inplace=True) #替换为Nan
# df.dropna(axis=0, how='any',inplace=True) 
# 
# def fill_na(x):
#     if (x["tc_id"] == 199807 and (x["time"]=="19981116" or 
#                                   x["time"]=="19981117")):
#         return None
#     else:
#         return 1
# df.loc[:,'mark']= df.apply(fill_na,axis=1)
# df.dropna(axis=0, how='any',inplace=True)
# df.drop('mark',axis=1,inplace=True)
# =============================================================================
#  这段直接在前面挑选的时候用tc_id 加date 不就行了吗


df.to_csv("F:\\snow_sts_data\\TC\\TC_dot_REOF.txt",index = False,sep=' ')