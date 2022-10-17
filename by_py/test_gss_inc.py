# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 10:53:14 2022
测试gss_inc有多少负值
@author: Lenovo
"""

#%% step 1 读取数据

# import pandas as pd

# snow_bytc=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_pre_gss.txt",
#                           sep='\s+',na_values=32700)
# def fill_existing2(x):
#     if (x["gss_inc"] <-30000 or x["gss_inc"]>=30000):
#         return None
#     else:
#         return x["gss_inc"]
# snow_bytc.loc[:,'gss_inc']= snow_bytc.apply(fill_existing2,axis=1)

# snow_all=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_pre_gss_all.txt",
#                           sep='\s+',na_values=32700)
# def fill_existing2(x):
#     if (x["gss_inc"] <-30000 or x["gss_inc"]>=30000):
#         return None
#     else:
#         return x["gss_inc"]
# snow_all.loc[:,'gss_inc']= snow_all.apply(fill_existing2,axis=1)

# w=snow_bytc[snow_bytc['station']==56227]

#%% 绘概率密度图

# import seaborn as sns
# import matplotlib.pyplot as plt

# sns.set_style('white')
# # 图表风格设置
# # 风格选择包括："white", "dark", "whitegrid", "darkgrid", "ticks"
# plt.figure(figsize=(5,4))#绘制画布
# sns.distplot(snow_bytc['gss_inc'],hist= False,kde = True,rug = True,
#               rug_kws = {'color':'goldenrod','lw':0.1,'alpha':0.5,'height':0.1} ,
#               # 设置数据频率分布颜色#控制是否显示观测的小细条（边际毛毯）
#               kde_kws={"color": 'goldenrod', "lw": 1.5, 'linestyle':'--'},
#               # 设置密度曲线颜色，线宽，标注、线形，#控制是否显示核密度估计图
#               label = 'Affected by TCs')
# sns.distplot(snow_all['gss_inc'],hist = False,kde = True,rug = True,
#               rug_kws = {'color':'g','lw':0.1,'alpha':0.5,'height':0.03} , 
#               kde_kws={"color": 'g', "lw": 1.5, 'linestyle':'--'},
#               label = 'All')

# ave_snow_bytc =snow_bytc['gss_inc'].mean()
# ave_snow_all  =snow_all['gss_inc'].mean()

# # plt.axvline(ave_snow_bytc,color='goldenrod',linestyle=":",alpha=0.8) 

# plt.text(4,0.5,'Affected by TCs: %.1fcm' % (ave_snow_bytc), 
#           color = 'goldenrod')

# # plt.axvline(ave_snow_all,color='g',linestyle=":",alpha=0.8)
# plt.text(4,0.4,'All: %.1fcm' % (ave_snow_all), color = 'g')

# # reference_line=0
# # plt.axvline(reference_line,color='red',linestyle=":",alpha=0.8) 

# plt.ylim([0,1.25]) #设置坐标上下限
# # plt.xlim([-100,100]) #设置坐标上下限
# plt.xlabel('SDI (cm)',fontsize=12)
# plt.ylabel('Density',fontsize=12)
# plt.grid(linestyle = '--')     # 添加网格线
# # plt.title("Distance between TCs and stations")  # 添加图表名

# plt.legend(fancybox=False) #显示并控制图例是指教还是圆角
# pic_dir="F:\\snow_related\\pic\\tc\\"
# plt.savefig(pic_dir+'测试gss_inc的概率密度图.jpg', dpi=750, bbox_inches = 'tight')
 
#%% 绘制 箱线图

# import seaborn as sns
# import matplotlib.pyplot as plt
# from matplotlib.pyplot import MultipleLocator

# plt.figure(figsize=(5,4))#绘制画布
# sns.set_style('ticks')
# # # 风格设置，选择包括："white", "dark", "whitegrid", "darkgrid", "ticks"
# data = pd.DataFrame({"All": snow_all['gss_inc'], 
#                      "Affected by TCs": snow_bytc['gss_inc']}) 
# sns.boxplot(data=data,width=0.4,saturation=0.8,fliersize=1.5,
#             capprops=dict(color='red',linewidth=1.0))

# # plt.yticks(range(0,5050,500))
# #whis默认值为whis=1.5,
# #IQR(Inter-Quartile Range)=Q3-Q1
# #上限为数列中不超过Q3+1.5*IQR的最大值，下限为数列中不小于Q1-1.5*IQR的最小值
# plt.ylabel("SDI (cm)") 
# # plt.xlabel("xlabel") # 我们设置横纵坐标的标题
# # y_minor_locator=MultipleLocator(100)
# # ax = plt.gca()#获取边框
# # ax.yaxis.set_minor_locator(y_minor_locator)
# # ax.spines['top'].set_color('black')  
# # ax.spines['bottom'].set_color('black')  
# # ax.spines['left'].set_color('black')  
# # ax.spines['right'].set_color('black')  
# pic_dir="F:\\snow_related\\pic\\tc\\"
# plt.savefig(pic_dir+'测试gss_inc的箱线图.jpg', dpi=750, bbox_inches = 'tight') 
