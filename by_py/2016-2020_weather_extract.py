# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 13:03:18 2021
提取2016-2020降雪天气信息 降水量 降雪量
其实这里的降水量和降雪量也用不上
0 无降水 1雨 2雪
@author: Lenovo

"""

import os
import pandas as pd

#  读取地面资料
path_in ='F:\\snow_sts_data\\2016-2020\\micaps_diamond1_2016_2020\\data\\'
path1_save="F:\\snow_sts_data\\2016-2020\\weather_snow\\out1\\"
path2_save="F:\\snow_sts_data\\2016-2020\\weather_snow\\out2\\"

#%% step1  读取高原站点 'station','time','w1','w2','6h_pre','ww','phase' 等信息

# # 读取高原站号
# path_sta='F:\\snow_sts_data\\station_pick\\TP_sta_id_by2014.txt'
# sta=pd.read_table(path_sta, header=None, usecols = [0])
# # print(sta)
# sta1=sta[0].tolist()
# # print(sta1)

# #1 rain; 2 snow; 0 no pre
# def get_phase(x):
#     if x['w1']==6 or x['w2']==6: 
#         return '1'
#     elif x['w1']==7 or x['w2']==7:
#         return '2'
#     elif (x['w1']==8 and 85<=x['ww']<=86)\
#         or (x['w2']==8 and 85<=x['ww']<=86):
#         return '2'
#     elif x['w1']==8 or ['w2']==8:
#         return '1'    
#     else:
#         return '0'
        
# f_list = os.listdir(path_in)  # 得到文件夹下的所有文件名称na_values='9999'
# for file in f_list:
#     hh=file[6:8]
#     if hh =='02' or hh =='08' or hh =='14' or hh =='20':
#         info=pd.read_table(path_in+file,sep = "\s+",encoding='gbk',
#                             header=None,skiprows=2,
#                             names=['station','w1','w2','6h_pre','ww'],
#                             usecols=[0,10,11,12,18])
#         info.loc[:, 'phase'] = info.apply(get_phase, axis=1) 
#         info['time'] = '20'+file[0:8]

#         dd =info[info.station.isin(sta1)] #法二 挑出高原站点 下三行不要也罢
#         frame=[] #要了也只是重置行索引的区别，不要上面直接重置行索引
#         frame.append(dd)
#         df = pd.concat(frame,ignore_index=True)

#         df.to_csv(path1_save+file,index = False,sep='\t',
#                   columns=['station','time','w1','w2','6h_pre','ww','phase'])
#         del df 


#%%  step2   进一步提取日值 以'time','snow','snow_f','snow_amt','pre_amt'保存
        
# f_list = os.listdir(path1_save)  # 得到文件夹下的所有文件名称 na_values='9999'

# f_frame=pd.DataFrame(f_list, columns=['filename']) 
# ymd=f_frame['filename'].astype(str).str[0:6] #年月日
# ymd_list=list(ymd)
# # print(type(ymd_list))
# for time in ymd_list:
#     info=[]    
#     for file in f_list:
#         file_ymd=file[0:6]
#         if file_ymd==time:
#             info.append(pd.read_table(path1_save+file,sep = "\t",encoding='gbk',
#                                       na_values='9999'))
#     df = pd.concat(info,ignore_index=True)
#     # dw=df.loc[df['station'] == 56312,['station','phase','6h_pre']]
    
#     df_pre_amt=df.groupby(by=['station'])['6h_pre'].sum() 
#     # refers to  https://www.cnpython.com/qa/83469
#     df_snow_f=df.groupby(by=['station']).apply(lambda x: sum(x['phase'] ==2))
#     # refers to https://www.cnblogs.com/lemonbit/p/6810972.html
    
#     df_snow_amt=df.groupby(by=['station']).\
#         apply(lambda x: x.loc[x['phase'] == 2,['6h_pre']].sum())
    
#     snow_frame=pd.concat([df_snow_f, df_snow_amt,df_pre_amt], axis=1,ignore_index=True)
#     def get_snow(x):
#         if x[0]>=1: 
#             return '1'
#         else:
#             return '0'
#     snow_frame.loc[:, 'snow'] = snow_frame.apply(get_snow, axis=1) 
#     snow_frame.loc[:, 'time'] = '20'+time 
#     snow_frame.columns = ['snow_f','snow_amt','pre_amt','snow','time'] #列标签
    
#     snow_frame.to_csv(path2_save+'20'+time+".txt",sep='\t',
#               columns = ['time','snow','snow_f','snow_amt','pre_amt'],na_rep='9999')
  

