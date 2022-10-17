# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 22:31:38 2021

分别找出1981-2015 2016-2020 天气现象 gss 文件中站号的并集
再取 1981-2015 2016-2020 站号的交集
@author: Lenovo
"""

#%% 1981-2015 两个文件夹下所有出现过的站号 用法一 逐行读取

# import os
# # import numpy as np
# sta = []
# # path='F:\\snow_sts_data\\1981-2015\\raw_data\\weather\\'
# # path1='F:\\snow_sts_data\\station_pick\\wea_sta_all.txt'

# path='F:\\snow_sts_data\\1981-2015\\raw_data\\GSS\\'
# path1='F:\\snow_sts_data\\station_pick\\GSS_sta_all.txt'

# f_list = os.listdir(path)  # 得到文件夹下的所有文件名称
# #print(len(f_list))
# #1 获取所有出现过的站号
# for file in f_list:
#     filename1=path+file
#     #print(filename1)
#     with open(filename1, 'r', encoding='UTF-8') as f1:
#         lines = f1.readlines()  # 按行给lines
#         for line in lines:
#             data=line.split()
#             #print(data)
#             if data[0] not in sta:
#                 sta.append(data[0])
                
# sta.sort()
# print(sta)
# print(len(sta))

# #2 写入文件
# with open(path1, 'w') as fw:
#     for i in range(len(sta)):
#         fw.write("%s \n" %(sta[i]))



#%% 将1981-2015 两个文件夹下的站号并集 取交集

# file1='F:\\snow_sts_data\\station_pick\\GSS_sta_all.txt'
# file2='F:\\snow_sts_data\\station_pick\\wea_sta_all.txt'

# sta1=[]
# with open(file1, 'r', encoding='UTF-8') as f1:
#     lines = f1.readlines()  # 按行给lines
#     for line in lines:
#         if line not in sta1:
#             sta1.append(line)
                
# sta2=[]
# with open(file2, 'r', encoding='UTF-8') as f2:
#     lines = f2.readlines()  # 按行给lines
#     for line in lines:
#         if line not in sta2:
#             sta2.append(line)

# sta = list(set(sta1).intersection(sta2)) # 求多个list的交集：a、b、c同时拥有的元素
# sta.sort()
# print(sta)
# print(len(sta))

# #2 写入文件
# path1='F:\\snow_sts_data\\station_pick\\sta_1981_2015.txt'

# with open(path1, 'w') as fw:
#     for i in range(len(sta)):
#         fw.write("%s" %(sta[i]))



#%% 2016-2020文件 所有出现过的站点信息 用法二 pandas

# import os
# import pandas as pd

# path='F:\\snow_sts_data\\micaps_diamond1_2016_2020\\data\\'

# # # #Test a single piece of data 
# # filename='H:\\micaps_diamond1_2015_2020\\datasets\\15010102.000'
# # info=pd.read_table(filename,sep = "\s+",header=None,
# #                     names=['station','lon','lat','alti'],skiprows=2,
# #                     encoding="gbk",usecols =[0,1,2,3])

# f_list = os.listdir(path)  # 得到文件夹下的所有文件名称
# # print(len(f_list))
# frame=[]
# for file in f_list:
#     filename=path+file
#     frame.append(pd.read_table(filename,sep = "\s+",header=None,
#                                 names=['station','lon','lat','alti'],skiprows=2,
#                                 encoding="gbk",usecols =[0,1,2,3]))
# df = pd.concat(frame,ignore_index=True)
# sta=df.drop_duplicates("station", keep='first').reset_index(drop=True)
# # print(df) df-原数据没有改变，所以需要sta保存，而df.duplicated() 被动改变原数据
# sta.to_csv("F:\\snow_sts_data\\station_pick\\sta_2016_2020.txt",index = False,
#             encoding = "utf-8")  
  
# # print(df[df['Station_Id_d'].duplicated(keep=False)]) #输出重复行



#%% # 16年前和16年后站号 取交集 将经纬度,海拔信息写入sta_info.txt

# import pandas as pd
# info_1981=pd.read_table('F:\\snow_sts_data\\station_pick\\sta_1981_2015.txt',
#                         header=None, usecols = [0])
# sta1_list=info_1981[0].tolist()

# info_2016=pd.read_table('F:\\snow_sts_data\\station_pick\\sta_2016_2020.txt',
#                     sep = ",", usecols = ['station','lon','lat','alti'])
# sta2_list=info_2016['station'].tolist()

# sta_common = list(set(sta1_list).intersection(sta2_list)) # 求多个list的交集：a、b、c同时拥有的元素
# sta_common.sort()
# print(sta_common)
# print(len(sta_common))
    
# frame=[]
# for i in sta_common:
#     # ii=str(i)
#     frame.append(info_2016.loc[info_2016['station'] == i, 
#                                ['station','lon','lat','alti']])
# df = pd.concat(frame,ignore_index=True)
# # print(len(df))
# df.to_csv("F:\\snow_sts_data\\station_pick\\sta_info.txt",index = False,
#           encoding = "utf-8")       


#%% # 将高原 的经纬度,海拔信息写入文本文件

# import pandas as pd
# path_sta='F:\\snow_sts_data\\station_pick\\TP_sta_id_by2014.txt' #by ncl
# sta=pd.read_table(path_sta, header=None, usecols = [0])
# # print(sta)
# sta1=sta[0].tolist()
# info=pd.read_table("F:\\snow_sts_data\\station_pick\\sta_info.txt",sep = ",",
#                     usecols = ['station','lon','lat','alti'])
# frame=[]
# for i in sta1:
#     # ii=str(i)
#     frame.append(info.loc[info['station'] == i, ['station','lon','lat','alti']])
# df = pd.concat(frame,ignore_index=True)

# # print(len(df))
# df.to_csv("F:\\snow_sts_data\\station_pick\\TP_sta_info_by2014.txt",
#           index = False,encoding = "utf-8")  