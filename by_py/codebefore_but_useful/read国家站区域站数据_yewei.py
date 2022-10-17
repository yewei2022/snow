# -*- coding: utf-8 -*-
"""
用于更正读错的文件
"""
import pandas as pd
import numpy as np
import os
from pandas import DataFrame
from collections import Counter
import re
path_file='H:\\surf_day_data\\2016-2020\\datasets\\2017\\'
path_save="F:\\snow_statistics_data\\2016-2020\\snow\\test_out\\"
seq = re.compile("\s+")#设置中间间隔标识为\s+
f_list_abandon = os.listdir("F:\\snow_statistics_data\\2016-2020\\snow\\abandon\\")  
# f_list = os.listdir(path_file)  # 得到文件夹下的所有文件名称
for name in f_list_abandon:
    file=open(path_file+name,'r',encoding='utf-8')#编码有问题，主要有中文，在记事本右下角看编码格式加utf-8
    result=list()
    for c in file.readlines():
            c_array=seq.split(c.strip())
            result.append(c_array[0:114])#读取txt文件前几列的数据
    file.close()
    
    d=[]
    for i in range(len(result)):
        d.append(result[i][2:-1])
    c=d[0]
    df = pd.DataFrame(d[1:-1][:], columns=c) 
    
    # path_sta='F:\\snow_statistics_data\\TP_sta.txt'
    # Tibet=pd.read_table(path_sta,sep = "\n", header=None, usecols = [0])     
    # tibet_list=list(Tibet[0]) 
    # # print(tibet_list)    
    
    # frame=[]
    # for i in tibet_list:
    #     ii=str(i)
    #     # print(ii)
    #     frame.append(df.loc[df['Station_Id_C'] == ii, ['Station_Id_C',\
    #      	'Year','Mon','Day','Snow','Snow_Depth','Q_Snow','Q_Snow_Depth']])
               
    # data = pd.concat(frame)
    # # print(data)
    # data.to_csv(path_save+name,index = False,sep = "\t",\
    #  	columns = ['Station_Id_C',\
    #      	'Year','Mon','Day','Snow','Snow_Depth','Q_Snow','Q_Snow_Depth'])
    # del data