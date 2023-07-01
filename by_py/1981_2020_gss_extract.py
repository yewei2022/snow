# -*- coding: utf-8 -*-
"""
逐行读取高原2016-2020的gss,再组合之前的1981-2015
reason：对于不规则的数组，逐行读取
"""
import pandas as pd
import os
import re
import numpy as np

#%% step1 提取2016-2020高原站点的积雪深度

# path_file='H:\\中国地面日值数据-2015-2021\\datasets\\2016-2020\\'
# path_save="F:\\snow_sts_data\\2016-2020\\GSS_snow\\"
# seq = re.compile("\s+")#设置中间间隔标识为\s+
# f_list = os.listdir(path_file)  
# for name in f_list:
#     # name='SURF_CHN_MUL_DAY-20160101.TXT'
#     file=open(path_file+name,'r',encoding='utf-8')#编码有问题，主要有中文，在记事本右下角看编码格式加utf-8
#     result=list()
#     for lines in file.readlines():
#             line=seq.split(lines.strip())
#             result.append(line[0:60])#读取txt文件前几列的数据
#     file.close()
        
#     d=[]
#     for i in range(len(result)):
#         d.append(result[i][2:-1]) #第三列到最后一列
#     c=d[0]
#     df = pd.DataFrame(d[1:-1][:], columns=c) #第二行到最后一行
#     info=df.loc[:,['Station_Id_C','Snow_Depth']]
#     path_sta='F:\\snow_sts_data\\station_pick\\TP_sta_info_by2014.txt'
#     stainfo=pd.read_table(path_sta,sep = ",")
#     stainfo['station']=stainfo['station'].astype(str)
#     #挑选高原站点
#     dd =info[info.Station_Id_C.isin(stainfo.station)]
#     dd.loc[:,'Snow_Depth']=dd['Snow_Depth'].replace('999999','999990')
#     dd.loc[:,'time']=name[17:25]
#     dd1=dd.reset_index(drop=True)
#     dd1.loc[:,'Snow_Depth']=dd1['Snow_Depth'].astype(float)
#     dd1.to_csv(path_save+name,index = False,sep = "\t",na_rep=999990)

 
#%% step2 分别读取两个时间段的数据，组合1981-2020高原站点的积雪深度

# path_gss1="F:\\snow_sts_data\\1981-2015\\GSS_snow\\"
# gss_list1 = os.listdir(path_gss1)
# gss1=[]
# for file in gss_list1:
#     gss1.append(pd.read_table(path_gss1+file,sep = "\t",encoding='utf-8',
#                               na_values=32766)) 
# # !!! 原始数据中32766是缺测
# gss_df1 = pd.concat(gss1,ignore_index=True)
# # #add 0 before number
# yy=gss_df1['yy'].apply(lambda x : '{:0>4d}'.format(x))
# mm=gss_df1['mm'].apply(lambda x : '{:0>2d}'.format(x))
# dd=gss_df1['dd'].apply(lambda x : '{:0>2d}'.format(x))
# time=yy+mm+dd
# gss_df1['time'] =time  # or snow_df1.loc[:, 'time'] = time 
# gss_df1.drop(columns = ['yy','mm','dd','Q'],inplace = True)

# path_gss2="F:\\snow_sts_data\\2016-2020\\GSS_snow\\"
# gss_list2 = os.listdir(path_gss2)
# gss2=[]
# for file in gss_list2:
#     gss2.append(pd.read_table(path_gss2+file,sep = "\t",encoding='utf-8',
#                               na_values=999990))
# gss_df2 = pd.concat(gss2,ignore_index=True) #变成dataframe
# # gss_df2.drop(columns = ['Station_Id_d'],inplace = True)
# gss_df2.columns=['station','gss','time']
# gss_df =pd.concat([gss_df1,gss_df2],ignore_index=True)
# gss_df.loc[:,'gss']=gss_df['gss'].replace(32700,0) 
# # !!! 原始数据中的32700代表微量
# gss_df.to_csv("F:\\snow_sts_data\\1981-2020\\gss_all.txt",index = False,
#                 sep='\t',na_rep=32700)


#%% step3 calculate gss_inc 后一天减去前一天的值，标记为前一天的时间（应该是吧？）

# info=pd.read_table("F:\\snow_sts_data\\1981-2020\\gss_all.txt",
#                   usecols=['time','station','gss'],na_values=32700)

# info.dropna(axis=0, how='any',inplace=True) #去掉station gss time中有缺测值的行 

# info['station']=info['station'].astype(int)

# # 去重 否则之后concat索引混乱
# info1=info.drop_duplicates(["station","time"], 
#                                           keep='first').reset_index(drop=True)
# #一定记得这里要先转成字符串才能转换成时间
# info1.loc[:,'time']=pd.to_datetime(info1['time'].astype(str)) 

# info1.set_index('time', inplace=True) # Datetime 列改为 index

# def f(group):
#     group_shift=group.shift(periods=-1, freq="D") #时间前移一天
#     return pd.DataFrame({'gss_inc': group_shift-group})
# gssinc=info1.groupby(by='station')['gss'].apply(f)

# info2=info1.reset_index()
# info2.set_index(['station','time'],inplace=True) #设置双索引
# df_gss = pd.concat([info2,gssinc],axis=1)
# df_gss.reset_index(inplace=True)
# df_gss.loc[:,'time']=df_gss['time'].dt.strftime("%Y%m%d")
# df_gss1 = df_gss.sort_values(by='time', ascending=True)

# df_gss1.to_csv("F:\\snow_sts_data\\1981-2020\\gss1981_2020.txt",index = False,
#                 sep=' ',na_rep=32700)



    
    