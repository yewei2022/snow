# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 21:34:48 2022
各个不同环流形势下的TC中心位置
@author: Lenovo
"""


#%% 不同环流形势下降雪日的TC位置 存入TC_dot_CTC.txt

# import pandas as pd

# # 读取降雪日日期和分类
# pth='snow'
# file_dir="F:\\snow_sts_data\\CTC\\"+pth+"\\"+pth+"_CTC_group.txt"
# date_id=pd.read_csv(file_dir,sep="\s+")
# tc_info=pd.read_csv("F:\\snow_sts_data\\TC\\BoB_ymdh_bjt_lon_lat.txt",sep="\t")
# tc_info.loc[:,"y4m2d2"]=tc_info['bjt'].astype(str).str[0:8]

# a0=tc_info.drop_duplicates(["y4m2d2"], keep='first').reset_index(drop=True)

# tc1=[]
# for i in range(0,len(date_id)):
#     tc1.append(tc_info[(tc_info['y4m2d2']==date_id['time'][i].astype(str))])
# tc2=pd.concat(tc1,ignore_index=True)

# label1=[]
# for time in tc2.y4m2d2:
#     label1.append(date_id.loc[date_id.time.astype(str) == time,['type']])
# label2=pd.concat(label1,ignore_index=True)
# df=pd.concat([tc2,label2],axis=1)

# # 199605和199606有重叠日期，但实际有影响的只有1996
# df['tc_id'].replace([199605],pd.NA,inplace=True) #替换为Nan
# # 同198204
# df['tc_id'].replace([198204],pd.NA,inplace=True) #替换为Nan
# df.dropna(axis=0, how='any',inplace=True) 

# def fill_na(x):
#     if (x["tc_id"] == 199807 and (x["y4m2d2"]=="19981116" or 
#                                   x["y4m2d2"]=="19981117")):
#         return None
#     else:
#         return 1
# df.loc[:,'mark']= df.apply(fill_na,axis=1)
# df.dropna(axis=0, how='any',inplace=True)
# df.drop('mark',axis=1,inplace=True)
# a=df[df['type']==2]
# a1=a.drop_duplicates(["y4m2d2"], keep='first').reset_index(drop=True)

# df.to_csv("F:\\snow_sts_data\\TC\\TC_dot_CTC.txt",index = False,sep=' ')


#%% 不同环流形势下极端降雪日的TC位置 存入TC_dot_CTC_extrm.txt

# import pandas as pd

# # 读取降雪日日期和分类
# file_dir='F:\\snow_sts_data\\CTC\\extrm\\extrm_CTC_mydown.txt'
# date_id=pd.read_csv(file_dir,sep="\s+")
# tc_info=pd.read_csv("F:\\snow_sts_data\\TC\\BoB_ymdh_bjt_lon_lat.txt",sep="\t")
# tc_info.loc[:,"y4m2d2"]=tc_info['bjt'].astype(str).str[0:8]
# tc1=[]
# for i in range(0,len(date_id)):
#     tc1.append(tc_info[(tc_info['y4m2d2']==date_id['time'][i].astype(str))])
# tc2=pd.concat(tc1,ignore_index=True)

# label1=[]
# for time in tc2.y4m2d2:
#     label1.append(date_id.loc[date_id.time.astype(str) == time,['type']])
# label2=pd.concat(label1,ignore_index=True)
# df=pd.concat([tc2,label2],axis=1)

# # 199605和199606有重叠日期，但实际有影响的只有1996
# df['tc_id'].replace([199605],pd.NA,inplace=True) #替换为Nan
# # 同198204
# df['tc_id'].replace([198204],pd.NA,inplace=True) #替换为Nan
# df.dropna(axis=0, how='any',inplace=True) 

# def fill_na(x):
#     if (x["tc_id"] == 199807 and (x["y4m2d2"]=="19981116" or 
#                                   x["y4m2d2"]=="19981117")):
#         return None
#     else:
#         return 1
# df.loc[:,'mark']= df.apply(fill_na,axis=1)
# df.dropna(axis=0, how='any',inplace=True)
# df.drop('mark',axis=1,inplace=True)

# df.to_csv("F:\\snow_sts_data\\TC\\TC_dot_CTC_extrm.txt",index = False,sep=' ')



