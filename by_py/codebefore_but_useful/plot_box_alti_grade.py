# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 19:50:52 2022
不同降雪等级站点海拔高度分布箱线图
高原总体的 风暴影响下的
@author: Lenovo
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

#%% 对于pre等级
filename="pre_grade_alti"
df1=pd.read_table("F:\\snow_sts_data\\percentile\\"+filename+"_all.txt",
                          sep='\s+',na_values=32700)
df1L_s=df1['Grade1']
df1M_s=df1['Grade2']
df1H_s=df1['Grade3']
df1S_s=df1['Grade4']

df1L=pd.DataFrame(list(df1L_s),columns=['alti'])
df1M=pd.DataFrame(list(df1M_s),columns=['alti'])
df1H=pd.DataFrame(list(df1H_s),columns=['alti'])
df1S=pd.DataFrame(list(df1S_s),columns=['alti'])

df1L.loc[:,"grade"]="Grade1"
df1M.loc[:,"grade"]="Grade2"
df1H.loc[:,"grade"]="Grade3"
df1S.loc[:,"grade"]="Grade4"

df1L.loc[:,"label"]="All"
df1M.loc[:,"label"]="All"
df1H.loc[:,"label"]="All"
df1S.loc[:,"label"]="All"


df2=pd.read_table("F:\\snow_sts_data\\percentile\\"+filename+".txt",
                          sep='\s+',na_values=32700)

df2L_s=df2['Grade1']
df2M_s=df2['Grade2']
df2H_s=df2['Grade3']
df2S_s=df2['Grade4']

df2L=pd.DataFrame(list(df2L_s),columns=['alti'])
df2M=pd.DataFrame(list(df2M_s),columns=['alti'])
df2H=pd.DataFrame(list(df2H_s),columns=['alti'])
df2S=pd.DataFrame(list(df2S_s),columns=['alti'])

df2L.loc[:,"grade"]="Grade1"
df2M.loc[:,"grade"]="Grade2"
df2H.loc[:,"grade"]="Grade3"
df2S.loc[:,"grade"]="Grade4"


df2L.loc[:,"label"]="TC"
df2M.loc[:,"label"]="TC"
df2H.loc[:,"label"]="TC"
df2S.loc[:,"label"]="TC"

data=pd.concat([df1L,df1M,df1H,df1S,df2L,df2M,df2H,df2S],axis=0)
data.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行

# 发现有无缺失值都一样 缺失值处理见deal500hPa            
plt.figure(figsize=(5,4))#绘制画布

sns.set_style('ticks')
# # 风格设置，选择包括："white", "dark", "whitegrid", "darkgrid", "ticks"
pal=['#75bbfd','#15b01a']
sns.boxplot(data=data,x="grade", y="alti", hue="label",
            width=0.4,saturation=0.9,fliersize=1.0,showmeans=True,
            flierprops={'marker':'x','markerfacecolor':'red'},
            meanprops={'marker':'o','markersize':5,'markerfacecolor':'black'},
            capprops=dict(color='red',linewidth=1.0),palette=pal)

plt.xticks(ticks=[0,1,2,3],labels=["Grade1","Grade2","Grade3","Grade4"])
plt.yticks(range(0,5050,500))
#whis默认值为whis=1.5,
#IQR(Inter-Quartile Range)=Q3-Q1
#上限为数列中不超过Q3+1.5*IQR的最大值，下限为数列中不小于Q1-1.5*IQR的最小值
plt.ylabel("Altitude (m)") 
plt.xlabel("Grade") # 我们设置横纵坐标的标题

plt.ylim([2000,5000]) #设置坐标上下限

y_minor_locator=MultipleLocator(100)
ax = plt.gca()#获取大图边框
ax.yaxis.set_minor_locator(y_minor_locator)
ax.spines['top'].set_color('black')  
ax.spines['bottom'].set_color('black')  
ax.spines['left'].set_color('black')  
ax.spines['right'].set_color('black')  

handles, labels = ax.get_legend_handles_labels()

#调整图例
#位置
# l = plt.legend(handles[0:2], labels[0:2], bbox_to_anchor=(0.825, 0.2), 
#                loc=2, borderaxespad=0.)
#删除
ax.get_legend().remove()

# 改变某个指定框的颜色   
#Change the appearance of that box
# mybox1 = ax.artists[-6]
# mybox1.set_facecolor('red')
# 改变某个指定框线的颜色
# mybox.set_edgecolor('black')
# mybox.set_linewidth(3)

pic_dir="F:\\snow_related\\pic\\snow_all\\" 
plt.savefig(pic_dir+filename+'.jpg', dpi=1000, bbox_inches = 'tight')

plt.show() #先保存才能plot.show