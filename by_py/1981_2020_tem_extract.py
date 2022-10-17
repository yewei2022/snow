# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 20:04:37 2021

@author: Lenovo
"""

# 读取40年高原日平均温度，重新存储
import pandas as pd
import numpy as np
import os


#%% step1 读取日平均温度分别将数据并另存

# # 读取高原站号
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",", usecols = ['station'])
# # print(sta)
# sta1=sta['station'].tolist()
# # print(sta1)

# cols=[0,4,5,6,7]
# colnames=["station","yy","mm","dd","dailytem"]
# # filename="SURF_CLI_CHN_MUL_DAY-PRE-13011-200810.TXT"
# path_info="H:\\1981-2020-daily-tem\\data\\"
# f_list = os.listdir(path_info)
# for file in f_list:
#     info=pd.read_table(path_info+file,sep = "\s+",header=None, names=colnames,
#                         na_values=32766,usecols=cols)
#     info_tp =info[info.station.isin(sta['station'])].reset_index(drop=True) 
#     # #add 0 before number
#     yy=info_tp['yy'].apply(lambda x : '{:0>4d}'.format(x))
#     mm=info_tp['mm'].apply(lambda x : '{:0>2d}'.format(x))
#     dd=info_tp['dd'].apply(lambda x : '{:0>2d}'.format(x))
#     time=yy+mm+dd
#     info_tp['time'] =time  # or info_tp.loc[:, 'time'] = time
#     info_tp.drop(columns = ['yy','mm','dd'],inplace = True)
#     info_tp['dailytem']=info_tp['dailytem']*0.1
#     # info_tp['dailypre'] = info_tp['dailypre'].apply(lambda x: format(x, '.1f'))
#     # 这里保留一位小数的话，na_rep命令无效 
#     info_tp.to_csv("F:\\snow_sts_data\\1981-2020-tem\\"+file[31:37]+".txt",
#               index = False,sep='\t',na_rep=32766)



#%% 组合为一个文件tem1981_2020.txt

# # # #读取tem变成dataframe 
# path_pre="F:\\snow_sts_data\\1981-2020-tem\\"
# f_list = os.listdir(path_pre)  
# info=[]
# for file in f_list:   
#     info.append(pd.read_table(path_pre+file,sep = "\t",na_values=32766))
# pre = pd.concat(info,ignore_index=True)

# pre.to_csv("F:\\snow_sts_data\\tem1981_2020.txt",index = False,
#                 sep=' ',na_rep=32700)
