# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 10:51:18 2022

@author: Lenovo
"""

import pandas as pd


#%% branch1  读数据 标记站点的区域 存入snow_pre_gss_RTC

# # #读取标签
# label=pd.read_csv('F:\\f\\snow_sts_data\\RTC\\f_mean_station_label_modify.txt',
#                 sep="\s+",na_values=32700)

# # 读取降雪数据
# need=pd.read_table("F:\\f\\snow_sts_data\\1981-2020\\snow_pre_gss.txt",
#                           sep='\s+',na_values=32700)
# # #将gss_inc<0 的值标记为为缺失值
# def fill_existing2(x):
#     if x["gss_inc"] <0:
#         return None
#     else:
#         return x["gss_inc"]
# need.loc[:,'gss_inc']= need.apply(fill_existing2,axis=1)

# sta_label=[]
# for j in range(len(need)):
#     sta_label.append(label.loc[label["station"] == need['station'][j],['sta_label']])
# sta_label_1=pd.concat(sta_label,ignore_index=True)

# need.loc[:,'sta_label']=sta_label_1
  
# need.to_csv("F:\\f\\snow_sts_data\\RTC\\snow_pre_gss_RTC.txt", index = False,
#             sep=' ',na_rep=32700)
        

#%% branch2  计算子区域的降雪日各个变量均值分布  存sta_avg_"+name+'_'+str(i)+".txt

# #读取标签
# label=pd.read_csv('F:\\f\\snow_sts_data\\RTC\\f_mean_station_label_modify.txt',
#                 sep="\s+",na_values=32700)

# # 读取降雪数据
# need=pd.read_table("F:\\f\\snow_sts_data\\1981-2020\\snow_pre_gss.txt",
#                           sep='\s+',na_values=32700)
# # #将gss_inc<0 的值标记为为缺失值
# def fill_existing2(x):
#     if x["gss_inc"] <0:
#         return None
#     else:
#         return x["gss_inc"]
# need.loc[:,'gss_inc']= need.apply(fill_existing2,axis=1)

# #添加位置信息，法二
# path_sta='F:\\f\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# sta.set_index('station', inplace=True) # column 改为 index  
 
# names=['dailypre','gss']
# for i in range(1,4):
#     #得到该类站点号
#     sub1=label[label['sta_label']==i]
#     #得到降该类站点的雪数据
#     a1 =need[need.station.isin(sub1.station)] 
#     # 由此得到该类站点的降雪日日期
#     a2=a1.drop_duplicates(['time'], keep='first').reset_index(drop=True)
#     #日期保存
#     a2.to_csv("F:\\f\\snow_sts_data\\RTC\\snow_date_"+str(i)+".txt",
#                         index = False,columns = ['time'],sep=' ',na_rep=32700)
#     #根据降雪日期挑选出原数据中引发该类站点降雪日的降雪数据
#     a3 =need[need.time.isin(a2.time)] 
#     for name in names:
#         avg1=a3.groupby(by=['station'])[name].mean()   
#         avg1=pd.concat([sta,avg1],axis=1)
#         avg2=avg1.reset_index()
#         avg2.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行
#         #将各个站点平均降雪强度写入文件
#         avg2.to_csv("F:\\f\\snow_sts_data\\RTC\\sta_avg_"+name+'_'+str(i)+".txt",
#                             index = False,sep=' ',na_rep=32700)
        
#%% branch2 计算  不同子区域 pre gss月变化

# import pandas as pd

# need=pd.read_csv("F:\\f\\snow_sts_data\\RTC\\snow_pre_gss_RTC.txt",
#                   sep="\s+",na_values=32700)
# need.loc[:,"mon"]=need['time'].astype(str).str[4:6]
# #准备 添加月份
# tim_list = ['02','04','05','06','09','10','11','12']
# add = list(range(8))
# add_table=pd.DataFrame(list(zip(tim_list,add)),columns=['mon','useless'])
# add_table.set_index('mon', inplace=True) # column 改为 index #inplace 改变原数据

# names=['dailypre','gss']
# file_names=['PA','SD']  
# for j in range(0,2):
#     type_mon=need.groupby(by=['sta_label','mon'])[names[j]].mean()
#     type_mon1=type_mon.reset_index()
#     # range(1,4) 左闭右开 1 2 3
#     for i in range(1,4):
#         type1=type_mon1[type_mon1['sta_label']==i] 
#         type1.set_index('mon', inplace=True) 
#         snow0 = pd.concat([type1,add_table],axis=1)
#         snow1 = snow0.sort_values(by='mon', ascending=True)
#         snow1.drop(['useless','sta_label'],axis=1,inplace=True)
#         snow1.reset_index(inplace=True)
#         snow1.to_csv("F:\\f\\snow_sts_data\\RTC\\mon_"+file_names[j]+\
#                       "_"+str(i)+".txt", index = False,sep=' ',na_rep=0) 
            


#%% branch2 计算  不同子区域 降雪日数月变化 这里不能像前面算pre gss那样

# import pandas as pd

# need=pd.read_csv("F:\\f\\snow_sts_data\\RTC\\snow_pre_gss_RTC.txt",
#                   sep="\s+",na_values=32700)
# need.loc[:,"mon"]=need['time'].astype(str).str[4:6]
# #准备 添加月份
# tim_list = ['02','04','05','06','09','10','11','12']
# add = list(range(8))
# add_table=pd.DataFrame(list(zip(tim_list,add)),columns=['mon','useless'])
# add_table.set_index('mon', inplace=True) # column 改为 index #inplace 改变原数据

# # range(1,4) 左闭右开 1 2 3
# for i in range(1,4):  
#     #得到降该类站点的雪数据 
#     a1 =need[need['sta_label']==i] 
#     # 由此得到该类站点的降雪日日期
#     a2=a1.drop_duplicates(['time'], keep='first').reset_index(drop=True)
#     type_mon=a2.groupby(by=['mon'])['snow'].sum()
#     type_mon1=type_mon.reset_index() 
#     type_mon1.set_index('mon', inplace=True) 
#     snow0 = pd.concat([type_mon1,add_table],axis=1)
#     snow1 = snow0.sort_values(by='mon', ascending=True)
#     snow1.drop(['useless'],axis=1,inplace=True)
#     snow1.reset_index(inplace=True)
#     snow1.to_csv("F:\\f\\snow_sts_data\\RTC\\mon_Days"+\
#                  "_"+str(i)+".txt", index = False,sep=' ',na_rep=0) 


