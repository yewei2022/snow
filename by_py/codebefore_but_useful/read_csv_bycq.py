# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 11:25:40 2022
计算四十年积雪
@author: YEWEI
"""

import pandas as pd
import datetime

#%%读取积雪
info=pd.read_csv("E:\\f\\at_home\\1980-2021.csv",
                 usecols=['Datetime','Station_Id_d','Snow_Depth'])
#读取高原站点
path_sta='E:\\f\\snow_sts_data\\tp_sta_info.txt'
stainfo=pd.read_table(path_sta,sep = ",")
info1 =info[info.Station_Id_d.isin(stainfo.station)].reset_index(drop=True)
info1.loc[:,'Datetime']=pd.to_datetime(info1['Datetime'])

# 用于测试
original_56257=info1[info1['Station_Id_d']==56257]

info1.set_index('Datetime', inplace=True) # Datetime 列改为 index

# # #这个part写成函数
# info2=info1[info1['Station_Id_d']==56227]
# info2_shift=info2.shift(periods=-1, freq="D") #时间后移一天
# info2.loc[:,'gss_inc']=info2['Snow_Depth']-info2_shift['Snow_Depth']

def f(group):
    group_shift=group.shift(periods=-1, freq="D") #时间前移一天
    return pd.DataFrame({'gss_inc': group_shift-group})
gssinc=info1.groupby(by='Station_Id_d')['Snow_Depth'].apply(f)

# 用于测试
gssinc_reset=gssinc.reset_index() 
shift_56257=gssinc_reset[gssinc_reset['Station_Id_d']==56257]

info2=info1.reset_index()
info2.set_index(['Station_Id_d','Datetime'],inplace=True) #设置双索引
df_gss = pd.concat([info2,gssinc],axis=1)
df_gss.reset_index(inplace=True)
df_gss.loc[:,'Datetime']=df_gss['Datetime'].dt.strftime("%Y%m%d")
df_gss1 = df_gss.sort_values(by='Datetime', ascending=True)
df_gss1.to_csv(r"E:\\f\\at_home\\gss1980_2021.txt",index = False,
                sep=' ',na_rep=32700)

#用于测试
final_56257=df_gss1[df_gss1['Station_Id_d']==56257] 
