# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 13:10:10 2023
回归后数据处理（R回归后）
@author: Lenovo
"""

import pandas as pd
import os


#%% branch1 step1 序列重组为每个自变量在所有站点的标准化系数 保存为一个变量一个文件

# # # 测试单条
# # df=pd.read_table("F:\\snow_sts_data\\ERA5\\regress\\coef\\51804.txt",
# #                   sep='\s+',usecols=[1,2,3,4],index_col=0)

# #所有循环读入
# varname=['WRPI','IBTI','rh','tcdist','tmp']
# for var in varname:
        
#     path_file="F:\\snow_sts_data\\regress\\coef\\"
#     f_list1 = os.listdir(path_file)
#     info=[]
#     for file in f_list1:
#         df_sta = pd.read_table(path_file+file,sep='\s+',usecols=[1,2,3,4],
#                                 index_col=0,na_values=32700)
#         df_sta.loc[:, 'station'] = file[0:5] 
#         info.append(df_sta.loc[var,:])
        
#     df = pd.concat(info,axis=1,ignore_index=True) #变成dataframe
#     df0 = df.T   
    
#     df0.columns=['coef','p','lmg','station']
#     df0.loc[:,'station'] = df0['station'].astype(int)
#     def get_sig(x):
#         if x['p']<0.05: 
#             return 1
#         else:
#             return 0
#     df0.loc[:, 'sig'] = df0.apply(get_sig, axis=1)
#     df0.drop(['p'],axis=1,inplace=True)
    
#     #添加位置信息，法二
#     path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
#     sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat','alti'])
#     #拼接
#     sta.set_index('station', inplace=True) # column 改为 index
#     df0.set_index('station', inplace=True) # column 改为 index
#     df1=pd.concat([sta,df0],axis=1,join="inner") #和80个站点信息取交集
#     df2=df1.reset_index()
#     #写入文件
#     df2.to_csv("F:\\snow_sts_data\\regress\\"+var+".txt",
#                         index = False,sep=' ',na_rep=32700, 
#                         columns=['station','lon','lat','alti','coef','sig','lmg'])

    
#%% branch2 step1 测试每个站点每个变量系数coef的范围 便于绘图看值的范围

# varname=['WRPI','IBTI','rh','tcdist','tmp']
# for count in range(0,5):
#     # count = 4
#     a = pd.read_table("F:\\snow_sts_data\\regress\\"+varname[count]+
#                             ".txt", sep='\s+')
#     print('"',varname[count],'"','正响应站点数: {}'.format(len(a[a['coef']>0])))
#     print('"',varname[count],'"','负响应站点数: {}'.format(len(a[a['coef']<0])))
#     print('"',varname[count],'"','显著的站点数: {}'.format(len(a[a['sig']==1])))
#     print('"',varname[count],'"','正响应且显著站点数: {}'.format(
#         len(a[(a['coef']>0) & (a['sig']==1)])))
#     print('"',varname[count],'"','负响应且显著站点数: {}'.format(
#         len(a[(a['coef']<0) & (a['sig']==1)])))
#     # a1 = a['coef']
#     # a2 = a1.quantile([0,0.25,0.5,0.75,0.8,0.9,0.95,1]) 
#     # print('"',varname[count],'"',"系数分布：",'\n', a2)

#%% branch3 step1 测试 有多少个站点的线性方程是显著的 R2的范围

# df0=pd.read_table("F:\\snow_sts_data\\regress\\R2_pf.txt",sep='\s+')
# def get_sig(x):
#     if x['pf']<0.05: 
#         return 1
#     else:
#         return 0
# df0.loc[:, 'sig'] = df0.apply(get_sig, axis=1)
# df0.drop(['pf'],axis=1,inplace=True)
# print('线性方程显著的站点数: \n{}'.format(len(df0[df0['sig']==1])))
# a1 = df0['R2']
# a2 = a1.quantile([0,0.25,0.5,0.75,0.8,0.9,0.95,1]) 
# print('R2 几分位数: \n{}'.format(a2))



 
