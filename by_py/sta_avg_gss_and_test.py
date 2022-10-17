# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 11:27:54 2022
计算并检验TC影响下站点平均gss，并计算异常值
@author: Lenovo
"""
from scipy import stats
import pandas as pd

# 读取高原站点总体均值
popl=pd.read_table("F:\\snow_sts_data\\1981-2020\\sta_avg_gss_all.txt",
                          sep='\s+',na_values=32700)
popl_avg=popl[['station','gss']]
popl_avg.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行


# 读取风暴数据
need=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_pre_gss.txt",
                          sep='\s+',na_values=32700)
#不必 这里用不上 将积雪深度增量负值替换为缺失值


# 均值的显著性检验
info=[]
g1=need.groupby(['station'])
for group_name, group_eles in g1:
    # print(group_name)
    newline = ['station','p']
    samp_pick=group_eles.gss
    popl_pick=float(popl_avg[popl_avg['station']==group_name]['gss'])
    # print(popl_pick)
    samp_pick.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行
    _,p = list(stats.ttest_1samp(samp_pick, popl_pick))
    newline[0]=group_name
    newline[1]=float(p)    
    info.append(newline)
info1=pd.DataFrame(info,columns=['station','p'])

def get_sig(x):
    if x['p']<0.05: 
        return 1
    else:
        return 0
info1.loc[:, 'sig'] = info1.apply(get_sig, axis=1) 

#计算各站点平均降雪强度
snow_avg=need.groupby(by=['station'])['gss'].mean()
#添加位置信息，法二
path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat','alti'])
#拼接
sta.set_index('station', inplace=True) # column 改为 index
popl_avg.columns=['station','popl_avg']
popl_avg.set_index('station', inplace=True) # column 改为 index
info2=pd.concat([sta,snow_avg,popl_avg],axis=1,join="inner") #和80个站点信息取交集
info1.set_index('station', inplace=True) # column 改为 index
info3=pd.concat([info2,info1],axis=1)
info4=info3.reset_index()
info4.drop(['p'],axis=1,inplace=True)
info4.loc[:,'dev']=info4['gss']-info4['popl_avg']

#写入文件
info4.to_csv("F:\\snow_sts_data\\1981-2020\\sta_avg_gss.txt",
                    index = False,sep=' ',na_rep=32700)


# =============================================================================
# # 测试某些有dailypre但p为nan的站点
# w=need[need['station']==52707]

# # 测试某个值以下占多少百分比
# info4=info3['gss'].dropna(axis=0, inplace=False) #删除任何有nan的行 
# per_nonan=info4.quantile([0,0.25,0.5,0.75,0.8,0.9,0.95,1]) 

# info5=info4['gss']
# per_younan=info5.quantile([0,0.25,0.5,0.75,0.8,0.9,0.95,1]) 
# print(per_younan)

# #实测，不管有nan无nan 百分位数计算结果相同 前提是去掉的nan真的是你要计算的那列数据
# =============================================================================


# =============================================================================
# 测试某个值以下占多少百分比
info5=info4['gss']
per_younan=info5.quantile([0,0.25,0.5,0.75,0.8,0.9,0.95,1]) 
print('积雪深度均值的百分位数: \n{}'.format(per_younan))
count=5
info6=info4[info4['gss']<count]
print("小于"+str(count) +"cm的站点数： "+str(len(info6)))

# #实测，用df计算百分位数 不管有nan无nan 百分位数计算结果相同 
# #前提是去掉的nan真的是你要计算的那列数据

info55=info4[info4['dev']>0]
print("积雪异常增强的站点数： "+str(len(info55)))
print("其中显著增强的站点数： "+str(len(info55[info55['sig']==1])))

