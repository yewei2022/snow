# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 10:23:29 2021
计算风暴影响半径
保存风暴影响降雪站点样本
降雪期间 极端降雪期间 距离的 概率密度图
@author: Lenovo
"""

import pandas as pd

path_save="F:\\snow_sts_data\\TC\\"
path_tc="F:\\snow_sts_data\\TC\\BoB_ymdh_bjt_lon_lat.txt"

    
#%% step 1 计算风暴影响半径

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
# def ave_dist(station,sta_time,sta_lat,sta_lon,sta_tc_id,path_tc):
#     tc_save = [] #保存影响时刻的台风信息
#     dist_info=[] #保存各影响时刻的距离
#     tc_info =pd.read_table(path_tc,sep = "\t")
#     tc_id=tc_info['tc_id'].tolist()
#     yyyymmddhh=tc_info['bjt'].tolist()
#     lat_tc=tc_info['lat_tc'].tolist()
#     lon_tc=tc_info['lon_tc'].tolist()
#     N=len(lon_tc)
#     for i in range(0,N):
#         newLine = ['station','sta_lat','sta_lon','tc_id', 'time', 
#                     'tc_lat', 'tc_lon']
#         if (str(yyyymmddhh[i])[0:8]==sta_time) & (tc_id[i]==sta_tc_id):
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
#         dist_ave=32700
#         print(str(station)+'在'+str(sta_time)+'期间无风暴记录！')
#     return dist_ave



#%% 挑选风暴影响降雪站点

# info=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_pre_gss.txt",sep='\s+',
#                     usecols=['station','time','lon','lat','tc_id'])
# station=info['station'].tolist()
# sta_lat=info['lat'].tolist()
# sta_lon=info['lon'].tolist()
# sta_time=info['time'].tolist()
# sta_tc_id=info['tc_id'].tolist()
# npts=len(station)
# dist_list=[]
# for i in range(0,npts):
#     dist_list.append(ave_dist(station[i],str(sta_time[i]),sta_lat[i],
#                               sta_lon[i],sta_tc_id[i],path_tc))
# info['dist']=dist_list
# info.to_csv(path_save+'tcdist_bysnow.txt',sep='\t',index=False,na_rep=32700)



#%% step 2 确定风暴半径平均值 分位数 

# df_tp   = pd.read_table(path_save+'tcdist_bysnow.txt',sep = "\t",na_values=32700)
# df_ave  = df_tp['dist'].mean() 
# print('风暴影响半径平均值:',df_ave)

# tp_500 = df_tp[df_tp['dist']<=500].shape[0]
# tp_500_1000 = df_tp[(df_tp['dist']<=1000) & (df_tp['dist']>500)].shape[0]
# tp_1000_1500 = df_tp[(df_tp['dist']<=1500) & (df_tp['dist']>1000)].shape[0]
# tp_1500_2000 = df_tp[(df_tp['dist']<=2000) & (df_tp['dist']>1500)].shape[0]
# tp_2000_2500 = df_tp[(df_tp['dist']<=2500) & (df_tp['dist']>2000)].shape[0]
# tp_2500 = df_tp[df_tp['dist']>2500].shape[0]
# cum_tp=df_tp['dist'].quantile([0,0.25,0.5,0.75,0.8,0.9,0.95,1])    #用df计算百分分位数
# df_dist_bysta=df_tp.groupby(by=['station'])['dist'].mean()  #平均值


#%% step 2.1 降雪期间 极端降雪期间 距离的 概率密度图

# import numpy as np
# # from scipy import stats, integrate
# import seaborn as sns
# import matplotlib.pyplot as plt

# # # 读数据
# df_tp1   = pd.read_table(path_save+'tcdist_bysnow.txt',sep = "\t",na_values=32700)
# df_ave1  = df_tp1['dist'].mean() 
# print('对高原降雪的影响距离:',df_ave1)
# # df_tp2   = pd.read_table(path_save+'tcdist_extrm.txt',sep = "\t",na_values=32700)
# # df_ave2      =df_tp2['dist'].mean() 
# # print('对极端降雪的影响距离:',df_ave2)

# sns.set_style('ticks')
# # 图表风格设置
# # 风格选择包括："white", "dark", "whitegrid", "darkgrid", "ticks"
# plt.figure(figsize=(4,4))#绘制画布
# sns.distplot(df_tp1['dist'],hist = False,kde = True,rug = True,
#               rug_kws = {'color':'g','lw':0.1,'alpha':0.5,'height':0.03} ,
#               # 设置数据频率分布颜色#控制是否显示观测的小细条（边际毛毯）
#               kde_kws={"color": 'g', "lw": 1.5, 'linestyle':'--'},
#               # 设置密度曲线颜色，线宽，标注、线形，#控制是否显示核密度估计图
#               label = 'Snowfall')

# # sns.distplot(df_tp2['dist'],hist = False,kde = True,rug = True,
# #               rug_kws = {'color':'goldenrod','lw':0.1,'alpha':0.5,'height':0.1} ,
# #               # 设置数据频率分布颜色#控制是否显示观测的小细条（边际毛毯）
# #               kde_kws={"color": 'goldenrod', "lw": 1.5, 'linestyle':'--'},
# #               # 设置密度曲线颜色，线宽，标注、线形，#控制是否显示核密度估计图
# #               label = 'Extreme Snowfall')

# plt.axvline(df_ave1,color='black',linestyle=":",alpha=0.8) 
# plt.text(df_ave1,0.0003,'%.0fkm' % (df_ave1), fontsize=12.5,color = 'g')

# # plt.axvline(df_ave2,color='black',linestyle=":",alpha=0.8) 
# # plt.text(df_ave2,0.00038,'%.0fkm' % (df_ave2), fontsize=12.5,color = 'goldenrod')

# # plt.text(0,0.00082,'(b)', fontsize=13,color = 'black')

# # ylist=np.arange(0,0.0008,0.0001)#.round(1)
# # plt.yticks(ylist)
# plt.ylim([0,0.00083]) #设置坐标上下限
# plt.xlim([0,3800])
# plt.xlabel('Distance (km)',fontsize=12,fontproperties='Helvetica')
# plt.ylabel('Density',fontsize=12,fontproperties='Helvetica')
# plt.tick_params(labelsize=12) #坐标轴标签
# ax = plt.gca()#获取大图边框
# ax.spines['top'].set_color('black')  
# ax.spines['bottom'].set_color('black')  
# ax.spines['left'].set_color('black')  
# ax.spines['right'].set_color('black')  

# # plt.grid(linestyle = '--')     # 添加网格线
# # plt.title("Distance between TCs and stations")  # 添加图表名
# pic_dir="F:\\snow_related\\pic\\TC\\"
# plt.savefig(pic_dir+'dist_by_snow.ps', dpi=1000, bbox_inches = 'tight')



#%% step 2.2 绘制箱线图

# import seaborn as sns
# import matplotlib.pyplot as plt
# from matplotlib.pyplot import MultipleLocator

# plt.figure(figsize=(4,4.2))#绘制画布
# sns.set_style('ticks')
# # # 风格设置，选择包括："white", "dark", "whitegrid", "darkgrid", "ticks"
# data = pd.DataFrame({"": df_tp['dist']}) 
# sns.boxplot(data=data,width=0.4,saturation=0.9,fliersize=1.0,showmeans=True,
#             meanprops={'marker':'o','markersize':5,'markerfacecolor':'black'},
#             flierprops={'marker':'x','markerfacecolor':'red'},
#             capprops=dict(color='red',linewidth=1.0),
#             color='g')


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
# pic_dir="F:\\snow_related\\pic\\tc\\"
# plt.savefig(pic_dir+'dist_box_by_snow.jpg', dpi=1000, bbox_inches = 'tight')
# plt.show() #先保存才能plot.show

  
