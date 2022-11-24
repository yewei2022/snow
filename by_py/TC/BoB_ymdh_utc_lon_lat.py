# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 19:17:14 2021

@author: Lenovo
"""

#读取BOB年月日/经纬度，id等信息存储
# 计算影响降雪的TC的活动日数（不管是否造成降雪）
import os
import pandas as pd

# # test time
# # time1 = datetime.datetime.strptime('2018010106', '%Y%m%d%H') #字符串变时间
# # # print(time1)
# # time=time1+datetime.timedelta(days=1)
# # time_str=time.strftime('%Y%m%d%H') #时间变字符串
# # print(time_str)

#%% step 1  读time，tc_id
utc = []
tc_id   = []
lat_tc=[]
lon_tc=[]
wind=[]
path='F:\\snow_sts_data\\BOB\\'
f_list = os.listdir(path)  # 得到文件夹下的所有文件名称
#print(len(f_list))

for file in f_list:
    filename1=path+file
    #print(filename1)
    with open(filename1, 'r', encoding='UTF-8') as f1:
        lines = f1.readlines()  # 按行给lines
        for line in lines:
            data=line.split(',')
            tc_id.append(file[3:9])
            utc.append(data[2].strip())
            # tc_id.append(data[2].strip()[0:4]+data[1].strip())
            lat_tc.append(float(data[6][0:4].strip())*0.1) #unit 1.0 degree
            lon_tc.append(float(data[7][0:5].strip())*0.1)
            wind.append(data[8].strip())
    
#%%  step 2   写入文件
tc_ymd_frame=pd.DataFrame(zip(tc_id,utc,lon_tc,lat_tc,wind),
                          columns=['tc_id','utc','lon_tc','lat_tc','wind'])

tc_ymd_frame['lat_tc'] =tc_ymd_frame['lat_tc'].apply(lambda x: format(x, '.1f'))
tc_ymd_frame['lon_tc'] =tc_ymd_frame['lon_tc'].apply(lambda x: format(x, '.1f'))
# 去重 !这里必须要满足4个条件
tc_ymd_info=tc_ymd_frame.drop_duplicates(["utc","tc_id","lon_tc","lat_tc"], 
                                         keep='first').reset_index(drop=True)
tc_ymd_info.to_csv(r"F:\\snow_sts_data\\TC\\BoB_ymdh_utc_lon_lat.txt",index = False,
            sep='\t',encoding = "utf-8")
