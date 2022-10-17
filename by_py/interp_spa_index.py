# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 13:42:12 2022
对降雪日降水场插值 
根据REOF结果计算space_index

@author: Lenovo
"""

import pandas as pd
import numpy as np


#%%  数据预处理 
 
need0=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_pre_gss.txt",
                          sep='\s+',na_values=32700)

# REOF降雪场的筛选 至少有三个站点产生降雪
snow_f=need0.groupby(by=['time'])['snow'].sum() 
snow_f1=snow_f[snow_f>=3]
snow_date=snow_f1.index
need=need0[need0.time.isin(snow_date)]
name='time'
pre1=need[[name,'station','dailypre']]
pre1['station']=pre1['station'].astype(int)
pre2=pre1.pivot(index=name, columns='station', values='dailypre')
data=pre2.fillna(0)
datavalue = data.values

#%% 插值

from metpy.interpolate import inverse_distance_to_grid
from scipy.interpolate import Rbf

#取站号 经纬度
idd = list(data.columns)
path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
station=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
st0 = station[station.station.isin(idd)]
st1 = st0.sort_values(by='station', ascending=True)
st=st1.reset_index(drop=True)

lon_min, lon_max = 70, 105
lat_min, lat_max = 25, 40
intervl=0.25
lon_grid = np.arange(lon_min, lon_max+intervl, intervl) 
lat_grid = np.arange(lat_min, lat_max+intervl, intervl) 
lon_gridmesh, lat_gridmesh = np.meshgrid(lon_grid, lat_grid)

drawdata = np.zeros((len(data),len(lat_grid),len(lon_grid)))

for i in range(len(data)):
    print(i)
    func = Rbf(st.lon, st.lat, datavalue[i], function='linear',smooth=2)
    stid_pre = func(lon_gridmesh, lat_gridmesh)
    rbfda = stid_pre
    # 另一种站点插值到格点的方法？
    # tm_grid = inverse_distance_to_grid(st.lon,st.lat,datavalue[i],lon_gridmesh,
    #                                     lat_gridmesh,r=15,min_neighbors=3)
    drawdata[i] = rbfda
    
    



#%% 掩码函数定义
import math
from shapely.prepared import prep

def polygon_to_mask(polygon, x, y):
    '''生成落入多边形的点的掩膜数组.'''
    x = np.atleast_1d(x)
    y = np.atleast_1d(y)
    if x.shape != y.shape:
        raise ValueError('x和y的形状不匹配')
    prepared = prep(polygon)

    def recursion(x, y):
        '''递归判断坐标为x和y的点集是否落入多边形中.'''
        xmin, xmax = x.min(), x.max()
        ymin, ymax = y.min(), y.max()
        xflag = math.isclose(xmin, xmax)
        yflag = math.isclose(ymin, ymax)
        mask = np.zeros(x.shape, dtype=bool)

        # 散点重合为单点的情况.
        if xflag and yflag:
            point = sgeom.Point(xmin, ymin)
            if prepared.contains(point):
                mask[:] = True
            else:
                mask[:] = False
            return mask

        xmid = (xmin + xmax) / 2
        ymid = (ymin + ymax) / 2

        # 散点落在水平和垂直直线上的情况.
        if xflag or yflag:
            line = sgeom.LineString([(xmin, ymin), (xmax, ymax)])
            if prepared.contains(line):
                mask[:] = True
            elif prepared.intersects(line):
                if xflag:
                    m1 = (y >= ymin) & (y <= ymid)
                    m2 = (y >= ymid) & (y <= ymax)
                if yflag:
                    m1 = (x >= xmin) & (x <= xmid)
                    m2 = (x >= xmid) & (x <= xmax)
                if m1.any(): mask[m1] = recursion(x[m1], y[m1])
                if m2.any(): mask[m2] = recursion(x[m2], y[m2])
            else:
                mask[:] = False
            return mask

        # 散点可以张成矩形的情况.
        box = sgeom.box(xmin, ymin, xmax, ymax)
        if prepared.contains(box):
            mask[:] = True
        elif prepared.intersects(box):
            m1 = (x >= xmid) & (x <= xmax) & (y >= ymid) & (y <= ymax)
            m2 = (x >= xmin) & (x <= xmid) & (y >= ymid) & (y <= ymax)
            m3 = (x >= xmin) & (x <= xmid) & (y >= ymin) & (y <= ymid)
            m4 = (x >= xmid) & (x <= xmax) & (y >= ymin) & (y <= ymid)
            if m1.any(): mask[m1] = recursion(x[m1], y[m1])
            if m2.any(): mask[m2] = recursion(x[m2], y[m2])
            if m3.any(): mask[m3] = recursion(x[m3], y[m3])
            if m4.any(): mask[m4] = recursion(x[m4], y[m4])
        else:
            mask[:] = False

        return mask

    return recursion(x, y)




#%%  生成高原掩码数组

import shapefile
import shapely.geometry as sgeom

filepath = 'F:\\snow_sts_data\\TPshp\\DBATP\\DBATP_Polygon.shp'
with shapefile.Reader(filepath) as reader:
    TP = sgeom.shape(reader.shape(0))
    
    
#%% 尝试mask 
# https://www.cnblogs.com/ShineLeBlog/p/15546092.html

# https://mp.weixin.qq.com/s?__
# biz=MzAwNDgyNTgxOA==&mid=2247525978&idx=3&sn=1a1674fc4845f7bcc52e3076b8708d0c
# &chksm=9b27d1efac5058f9f6e6a541813ef6043d0a55f8e5fa8a8aabc9b61adbfb4ded2ef6d1108429
# &scene=27

# 对于数据中是否有np.nan对计算mean sum的影响
# https://blog.csdn.net/kong_jie123/article/details/123777692

import numpy as np
import numpy.ma as ma

#测试用mask将等于某值的数值做掩码
# a=np.array([0,1,5,999])
# b=np.ma.masked_equal(a,999)
# c=b.filled(np.nan)
# z=np.mean(b) 
# z=np.mean(c) 
# z=np.nanmean(c) 

# mask 高原
mask = polygon_to_mask(TP, lon_gridmesh, lat_gridmesh)
mask_inv=~mask

# # 法一 
# # x0=drawdata[0,:,:]
# # x0[~mask] = np.nan #直接把外面的设置nan 因为外面是false 变True 把true的值变成nan

# 法二 用mask
# # 测试单条
# x0=drawdata[0,:,:]
# x1=ma.array(x0, mask=mask_inv)
# x2=x1.filled(fill_value=-999)

data_mask1 = np.zeros((len(snow_date),len(lat_grid),len(lon_grid)))
for i in range(0,len(snow_date)):
    a=ma.array(drawdata[i,:,:], mask=mask_inv)
    # a1=a.filled(fill_value=-999) #先不填充 后面还要计算呢
    data_mask1[i,:,:]=a


#%% 计算空间指数

import xarray as xr
import numpy as np
import numpy.ma as ma

ncfile_path="F:\\snow_sts_data\\REOF\\time_reof_pre.nc"
space = xr.open_dataset(ncfile_path)
space1=space.pre.sel(m_pcs=0)
space2=space.pre.sel(m_pcs=1)
spa1 = space1.values
spa2 = space2.values

# mask 高原
spa1_tp=ma.array(spa1, mask=mask_inv)
spa2_tp=ma.array(spa2, mask=mask_inv)

# #测试单条
# x0=data_mask1[0,:,:]
# s_pos=ma.masked_where(spa1_tp<=0.2, x0)
# s_neg=ma.masked_where(spa1_tp>=-0.2, x0)
# s_index=np.mean(s_pos)-np.mean(s_neg)

#批量 
spa_index = np.zeros((len(snow_date),2))
for i in range(0,len(snow_date)):
    x0=data_mask1[i,:,:]
    s_pos=ma.masked_where(spa1_tp<=0.2, x0)
    s_neg=ma.masked_where(spa1_tp>=-0.2, x0)
    s_index=np.mean(s_pos)-np.mean(s_neg)
    n_pos=ma.masked_where(spa2_tp<=0.2, x0)
    n_neg=ma.masked_where(spa2_tp>=-0.2, x0)
    n_index=np.mean(n_pos)-np.mean(n_neg)
    spa_index[i,0]=s_index
    spa_index[i,1]=n_index


spa_index_df=pd.DataFrame(spa_index,columns=['s_index','n_index'],index=snow_date)
df=spa_index_df.reset_index()

def spa_type(x):    
    if x['s_index']>x['n_index']: 
        return 1
    elif x['s_index']<x['n_index']:
        return 2
    else:
        return 0
df.loc[:, 'type']=df.apply(spa_type, axis=1) 
# w=df[df['type']==1]

df.to_csv("F:\\snow_sts_data\\REOF\\spa_index.txt",index = False,
                sep=' ',na_rep=32700)

#%% 将数据保存为nc 文件  保存前需把nan填充
# https://blog.csdn.net/qq_44907989/article/details/125907641
    
# import xarray as xr
# import numpy as np
# from metpy.units import units

# ds = xr.Dataset()
# # *units.degC 是给气温赋单位，有没有单位都可以，锦上添花的东西

# ds['pre'] = (('time','lat','lon'),data_mask1*units('mm'))
# time=list(snow_date)
# ds.coords['time'] = ('time',time)
# ds.coords['lat'] = ('lat',lat_grid)
# ds.coords['lon'] = ('lon',lon_grid)

# ds.to_netcdf('F:\\snow_sts_data\\REOF\\'+name+'_tpmask_pre.nc')


