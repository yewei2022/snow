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
latmax2=16
p2= Path([(lonmin2,latmin2),(lonmax2,latmin2),(lonmax2,latmax2),
              (lonmin2, latmax2)])

#199506更正
lonmin1=93
lonmax1=96
latmin1=15
latmax1=18
p1= Path([(lonmin1,latmin1),(lonmax1,latmin1),(lonmax1,latmax1),
              (lonmin1, latmax1)])
                  

#%% 取最终登陆点或消失点

info=[]
g1=tc.groupby(['tc_id'])
for group_name, group_eles in g1:
    print('tc_id: \n{}'.format(group_name))
    newline = ['tc_id','lon','lat','landfall']
    g2=group_eles.reset_index(drop=True)
    lon=g2.lon_tc
    lat=g2.lat_tc
    for i in range(len(g2)):
        point=[lon[i],lat[i]]
        m=len(g2)-1 #假设都没有登陆 那就是最后一个点
        n='no' #做未登陆的标记
        #实际上要判断 如果登陆了
        if (geometry.Point(point).within(geometry.shape(shapes[0]))) \
            & (not (p2.contains_point(point))) \
                & (not (p1.contains_point(point))):
            print('登陆点: \n{}'.format(point))            
            m=i
            n='yes'
            break
    newline[0]=group_name
    newline[1]=lon[m]
    newline[2]=lat[m]
    newline[3]=n
    info.append(newline)
info1=pd.DataFrame(info,columns=['tc_id','lon','lat','landfall'])

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


info1['path']='/mnt/f/snow_sts_data/BOB/bio'+info1['tc_id'].astype(str)\
    +'.txt'
tp_tc=pd.read_table("F:\\snow_sts_data\\TC\\tc_date_infl.txt",usecols=['tc_id'],
                  sep = "\s+")

tc_info1 =info1[info1.tc_id.isin(tp_tc.tc_id)]

tc_info1.to_csv("F:\\snow_sts_data\\TC\\track_in_direction.txt",index=False,sep=" ")

#%% 根据 TC_dot.txt 将dot按路径分类 得到TC_dot_track.txt


dot=pd.read_table("F:\\snow_sts_data\\TC\\TC_dot.txt",
                        sep = "\s+")
track_label=[]
for tc in dot.tc_id:
    track_label.append(tc_info1.loc[tc_info1["tc_id"] == tc,['track_label']])
track_label_df = pd.concat(track_label,ignore_index=True)
dot1=pd.concat([dot,track_label_df],axis=1)
dot1.drop(['y4m2d2'],axis=1,inplace=True)

dot1.to_csv("F:\\snow_sts_data\\TC\\TC_dot_track.txt",index=False,sep=" ")

info1.loc[:,'count']= 1
tc_info1.loc[:,'count']= 1
a1=info1.groupby(by=['track_label'])['count'].sum()
a2=tc_info1.groupby(by=['track_label'])['count'].sum()
print('所有TC各路径数量: \n{}'.format(a1))
print('影响高原TC各路径数量: \n{}'.format(a2))

a3=dot1[dot1['track_label']=='3NE'] #199506

b1=info1.groupby(by=['landfall'])['count'].sum()
b2=tc_info1.groupby(by=['landfall'])['count'].sum()
print('所有TC登陆数量: \n{}'.format(b1))
print('影响高原TC登陆数量: \n{}'.format(b2))






    
    
