# -*- coding: utf-8 -*-
"""
Spyder Editor
有中文该咋整看注释
主要读取20年的国家站和区域站的数据，最后生成dataframe。
This is a temporary script file.
"""
import pandas as pd
import numpy as np
import os
from pandas import DataFrame
from collections import Counter
import re
#Tibet=pd.read_csv('F:/data2015-2020/1.txt',sep='\s+')
seq = re.compile("\s+")#设置中间间隔标识为\s+
file=open('F:/data2015-2020/SURF_CHN_MUL_DAY-20150105.txt','r',encoding='utf-8')#编码有问题，主要有中文，在记事本右下角看编码格式加utf-8
result=list()
for c in file.readlines():
        c_array=seq.split(c.strip())
        result.append(c_array[0:69])#读取txt文件前几列的数据
Tibet=pd.read_csv('D:/data/test/20211203/tibet.csv')
file.close()
#%%
d=[]
for i in range(len(result)):
    d.append(result[i][2:-1])
c=d[0]
df = pd.DataFrame(d[1:-1][:], columns=c) 
#%%
     
tibet_list=list(Tibet.Station_Id)     
dd=df[df.Station_Id_C.isin(tibet_list)]
da=[]
da.append(dd)
data = pd.concat(da)
#%%
#data_array=np.full((len(Tibet),11), np.nan)#因为原数据中有字符串，所以没法直接读到数列里，所以该方法不行
table_name = ('Station','Lat','Lon','Alti','Year',\
        'Mon','Day','Tmax','Tmin','Pre','Ssh')
data_array0=pd.Series(data['Station_Id_C'])
cc=data['Station_Id_C']
data_array1=pd.Series(data['Lat'])
data_array2=pd.Series(data['Lon'])
data_array3=pd.Series(data['Alti'])
data_array4=pd.Series(data['Year'])
data_array5=pd.Series(data['Mon'])
data_array6=pd.Series(data['Day'])
data_array7=pd.Series(data['TEM_Max'])
data_array8=pd.Series(data['TEM_Min'])
data_array9=pd.Series(data['PRE_Time_2020'])
data_array10=pd.Series(data['SSH'])
data_table=pd.DataFrame(list(zip(data_array0,data_array1,data_array2,data_array3,data_array4,\
                                 data_array5,data_array6,data_array7,data_array8,\
                                     data_array9,data_array10)),columns=table_name)#利用series生成dataframe

    
    
'''
这些都是草稿    
#%%
d=[]
for i in range(len(result)):
    d.append(result[i][2:10])
c=d[0]
df = pd.DataFrame(d, columns=c) 
df.to_csv("D:/data/test/20211203/data2020.csv")













#%%
Tibet=pd.read_csv('F:/data2015-2020/SURF_CHN_MUL_DAY-20201211.txt',error_bad_lines=False,sep='\s+') 

#%%
data=[]
with open('F:/data2015-2020/SURF_CHN_MUL_DAY-20170311.txt', 'r',encoding='utf-8-sig') as f_input:
    for line in f_input:
        data.append(list(line.strip().split('\s+')))
dataset=pd.DataFrame(data)

#%%
Tibet=pd.read_csv('F:/data2015-2020/SURF_CHN_MUL_DAY-20170311.txt',sep='\s+') 
#cc=max(Tibet[''])

#%%
#tt=pd.read_csv('D:/data/SURF_CLI_CHN_MUL_DAY_V3.0/datasets/SSD/SURF_CLI_CHN_MUL_DAY-SSD-14032-201502.txt',encoding='gbk',skiprows=1,sep='\s+',header=None,names=['station','name','p','time','ssd']) 
Tibet=pd.read_csv('D:/data/SURF_CLI_CHN_MUL_DAY_V3.0/datasets/SSD/SURF_CLI_CHN_MUL_DAY-SSD-14032-201502.txt',skiprows=1,sep='\s+',header=None,names=['station','lat','lon','hb','y','ye','d','s','c']) 
#%%
b = []
b[0,:]
#%%
d=dict(Counter(tt['station']))
e=[key for key,value in d.items()]
f=set(c)^set(e)

low_memory=False,error_bad_lines=False
'''