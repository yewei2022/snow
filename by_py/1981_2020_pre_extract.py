# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 20:04:37 2021

@author: Lenovo
"""

# 读取40年高原日降水，重新存储
import pandas as pd
import numpy as np
import os


#%% 读取高原日降水分别将数据并另存

# # 读取高原站号
# path_sta="F:\\snow_sts_data\\station_pick\\TP_sta_id_by2014.txt"
# sta=pd.read_table(path_sta, header=None, usecols = [0])
# # print(sta)
# sta1=sta[0].tolist()
# # print(sta1)

# cols=[0,4,5,6,9]
# colnames=["station","yy","mm","dd","dailypre"]
# # filename="SURF_CLI_CHN_MUL_DAY-PRE-13011-200810.TXT"
# path_info="F:\\snow_sts_data\\1981-2020-dailypre-from-weina\\data\\"
# f_list = os.listdir(path_info) 
# for file in f_list:
#     info=pd.read_table(path_info+file,sep = "\s+",header=None, names=colnames,
#                         na_values=32766,usecols=cols)
#     # !!! 原始数据中32766是缺测
#     info_tp =info[info.station.isin(sta[0])].reset_index(drop=True) 
#     # #add 0 before number
#     yy=info_tp['yy'].apply(lambda x : '{:0>4d}'.format(x))
#     mm=info_tp['mm'].apply(lambda x : '{:0>2d}'.format(x))
#     dd=info_tp['dd'].apply(lambda x : '{:0>2d}'.format(x))
#     time=yy+mm+dd
#     info_tp['time'] =time  # or info_tp.loc[:, 'time'] = time
#     info_tp.drop(columns = ['yy','mm','dd'],inplace = True)
#     # !!! 原始数据中的32700代表微量
#     info_tp['dailypre']=info_tp['dailypre'].replace(32700,0) #将微量替换为0
#     info_tp['dailypre']=info_tp['dailypre']*0.1
#     # info_tp['dailypre'] = info_tp['dailypre'].apply(lambda x: format(x, '.1f'))
#     # 这里保留一位小数的话，na_rep命令无效 
#     info_tp.to_csv("F:\\snow_sts_data\\1981-2020-dailypre-TP\\"+file[31:37]+".txt",
#               index = False,sep='\t',na_rep=32766)



#%% 组合为一个文件pre1981_2020.txt

# # # #读取pre变成dataframe 
# path_pre="F:\\snow_sts_data\\1981-2020-dailypre-TP\\"
# f_list = os.listdir(path_pre)  
# info=[]
# for file in f_list:   
#     info.append(pd.read_table(path_pre+file,sep = "\t",na_values=32766))
# pre = pd.concat(info,ignore_index=True)

# pre.to_csv("F:\\snow_sts_data\\1981-2020\\pre1981_2020.txt",index = False,
#                 sep=' ',na_rep=32700)
