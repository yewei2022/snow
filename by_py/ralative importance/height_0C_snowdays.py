# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 11:15:47 2022
计算降雪日站点的0C高度 
没必要
可以计算TC活动日所有点的
最后所有变量一起提取
@author: Lenovo
"""

import xarray as xr
import datetime
import pandas as pd

#%% 读取数据做平均
file_path="F:\\snow_sts_data\\ERA5\\all\\pick\\tmp_selbox.nc"
data0 = xr.open_dataset(file_path)
var0=data0.t.loc[:, 400:1000,40:25,70:105]
time0=data0.time
level0=data0.level.loc[400:1000]
lon = data0.longitude.loc[70:105]
lat = data0.latitude.loc[40:25]
# 时间转换为可处理的格式
time1 = pd.to_datetime(time0,format = '%Y-%m-%d %H:%M:%S')
#再赋给var0
time2 = (time1 + datetime.timedelta(hours=8))#.strftime("%Y-%m-%d %H:%M:%S")
# 不用.strftime("%Y-%m-%d %H:%M:%S")  不然还要再转回原来时间格式
var0.coords['time'] = time2
daily_var = var0.resample(time='1D',closed='left',label='left').mean()
print(daily_var)


#%% 挑选降雪日时间 
# 参考 https://www.thinbug.com/q/57781130

import pandas as pd
import numpy as np

need_time=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_date.txt" ,
                          sep='\s+')
sel_date = pd.to_datetime(need_time['time'],format = '%Y%m%d')
var_sel = daily_var.sel(time=sel_date.values)
print(var_sel.shape)


#%% 垂直坐标轴插值
# https://blog.csdn.net/weixin_39864682/article/details/111009962

from scipy import interpolate

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

fx = interpolate.interp1d(np.log(level0), var_sel, kind='linear',axis=1)
var_interp= fx(np.log(need_level))
print('对数插值后的数据: \n{}'.format(var_interp.shape))

#%% 转换成高度
# https://unidata.github.io/MetPy/latest/api/generated/metpy.calc.html
import metpy.calc as mpcalc
from metpy.units import units

need_lv = xr.DataArray(data=need_level*units.hPa, dims={'level':need_level})
hgt=mpcalc.pressure_to_height_std(need_lv)

#%% 找0C高度
# # https://zhuanlan.zhihu.com/p/425885524
# https://cloud.tencent.com/developer/ask/sof/299893
import numpy as np

# #时间维和气压维交换 不用  我需要它在最右轴 和高度层匹配
# var_interp1=np.swapaxes(var_interp, 0, 1)

# 常数扩展成var_interp 同维数组
arr_tmp=np.tile(273.15,var_interp.shape)
# print(arr_tmp.shape)

# 一维高度层扩展成数组 在右轴
arr_hgt=np.broadcast_to(hgt,(len(need_time),len(lat),len(lon),
                                   len(need_level)))
# print(arr_lv.shape)

# 第2轴滚动到第4轴
idx = np.argmin(np.abs(np.rollaxis(var_interp,1,4) 
                        - np.rollaxis(arr_tmp,1,4)), axis=3)
num_days=len(need_time)
k,i,j = np.ogrid[:num_days,:61,:141]
arr_hgt1=arr_hgt[k,i,j,idx[k,i,j]]
print('0C高度: \n{}'.format(arr_hgt1.shape)) 


#%%  插值到站点 
from scipy import interpolate

path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
station=pd.read_table(path_sta,sep = ",")
sta_lat=station['lat']
sta_lon=station['lon']
time_index=np.arange(0,len(need_time))
#插值要求该维递增
lat1=lat[::-1]
arr_hgt11=arr_hgt1[:,::-1,:]
arr_hgt2 = np.zeros((len(need_time),len(sta_lat)))
for i in range(len(need_time)):
    for j in range(len(sta_lat)):
        xi=np.array([time_index[i], sta_lat[j], sta_lon[j]])
        # print(xi)
        interp_value=interpolate.interpn((time_index, lat1, lon), arr_hgt11,xi,method='linear')
        arr_hgt2[i,j]=interp_value

#%% 增加坐标属性 挑选降雪日站点

# 一维站点海拔高度扩展成数组 在右轴
sta_alti=np.broadcast_to(station['alti'],(len(need_time),len(station)))
# print(sta_alti[0,:])
# print(sta_lat)

hgt_net=arr_hgt2*1000.-sta_alti
ds = xr.Dataset()
ds['hgt0C'] = (('time','station'),hgt_net*units.meter)
ds.coords['time'] = ('time',need_time['time'].values)
ds.coords['station'] = ('station',station['station'].values)
# print(ds)
snow=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_pre_gss.txt",
                          sep='\s+',na_values=32700)
snow1=snow[['station','time']]
df_hgt=[]
for snow_date in need_time['time'].values:
    # 测试单条
    # snow_date=19811121
    print(snow_date)
    ds_arry=ds.sel(time=snow_date)
    # print(ds_arry)
    sta_arry=snow1[snow1['time']==snow_date]['station']
    # print(sta_arry)
    hgt_need1= ds_arry.sel(station=np.array(sta_arry))
    # print(hgt_need1)
    # 转换为numpy数组并铺平
    hgt_need2=hgt_need1.to_array().values.ravel()
    # print(hgt_need2)
    data_table=pd.DataFrame(list(zip(sta_arry,hgt_need2)),columns=('station','hgt_0C'))
    data_table.loc[:,'time']=snow_date
    df_hgt.append(data_table)
df_hgt1=pd.concat(df_hgt,ignore_index=True)

#%%  保存文件

#对某列特定值进行操作 https://blog.csdn.net/gisaavg/article/details/124714621
df_hgt1.loc[df_hgt1.hgt_0C < 0,'hgt_0C'] = np.nan
df_hgt2=df_hgt1.dropna(axis=0, how='any',inplace=False) #删除任何有nan的行 
df_hgt2.to_csv("F:\\snow_sts_data\\1981-2020\\hgt_0C.txt",index = False,
               sep=' ',columns=['time','station','hgt_0C'],na_rep=32700) 




