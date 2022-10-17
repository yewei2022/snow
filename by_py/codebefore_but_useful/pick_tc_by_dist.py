# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 19:00:12 2021
计算站点到TC距离，根据R挑出风暴活动日在此范围内的站点
@author: Lenovo
"""
import os
import pandas as pd
from math import sin,radians,cos,asin,sqrt

#%%  pick TCs influencing each station
def SphereDistance(lon1, lat1, lon2, lat2):
    radius = 6371.0 # radius of Earth, unit:KM
    # degree to radians
    lon1, lat1,lon2, lat2 = map(radians,[lon1, lat1,lon2, lat2])
    dlon = lon2 -lon1
    dlat = lat2 -lat1
    arg  = sin(dlat*0.5)**2 +  \
            cos(lat1)*cos(lat2)*sin(dlon*0.5)**2
    dist = 2.0 * radius * asin(sqrt(arg))
    return dist

def pick_tc_inl(station,latSite,lonSite,f_list):
    tc_infl   = [] # 保存影响的台风编号
    tc_info = [] #保存影响时段的台风信息  
    for file in f_list:
        filepath =  path+file
        # print("Processing File : %s" %filepath )
        with open(filepath, 'r', encoding='UTF-8') as f1:
            lines = f1.readlines()
            numberTy= file[3:9] # typhoon number
            newLine = ['station','sta_lat','sta_lon','tc_id', 'time', 'lat', 'lon']
            for line in lines:
                data=line.split(',')
                yyymmddhh = data[2].strip()
                latRec    = float(data[6][0:4].strip())*0.1 #unit 1.0 degree
                lonRec    = float(data[7][0:5].strip())*0.1
                newLine[0] = station
                newLine[1] = latSite
                newLine[2] = lonSite                
                newLine[3] = numberTy
                newLine[4] = yyymmddhh
                newLine[5] = latRec
                newLine[6] = lonRec
                # print(newLine)
                #计算距离
                distTy2Site = SphereDistance(lonRec,latRec,lonSite,latSite)
                if distTy2Site > R:
                    # 影响半径外的台风，不计入
                    continue 
                else:
                    if newLine not in tc_info:
                        tc_info.append(newLine)
                    if numberTy not in tc_infl:
                        tc_infl.append(numberTy)
        f1.close
    out_info = pd.DataFrame(tc_info,columns=['station','sta_lat','sta_lon',
                                              'tc_id', 'time', 'lat', 'lon'])
    # out_info=new_info.drop_duplicates('tc_id', keep='first').reset_index(drop=True)
    out_info['lat'] = out_info['lat'].apply(lambda x: format(x, '.1f'))
    out_info['lon'] = out_info['lon'].apply(lambda x: format(x, '.1f'))

    # output
    print(tc_infl)
    print(len(tc_infl))
    if len(tc_infl) > 0:
        outFileName = "F:\\snow_sts_data\\site_by_tc\\"+str(station)+".txt"
        print("output data : ",outFileName)
        out_info.to_csv(outFileName, index = False,sep= '\t',encoding = "utf-8")


R = 2236 # influence radius ,unit:KM
path="F:\\snow_sts_data\\BOB\\"
f_list = os.listdir(path)

# station = '55960' 
# latSite = 27.98
# lonSite = 91.95
# pick_tc_inl(station,latSite,lonSite,f_list)

path_sta='F:\\snow_sts_data\\tp_sta_info.txt'
tp_sta_info=pd.read_table(path_sta,sep = ",")
# print(sta)
tp_sta=tp_sta_info['station'].tolist()
tp_lat=tp_sta_info['lat'].tolist()
tp_lon=tp_sta_info['lon'].tolist()
npts=len(tp_sta)
for i in range(0,npts):
    pick_tc_inl(tp_sta[i],tp_lat[i],tp_lon[i],f_list)
#%%  TC frequency influencing each station
# path="F:\\snow_sts_data\\site_by_tc\\"
# path_save="F:\\snow_sts_data\\sta_tc_f.txt"
# f_list = os.listdir(path)
# info=[]
# for file in f_list:
#     info.append(pd.read_table(path+file,sep = "\t"))
# df = pd.concat(info,ignore_index=True)
# df_tc_f=df['sta_lat'].groupby(df['station']).value_counts() #一列
# df_tc_f.to_csv(path_save,sep='\t')
# del df_tc_f
# df_tc_f=pd.read_table(path_save,sep = "\t",usecols=[0,2])
# df_tc_f.to_csv(path_save,sep='\t',index=False,header=['station','tc_f'])
# del df_tc_f
# df_tc_f=pd.read_table(path_save,sep = "\t")
# need_sta=df_tc_f['station'].tolist()
# dd =df[df.station.isin(need_sta)]
# dd_drop=dd.drop_duplicates('station', keep='first').reset_index(drop=True)
# dd_need=dd_drop[['sta_lat','sta_lon']]
# df_save=pd.concat([df_tc_f,dd_need],axis=1)
# df_save.to_csv(path_save,sep=',',index=False,columns=['station','sta_lat',
#                                                        'sta_lon','tc_f'])



