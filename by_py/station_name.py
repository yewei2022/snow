# -*- coding: utf-8 -*-
"""
Created on Fri May  5 13:31:54 2023

@author: Lenovo
"""

import pandas as pd
from xpinyin import Pinyin

# 所有站点
file_dir = "F:\\snow_sts_data\\1981-2020-dailypre-from-weina\\" + \
    "数据说明\\station_name.txt"
station_name = pd.read_table(file_dir)
station_name.columns = ['station','province','name']

# 高原站点
path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
station_tp=pd.read_table(path_sta,sep = ",")

sta_name = station_name[station_name.station.isin(station_tp.station)]
sta_name1 = sta_name.reset_index(drop = True)

station_tp.set_index('station', inplace=True) # column 改为 index
sta_name1.set_index('station', inplace=True) # column 改为 index
df1=pd.concat([sta_name1,station_tp],axis=1,join="inner") #和80个站点信息取交集
df2=df1.reset_index()

sta_id = 55680
name = df2.loc[df2['station'] == sta_id, ['name']]
print('站号: {} 的中文名是：{}'.format(sta_id,name.values))


# 写入文件
df2.to_csv("F:\\snow_sts_data\\站点信息.txt",index = False,sep=' ')



# # 测试单条
# p = Pinyin()
# result1 = p.get_pinyin(station_name['站名'][0])
# s = result1.split('-')
# result2 = ''.join([i[0].upper() for i in s])

# def name_pinyin(x):
#     p = Pinyin()
#     result1 = p.get_pinyin(x['站名'][0])
#     s = result1.split('-')
#     result2 = ''.join([i[0].upper() for i in s])
#     return result2

# station_name.loc[:, 'pinyin']=station_name.apply(name_pinyin, axis=1) 

