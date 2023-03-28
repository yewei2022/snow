# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 22:41:38 2023
画不同第一主导因子所占比例 饼图
*获取dataframe某一行的最大值的列名称
* https://blog.csdn.net/weixin_42386361/article/details/118800235
*获取dataframe某一行的第n大值的列名称
*https://www.5axxw.com/questions/content/qrp2hw
* pyecharts绘图自己设置颜色
@author: Lenovo
"""


import pandas as pd
import os
import numpy as np


#%% 统计

pic_dir = "F:\\snow_related\\pic\\regress\\"        
path_file="F:\\snow_sts_data\\regress\\coef\\"
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
df0.columns = ['IBTI', 'RH','DIS','TEM','WRPI','station']
order = ['WRPI','IBTI','RH','DIS','TEM','station']
df0 = df0[order]
df0.loc[:,'station'] = df0['station'].astype(int)
df1 = df0.set_index(['station']) #设置索引

# # 行最大值列索引 不用这个
# df2 = df1.astype(float).idxmax(axis=1) #行最大值的列索引
# df3 = pd.DataFrame(df2 , columns=['col_name'])

# 行第n大值的索引
n = 2
df1['col_name'] = df1.columns.to_numpy()[np.argsort(df1.to_numpy())[:, -n]]


#%%  保存文件

# #添加位置信息，法二 保存
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat','alti'])
# #拼接
# # print(df0['station']) #拼接的两个dataframe 行索引数据类型需相同
# # print(sta['station'])
# sta.set_index('station', inplace=True) # column 改为 index
# df11=pd.concat([sta,df1],axis=1,join="inner") #和80个站点信息取交集
# df2=df11.reset_index()
# #写入文件
# df2.to_csv("F:\\snow_sts_data\\regress\\lmg"+str(n)+".txt",
#                     index = False,sep=' ',na_rep=32700, 
#                     columns=['station','lon','lat','alti','col_name'])



#%%画图

import matplotlib.pyplot as plt

df3 = df1
df_g1 = df3[df3['col_name']=='WRPI']
df_g2 = df3[df3['col_name']=='IBTI']
df_g3 = df3[df3['col_name']=='RH']
df_g4 = df3[df3['col_name']=='DIS']
df_g5 = df3[df3['col_name']=='TEM']
position=['WRPI','IBTI','RH','DIS','TEM']
Num0= [len(df_g1), len(df_g2),len(df_g3),len(df_g4),len(df_g5)] 
 
plt.figure(figsize=(5, 5))
# explode = (0, 0, 0,0,0)
# plt.pie(Num0, labels=position, explode=explode, autopct="%1.2f%%", colors=['c', 'm', 'y'],
#         textprops={'fontsize': 24}, labeldistance=1.05, pctdistance=1.2, startangle=90)
# plt.pie([1], radius=0.7, colors='w')
# plt.legend(loc='upper right', fontsize=16)
# plt.axis('equal')
# plt.rcParams['font.sans-serif']= ['Arial']    # 设置字体
# plt.show()

patches,texts,autotexts = plt.pie(Num0,autopct="%.1f%%",
                                  textprops={"size":20},shadow=False,
                                  pctdistance=1.2,
                                  startangle=0,
                                  colors=["xkcd:deep sky blue","xkcd:cyan",
                                          "xkcd:light gold","xkcd:blush",
                                          "xkcd:bubble gum pink"])

# #为了解决n=1时的标签重叠问题 单独对某个标签确定位置
# for i in range(len(autotexts)):
#     if i == 0: #第1个标签的位置
#         print(texts[i].set_y(0.1))
#         print(autotexts[i].set_y(0.05)) #值越小越靠下
#     if i == 1:
#         print(texts[i].set_y(0.05))
#         print(autotexts[i].set_y(0.2))
        
plt.pie([1], radius=0.3, colors='w') # 圆环，里面那个圆为白色
plt.legend(labels=position,loc='upper right', fontsize=15,
            bbox_to_anchor=(1.5, 1),frameon=False)
# bbox 位置 frameon 边框
plt.axis('equal') #饼图显示为正圆形
plt.rcParams['font.sans-serif']= ['Arial']    # 设置字体 
plt.savefig(pic_dir+"lmg"+str(n)+'_pie.jpg',dpi=1000,bbox_inches='tight')
#bboxinches 边缘少留白
plt.show()


# # https://blog.csdn.net/Foools/article/details/115867102

# # 如何解决饼图标签重叠问题
# # https://www.jb51.net/article/257801.htm
# # https://www.freesion.com/article/7189953919/