# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 21:35:18 2022
不同海拔高度站点 PA 和SD分布
@author: Lenovo
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from scipy import stats

#%% 计算不同海拔高度站点分类
count=0
var=['dailypre','gss']
picname="F:\\snow_related\\pic\\snow_byTC\\"+var[count]
need=pd.read_table("H:\\snow_sts_data\\1981-2020\\snow_pre_gss.txt",
                          sep='\s+',na_values=32700)

# # 测试某个值以下占多少百分比
# df_pre=need['dailypre'].quantile([0,0.25,0.5,0.75,0.8,0.9,0.95,1]) 
# print(df_pre)
# df_gss=need['gss'].quantile([0,0.25,0.5,0.75,0.8,0.9,0.95,1]) 
# print(df_gss)

# # 测试95 22.225mm
# df3=df1[df1['dailypre']<=22.225]
# a=len(df3)/len(df1)
# print(a) # 0.94981 确实 可靠

# #添加海拔 法一 循环添加
#添加海拔
path_sta='H:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
sta=pd.read_table(path_sta,sep = ",",usecols=['station','alti'])
alti=[]
for i in need.station.tolist():
    alti.append(sta.loc[sta["station"] == i,['alti']])
alti_df = pd.concat(alti,ignore_index=True)
need1=pd.concat([need,alti_df],axis=1)

# def alti_label(x):    
#     if x['alti']<2500: 
#         return '(2000,2500)'
#     elif (2500<=x['alti']<3000):
#         return '[2500,3000)'
#     elif (3000<=x['alti']<3500):
#         return '[3000,3500)'
#     elif (3500<=x['alti']<4000):
#         return '[3500,4000)' 
#     elif (4000<=x['alti']<4500):
#         return '[4000,4500)'   
#     elif x['alti']>=4500:
#         return '[4500,5000)'
def alti_label(x):    
    if x['alti']<2500: 
        return 1
    elif (2500<=x['alti']<3000):
        return 2
    elif (3000<=x['alti']<3500):
        return 3
    elif (3500<=x['alti']<4000):
        return 4 
    elif (4000<=x['alti']<4500):
        return 5   
    elif x['alti']>=4500:
        return 6   
need1.loc[:, 'alti_label']=need1.apply(alti_label, axis=1) 

data = need1[[var[count],'alti_label']]

# # 测试某批数据为何中位数线看不见 原因 与Q1重合0.25=0.5
# df_var=need1[need1['alti_label']==5][var[count]].quantile([0.25,0.5,0.75]) 
# print(df_var)

#%% 画图 这个图不太能看
       
plt.figure(figsize=(6.5,4))#绘制画布

sns.set_style('ticks')
# # 风格设置，选择包括："white", "dark", "whitegrid", "darkgrid", "ticks"
# https://xkcd.com/color/rgb/ 颜色设置网页
pal=[['#15b01a'],['#ffab0f']]
sns.boxplot(data=data,x='alti_label',y=var[count],width=0.4,saturation=0.9,
            fliersize=1.0,color='black',showmeans=True,
            flierprops={'marker':'x','markerfacecolor':'red'},
            meanprops={'marker':'o','markersize':5,'markerfacecolor':'black'},
            capprops=dict(color='red',linewidth=1.0),palette=pal[count])
            # pal必须是palette 即[]的格式
plt.xticks(ticks=[0,1,2,3,4,5],
            labels=['(2000,2500)','[2500,3000)','[3000,3500)','[3500,4000)',
                    '[4000,4500)','[4500,5000)'])

# plt.yticks(range(0,100,10))
#whis默认值为whis=1.5,
#IQR(Inter-Quartile Range)=Q3-Q1
#上限为数列中不超过Q3+1.5*IQR的最大值，下限为数列中不小于Q1-1.5*IQR的最小值
ylabels=['PA (mm)','SD (cm)']
ymaxs=[45,10]
plt.ylabel(ylabels[count]) 
plt.xlabel("Altitude (m)") # 我们设置横纵坐标的标题
plt.ylim([0,ymaxs[count]]) #设置坐标上下限
yaxis_int=[5,1]
y_minor_locator=MultipleLocator(yaxis_int[count])


ax = plt.gca()#获取Figure边框
ax.yaxis.set_minor_locator(y_minor_locator)
ax.spines['top'].set_color('black')  
ax.spines['bottom'].set_color('black')  
ax.spines['left'].set_color('black')  
ax.spines['right'].set_color('black')  

plt.savefig(picname+'.ps', dpi=1000, bbox_inches = 'tight')

plt.show() #先保存才能plot.show