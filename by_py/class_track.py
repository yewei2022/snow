# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 23:08:21 2022
判断TC路径 根据段旭
@author: Lenovo
"""

import pandas as pd
import shapefile
import shapely.geometry as geometry


#%%  得到登陆点或消失点
from matplotlib.path import Path

shp_path = 'F:\\snow_sts_data\\shp\\l\\GSHHS_l_L1.shp'
sf = shapefile.Reader(shp_path)
shapes = sf.shapes()
  

#获取文件基本信息  
# point = [100, 15] 
# a0=shapes[0].shapeType  
# a1=shapes[0].shapeTypeName  
# a2=shapes[0].bbox  
# a3=shapes[0].points #线上的每个点坐标(x,y)
# # 测试第几个多边形是目标多边形 第1个
# b=[]
# for i in range(len(shapes)):
#     b.append(geometry.Point(point).within(geometry.shape(shapes[i])))
# print('列表元素是否全为true: \n{}'.format(all(b))) 
# print('列表元素是否有true: \n{}'.format(any(b)))

    
tc=pd.read_table('F:\\snow_sts_data\\TC\\BoB_ymdh_bjt_lon_lat.txt',sep='\t')
# 需排除的区域
lonmin2=91
lonmax2=105
latmin2=0
latmax2=15
p2= Path([(lonmin2,latmin2),(lonmax2,latmin2),(lonmax2,latmax2),
              (lonmin2, latmax2)])
                  

#%%

info=[]
g1=tc.groupby(['tc_id'])
for group_name, group_eles in g1:
    print('tc_id: \n{}'.format(group_name))
    newline = ['tc_id','lon','lat']
    g2=group_eles.reset_index(drop=True)
    lon=g2.lon_tc
    lat=g2.lat_tc
    for i in range(len(g2)):
        point=[lon[i],lat[i]]
        m=len(g2)-1 #假设都没有登陆 那就是最后一个点
        #实际上要判断 如果登陆了
        if (geometry.Point(point).within(geometry.shape(shapes[0]))) & (not (p2.contains_point(point))):
            print('登陆点: \n{}'.format(point))            
            m=i
            break
    newline[0]=group_name
    newline[1]=lon[m]
    newline[2]=lat[m]
    info.append(newline)
info1=pd.DataFrame(info,columns=['tc_id','lon','lat'])

#%% 判断点的位置


def track_label(x):
    if (x["lon"] <90) & (x["lat"]>15) :
        return '1NW'
    if (x["lon"] <90) & (x["lat"]<15) :
        return '2W'  
    if (x["lon"] >90) & (x["lat"]>15) :
        return '3NE'
    else:
        return '4E'
info1.loc[:,'track_label']= info1.apply(track_label,axis=1)

#将唯一一个4E,即198805的路径改为3NE
info1['track_label'].replace('4E','3NE',inplace=True)


#%% 得到标记不同路径的文件目录



    
    
