# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 10:23:29 2021
# 根据直接降水确定风暴影响半径
注意path1_save和path2_save的文件夹里2000年以前是BJT，2000以后则是UTC
@author: Lenovo
"""

import os
import pandas as pd

pic_dir="F:\\snow_related\\pic\\tc\\"


# path_file ='F:\\snow_sts_data\\zj\\after2000\\xiaoting\\'
# path1_save="F:\\snow_sts_data\\zj\\after2000\\deal\\"
# path2_save="F:\\snow_sts_data\\zj\\after2000\\dist_all\\"
# path_tc="F:\\snow_sts_data\\TC\\BoB_ymdh_utc_lon_lat.txt"

path_file ='F:\\snow_sts_data\\zj\\before2000\\xiaoting\\'
path1_save="F:\\snow_sts_data\\zj\\before2000\\deal\\"
path2_save="F:\\snow_sts_data\\zj\\before2000\\dist_all\\"
path_tc="F:\\snow_sts_data\\TC\\BoB_ymdh_bjt_lon_lat.txt"

#%% 处理降水数据时间
# # step1 将2000年以后的降水数据时间转换为UTC
# import datetime 
# f_list1 = os.listdir(path_file)
# for file in f_list1:
#     info=pd.read_table(path_file+file,sep = "\s+",encoding='gbk',
#                         header=None,names=['station','lon','lat'],
#                         usecols=[0,1,2])
#     time0='20'+file[0:8]
#     time1= datetime.datetime.strptime(time0, '%Y%m%d%H') #字符串变时间
#     time2=time1-datetime.timedelta(hours=32) #往前32h,to prep start UTC
#     time3=time2.strftime('%Y%m%d%H')[0:8]
#     info['time'] = time3 #时间变字符串,并提取年月日
#     info.to_csv(path1_save+time3+'.txt',index = False,sep='\t',
#               columns=['station','lon','lat','time'])

# # step2 将2000年以前的文件名改成yyyymmdd
# f_list1 = os.listdir(path_file)
# for file in f_list1:
#     info=pd.read_table(path_file+file,sep = "\s+",encoding='gbk',
#                         header=None,names=['station','lon','lat'],
#                         usecols=[0,1,2])
#     time0=file[3:11]
#     info['time'] = time0 #时间变字符串,并提取年月日
#     info.to_csv(path1_save+time0+'.txt',index = False,sep='\t',
#               columns=['station','lon','lat','time'])
    
#%% 计算风暴影响半径，2000以后UTC，2000以前BJT
# from math import sin,radians,cos,asin,sqrt
# import numpy as np

# def SphereDistance(lon1, lat1, lon2, lat2):
#     radius = 6371.0 # radius of Earth, unit:KM
#     # degree to radians
#     lon1, lat1,lon2, lat2 = map(radians,[lon1, lat1,lon2, lat2])
#     dlon = lon2 -lon1
#     dlat = lat2 -lat1
#     arg  = sin(dlat*0.5)**2 +  \
#             cos(lat1)*cos(lat2)*sin(dlon*0.5)**2
#     dist = 2.0 * radius * asin(sqrt(arg))
#     return dist

# # 函数：根据站点经纬度，时间，返回当天各个时次距离的平均值
# def ave_dist(station,sta_time,sta_lat,sta_lon,path_tc):
#     tc_save = [] #保存影响时刻的台风信息
#     dist_info=[] #保存各影响时刻的距离
#     tc_info =pd.read_table(path_tc,sep = "\t")
#     tc_id=tc_info['tc_id'].tolist()
#     yyyymmddhh=tc_info['bjt'].tolist()
#     lat_tc=tc_info['lat_tc'].tolist()
#     lon_tc=tc_info['lon_tc'].tolist()
#     N=len(lon_tc)
#     newLine = ['station','sta_lat','sta_lon','tc_id', 'time', 
#                 'tc_lat', 'tc_lon']
#     for i in range(0,N):
#         if str(yyyymmddhh[i])[0:8]==sta_time:
#             dist_tc2sta = SphereDistance(lon_tc[i],lat_tc[i],sta_lon,sta_lat)                    
#             newLine[0] = station
#             newLine[1] = sta_lat
#             newLine[2] = sta_lon                
#             newLine[3] = tc_id[i]
#             newLine[4] = str(yyyymmddhh[i])
#             newLine[5] = lat_tc[i]
#             newLine[6] = lon_tc[i]
#             # print(newLine)
#             if newLine not in tc_save:
#                 tc_save.append(newLine)
#                 dist_info.append(dist_tc2sta)
#     if len(tc_save)>0:
#         dist_ave=np.mean(dist_info)
#         print(tc_save)
#         print(dist_info)
#         print(dist_ave)
#     else:
#         dist_ave=-9999.
#         print(str(station)+'在'+str(sta_time)+'期间无风暴记录！')
#     return dist_ave

# # test one statino
# # station = '55960' 
# # sta_lat = 27.98
# # sta_lon = 91.95
# # sta_time='20001027'
# # ave_dist(station,sta_time,sta_lat,sta_lon,tc_list)

# file_list=os.listdir(path1_save)
# for file in file_list:
#     info=pd.read_table(path1_save+file,sep = "\t",encoding='gbk')
#     station=info['station'].tolist()
#     sta_lat=info['lat'].tolist()
#     sta_lon=info['lon'].tolist()
#     sta_time=info['time'].tolist()
#     npts=len(station)
#     dist_list=[]
#     for i in range(0,npts):
#         dist_list.append(ave_dist(station[i],str(sta_time[i]),sta_lat[i],
#                                   sta_lon[i],path_tc))
#     info['dist']=dist_list
#     info.to_csv(path2_save+file,sep='\t',index=False)
#     del info

#%%  step3 分别读取两段时期的影响半径
path_dist1="F:\\snow_sts_data\\zj\\before2000\\dist_all\\"
path_dist2="F:\\snow_sts_data\\zj\\after2000\\dist_all\\"

dist_list1=os.listdir(path_dist1)
info1=[]
for file in dist_list1:
    info1.append(pd.read_table(path_dist1+file,sep = "\t",encoding='utf-8',
                              na_values=-9999.))
df1           = pd.concat(info1,ignore_index=True)
dist_list2=os.listdir(path_dist2)
info2=[]
for file in dist_list2:
    info2.append(pd.read_table(path_dist2+file,sep = "\t",encoding='utf-8',
                              na_values=-9999.))
df2          = pd.concat(info2,ignore_index=True)
df           = pd.concat([df1,df2],ignore_index=True)

ave_dist      =df['dist'].mean() 
path_sta     ='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
tp_sta_info  =pd.read_table(path_sta,sep = ",")
df_tp        =df[df.station.isin(tp_sta_info['station'])].reset_index(drop=True)
ave_dist_tp  =df_tp['dist'].mean()
print('所有站点计算出的平均风暴影响半径:',ave_dist)
print('高原站点计算出的平均风暴影响半径:',ave_dist_tp)


# 没啥用
# # tp_500 = df_tp[df_tp['dist']<=500].shape[0]
# # tp_500_1000 = df_tp[(df_tp['dist']<=1000) & (df_tp['dist']>500)].shape[0]
# # tp_1000_1500 = df_tp[(df_tp['dist']<=1500) & (df_tp['dist']>1000)].shape[0]
# # tp_1500_2000 = df_tp[(df_tp['dist']<=2000) & (df_tp['dist']>1500)].shape[0]
# # tp_2000_2500 = df_tp[(df_tp['dist']<=2500) & (df_tp['dist']>2000)].shape[0]
# # tp_2500 = df_tp[df_tp['dist']>2500].shape[0]

#%% 绘图  概率密度图
from scipy import stats, integrate
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style('white')
# 图表风格设置
# 风格选择包括："white", "dark", "whitegrid", "darkgrid", "ticks"
plt.figure(figsize=(6,4))#绘制画布
sns.distplot(df_tp['dist'],hist = False,kde = True,rug = True,
              rug_kws = {'color':'goldenrod','lw':0.05,'alpha':0.5,'height':0.1} ,
              # 设置数据频率分布颜色#控制是否显示观测的小细条（边际毛毯）
              kde_kws={"color": 'goldenrod', "lw": 1.5, 'linestyle':'--'},
              # 设置密度曲线颜色，线宽，标注、线形，#控制是否显示核密度估计图
              label = 'TP station distance')
sns.distplot(df['dist'],hist = False,kde = True,rug = True,
              rug_kws = {'color':'g','lw':0.05,'alpha':0.5,'height':0.03} , 
              kde_kws={"color": 'g', "lw": 1.5, 'linestyle':'--'},
              label = 'All station distance')
plt.axvline(ave_dist_tp,color='goldenrod',linestyle=":",alpha=0.8) 
plt.text(ave_dist_tp+2,0.0005,'TP_sta_mean: %.0fkm' % (ave_dist_tp), color = 'goldenrod')

plt.axvline(ave_dist,color='g',linestyle=":",alpha=0.8)
plt.text(ave_dist+2,0.0004,'All_sta_mean: %.0fkm' % (ave_dist), color = 'g')

plt.ylim([0,0.0009]) #设置坐标上下限
# plt.xlim([-500,5500]) #设置坐标上下限
plt.xlabel('Distance (km)',fontsize=12)
plt.ylabel('Density',fontsize=12)
plt.grid(linestyle = '--')     # 添加网格线
plt.title("Distance between TCs and stations")  # 添加图表名
pic_dir="F:\\snow_related\\pic\\tc\\"
plt.savefig(pic_dir+'prebyxiaoting.jpg', dpi=750, bbox_inches = 'tight')

# # xx=pd.concat([df_tp['dist'],df['dist']],axis=1,keys=['TP station','All station'])
# # sns.ecdfplot(data=xx)

#%% 计算百分位数 
# cum_tp=df_tp['dist'].quantile([0,0.25,0.5,0.75,0.8,0.9,0.95,1])    #分位数
# cum_all=df['dist'].quantile([0,0.25,0.5,0.75,0.8,0.9,0.95,1])    

#%% 绘图  箱线图

# import seaborn as sns
# import matplotlib.pyplot as plt
# from matplotlib.pyplot import MultipleLocator

# plt.figure(figsize=(5,4))#绘制画布
# sns.set_style('ticks')
# # # 风格设置，选择包括："white", "dark", "whitegrid", "darkgrid", "ticks"
# data = pd.DataFrame({"All stations": df['dist'], "TP stations": df_tp['dist']}) 
# sns.boxplot(data=data,width=0.4,saturation=0.8,fliersize=1.5,
#             capprops=dict(color='red',linewidth=1.0))


# plt.yticks(range(0,5050,500))
# #whis默认值为whis=1.5,
# #IQR(Inter-Quartile Range)=Q3-Q1
# #上限为数列中不超过Q3+1.5*IQR的最大值，下限为数列中不小于Q1-1.5*IQR的最小值
# plt.ylabel("Distance (km)") 
# # plt.xlabel("xlabel") # 我们设置横纵坐标的标题
# y_minor_locator=MultipleLocator(100)
# ax = plt.gca()#获取边框
# ax.yaxis.set_minor_locator(y_minor_locator)
# ax.spines['top'].set_color('black')  
# ax.spines['bottom'].set_color('black')  
# ax.spines['left'].set_color('black')  
# ax.spines['right'].set_color('black')  
# plt.savefig(pic_dir+'box_prebyxiaoting.jpg', dpi=750, bbox_inches = 'tight')
# plt.show() #先保存才能plot.show


