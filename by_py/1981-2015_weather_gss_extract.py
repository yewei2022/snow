# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 10:13:50 2021

@author: Lenovo
"""
# 循环或者pandas挑出高原站点对应的天气信息均可以

#%%  # branch1 根据公共站号 读取2016前 weather里的降雪信息

# import os
# import pandas as pd
# #1 读取高原站号
# path_sta='F:\\snow_sts_data\\station_pick\\TP_sta_id_by2014.txt'
# sta=pd.read_table(path_sta, header=None, usecols = [0])
# # print(sta)
# sta1=sta[0].tolist()
# # print(sta1)
# # 2 读取weather文件
# path_in='F:\\snow_sts_data\\1981-2015\\raw_data\\weather\\'
# path_out='F:\\snow_sts_data\\1981-2015\\weather_snow\\'
# f_list = os.listdir(path_in)  # 得到文件夹下的所有文件名称
# for file in f_list:
#     filename=path_in+file
#     # print(filename)
#     info=pd.read_table(filename,sep = "\t",header=None,\
#      	names=['station','yy','mm','dd','snow'],\
#      	usecols = [0,1,2,3,6])
#     df =info[info.station.isin(sta1)].reset_index(drop=True) 
#     df.to_csv(path_out+file,index = False,sep = "\t",\
#           columns = ['station','yy','mm','dd','snow'])
#     del df   
    
    
#%%  # branch2 根据公共站号 读取2016前 GSS信息

# import os
# import pandas as pd
# #1 读取高原站号
# path_sta='F:\\snow_sts_data\\station_pick\\TP_sta_id_by2014.txt'
# sta=pd.read_table(path_sta, header=None, usecols = [0])
# # print(sta)
# sta1=sta[0].tolist()
# # print(sta1)
# # 2 读取gss文件
# path_file='F:\\snow_sts_data\\1981-2015\\raw_data\\GSS\\'
# path_save='F:\\snow_sts_data\\1981-2015\\GSS_snow\\'
# f_list = os.listdir(path_file)  # 得到文件夹下的所有文件名称
# for file in f_list:
#  	filename=path_file+file
#  	# print(filename)
#  	info=pd.read_table(filename,sep = "\s+",header=None,\
#  	  names=['station','yy','mm','dd','gss','Q'],\
#  	  usecols = [0,4,5,6,7,9])
#  	# print(info)
#  	frame=[]
#  	#法一
#  	#  for i in sta1:
#  	#      ii=str(i)
#  	#      print(ii)
#  	#      frame.append(info.loc[info['station'] == ii, ['station',\
#  	  # 'yy','mm','dd','snow']])

#  	#法二 
#  	dd =info[info.station.isin(sta1)]
#  	frame.append(dd)
#     # 两种方法都可以

#  	df = pd.concat(frame,ignore_index=True)
#  	# print(df)
#  	df.to_csv(path_save+file,index = False,sep = "\t",\
# 		  columns = ['station','yy','mm','dd','gss','Q'])
#  	del df  