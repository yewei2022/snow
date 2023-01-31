# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 19:17:14 2021
#读取BOBTC 位置 风速 RMW 35kt风圈半径 ，转换成BJT，存储
@author: Lenovo
"""


import os
import datetime
import pandas as pd

# test time
# time1 = datetime.datetime.strptime('2018010106', '%Y%m%d%H') #字符串变时间
# # print(time1)
# time=time1+datetime.timedelta(days=1)
# time_str=time.strftime('%Y%m%d%H') #时间变字符串
# print(time_str)

date_infl=pd.read_csv("F:\\snow_sts_data\\1981-2020\\snow_date.txt",sep="\s+")

#%% 法一 pandas 读取 把缺测一起读 
#1 提取数据
info1=[]
path='F:\\snow_sts_data\\BOB2001\\'
f_list = os.listdir(path)  # 得到文件夹下的所有文件名称
#print(len(f_list))
for file in f_list:
    tc_id=file[3:9]
    filename1=path+file
    #print(filename1)
    info=pd.read_table(filename1,sep = ",",header=None,
    names=['tc_id','utc','lat_tc','lon_tc','Vmax','RAD','WINDCODE','RAD1',
           'RAD2','RAD3','RAD4','RADP','RRP','MRD'],
     	usecols = [1,2,6,7,8,11,12,13,14,15,16,17,18,19])
    info.loc[:,'tc_id'] =tc_id
    info1.append(info)
info2=pd.concat(info1,ignore_index=True)

info2.loc[:,'lat_tc'] =info2['lat_tc'].apply(lambda x: float(x[0:4].strip())*0.1)
info2.loc[:,'lon_tc'] =info2['lon_tc'].apply(lambda x: float(x[0:5].strip())*0.1)

#2 UTC变成BJT

info2.loc[:,'utc'] = pd.to_datetime(info2['utc'].astype(str),format='%Y%m%d%H')
info2['bjt'] = info2['utc'] + pd.Timedelta(hours=8)
info2['bjt'] = info2['bjt'].dt.strftime('%Y%m%d%H')
info2.drop(['utc'],axis=1,inplace=True)
tc_info=info2.drop_duplicates(["tc_id","bjt","lon_tc","lat_tc"], 
                                          keep='first').reset_index(drop=True)
tc_info1 = tc_info.loc[:, ['tc_id','bjt','lat_tc','lon_tc','Vmax','RAD',
                           'WINDCODE','RAD1','RAD2','RAD3','RAD4','RADP',
                           'RRP','MRD']]



#%% 法二 按行读   但是有些列没有'RADP','RRP','MRD'就没法读

#1 读数据

# utc = [] #第3列
# tc_id   = []
# lat_tc=[] #第7列
# lon_tc=[] #第8列
# Vmax=[] #第9列
# R = [] #保存影响时刻的台风信息
# # RAD,WINDCODE,RAD1,RAD2,RAD3,RAD4,RADP,RRP,MRD=([] for i in range(9))  
# # #第12/13/14/15/16/17/18/19/20列  共9列
# # RADP,RRP,MRD另外做，因为很多样本都没有

# path='F:\\snow_sts_data\\BOB2001\\'
# f_list = os.listdir(path)  # 得到文件夹下的所有文件名称
# #print(len(f_list))

# for file in f_list:
#     filename1=path+file
#     #print(filename1)
#     with open(filename1, 'r', encoding='UTF-8') as f1:
#         lines = f1.readlines()  # 按行给lines
#         for line in lines:
#             data=line.split(',')
#             tc_id.append(file[3:9])
#             utc.append(data[2].strip())
#             # tc_id.append(data[2].strip()[0:4]+data[1].strip())
#             lat_tc.append(float(data[6][0:4].strip())*0.1) #unit 1.0 degree
#             lon_tc.append(float(data[7][0:5].strip())*0.1)
#             Vmax.append(data[8].strip())
#             newLine = ['RAD','WINDCODE','RAD1','RAD2','RAD3','RAD4']
#             for i in range(11,17):
#                 ii=i-11
#                 newLine[ii] = data[i].strip()
#             R.append(newLine)
# R_df=pd.DataFrame(R)#利用series生成dataframe
# R_df.columns=['RAD','WINDCODE','RAD1','RAD2','RAD3','RAD4']


#2  transforms UTC into BJT

# bjt=[]
# for i in utc:
#     time1= datetime.datetime.strptime(i, '%Y%m%d%H') #字符串变时间
#     time2=time1+datetime.timedelta(hours=8) #往后8h
#     bjt.append(time2.strftime('%Y%m%d%H')) #时间变字符串

#3 组合数据

# tc_df=pd.DataFrame(zip(tc_id,bjt,lat_tc,lon_tc,Vmax),columns=['tc_id',
#                     'bjt','lat_tc','lon_tc','Vmax'])#利用series生成dataframe
# tc_R=pd.concat([tc_df,R_df],axis=1)
# tc_info=tc_R.drop_duplicates(["tc_id","bjt","lon_tc","lat_tc"], 
#                                          keep='first').reset_index(drop=True)
                

    
#%% 尺度统计 R34 34kt风圈半径 

# r34=tc_info1[tc_info1['RAD']==34]
# #筛选全为有效记录的数据
# # r34_all=r34.drop(r34[(r34['RAD1']==0)|(r34['RAD2']==0)|(r34['RAD3']==0)|
# #                (r34['RAD4']==0)].index).loc[:,['tc_id','bjt','lat_tc',
# #                         'lon_tc','RAD','WINDCODE','RAD1','RAD2','RAD3','RAD4']]

# #筛选有用记录数大于2的数据                                               
# r34.loc[:,['RAD1','RAD2','RAD3','RAD4']]=r34[['RAD1','RAD2','RAD3',
#                                               'RAD4']].replace(0,None) #替换特定值
# r34.loc[:,'nan_count']=r34[['RAD1','RAD2','RAD3','RAD4']].isnull().sum(axis=1)
# r34_all=r34.drop(r34[r34['nan_count']>2].index).loc[:,['tc_id','bjt','lat_tc',
#                         'lon_tc','RAD','WINDCODE','RAD1','RAD2','RAD3','RAD4']]
                                             
# r34_all.loc[:,'r34_ave']=r34_all.loc[:,['RAD1','RAD2','RAD3',
#                                         'RAD4']].mean(axis=1)*1.852

# def tc_r34(x):    
#     if x['r34_ave']<50: 
#         return "1"
#     elif (50<=x['r34_ave']<100):
#         return "2"
#     elif (100<=x['r34_ave']<150):
#         return "3"   
#     elif(150<=x['r34_ave']<200):
#         return "4"
#     elif(200<=x['r34_ave']<250):
#         return "5"
#     else:
#         return "6"
# r34_all.loc[:, 'r34_level']=r34_all.apply(tc_r34, axis=1) 

# r34_all['day']=r34_all['bjt'].astype(str).str[0:8]
# r34_infl=r34_all[r34_all.day.isin(date_infl.time.astype(str))]


# r34_all_ave=r34_all['r34_ave'].mean() 
# r34_infl_ave=r34_infl['r34_ave'].mean() 

# r34_all.loc[:,'count_all']=1
# r34_infl.loc[:,'count_infl']=1

# r34_all_freq=r34_all.groupby(by=['r34_level'])['count_all'].sum() 
# r34_infl_freq=r34_infl.groupby(by=['r34_level'])['count_infl'].sum() 
# r34_freq = pd.concat([r34_all_freq,r34_infl_freq],axis=1)
# r34_freq1=r34_freq.reset_index()
# r34_freq1.loc[:,'per_all']=r34_freq1['count_all']/len(r34_all)
# r34_freq1.loc[:,'per_infl']=r34_freq1['count_infl']/len(r34_infl)

# r34_freq1['count_all'] =r34_freq1['count_all'].apply(lambda x: format(x, '.0f'))
# r34_freq1['count_infl'] =r34_freq1['count_infl'].apply(lambda x: format(x, '.0f'))
# r34_freq1.to_csv("F:\\snow_sts_data\\TC\\TC_r34_freq.txt",index = False,
#                 na_rep=32700,sep=' ')



#%% 尺度统计 RRP 最外围闭合等压线半径 

# rrp_all=tc_info1[(tc_info1['RRP'].notna())&(tc_info1['RRP']!=0)].loc[:,
#                                 ['tc_id','bjt','lat_tc','lon_tc','RRP']]
# rrp_all['RRP_km']=rrp_all['RRP']*1.852

# def tc_rrp(x):    
#     if x['RRP_km']<100: 
#         return "1"
#     elif (100<=x['RRP_km']<200):
#         return "2"
#     elif (200<=x['RRP_km']<300):
#         return "3"   
#     elif(300<=x['RRP_km']<400):
#         return "4"
#     elif(400<=x['RRP_km']<500):
#         return "5"     
#     else:
#         return "6"
# rrp_all.loc[:, 'rrp_level']=rrp_all.apply(tc_rrp, axis=1) 

# rrp_all['day']=rrp_all['bjt'].astype(str).str[0:8]
# rrp_infl=rrp_all[rrp_all.day.isin(date_infl.time.astype(str))]

# rrp_all_ave=rrp_all['RRP_km'].mean() 
# rrp_infl_ave=rrp_infl['RRP_km'].mean() 

# rrp_all.loc[:,'count_all']=1
# rrp_infl.loc[:,'count_infl']=1

# rrp_all_freq=rrp_all.groupby(by=['rrp_level'])['count_all'].sum() 
# rrp_infl_freq=rrp_infl.groupby(by=['rrp_level'])['count_infl'].sum() 

# rrp_freq = pd.concat([rrp_all_freq,rrp_infl_freq],axis=1)
# rrp_freq1=rrp_freq.reset_index()
# rrp_freq1.loc[:,'per_all']=rrp_freq1['count_all']/len(rrp_all)
# rrp_freq1.loc[:,'per_infl']=rrp_freq1['count_infl']/len(rrp_infl)

# rrp_freq1['count_all'] =rrp_freq1['count_all'].apply(lambda x: format(x, '.0f'))
# rrp_freq1['count_infl'] =rrp_freq1['count_infl'].apply(lambda x: format(x, '.0f'))
# rrp_freq1.to_csv("F:\\snow_sts_data\\TC\\TC_rrp_freq.txt",index = False,
#                  na_rep=32700,sep=' ')


#%% 尺度统计 RMW 

# rmw_all=tc_info1[(tc_info1['MRD'].notna())&(tc_info1['MRD']!=0)]
# rmw_all.loc[:,'MRD']=rmw_all['MRD']*1.852

# rmw_all['day']=rmw_all['bjt'].astype(str).str[0:8]
# rmw_infl=rmw_all[rmw_all.day.isin(date_infl.time.astype(str))]

# def tc_rmw(x):    
#     if x['MRD']<30: 
#         return "1"
#     elif (30<=x['MRD']<60):
#         return "2"
#     elif (60<=x['MRD']<90):
#         return "3"   
#     elif(90<=x['MRD']<120):
#         return "4"    
#     else:
#         return "5"
# rmw_all.loc[:, 'rmw_level']=rmw_all.apply(tc_rmw, axis=1) 

# rmw_all['day']=rmw_all['bjt'].astype(str).str[0:8]
# rmw_infl=rmw_all[rmw_all.day.isin(date_infl.time.astype(str))]

# rmw_all_ave=rmw_all['MRD'].mean() 
# rmw_infl_ave=rmw_infl['MRD'].mean() 

# rmw_all.loc[:,'count_all']=1
# rmw_infl.loc[:,'count_infl']=1

# rmw_all_freq=rmw_all.groupby(by=['rmw_level'])['count_all'].sum() 
# rmw_infl_freq=rmw_infl.groupby(by=['rmw_level'])['count_infl'].sum() 
# rmw_freq = pd.concat([rmw_all_freq,rmw_infl_freq],axis=1)
# rmw_freq1=rmw_freq.reset_index()
# rmw_freq1.loc[:,'per_all']=rmw_freq1['count_all']/len(rmw_all)
# rmw_freq1.loc[:,'per_infl']=rmw_freq1['count_infl']/len(rmw_infl)

# rmw_freq1['count_all'] =rmw_freq1['count_all'].apply(lambda x: format(x, '.0f'))
# rmw_freq1['count_infl'] =rmw_freq1['count_infl'].apply(lambda x: format(x, '.0f'))

# rmw_freq1.to_csv("F:\\snow_sts_data\\TC\\TC_rmw_freq.txt",index = False,
#                   na_rep=32700,sep=' ')


#%% 尺度统计 丰满度 不太合适

# r17=tc_info1[tc_info1['RAD']==34]
# r17.loc[:,['RAD1','RAD2','RAD3','RAD4']]=r17[['RAD1','RAD2','RAD3',
#                                               'RAD4']].replace(0,None) #替换特定值
# r17.loc[:,'nan_count']=r17[['RAD1','RAD2','RAD3','RAD4']].isnull().sum(axis=1)
# r17_all=r17.drop(r17[r17['nan_count']>2].index)
# r17_all.loc[:,'r17_ave']=r17_all.loc[:,['RAD1','RAD2','RAD3',
#                                         'RAD4']].mean(axis=1)                                             
                                        
# r17_rmw_all=r17_all[(r17_all['MRD'].notna())&(r17_all['MRD']!=0)]

# r17_rmw_all['tcf']=1-r17_rmw_all['MRD']*1.0/r17_rmw_all['r17_ave']

# r17_rmw_all['day']=rrp_all['bjt'].astype(str).str[0:8]
# r17_rmw_infl=r17_rmw_all[r17_rmw_all.day.isin(date_infl.time.astype(str))]


#%% 结构统计 alpha theta

import numpy as np
import math

alpha=tc_info1[tc_info1['RAD']==34]
alpha['day']=alpha['bjt'].astype(str).str[0:8]

#筛选全为有效记录的数据
alpha_all=alpha.drop(alpha[(alpha['RAD1']==0)|(alpha['RAD2']==0)|(alpha['RAD3']==0)|
                (alpha['RAD4']==0)].index).loc[:,['tc_id','bjt','day','lat_tc',
                        'lon_tc','RAD','WINDCODE','RAD1','RAD2','RAD3','RAD4']]
alpha_all.loc[:,"alpha_base"] =np.power(alpha_all['RAD1']-alpha_all['RAD3'],2)+\
        np.power(alpha_all['RAD2']-alpha_all['RAD4'],2) 
alpha_all.loc[:,"alpha"]=alpha_all.apply(lambda x: 1.852*0.5*\
                                      np.sqrt(x["alpha_base"]), axis=1)
alpha_infl=alpha_all[alpha_all.day.isin(date_infl.time.astype(str))]

#筛选alpha不为0的样本
theta_alpha_all=alpha_all[alpha_all["alpha"]!=0]
theta_alpha_all.loc[:,"delta_y"]=theta_alpha_all['RAD1']-theta_alpha_all['RAD2']\
                -theta_alpha_all['RAD3']+theta_alpha_all['RAD4']
theta_alpha_all.loc[:,"delta_x"]=theta_alpha_all['RAD1']+theta_alpha_all['RAD2']\
    -theta_alpha_all['RAD3']-theta_alpha_all['RAD4']
theta_alpha_all.loc[:,"theta_base"]=theta_alpha_all.apply(lambda x: math.atan2(x["delta_y"],
                                                    x["delta_x"]), axis=1)
theta_alpha_all.loc[:,"theta"]=theta_alpha_all.apply(lambda x: x["theta_base"]/math.pi*180,
                                          axis=1)
# 分档
def tc_alpha(x):    
    if x['alpha']<20: 
        return "1"
    elif (20<=x['alpha']<40):
        return "2"
    elif (40<=x['alpha']<60):
        return "3"
    elif (60<=x['alpha']<80):
        return "4"   
    elif(80<=x['alpha']<100):
        return "5"    
    else:
        return "6"
theta_alpha_all.loc[:, 'alpha_level']=theta_alpha_all.apply(tc_alpha, axis=1) 

def tc_theta(x):    
    if x['theta']==0: 
        return "1E"
    elif (0<=x['theta']<90):
        return "2NE"
    elif (x['theta']==90):
        return "3N"
    elif (90<=x['theta']<180):
        return "4NW"
    elif (x['theta']==180):
        return "5W"   
    elif(-180<x['theta']<-90):
        return "6SW"
    elif (x['theta']==-90):
        return "7S"
    elif(-90<x['theta']<0):
        return "8SE"  
theta_alpha_all.loc[:, 'theta_level']=theta_alpha_all.apply(tc_theta, axis=1) 

theta_alpha_infl=theta_alpha_all[theta_alpha_all.day.isin(date_infl.time.astype(str))]
print('所有样本α=0的样本数: \n{}'.format(len(alpha_all[alpha_all["alpha"]==0])))
print('影响期间样本α=0的样本数: \n{}'.format(len(alpha_infl[alpha_infl["alpha"]==0])))


#%%  统计alpha不等于0的alpha样本

alpha_all_ave=theta_alpha_all['alpha'].mean() 
alpha_infl_ave=theta_alpha_infl['alpha'].mean() 

theta_alpha_all.loc[:,'count_all']=1
theta_alpha_infl.loc[:,'count_infl']=1

alpha_all_freq=theta_alpha_all.groupby(by=['alpha_level'])['count_all'].sum() 
alpha_infl_freq=theta_alpha_infl.groupby(by=['alpha_level'])['count_infl'].sum() 
alpha_freq = pd.concat([alpha_all_freq,alpha_infl_freq],axis=1)
alpha_freq1=alpha_freq.reset_index()
alpha_freq1.loc[:,'per_all']=alpha_freq1['count_all']/len(theta_alpha_all)
alpha_freq1.loc[:,'per_infl']=alpha_freq1['count_infl']/len(theta_alpha_infl)

alpha_freq1['count_all'] =alpha_freq1['count_all'].apply(lambda x: format(x, '.0f'))
alpha_freq1['count_infl'] =alpha_freq1['count_infl'].apply(lambda x: format(x, '.0f'))

# alpha_freq1.to_csv("F:\\snow_sts_data\\TC\\TC_alpha_freq.txt",index = False,
#                   na_rep=32700,sep=' ')


#%%  统计alpha不等于0的theta样本


# theta_alpha_all.loc[:,'count_all']=1
# theta_alpha_infl.loc[:,'count_infl']=1

# theta_all_freq=theta_alpha_all.groupby(by=['theta_level'])['count_all'].sum() 
# theta_infl_freq=theta_alpha_infl.groupby(by=['theta_level'])['count_infl'].sum() 
# theta_freq = pd.concat([theta_all_freq,theta_infl_freq],axis=1)
# theta_freq1=theta_freq.reset_index()
# theta_freq1.loc[:,'per_all']=theta_freq1['count_all']/len(theta_alpha_all)
# theta_freq1.loc[:,'per_infl']=theta_freq1['count_infl']/len(theta_alpha_infl)

# theta_freq1['count_all'] =theta_freq1['count_all'].apply(lambda x: format(x, '.0f'))
# theta_freq1['count_infl'] =theta_freq1['count_infl'].apply(lambda x: format(x, '.0f'))

# theta_freq1.to_csv("F:\\snow_sts_data\\TC\\TC_theta_freq.txt",index = False,
#                   na_rep=32700,sep=' ')
                                                
