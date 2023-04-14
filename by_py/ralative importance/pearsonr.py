# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 21:21:28 2023
降水量和各变量的相关系数
@author: Lenovo
"""

import pandas as pd
import xarray as xr

folder = "third_wf_Ri"

#%% branch1 所有风暴活动日的发生降雪站点的所有因子 将数据处理为1个站点一个文本

# snow=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_pre_gss_all.txt",
#                           sep='\s+',na_values=32700)
# snow1=snow[['station','time','snow']]

# path2='F:\\snow_sts_data\\regress\\data_station.nc'
# data2 = xr.open_dataset(path2)
# print(data2)

# xyname=['pre','rh','tcdist','WRPI','IBTI','tmp','hgt0C','Wf','Ri','prs']

# # # 测试单条
# # station=55690

# # # 循环每个站点
# station=data2.station
# record=[]
# for j in range(len(station)):

#     sta_reg=[]
#     for i in range(len(xyname)):
#         time2=data2.time.dt.strftime('%Y%m%d') #时间变字符串
#         name1=xyname[i]
#         a1=data2[name1].loc[:,station[j]]
#         a2=pd.DataFrame(a1,columns=[name1],index=time2)
#         print('读取至第{}个变量:{}'.format(i,name1))
#         sta_reg.append(a2)
#     sta_reg1 = pd.concat(sta_reg,axis=1) #1025  
#     snow2 = snow1[snow1['station']==station[j].values]
#     snow2.set_index('time',inplace=True)
#     sta_reg2 = sta_reg1[sta_reg1.index.astype(int).isin(snow2.index)]
#     sta_reg3 = sta_reg2.reset_index()
#     sta_reg3.rename(columns={"index":"time"},inplace=True)
#     # #删除任何有nan的行
#     sta_reg4=sta_reg3.dropna(axis=0, how='any') #每个站点不同
#     sta_reg4.to_csv("F:\\snow_sts_data\\regress\\"+folder+"\\sta_snow_nostd\\"+ 
#                     str(station[j].values)+".txt", index = False,sep=' ')
#     print('读取至第{}个站点:{}'.format(j,station[j].values))
#     print('站点 {} 有 {} 条记录'.format(station[j].values,len(sta_reg4)))
#     newline=[station[j].values,len(sta_reg4)]
#     record.append(newline)
# record1 = pd.DataFrame(record,columns=['station','len'])
# record1.to_csv("F:\\snow_sts_data\\regress\\"+folder+
#                "\\sta_snow_nostd\\record.txt", index = False,sep=' ')



#%% branch2 step1 相关性 0.3-0.8之间

# import pandas as pd
# from scipy.stats import pearsonr
# import numpy as np

# # # 测试单条
# # df = pd.read_table("F:\\snow_sts_data\\regress\\"+folder+"\\sta_snow_nostd\\"+
# #                    "52713.txt", sep='\s+')

# record = pd.read_table("F:\\snow_sts_data\\regress\\"+folder+
#                    "\\sta_snow_nostd\\record.txt",
#                   sep='\s+')
# sta1=record[record['len']>=15]

# r = []
# p = []
# for station in sta1.station.tolist():
#     print(station)
#     df = pd.read_table("F:\\snow_sts_data\\regress\\"+folder+
#                        "\\sta_snow_nostd\\"+str(station)+".txt", sep='\s+')
#     a = df['pre']
#     varname=['rh','tcdist','WRPI','IBTI','tmp','hgt0C','Wf','Ri','prs']
#     newline_r = ['station','rh','tcdist','WRPI','IBTI','tmp','hgt0C',
#                  'Wf','Ri','prs']
#     newline_p = ['station','rh','tcdist','WRPI','IBTI','tmp','hgt0C',
#                  'Wf','Ri','prs']
#     newline_r[0] = station
#     newline_p[0] = station
#     for i in range(0,len(varname)):
#         b = df[varname[i]]
#         j = i+1 #第一个被station占了
#         newline_r[j],newline_p[j] = pearsonr(a,b)
#     r.append(newline_r)
#     p.append(newline_p)
    
# r_df=pd.DataFrame(r,columns=['station','rh','tcdist','WRPI','IBTI','tmp',
#                              'hgt0C','Wf','Ri','prs'])
# p_df=pd.DataFrame(p,columns=['station','rh','tcdist','WRPI','IBTI','tmp',
#                              'hgt0C','Wf','Ri','prs'])

# # 转换成一个系数一个文件
# r_df.set_index('station', inplace=True) # column 改为 index
# p_df.set_index('station', inplace=True) # column 改为 index 
# for var in varname:
#     df0 = pd.concat([r_df[[var]],p_df[[var]]],axis=1) 
#     df0.columns=['r','p']
    
#     def get_sig(x):
#         if x['p']<0.05: 
#             return 1
#         else:
#             return 0
#     df0.loc[:, 'sig'] = df0.apply(get_sig, axis=1)
#     df0.drop(['p'],axis=1,inplace=True)
    
#     #添加位置信息，法二
#     path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
#     sta_info = pd.read_table(path_sta,sep = ",",
#                              usecols=['station','lon','lat','alti'])
#     #拼接
#     sta_info.set_index('station', inplace=True) # column 改为 index
#     df1=pd.concat([sta_info,df0],axis=1,join="inner") #和80个站点信息取交集
#     df2=df1.reset_index()
    
#     #写入文件
#     df2.to_csv("F:\\snow_sts_data\\regress\\"+folder+"\\r_p\\"+var+".txt",
#                         index = False,sep=' ',na_rep=32700)
