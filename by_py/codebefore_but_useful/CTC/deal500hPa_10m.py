# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 16:56:54 2021

@author: Lenovo
"""
import pandas as pd


#%% 读取500位势高度，标准化，并赋予序号 改三处 文件处

# import pandas as pd

# pth='snow'
# df1=pd.read_table("F:\\snow_sts_data\\CTC\\"+pth+"\\geopotential_group.txt",
#                       header=None,sep=',')
# df1.dropna(axis=1, how='any',inplace=True) #删除最后一列空白值
# # geo500 = 1.0*(df1 - df1.mean())/df1.std() #标准化，适用于有极端值的情况
# geo500=df1 #不标准化

# df2=pd.read_table("F:\\snow_sts_data\\CTC\\"+pth+"\\u10_group.txt",
#                       header=None,sep=',')
# df2.dropna(axis=1, how='any',inplace=True) #删除最后一列空白值
# # u500 = 1.0*(df2 - df2.mean())/df2.std() #标准化，适用于有极端值的情况
# u500=df2

# df3=pd.read_table("F:\\snow_sts_data\\CTC\\"+pth+"\\v10_group.txt",
#                       header=None,sep=',')
# df3.dropna(axis=1, how='any',inplace=True) #删除最后一列空白值
# # v500 = 1.0*(df3 - df3.mean())/df3.std() #标准化，适用于有极端值的情况
# v500=df3

# date_id=pd.read_table("F:\\snow_sts_data\\CTC\\"+pth+"_date.txt",
#                     usecols=["time"],sep=' ') 
# npts=len(date_id)
# add = list(range(npts+1))
# date_id['time']=add[1:npts+1]

# geo500_id= pd.concat([date_id,geo500],axis=1)
# geo500_id.to_csv("F:\\snow_sts_data\\CTC\\"+pth+"\\geo500_id_group.txt",
#                     index=False,header=False,sep=" ")
# u500_id= pd.concat([date_id,u500],axis=1)
# u500_id.to_csv("F:\\snow_sts_data\\CTC\\"+pth+"\\u10_id_group.txt",
#                     index=False,header=False,sep=" ")
# v500_id= pd.concat([date_id,v500],axis=1)
# v500_id.to_csv("F:\\snow_sts_data\\CTC\\"+pth+"\\v10_id_group.txt",
#                     index=False,header=False,sep=" ")


#%% 根据分类结果，把日期对应上去 

# import pandas as pd

# pth="snow"
# file_date="F:\\snow_sts_data\\CTC\\"+pth+"_date.txt"
# file_catelog= "F:\\snow_sts_data\\CTC\\"+pth+"\\catelog.txt"
# date=pd.read_csv(file_date,sep="\s+",usecols=['time'])
# catelog = pd.read_csv(file_catelog,sep="\s+",header=None,usecols=[1],
#                       names=['type'])
# date_cate=pd.concat([date,catelog],axis=1)
# a=date_cate[date_cate['type']==2]

# date_cate.to_csv("F:\\snow_sts_data\\CTC\\"+pth+"\\"+pth+"_CTC_group.txt",
#                     index = False,sep=' ') 



#%% 计算解释方差 并绘图
#https://zhuanlan.zhihu.com/p/91501674
#https://blog.csdn.net/qq_20135597/article/details/95247381

# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.decomposition import PCA

# pth="extrm"
# pic_dir="F:\\snow_related\\pic\\CTC\\"+pth+"_mydown\\PCA_Var_"+pth+"_mydown.jpg"

# df1=pd.read_table("F:\\snow_sts_data\\CTC\\"+pth+"\\geopotential_mydown.txt",
#                       header=None,sep=',')
# df2=pd.read_table("F:\\snow_sts_data\\CTC\\"+pth+"\\u_mydown.txt",
#                       header=None,sep=',')
# df3=pd.read_table("F:\\snow_sts_data\\CTC\\"+pth+"\\v_mydown.txt",
#                       header=None,sep=',')

# # print(np.isnan(scaled_df).any()) #检查是否有缺失值 True 有
# # print(np.isfinite(scaled_df).all())#检查是否有无穷数据 结果False 没有
# #-------------------------缺失值处理-----------------
# # df1=df.iloc[:,-1] #发现最后一列全是nan
# # df.drop(df.columns[len(df.columns)-1], axis=1, inplace=True)#删除指定列，最后一列
# #发现原数据多了一列空白值
# df1.dropna(axis=1, how='any',inplace=True) #删除最后一列空白值
# df2.dropna(axis=1, how='any',inplace=True) #删除最后一列空白值
# df3.dropna(axis=1, how='any',inplace=True) #删除最后一列空白值

# df=pd.concat([df1,df2,df3],axis=1)

# classnum=8
# pca = PCA(n_components = classnum) 
# x_pca = pca.fit_transform(df) 
# #fit训练，求训练集X的均值，方差，最大值，最小值等；transform，fit基础上标准化归一化
# percent_variance=pca.explained_variance_ratio_
# print('各主成分贡献度:{}'.format(percent_variance))
# print('各主成分累计贡献度:{}'.format(np.cumsum(percent_variance)))


# #画图
# plt.bar(x = range(1,classnum+1),height=percent_variance,
#         tick_label=["PC" + str(i) for i in range(1,classnum+1)])
# plt.ylabel('Percentate of Variance Explained')
# plt.xlabel('Principal Component')
# # plt.title('PCA Scree Plot')
# plt.savefig(pic_dir, dpi=1000, bbox_inches = 'tight')




