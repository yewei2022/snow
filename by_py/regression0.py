# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 20:11:27 2023
数据预处理，用于做回归分析
@author: Lenovo
"""
import xarray as xr
import pandas as pd

#%% branch1 组合文件
# https://blog.csdn.net/LHgwei/article/details/127902909

# import os
# path1="F:\\snow_sts_data\\ERA5\\regress\\variable\\"
#   #文件夹路径
# file_list=[]#新建列表
# for filename in os.listdir(path1):
#     file_list.append(path1+filename) #将文本写入列表
# file_new=[]
# for i in range(len(file_list)):
#       hgt0C=xr.open_dataset(file_list[i])
#       file_new.append((hgt0C))  
# new_file=xr.merge(file_new)#合并 
# print(new_file)

# #测试
# data1 = xr.open_dataset(file_list[6])
# tmp1=data1.tmp
# tmp2=new_file.tmp
# # print(tmp1.time)
# print(tmp1.loc['1981-10-26T00:00:00',55690])
# print(tmp2.loc['1981-10-26T00:00:00',55690])

# new_file.to_netcdf('F:\\snow_sts_data\\ERA5\\regress\\data_station.nc')#输出合并后的nc文件  


#%% branch2 所有风暴活动日所有站点 将数据处理为1个站点一个文本 对每个站点做回归

  
# path2='F:\\snow_sts_data\\ERA5\\regress\\data_station.nc'
# data2 = xr.open_dataset(path2)
# xyname=['pre','hgt0C','prs','rh','tcdist','tmp']
# station=data2.station
# for j in range(len(station)):
# # for j in range(2):
#     sta_reg=[]
#     for i in range(len(xyname)):
#         time2=data2.time.dt.strftime('%Y%m%d') #时间变字符串
#         name1=xyname[i]
#         a1=data2[name1].loc[:,station[j]]
#         a2=pd.DataFrame(a1,columns=[name1],index=time2)
#         # a3 = 1.0*(a2 - a2.mean())/a2.std() #标准化，适用于有极端值的情况
#         a3=a2 # 先不标准化
#         print('读取至第{}个变量:{}'.format(i,name1))
#         sta_reg.append(a3)
#     sta_reg1 = pd.concat(sta_reg,axis=1) #1025
#     sta_reg2 = sta_reg1.reset_index()
#     sta_reg2.rename(columns={"index":"time"},inplace=True)    
#     # #删除任何有nan的行
#     sta_reg3=sta_reg2.dropna(axis=0, how='any',inplace=False) #885
#     sta_reg3.to_csv("F:\\snow_sts_data\\ERA5\\regress\\sta\\"+
#                     str(station[j].values)+".txt", index = False,sep=' ')
#     print('读取至第{}个站点:{}'.format(j,station[j].values))


#%% branch3 风暴活动日降雪站点 将数据处理为1个站点一个文本 对每个站点做回归
# https://zhuanlan.zhihu.com/p/101250372?from_voters_page=true 标准化

snow=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_pre_gss_all.txt",
                          sep='\s+',na_values=32700)
snow1=snow[['station','time','snow']]

path2='F:\\snow_sts_data\\ERA5\\regress\\data_station.nc'
data2 = xr.open_dataset(path2)
xyname=['pre','hgt0C','prs','rh','tcdist','tmp']

# # 测试单条
# station=55690

# # 循环每个站点
station=data2.station
record=[]
for j in range(len(station)):

    sta_reg=[]
    for i in range(len(xyname)):
        time2=data2.time.dt.strftime('%Y%m%d') #时间变字符串
        name1=xyname[i]
        a1=data2[name1].loc[:,station[j]]
        a2=pd.DataFrame(a1,columns=[name1],index=time2)
        a3 = 1.0*(a2 - a2.mean())/a2.std() #标准化，适用于有极端值的情况
        # a3=a2 #不标准化
        print('读取至第{}个变量:{}'.format(i,name1))
        sta_reg.append(a3)
    sta_reg1 = pd.concat(sta_reg,axis=1) #1025  
    snow2 = snow1[snow1['station']==station[j].values]
    snow2.set_index('time',inplace=True)
    sta_reg2 = sta_reg1[sta_reg1.index.astype(int).isin(snow2.index)]
    sta_reg3 = sta_reg2.reset_index()
    sta_reg3.rename(columns={"index":"time"},inplace=True)
    # #删除任何有nan的行
    sta_reg4=sta_reg3.dropna(axis=0, how='any') #每个站点不同
    sta_reg4.to_csv("F:\\snow_sts_data\\ERA5\\regress\\sta_snow\\"+
                    str(station[j].values)+".txt", index = False,sep=' ')
    print('读取至第{}个站点:{}'.format(j,station[j].values))
    print('站点 {} 有 {} 条记录'.format(station[j].values,len(sta_reg4)))
    newline=[station[j].values,len(sta_reg4)]
    record.append(newline)
record1=pd.DataFrame(record,columns=['station','len'])
record1.to_csv("F:\\snow_sts_data\\ERA5\\regress\\sta_snow\\record.txt", 
                index = False,sep=' ')



