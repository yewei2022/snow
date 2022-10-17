# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 19:50:52 2022
海拔高度分布箱线图
高原总体的 风暴影响下的
@author: Lenovo
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from scipy import stats

#%% 

filename="snow_alti"
df1=pd.read_table("F:\\snow_sts_data\\1981-2020\\"+filename+"_all.txt",
                          sep='\s+',na_values=32700)
df2=pd.read_table("F:\\snow_sts_data\\1981-2020\\"+filename+".txt",
                          sep='\s+',na_values=32700)

data = pd.DataFrame({"All": df1['alti'], "TC influencing": df2['alti']}) 
print(df1['alti'].mean())
print(df2['alti'].mean())


# 3761.762756056496
# 3966.4623552123553
# 样本与总体的均值差异性显著

# TC影响下降雪站点的海拔高度均值的显著性检验
popl_pick=df1['alti'].mean()
samp_pick=df2['alti']
samp_pick.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行
_,p = list(stats.ttest_1samp(samp_pick, popl_pick))

if p<0.05: 
    print("样本与总体的均值差异性显著")
else:
    print("不显著！")
    

#%% 画图
       
plt.figure(figsize=(2.25,2))#绘制画布

sns.set_style('ticks')
# # 风格设置，选择包括："white", "dark", "whitegrid", "darkgrid", "ticks"
pal=['#75bbfd','#15b01a']
sns.boxplot(data=data,width=0.4,saturation=0.9,fliersize=1.0,showmeans=True,
            flierprops={'marker':'x','markerfacecolor':'red'},
            meanprops={'marker':'o','markersize':5,'markerfacecolor':'black'},
            capprops=dict(color='red',linewidth=1.0),palette=pal)

# plt.xticks(ticks=[0,1,2,3],labels=["Grade1","Grade2","Grade3","Grade4"])
plt.yticks(range(0,5050,500))
#whis默认值为whis=1.5,
#IQR(Inter-Quartile Range)=Q3-Q1
#上限为数列中不超过Q3+1.5*IQR的最大值，下限为数列中不小于Q1-1.5*IQR的最小值
plt.ylabel("Alti (m)") 
# plt.xlabel("Grade") # 我们设置横纵坐标的标题

plt.ylim([2000,5000]) #设置坐标上下限

y_minor_locator=MultipleLocator(100)
ax = plt.gca()#获取大图边框
ax.yaxis.set_minor_locator(y_minor_locator)
ax.spines['top'].set_color('black')  
ax.spines['bottom'].set_color('black')  
ax.spines['left'].set_color('black')  
ax.spines['right'].set_color('black')  

handles, labels = ax.get_legend_handles_labels()

pic_dir="F:\\snow_related\\pic\\snow_all\\" 
# plt.savefig(pic_dir+filename+'.jpg', dpi=1000, bbox_inches = 'tight')
plt.savefig(pic_dir+filename+'.eps', dpi=1000, bbox_inches = 'tight')

plt.show() #先保存才能plot.show