# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 16:56:54 2021

@author: Lenovo
"""
import os  # os是用来切换路径和创建文件夹的。
# from shutil import copy  # shutil 是用来复制黏贴文件的
import shutil
import pandas as pd
import datetime

#%% branch1 #读取时间信息 #批量读取文件，根据时间复制相关时间的tbb文件至另一文件夹

# path_time='F:\snow_sts_data\\tc_tims_1h.txt' #时间精确到时
# tim0=pd.read_table(path_time) 
# tim1=tim0.loc[:,['tc_id','utc_init','utc_end']][tim0.tc_id>202000]\
#     [tim0.tc_id<202002]
# tc_id=tim1['tc_id'].astype(str).tolist()
# utc_init = tim1['utc_init'].astype(str).str[2:10].tolist()
# utc_end = tim1['utc_end'].astype(str).str[2:10].tolist()
# for i in range(len(tc_id)):
#     utc1= datetime.datetime.strptime(utc_init[i], '%y%m%d%H') #字符串变时间
#     utc2= datetime.datetime.strptime(utc_end[i], '%y%m%d%H') #字符串变时间
#     tim_1h= pd.date_range(utc1,utc2,freq="H").strftime("%y%m%d%H").astype(str)
#     # tim_1h1=pd.DataFrame(tim_1h0)
#     # tim_1h=tim_1h1[0].astype(str).str[1:8]
    
#     newname1='TBB_'+tim_1h+'.grd'
#     newname=list(set(newname1)) #Delete duplicate elements
#     #注意1999年的格式grd前面有些有空格
    
#     # 源文件夹中的文件包含字符key则复制到to_dir_path文件夹中
#     for key in newname:    
#         src_dir_path = 'G:\\data\\TBB\\'+tc_id[i][0:4]       # 源文件夹    
#         to_dir_path = 'H:\\TBB-from-1998-of-BOB-TC\\datasets\\'+tc_id[i]   # 存放复制文件的文件夹
       
#         if not os.path.exists(to_dir_path):
#             print("to_dir_path not exist,so create the dir")
#             os.mkdir(to_dir_path,1)
#         if os.path.exists(src_dir_path):
#             print("src_dir_path exitst")
#             for file in os.listdir(src_dir_path):
#                 # is file
#                 if os.path.isfile(src_dir_path+'/'+file):
#                     if key in file:
#                         print('找到包含"'+key+'"字符的文件,绝对路径为----->'+src_dir_path+'/'+file)
#                         print('复制到----->'+to_dir_path+file)
#                         shutil.copy(src_dir_path+'/'+file,to_dir_path+'/'+file)



#%% branch2 #读取时间信息 #批量读取文件，根据时间复制相关时间的ERA5文件至另一文件夹

# # 读取时间
# file_date="F:\\snow_sts_data\\REOF\\spa_index.txt"
# date=pd.read_csv(file_date,sep="\s+",usecols=['time'])

# # 前一天的时间
# date.loc[:,'time']=pd.to_datetime(date['time'].astype(str)) 
# date1=date.set_index('time') # Datetime 列改为 index
# date2=date1.shift(periods=-1, freq="D") #时间前移一天
# date3=date2.reset_index(drop=False)
# # 合并两个时间 去掉重复时间
# date4=pd.concat([date,date3])
# date4.loc[:,'time']=date4['time'].dt.strftime("%Y%m%d")
# date5 = date4.sort_values(by='time', ascending=True)
# date6=date5.drop_duplicates(['time'],keep='first').reset_index(drop=True)

# date0=date6['time'].astype(str).tolist()  


# # # # 生成需要的时间
# # # yyyy = pd.date_range("1979-10-27 00:00","2009-10-27 00:00",
# # #                               freq="Y").strftime("%Y").to_list()
# # # yyyy_df=pd.DataFrame(yyyy,columns=["year"])
# # # mm ="1027"
# # # yyyy_df['date']=yyyy_df["year"]+mm
# # # date=yyyy_df.date.tolist()


# fromdirname =  ['I:\\ERA5\\10m_u_component_of_wind\\','I:\\ERA5\\10m_v_component_of_wind\\',
#                 'G:\\geopotential\\','G:\\u_component_of_wind\\',
#                 'G:\\v_component_of_wind\\','G:\\specific_humidity\\']
# varname=['era5.10m_u_component_of_wind.','era5.10m_v_component_of_wind.',
#           'era5.geopotential.','era5.u_component_of_wind.',
#           'era5.v_component_of_wind.','era5.specific_humidity.']
# todirname =  ['10u','10v','geopotential', 'u', 'v','q']

# newname=[]
# i=2
# # for i in range(0,4):
# for day in date0: 
#     newname.append(varname[i]+day+'.nc')
    
# # 源文件夹中的文件包含字符key则复制到to_dir_path文件夹中
# for key in newname:    
#     src_dir_path = fromdirname[i]     # 源文件夹    
#     to_dir_path = 'F:\\snow_sts_data\\ERA5\\'+todirname[i]+'\\'   # 存放复制文件的文件夹
   
#     if not os.path.exists(to_dir_path):
#         print("to_dir_path not exist,so create the dir")
#         os.mkdir(to_dir_path,1)
#     if os.path.exists(src_dir_path):
#         print("src_dir_path exitst")
#         for file in os.listdir(src_dir_path):
#             # is file
#             if os.path.isfile(src_dir_path+'/'+file):
#                 if key in file:
#                     print('找到包含"'+key+'"字符的文件,绝对路径:'+src_dir_path+file)
#                     print('复制到:'+to_dir_path+file)
#                     shutil.copy(src_dir_path+file,to_dir_path+file)


#%% branch3 #读取时间信息 #批量读取所有tc活动日数文件，根据时间复制相关时间的ERA5文件至另一文件夹

# 读取时间
file_date="F:\\snow_sts_data\\TC\\all_tc_days.txt"
date=pd.read_csv(file_date,sep="\s+",usecols=['bjt'])

# 前一天的时间
date.loc[:,'bjt']=pd.to_datetime(date['bjt'].astype(str)) 
date1=date.set_index('bjt') # Datetime 列改为 index
date2=date1.shift(periods=-1, freq="D") #时间前移一天
date3=date2.reset_index(drop=False)
# 合并两个时间 去掉重复时间
date4=pd.concat([date,date3])
date4.loc[:,'bjt']=date4['bjt'].dt.strftime("%Y%m%d")
date5 = date4.sort_values(by='bjt', ascending=True)
date6=date5.drop_duplicates(['bjt'],keep='first').reset_index(drop=True)

date0=date6['bjt'].astype(str).tolist()  

# # 少了一个文件 测试 19820430
# path_file='F:\\snow_sts_data\\ERA5\\all\\geopotential\\'
# f_list = os.listdir(path_file) 
# f_list1=[]
# for f in f_list:
#     f_list1.append(str(f)[18:26])
    
# set1=set(date0)
# set2=set(f_list1)
# print(set3=set1^set2)


fromdirname =  ['G:\\geopotential\\','H:\\u_component_of_wind\\',
                'H:\\v_component_of_wind\\','H:\\specific_humidity\\',
                'G:\\relative_humidity\\','H:\\temperature\\']
varname     =  ['era5.geopotential.','era5.u_component_of_wind.',
              'era5.v_component_of_wind.','era5.specific_humidity.',
              'era5.relative_humidity.', 'era5.temperature.']
todirname   =  ['geopotential', 'u', 'v','q','rh','tmp']

newname=[]
i=5
# for i in range(0,4):
for day in date0: 
    newname.append(varname[i]+day+'.nc')
    
# 源文件夹中的文件包含字符key则复制到to_dir_path文件夹中
for key in newname:    
    src_dir_path = fromdirname[i]     # 源文件夹    
    to_dir_path = 'F:\\snow_sts_data\\ERA5\\all\\'+todirname[i]+'\\'   # 存放复制文件的文件夹
   
    if not os.path.exists(to_dir_path):
        print("to_dir_path not exist,so create the dir")
        os.mkdir(to_dir_path,1)
    if os.path.exists(src_dir_path):
        print("src_dir_path exitst")
        for file in os.listdir(src_dir_path):
            # is file
            if os.path.isfile(src_dir_path+'/'+file):
                if key in file:
                    print('找到包含"'+key+'"字符的文件,绝对路径:'+src_dir_path+file)
                    print('复制到:'+to_dir_path+file)
                    shutil.copy(src_dir_path+file,to_dir_path+file)






   