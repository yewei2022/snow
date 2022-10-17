# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 14:11:09 2022
风暴影响下温度统计
@author: Lenovo
"""


#%% 读取tem 存入 snow_pre_gss_RTC_tem.txt

# import pandas as pd
# #读取tem
# pre=pd.read_table("F:\\f\\snow_sts_data\\tem1981_2020.txt",sep='\s+',na_values=32700)
# # 读取降雪数据
# snow_df=pd.read_table("F:\\f\\snow_sts_data\\RTC\\snow_pre_gss_RTC.txt",
#                           sep='\s+',na_values=32700)

# #add tem
# pre0=[]
# for i in range(0,len(snow_df)):
#     pre0.append(pre[(pre['time']==snow_df['time'][i]) & \
#                           (pre['station']==snow_df['station'][i])])
# pre1=pd.concat(pre0,ignore_index=True)

# pre11=pre1.set_index(['station','time']) #设置双索引
# snow_df1=snow_df.set_index(['station','time']) #设置双索引
# snow_df2 = pd.concat([snow_df1,pre11],axis=1)
# snow_df2.reset_index(inplace=True)

# snow_df2.to_csv("F:\\f\\snow_sts_data\\RTC\\snow_pre_gss_RTC_tem.txt",index = False,
#                 sep=' ',na_rep=32700)


#%% 各子区域的地面温度分布箱线图 tem.jpg

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

pic_dir="H:\\f\\snow_related\\pic\\RTC\\" 

extrm=pd.read_table("J:\\f\\snow_sts_data\\RTC\\snow_pre_gss_RTC_tem.txt",sep='\s+')

# 看数据===================================================================
a1=extrm[extrm['sta_label']==1]['dailytem'].quantile([0,0.25,0.5,0.75,1]) 
b1=float(extrm[extrm['sta_label']==1]['dailytem'].mean())

a2=extrm[extrm['sta_label']==2]['dailytem'].quantile([0,0.25,0.5,0.75,1]) 
b2=float(extrm[extrm['sta_label']==2]['dailytem'].mean())

a3=extrm[extrm['sta_label']==3]['dailytem'].quantile([0,0.25,0.5,0.75,1]) 
b3=float(extrm[extrm['sta_label']==3]['dailytem'].mean())

aa=(b1+b2+b3)/3.
# ==================================================================


plt.figure(figsize=(3,4))#绘制画布

sns.set_style('ticks')
# # 风格设置，选择包括："white", "dark", "whitegrid", "darkgrid", "ticks"
pal=['#15b01a']
sns.boxplot(data=extrm,x='sta_label',y='dailytem',width=0.4,saturation=0.9,fliersize=1.0,showmeans=True,
            flierprops={'marker':'x','markerfacecolor':'red'},
            meanprops={'marker':'o','markersize':5,'markerfacecolor':'black'},
            capprops=dict(color='red',linewidth=1.0),palette=pal)

plt.xticks(ticks=[0,1,2],labels=["E","C","S"])
# np1=np.arange(-6.5,7.5,1,'d')
# plt.yticks(np1)
#whis默认值为whis=1.5,
#IQR(Inter-Quartile Range)=Q3-Q1
#上限为数列中不超过Q3+1.5*IQR的最大值，下限为数列中不小于Q1-1.5*IQR的最小值
plt.ylabel("Temperature (°C)") 
plt.xlabel("Subregion") # 我们设置横纵坐标的标题

# plt.ylim([-6.5,7.5]) #设置坐标上下限
#纵坐标间隔1
y_minor_locator=MultipleLocator(1)
ax = plt.gca()#获取大图边框
ax.yaxis.set_minor_locator(y_minor_locator)
ax.spines['top'].set_color('black')  
ax.spines['bottom'].set_color('black')  
ax.spines['left'].set_color('black')  
ax.spines['right'].set_color('black')  

handles, labels = ax.get_legend_handles_labels()

plt.savefig(pic_dir+'tem.jpg', dpi=1000, bbox_inches = 'tight')

plt.show() #先保存才能plot.show


#%% 高原总体 降雪日的地面温度 存入snow_tem_all.txt

# import pandas as pd

# # #读取tem
# tem=pd.read_table("F:\\snow_sts_data\\tem1981_2020.txt",sep='\s+',na_values=32700)
# # 读取高原总体降雪日和站点
# snow_df=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_pre_gss_all.txt",
#                           sep='\s+',na_values=32700)
# #将gss_inc<0 的值标记为为缺失值
# def fill_existing2(x):
#     if x["gss_inc"] <0:
#         return None
#     else:
#         return x["gss_inc"]
# snow_df.loc[:,'gss_inc']= snow_df.apply(fill_existing2,axis=1)

# # #add tem 法一
# # tem0=[]
# # for i in range(0,len(snow_df)):
# #     tem0.append(tem[(tem['time']==snow_df['time'][i]) & \
# #                           (tem['station']==snow_df['station'][i])])
# # tem1=pd.concat(tem0,ignore_index=True)

# # tem11=tem1.set_index(['station','time']) #设置双索引
# # snow_df1=snow_df.set_index(['station','time']) #设置双索引
# # snow_df2 = pd.concat([snow_df1,tem11],axis=1)
# # snow_df2.reset_index(inplace=True)

# # #add tem 法二
# tem0=tem.set_index(['station','time']) #设置双索引
# snow_df1=snow_df.set_index(['station','time']) #设置双索引
# snow_df2=pd.concat([snow_df1,tem0],ignore_index=True,axis=1,join="inner")
# # 这里ignore_index=True后之后就得重新设置index 下面第二行 没有必要
# snow_df2.reset_index(inplace=True)
# snow_df2.columns=['station', 'time', 'snow', 'lon', 'lat', 'dailypre', 'gss',
#                   'gss_inc', 'dailytem']
# # 法一和法二结果相同，法二取交集速度更快，刚好snow_df是tem0的子集 可以得到我想要的

# snow_df2.to_csv("F:\\snow_sts_data\\1981-2020\\snow_tem_all.txt",index = False,
#                 sep=' ',na_rep=32700)


#%% 计算高原总体降雪日的站点平均tem sta_avg_tem_all.txt

# import pandas as pd

# # #读取tem
# tem_df=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_tem_all.txt",sep='\s+',
#                   na_values=32700)
# # 读取高原总体降雪日和站点
# tem=tem_df.groupby(by=['station'])['dailytem'].mean()
# #添加位置信息，法二
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# sta.set_index('station', inplace=True) # column 改为 index

# tem1=pd.concat([sta,tem],axis=1)
# tem2=tem1.reset_index()

# #写入文件
# tem2.to_csv("F:\\snow_sts_data\\1981-2020\\sta_avg_tem_all.txt",
#                     index = False,sep=' ',na_rep=32700)

# # # 测试某个值以下占多少百分比
# # pre3=pre2['dailypre'].dropna(axis=0, how='any',inplace=False) #删除任何有nan的行 便于后面进行缺测的计数
# # per=pre3.quantile([0,0.25,0.5,0.75,0.8,0.9,0.95,1])   



#%% 全区气温平均值 异常值 显著性检验 sta_avg_tem_test.txt

# import pandas as pd
# from scipy import stats

# # #读取降雪气温文件
# extrm=pd.read_table("F:\\f\\snow_sts_data\\RTC\\snow_pre_gss_RTC_tem.txt",sep='\s+')
# need=extrm[['station','time','dailytem']]
# need.reset_index(drop=True,inplace=True)

# # #读取高原总体站点降雪日的站点平均气温
# tem_all=pd.read_table("F:\\f\\snow_sts_data\\1981-2020\\sta_avg_tem_all.txt",
#                       sep='\s+', na_values=32700)
# popl_avg=tem_all[['station','dailytem']]

# # 均值的显著性检验
# info=[]
# g1=need.groupby(['station'])
# for group_name, group_eles in g1:
#     # print(group_name)
#     newline = ['station','p']
#     samp_pick=group_eles.dailytem
#     popl_pick=float(popl_avg[popl_avg['station']==group_name]['dailytem'])
#     # print(popl_pick)
#     samp_pick.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行
#     _,p = list(stats.ttest_1samp(samp_pick, popl_pick))
#     newline[0]=group_name
#     newline[1]=float(p)    
#     info.append(newline)
# info1=pd.DataFrame(info,columns=['station','p'])

# def get_sig(x):
#     if x['p']<0.05: 
#         return 1
#     else:
#         return 0
# info1.loc[:, 'sig'] = info1.apply(get_sig, axis=1)

# #计算各站点平均tem
# snow_avg=need.groupby(by=['station'])['dailytem'].mean()
# #添加位置信息，法二
# path_sta='F:\\f\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat','alti'])
# #拼接
# sta.set_index('station', inplace=True) # column 改为 index
# popl_avg.columns=['station','popl_avg']
# popl_avg.set_index('station', inplace=True) # column 改为 index
# info2=pd.concat([sta,snow_avg,popl_avg],axis=1,join="inner")
# info1.set_index('station', inplace=True) # column 改为 index
# info3=pd.concat([info2,info1],axis=1)
# info4=info3.reset_index()
# info4.drop(['p'],axis=1,inplace=True)
# info4.loc[:,'dev']=info4['dailytem']-info4['popl_avg']

# a=info4[info4['dev']>=0]

# #将各个站点平均气温写入文件
# info4.to_csv("F:\\f\\snow_sts_data\\RTC\\sta_avg_tem_test.txt",
#                     index = False,sep=' ',na_rep=32700)


 