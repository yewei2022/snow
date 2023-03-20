# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 20:11:27 2023
做回归分析
样本量至少应有自变量数量的2-3倍
最终用R来做 R的结果与这里相同
# https://blog.csdn.net/YangMax1/article/details/120812509
@author: Lenovo
"""
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor


#%% branch1 最小二乘法建立线性回归模型 
sta=pd.read_table("F:\\snow_sts_data\\regress\\sta_snow\\record.txt",
                  sep='\s+')
sta1=sta[sta['len']>=15]
station=52645


# reg_info=[]
# for station in sta1.station.tolist():
#     print(station)

#======================可缩进=================================
df=pd.read_table("F:\\snow_sts_data\\regress\\sta_snow\\"+str(station)
                  +".txt", 
                  sep='\s+',usecols=['pre','rh','tcdist','WRPI','IBTI','tmp'])

# #读取数据的基础信息
# print(df.info())
# # 判断数据中是否存在重复观测
# print(df.duplicated().any())
# # 判断各变量中是否存在缺失值
# print(df.isnull().any(axis = 0))
# # 各变量中缺失值的数量
# print(df.isnull().sum(axis = 0))
# # 各变量中缺失值的比例
# print(df.isnull().sum(axis = 0)/df.shape[0])

model = smf.ols(formula='pre ~ rh + tcdist + WRPI + IBTI + tmp ', data=df)
modelfit =model.fit()
print(modelfit.summary()) 
#============================================================    
    
    
    # # 导出结果
    # # https://zhuanlan.zhihu.com/p/576081003?utm_id=0
    # # https://blog.csdn.net/weixin_43230383/article/details/121607538
    
    # # df_out = pd.concat((modelfit.params, modelfit.pvalues), axis=1)
    # # df_out.columns=['coef', 't_p']
    # # df_out0=df_out.round(2) #保留两位小数
    # df_out1 = pd.DataFrame((station,modelfit.rsquared, round(modelfit.f_pvalue,3)),
    #                         index=['station','R2','F_p'])
    # reg_info.append(df_out1)

# reg_info1 = pd.concat(reg_info,axis=1,ignore_index=True)
# reg_info2 = reg_info1.T 
 


#%% 如何得到均方根误差

# https://www.cnpython.com/qa/1448120
# https://www.statsmodels.org/stable/generated/statsmodels.regression
# .linear_model.RegressionResults.html

# 法一：不知道这都是些啥
# rmse_model = np.sqrt(modelfit.mse_model)
# print('rmse_model: \n{}'.format(rmse_model))
# rmse_resid = np.sqrt(modelfit.mse_resid)
# print('rmse_resid: \n{}'.format(rmse_resid))
# rmse_total = np.sqrt(modelfit.mse_total)
# print('rmse_total: \n{}'.format(rmse_total))

# 法二：随便测试一条 都不对 rmse出来的竟然是一列数而不是一个数
# # https://www.statsmodels.org/stable/tools.html

# from statsmodels.tools.eval_measures import rmse
# X = df[['hgt0C','prs','rh','tcdist','tmp']]
# Y_predict=modelfit.predict(X)
# # predict_y=modelfit.predict(X)
# rmse1 = rmse(df[["pre"]], modelfit.predict(X))
# rmse2= np.sqrt(np.mean(rmse1)) 

# 法三：用sklearn 感觉这个是对的
# https://blog.csdn.net/weixin_42163563/article/details/124696448

# from sklearn.metrics import mean_squared_error
# X = df[['hgt0C','prs','rh','tcdist','tmp']]
# Y_predict=modelfit.predict(X)
# rmse=mean_squared_error(df[["pre"]], Y_predict)
# print('均方根误差或标准误差: \n{}'.format(rmse))


#%%  branch2 拟合效果不好 看是否存在多重共线性

# #  相关性
# xdata = df[['hgt0C','prs','rh','tcdist','tmp']]
# print(xdata.corr())


# # 方差膨胀因子VIF 
# exog = model.exog #获取自变量矩阵（第一列为截距项）
# exog_names = model.exog_names #获取自变量名称（第一个为截距项）

# vif = []
# for i in range(exog.shape[1]-1):
#     vif.append(variance_inflation_factor(exog,i+1))
#     print(f'{exog_names[i+1]} 的方差膨胀因子VIF = {vif[i]}')
