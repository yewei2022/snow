# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 11:15:47 2022
所有TC活动日站点的0C高度
@author: Lenovo
"""

import xarray as xr
import datetime
import pandas as pd
from scipy import interpolate
import numpy as np
import metpy.calc as mpcalc
from metpy.units import units

# ==================================================================================

#%% branch1 step1 读取数据 转化为北京时 做平均

# file_path="F:\\backups\\f\\snow_sts_data\\ERA5\\all\\pick\\tmp_selbox.nc"
# data0 = xr.open_dataset(file_path)
# var0=data0.t.loc[:, 400:1000,40:25,70:105]
# time0=data0.time
# level0=data0.level.loc[400:1000]
# lon = data0.longitude.loc[70:105]
# lat = data0.latitude.loc[40:25]
# # 时间转换为可处理的格式
# time1 = pd.to_datetime(time0,format = '%Y-%m-%d %H:%M:%S')
# #再赋给var0
# time2 = (time1 + datetime.timedelta(hours=8))#.strftime("%Y-%m-%d %H:%M:%S")
# # 不用.strftime("%Y-%m-%d %H:%M:%S")  不然还要再转回原来时间格式
# var0.coords['time'] = time2
# daily_var = var0.resample(time='1D',closed='left',label='left').mean()
# print(daily_var)


#%% branch1 step2挑选TC活动日时间 写入文件 在ncl里对垂直坐标层插值
# 参考 https://www.thinbug.com/q/57781130

# import pandas as pd

# need_time=pd.read_table("F:\\backups\\f\\snow_sts_data\\TC\\all_tc_days.txt" ,
#                           sep='\s+')
# need_time.columns=['tc_id','time']
# sel_date = pd.to_datetime(need_time['time'],format = '%Y%m%d')
# var_sel = daily_var.sel(time=sel_date.values)
# print('变量维度: \n{}'.format(var_sel.shape))
# print(var_sel)

# var_sel.to_netcdf('F:\\backups\\f\\snow_sts_data\\ERA5\\all\\deal\\tmp_alltcdays.nc')

# ========================================================================================


#%% branch2 step1 开始循环 一小块一小块算 因为数据量太大 内存不够

num=np.arange(0, 1025,50)
num_list=list(num)
num_list.append(1025)
ser=np.arange(1, len(num_list),1) #文件比数少1
# 循环算 则该branch 后文均需要缩进
# for l in range(0,len(num_list)):
    
#%% 垂直坐标轴插值 我的笔记本不行 内存不够
# https://blog.csdn.net/weixin_39864682/article/details/111009962

file_path1='F:\\snow_sts_data\\ERA5\\all\\deal\\tmp_alltcdays.nc'
data1 = xr.open_dataset(file_path1)

l=20 #单个算
var_sel1=data1.t[num_list[l]:num_list[l+1],:,:,:] #???! 
level1=data1.level
time1=data1.time[num_list[l]:num_list[l+1]] #???! 
time2 = pd.to_datetime(time1,format = '%Y-%m-%d %H:%M:%S')
lon = data1.longitude
lat = data1.latitude

print('原始时间格式: \n{}'.format(time1))
print('字符串时间格式: \n{}'.format(time2))

print('变量: \n{}'.format(var_sel1))

need_level=np.linspace(400, 1000, 601)

# =============================================================================
# # # 测试
# # fx_test = interpolate.interp1d(np.log(level0), var0[0,:,0,0], kind='linear')
# # my_test= fx_test(np.log(need_level))
# # # print('原气压层: \n{}'.format(level0))
# # # print('需要插值的气压层: \n{}'.format(need_level))
# # # print('原数据: \n{}'.format(var0[0,:,0,0]))
# # # print('原数据长度: \n{}'.format(len(var0[0,:,0,0])))
# # # print('对数插值后的数据: \n{}'.format(my_test))
# # # print('对数插值后的数据长度: \n{}'.format(len(my_test)))
# =============================================================================

var_sel32=np.float32(var_sel1) #转化为float32 缩小内存
fx = interpolate.interp1d(np.log(level1), var_sel32, kind='linear',axis=1)
var_interp= fx(np.log(need_level))
print('对数插值后的数据: \n{}'.format(var_interp.shape))


#%% 转换成高度
# # https://unidata.github.io/MetPy/latest/api/generated/metpy.calc.html

need_lv = xr.DataArray(data=need_level*units.hPa, dims={'level':need_level})
hgt=mpcalc.pressure_to_height_std(need_lv)

#%% 找0C高度
# # # https://zhuanlan.zhihu.com/p/425885524
# # https://cloud.tencent.com/developer/ask/sof/299893

# #时间维和气压维交换 不用  我需要它在最右轴 和高度层匹配
# var_interp1=np.swapaxes(var_interp, 0, 1)

# 常数扩展成var_interp 同维数组
arr_tmp=np.tile(273.15,var_interp.shape)
# print(arr_tmp.shape)

# 一维高度层扩展成数组 在右轴
arr_hgt=np.broadcast_to(hgt,(len(time2),len(lat),len(lon),
                                    len(need_level)))
# print(arr_lv.shape)

# 第2轴滚动到第4轴
idx = np.argmin(np.abs(np.rollaxis(var_interp,1,4) 
                        - np.rollaxis(arr_tmp,1,4)), axis=3)
num_days=len(time2)
k,i,j = np.ogrid[:num_days,:61,:141]
arr_hgt1=arr_hgt[k,i,j,idx[k,i,j]]
print('0C高度: \n{}'.format(arr_hgt1.shape)) 


#%%  插值到站点 

path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
station=pd.read_table(path_sta,sep = ",")
sta_lat=station['lat']
sta_lon=station['lon']
time_index=np.arange(0,len(time2))
#插值要求输出维该维递增
lat1=lat[::-1]
arr_hgt11=arr_hgt1[:,::-1,:]
arr_hgt2 = np.zeros((len(time2),len(sta_lat)))
for i in range(len(time2)):
    for j in range(len(sta_lat)):
        xi=np.array([time_index[i], sta_lat[j], sta_lon[j]])
        # print(xi)
        interp_value=interpolate.interpn((time_index, lat1, lon), arr_hgt11,xi,method='linear')
        arr_hgt2[i,j]=interp_value

# %% 增加坐标属性 保存文件

# 一维站点海拔高度扩展成数组 在右轴
sta_alti=np.broadcast_to(station['alti'],(len(time2),len(station)))
# print(sta_alti[0,:])
# print(sta_lat)

hgt_net=arr_hgt2*1000.-sta_alti
ds = xr.Dataset()
ds['hgt0C'] = (('time','station'),hgt_net*units.meter)
ds.coords['time'] = ('time',time2)
ds.coords['station'] = ('station',station['station'].values)
print('保存的数据: \n{}'.format(ds))
print('已计算完至第: \n{} 个文件'.format(ser[l]))
ds.to_netcdf('F:\\snow_sts_data\\ERA5\\all\\deal\\tmp_station'+str(ser[l])+'.nc') #???!

    
#%% branch3 step1 组合文件
# https://blog.csdn.net/LHgwei/article/details/127902909

# import os
# path2="F:\\snow_sts_data\\ERA5\\all\\deal\\"
#  #文件夹路径
# file_list=[]#新建列表
# for m in range(1,22):
#     print(m)    
#     fn=os.path.join(path2+'tmp_station'+str(m)+'.nc')# 将路径与有规律的文件名拼接起来
#     file_list.append(fn) #将文本写入列表
# file_new=[]
# for i in range(len(file_list)):
#      hgt0C=xr.open_dataset(file_list[i])['hgt0C']
#      file_new.append((hgt0C))  
# new_file=xr.concat(file_new,dim='time')#合并 
# new_file.to_netcdf(path2+'hgt0C_station.nc')#输出合并后的nc文件  

# #%% branch3 step2 读取组合后文件
   
# file_path2="F:\\snow_sts_data\\ERA5\\all\\deal\\hgt0C_station.nc"
# data2 = xr.open_dataset(file_path2)
# var2=data2.hgt0C
# print(var2)
# print(var2.loc[:,55690])




