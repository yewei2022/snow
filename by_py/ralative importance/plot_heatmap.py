# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 22:57:33 2023
绘制 因子-站号 热力图

@author: Lenovo
"""

# # 数据排列方式：行-因子 列-站号

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from decimal import Decimal

folder = "third_wf_Ri"
pic_dir = "F:\\snow_related\\pic\\regress\\"+folder+"\\"        
path_file="F:\\snow_sts_data\\regress\\"+folder+"\\"+"coef\\"
f_list1 = os.listdir(path_file)
info=[]
for file in f_list1:
    df_sta = pd.read_table(path_file+file,sep='\s+',usecols=[1,2,3,4],
                            index_col=0,na_values=32700)
    df_sta.loc['station', :] = file[0:5] 
    info.append(df_sta.loc[:,"lmg1"])
    
df = pd.concat(info,axis=1,ignore_index=True) #变成dataframe
df0 = df.T
df0.drop(['(Intercept)'],axis=1,inplace=True)
# 以前只有5个变量
# df0.columns = ['IBTI', 'RH','DIS','TEM','WRPI','station']
# order = ['WRPI','IBTI','RH','DIS','TEM','station']
# 现在7个变量
df0.columns = ['IBTI', 'RH','Ri','DIS','TEM','Wf','WRPI',
                'station'] #!!! 得看df0变量顺序
order = ['WRPI','IBTI','RH','DIS','TEM','Wf','Ri','station'] #!!!
df0 = df0[order]
df1 = df0.set_index(['station']) #设置索引
df1.loc['ave'] = df1.apply(lambda x: x.mean())

# 输出各因子平均贡献百分比
for name in order[0:7]:
    a1 = df1[name].mean()
    # 精确的四舍五入，精确到0.001 np.round(a1,3) 没那么精确
    a2 = str(a1)
    a3 = Decimal(a2).quantize(Decimal("0.001"),rounding = "ROUND_HALF_UP")
    print('{} 的平均贡献百分比是 {}'.format(name, a3))

df2 = df1.T


#%%  branch1 绘制热力图

# num=np.arange(0, 70,35)
# num_list=list(num)
# num_list.append(70)
# # ser=np.arange(1, len(num_list),1) #文件比数少1
# for i in range(0,len(num_list)-1):
#     df3 = df2.iloc[:,num_list[i]:num_list[i+1]]
#     df4 = df3.astype(np.float64) #!!! 很重要不然会报错
#     ax = sns.heatmap(df4,square=True, annot=False, fmt='.2f', vmin=0, vmax=0.8, 
#                       linewidth=1, linecolor='white', cbar=False,
#                       cmap="YlGn",
#                       #格子里的文字
#                       annot_kws={'size':8,'weight':'normal','color':'black'},
#                       cbar_kws={'fraction':0.046, 'pad':0.03})
#     plt.rcParams['font.sans-serif']= ['Arial']    # 设置字体
#     # plt.rcParams['font.sans-serif']= ['Arial Unicode MS'] # 显示中文
#     plt.xticks(rotation=45)  # x轴的标签旋转45度
#     plt.yticks(rotation=45)  # y轴的标签旋转45度
#     plt.xticks(fontsize=8) #x轴标签字体大小
#     plt.yticks(fontsize=8)    
#     plt.ylabel("") 
#     plt.xlabel("") # 我们设置横纵坐标的标题
#     plt.savefig(pic_dir+'heatmap_lmg'+str(i)+'.jpg', dpi=1000, bbox_inches = 'tight')
#     plt.show()

#%% branch2 绘制色标条
    
# df3 = df2.iloc[:,0:10]
# df4 = df3.astype(np.float64) #!!! 很重要不然会报错
# ax = sns.heatmap(df4,square=True, annot=False, fmt='.2f', vmin=0, vmax=0.8, 
#                   linewidth=1, linecolor='white', cbar=True,
#                   cmap="YlGn",
#                   annot_kws={'size':8,'weight':'normal','color':'black'},
#                   cbar_kws={'fraction':0.046, 'pad':0.03})
# plt.rcParams['font.sans-serif']= ['Arial']    # 设置字体
# # plt.rcParams['font.sans-serif']= ['Arial Unicode MS'] # 显示中文
# plt.xticks(rotation=45)  # x轴的标签旋转45度
# plt.yticks(rotation=45)  # y轴的标签旋转45度

# plt.ylabel("") 
# plt.xlabel("") # 我们设置横纵坐标的标题
# plt.savefig(pic_dir+'lmg_colorbar.jpg', dpi=1000, bbox_inches = 'tight')
# plt.show()