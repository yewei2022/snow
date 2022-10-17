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

#%% branch1 
#读取文件，选取tc wind max 达到34 的tc文件复制至另一文件夹 不用 算了

tim0=pd.read_table('F:\\snow_sts_data\\TC\\BoB_ymdh_utc_lon_lat.txt') 
tim1=tim0.groupby(by=['tc_id'])['wind'].max().reset_index()
# tim2=tim1[tim1['wind']>34] 
    
    # newname1='TBB_'+tim_1h+'.grd'
    # newname=list(set(newname1)) #Delete duplicate elements
    # #注意1999年的格式grd前面有些有空格
    
    # # 源文件夹中的文件包含字符key则复制到to_dir_path文件夹中
    # for key in newname:    
    #     src_dir_path = 'F:\\snow_sts_data\\BOB'+tc_id[i][0:4]       # 源文件夹    
    #     to_dir_path = 'F:\\snow_sts_data\\BOBts'+tc_id[i]   # 存放复制文件的文件夹
       
    #     if not os.path.exists(to_dir_path):
    #         print("to_dir_path not exist,so create the dir")
    #         os.mkdir(to_dir_path,1)
    #     if os.path.exists(src_dir_path):
    #         print("src_dir_path exitst")
    #         for file in os.listdir(src_dir_path):
    #             # is file
    #             if os.path.isfile(src_dir_path+'/'+file):
    #                 if key in file:
    #                     print('找到包含"'+key+'"字符的文件,绝对路径为----->'+src_dir_path+'/'+file)
    #                     print('复制到----->'+to_dir_path+file)
    #                     shutil.copy(src_dir_path+'/'+file,to_dir_path+'/'+file)







   