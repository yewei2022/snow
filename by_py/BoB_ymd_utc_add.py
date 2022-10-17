# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 19:17:14 2021

@author: Lenovo
"""

#读取BOB年月日信息，每个个例后面再加一天,存储
import os
import datetime
import pandas as pd

# test time
# time1 = datetime.datetime.strptime('2018010106', '%Y%m%d%H') #字符串变时间
# # print(time1)
# time=time1+datetime.timedelta(days=1)
# time_str=time.strftime('%Y%m%d%H') #时间变字符串
# print(time_str)

#%% step 1  读time，tc_id
utc = []
tc_id   = []
path='F:\\snow_sts_data\\BOB\\'
f_list = os.listdir(path)  # 得到文件夹下的所有文件名称
#print(len(f_list))

for file in f_list:
    filename1=path+file
    #print(filename1)
    with open(filename1, 'r', encoding='UTF-8') as f1:
        lines = f1.readlines()  # 按行给lines
        s0=len(lines)
        s=s0-1
        i=0
        for line in lines:
            data=line.split(',')
            utc.append(data[2].strip()[0:8])
            tc_id.append(file[3:9])
            # tc_id.append(data[2].strip()[0:4]+data[1].strip())
            if i==s:
                utc0=data[2].strip()
                print(utc0)
                utc1= datetime.datetime.strptime(utc0, '%Y%m%d%H') #字符串变时间
                utc2=utc1+datetime.timedelta(days=1) #往后一天
                utc_end=utc2.strftime('%Y%m%d%H') #时间变字符串
                print(utc_end)
                utc.append(utc_end[0:8])
                tc_id.append(file[3:9])
            i=i+1
            
#%%  step 2   写入文件
tc_ymd_frame=pd.DataFrame(zip(tc_id,utc),columns=['tc_id','utc'])
# 去重
tc_ymd_info=tc_ymd_frame.drop_duplicates(["utc","tc_id"], 
                                         keep='first').reset_index(drop=True)
tc_ymd_info.to_csv("F:\\snow_sts_data\\TC\\BoB_ymd_utc_add.txt",index = False,
           sep=' ',encoding = "utf-8")
        