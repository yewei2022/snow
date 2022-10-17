# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 20:01:38 2022

@author: Lenovo
"""

#%% K均值聚类 结果保存至all_tc_label.txt tp_tc_label.txt extrm_tc_label.txt

import pandas as pd
import math
from sklearn.cluster import KMeans

# 计算各参数
info=pd.read_table('F:\\snow_sts_data\\TC\\BoB_ymdh_bjt_lon_lat.txt',sep='\t')
# 质心
info['wi']=info['wind'].apply(lambda x: math.sqrt(x))
wi_sum = info.groupby(by=['tc_id'])['wi'].sum() 
info['wixi']= info['wi']*info['lon_tc']
wixi_sum = info.groupby(by=['tc_id'])['wixi'].sum() 
xba=wixi_sum/wi_sum
xba.name = "xba"

info['wiyi']= info['wi']*info['lat_tc']
wiyi_sum = info.groupby(by=['tc_id'])['wiyi'].sum() 
yba=wiyi_sum/wi_sum
yba.name = "yba"

info.set_index('tc_id', inplace=True)
info_xba=pd.concat([info,xba],axis=1)
info_xba_yba=pd.concat([info_xba,yba],axis=1).reset_index()

info_xba_yba['varx_topi']=(info_xba_yba['lon_tc']-info_xba_yba['xba'])**2\
    *info_xba_yba['wi']  
info_xba_yba['vary_topi']=(info_xba_yba['lat_tc']-info_xba_yba['yba'])**2\
    *info_xba_yba['wi']

varx=info_xba_yba.groupby(by=['tc_id'])['varx_topi'].sum()/wi_sum
varx.name = "varx" 

vary=info_xba_yba.groupby(by=['tc_id'])['vary_topi'].sum()/wi_sum 
vary.name = "vary" 

info_xba_yba['varxy_topi']=(info_xba_yba['lon_tc']-\
 	info_xba_yba['xba'])*(info_xba_yba['lat_tc']-info_xba_yba['yba'])\
    *info_xba_yba['wi']
varxy=info_xba_yba.groupby(by=['tc_id'])['varxy_topi'].sum()/wi_sum
varxy.name = "varxy" 
end_pos0=info_xba_yba.drop_duplicates("tc_id", keep='last')\
    .reset_index(drop=True)
end_posx=end_pos0['lon_tc']
end_posy=end_pos0['lat_tc']
end_posx.index=end_pos0['tc_id']
end_posy.index=end_pos0['tc_id']

df = pd.concat([xba,yba,varx,vary,varxy,end_posx,end_posy],axis=1) 
# df_zs=df.apply(lambda x : (x-np.min(x))/(np.max(x)-np.min(x)))#归一化
df_zs = 1.0*(df - df.mean())/df.std() #标准化，适用于有极端值的情况

dm=df_zs.reset_index() #为了下一步
# initdf=dm.loc[(dm['tc_id']==201203)|(dm['tc_id']==201004)|(dm['tc_id']==200903)]
# initdf.set_index('tc_id', inplace=True) # column 改为 index

#daaframe to array,其实不用
# traj = np.array(df_zs) # 或者traj=df_zs.values #取数值
# init=np.array(initdf)
traj = df_zs 
# init=initdf

km = KMeans(n_clusters=3,random_state=150)#构造聚类器,random_state=150

# km = KMeans(n_clusters=3,init=init,n_init=1,random_state=150)#构造聚类器,random_state=150
km.fit(traj)#聚类,init=init,n_init=1
# label = km.labels_ #获取聚类标签
label=km.predict(traj)#分组结果

# # #测试 聚类为2类最优 S局部最大，SSE拐点 绘图
# 参考https://blog.csdn.net/weixin_43718084/article/details/90273463
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
# 轮廓系数
from sklearn.metrics import silhouette_score  

plt.figure(figsize=(4,4))#绘制画布
  
S = []  # 存放轮廓系数
num = range(2,10)#分别模拟k为2~9的情况
for i in num:
    kmeans = KMeans(n_clusters=i,random_state=150)  # 构造聚类器
    kmeans.fit(traj)
    S.append(silhouette_score(traj,kmeans.labels_,metric='euclidean'))
    # silhouette_score()计算每类所有点的平均轮廓系数，而silhouette_samples()返回每个点的轮廓系数
    
    
plt.plot(num,S,'r*:')#'b*:'为线的格式设置，b表示蓝色，*为点的标记，:表示线型为点状线条。
plt.xlabel('k',fontsize=12,fontproperties='Helvetica')
plt.ylabel('S',fontsize=12,fontproperties='Helvetica')
# plt.title('find the best K value')
plt.tick_params(labelsize=12) #坐标轴标签字号

x_minor_locator=MultipleLocator(1)
ax = plt.gca()#获取大图边框
ax.xaxis.set_minor_locator(x_minor_locator)

# plt.text(1.56,0.319,'(a)', fontsize=13,color = 'black')


pic_dir="F:\\snow_related\\pic\\tc\\"
plt.savefig(pic_dir+'路径分类轮廓系数.jpg', dpi=1000, bbox_inches = 'tight')
plt.show()

# SSE误差平方和绘图
num = range(1,10)#分别模拟k为1~9的情况

plt.figure(figsize=(4,4))#绘制画布

sse_result=[]#用于存放每种k聚类后的SSE
for k in num:
    kmeans=KMeans(n_clusters=k)
    kmeans.fit(traj)
    sse_result.append(kmeans.inertia_)#inertia_表示样本到最近的聚类中心的距离总和。
    
    
plt.plot(num,sse_result,'b*:')#'b*:'为线的格式设置，b表示蓝色，*为点的标记，:表示线型为点状线条。
plt.xlabel('k',fontsize=12,fontproperties='Helvetica')
plt.ylabel('SSE',fontsize=12,fontproperties='Helvetica')
plt.tick_params(labelsize=12) #坐标轴标签

x_minor_locator=MultipleLocator(1)
ax = plt.gca()#获取大图边框
ax.xaxis.set_minor_locator(x_minor_locator)

# plt.text(0.6,1036,'(b)', fontsize=13,color = 'black')

plt.savefig(pic_dir+'路径分类误差平方和.jpg', dpi=1000, bbox_inches = 'tight')
plt.show()
    

dm['label']=label
num_label_all=dm['label'].value_counts()

tp_tc=pd.read_table("F:\\snow_sts_data\\TC\\tc_date_infl.txt",sep=' ')
tp_tc.sort_values(by='tc_id', ascending=True,inplace=True)

tc_need =dm[dm.tc_id.isin(tp_tc.tc_id)]
tc_need.set_index('tc_id', inplace=True) # column 改为 index
tp_tc.set_index('tc_id', inplace=True)
d1=pd.concat([tp_tc,tc_need],axis=1)
d2=d1.reset_index()
d3=d2[['tc_id','label']]

num_label_tp=d3['label'].value_counts()

extrm_tc=pd.read_table("F:\\snow_sts_data\\TC\\tc_date_infl_extrm.txt",sep=' ')
extrm_tc.sort_values(by='tc_id', ascending=True,inplace=True)
extrm_need =dm[dm.tc_id.isin(extrm_tc.tc_id)]
extrm_need.set_index('tc_id', inplace=True) # column 改为 index
extrm_tc.set_index('tc_id', inplace=True)
d11=pd.concat([extrm_tc,extrm_need],axis=1)
d22=d11.reset_index()
d33=d22[['tc_id','label']]
num_label_extrm=d33['label'].value_counts()

print('所有TC分类',num_label_all)
print('影响TC分类',num_label_tp)
print('极端影响分类',num_label_extrm)

# dm.to_csv("F:\\snow_sts_data\\TC\\all_tc_label.txt",index = False,
#                 sep=' ',columns=['tc_id','label'])
# d3.to_csv("F:\\snow_sts_data\\TC\\tp_tc_label.txt",index = False,
#                 sep=' ',columns=['tc_id','label'])
# d33.to_csv("F:\\snow_sts_data\\TC\\extrm_tc_label.txt",index = False,
#                 sep=' ',columns=['tc_id','label'])



#%% branch4 根据label，生成三类路径的文件目录

# import pandas as pd

# catalog=pd.read_table("F:\\snow_sts_data\\TC\\tp_tc_label.txt",sep='\s+')
# catalog['prefix']='/mnt/f/snow_sts_data/BOB/bio'
# catalog['suffix']='.txt'
# catalog['filename']=catalog['prefix']+catalog['tc_id'].astype(str)\
#     +catalog['suffix']
# typeA=catalog[catalog['label']==0] 
# typeB=catalog[catalog['label']==1]
# typeC=catalog[catalog['label']==2] 
# typeA.to_csv("F:\\snow_sts_data\\TC\\typeA_catalog.txt",index=False,
#                 header=False,columns = ['filename'])
# typeB.to_csv("F:\\snow_sts_data\\TC\\typeB_catalog.txt",index=False,
#                 header=False,columns = ['filename'])
# typeC.to_csv("F:\\snow_sts_data\\TC\\typeC_catalog.txt",index=False,
#                 header=False,columns = ['filename'])
