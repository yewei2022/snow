# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 22:41:38 2023
画不同第一主导因子所占比例 饼图
*获取dataframe某一行的最大值的列名称
* https://blog.csdn.net/weixin_42386361/article/details/118800235
*获取dataframe某一行的第n大值的列名称
*https://www.5axxw.com/questions/content/qrp2hw
* pyecharts绘图自己设置颜色
@author: Lenovo
"""


import pandas as pd
import os
import numpy as np


#%% 统计
pic_dir = "F:\\snow_related\\pic\\regress\\"        
path_file="F:\\snow_sts_data\\regress\\coef\\"
f_list1 = os.listdir(path_file)
info=[]
for file in f_list1:
    df_sta = pd.read_table(path_file+file,sep='\s+',usecols=[1,2,3,4],
                            index_col=0,na_values=32700)
    df_sta.loc['station', :] = file[0:5] 
    info.append(df_sta.loc[:,"lmg1"])
    
df = pd.concat(info,axis=1,ignore_index=True) #变成dataframe
df0 = df.T
df0.drop(['(Intercept)'],axis=1,inplace=True)
df0.columns = ['IBTI', 'RH','DIS','TEM','WRPI','station']
order = ['WRPI','IBTI','RH','DIS','TEM','station']
df0 = df0[order]
df0.loc[:,'station'] = df0['station'].astype(int)
df1 = df0.set_index(['station']) #设置索引

# 最大值 只能求行最大值列索引
df2 = df1.astype(float).idxmax(axis=1) #行最大值的列索引
df3 = pd.DataFrame(df2 , columns=['col_name'])

#第n大值均可求
n = 1
df1['col_name'] = df1.columns.to_numpy()[np.argsort(df1.to_numpy())[:, -n]]

#%%  保存文件

# #添加位置信息，法二 保存
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat','alti'])
# #拼接
# # print(df0['station']) #拼接的两个dataframe 行索引数据类型需相同
# # print(sta['station'])
# sta.set_index('station', inplace=True) # column 改为 index
# df11=pd.concat([sta,df1],axis=1,join="inner") #和80个站点信息取交集
# df2=df11.reset_index()
# #写入文件
# df2.to_csv("F:\\snow_sts_data\\regress\\lmg"+str(n)+".txt",
#                     index = False,sep=' ',na_rep=32700, 
#                     columns=['station','lon','lat','alti','col_name'])



#%%画图

from pyecharts.charts import Pie
from pyecharts import options as opts
from pyecharts.globals import ThemeType
theme = ThemeType.LIGHT #此处 改风格

df3 = df1
df_g1 = df3[df3['col_name']=='WRPI']
df_g2 = df3[df3['col_name']=='IBTI']
df_g3 = df3[df3['col_name']=='RH']
df_g4 = df3[df3['col_name']=='DIS']
df_g5 = df3[df3['col_name']=='TEM']
position=['WRPI','IBTI','RH','DIS','TEM']
Num0= [len(df_g1), len(df_g2),len(df_g3),len(df_g4),len(df_g5)]

Num=list(map(str,Num0))
data_pair = [list(z) for z in zip(position, Num)]
pie = Pie(init_opts=opts.InitOpts(theme=theme)) #主题颜色
# pie = Pie(init_opts=opts.InitOpts()) # 不要主题颜色 最后自己设置

pie.add(series_name=["Factor"],
        data_pair=data_pair,
        center=["48%", "50%"],
        radius=["30%", "75%"], #区分传统饼图和有圆圈的饼图
        rosetype= None,
        itemstyle_opts = None,
        # label_opts=opts.LabelOpts(is_show= True, position="center") #后面设置
        )

#全局设置
pie.set_global_opts(
    # #设置标题
    # title_opts=opts.TitleOpts(
    #     #名字
    #     title="",#标题无
    #     # #组件距离容器左侧的位置
    #     pos_left="center",
    #     # #组件距离容器上方的像素值
    #     pos_top="4%",
    #     #设置标题颜色
    #     title_textstyle_opts=opts.TextStyleOpts(color="black"),
    # ),
    #图例配置项
    legend_opts=opts.LegendOpts(
        orient="vertical", #图例垂直放置
        pos_top="12%",# 图例位置调整
        pos_left="80%",
        textstyle_opts=opts.TextStyleOpts(font_size=18,
              font_weight=700,font_family='Arial',color="black")),
)
#系列设置
pie.set_series_opts(
    tooltip_opts=opts.TooltipOpts(
        trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
    ),
    #标签设置
    label_opts=opts.LabelOpts(color="black",            # position 标签的位置
            is_show= True,            
            position="inside", # 文字也可在内部
            # 回调函数，回调函数格式：
            # (params: Object|Array) => string
            # 设置标签的显示样式
            # formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
            formatter="{per|{d}%}  ",
            font_family='Arial',
            distance = 0.5,
            # 背景颜色
            background_color='rgba(247,251,245,.0001)',#白色透明色
            # # 边框颜色
            # border_color="#aaa",
            # # 边框宽度
            # border_width=2,          
            # # 边框四角弧度
            # border_radius=4,
            rich={
            # "a": {"fontSize": 18,
            #       "fontWeight": 700,
            #       "color": "black",
            #       "lineHeight": 22,
            #       "align": "center" #对齐方式
            #       },
            
            
            # "abg": {
            #     "fontSize": 18,
            #     "fontWeight": 700,
            #     "backgroundColor": "#e3e3e3", 
            #     "width": "100%",
            #     "align": "right",
            #     "height": 22,
            #     "borderRadius": [4, 4, 0, 0],
            #       },
            
            
            # "hr": {
            #     "fontSize": 18,
            #     "fontWeight": 700,
            #     "borderColor": "#aaa",
            #     "width": "100%",
            #     "borderWidth": 0.5,
            #     "height": 0,
            #     },
            
            
            # "b": {"fontSize": 18,
            #       "fontWeight": 700,
            #       "lineHeight": 33
            #       },
            
            
            #百分比
            "per": {
                "color": "black", #字体颜色
                "fontWeight": 700, #字体粗细
                "fontSize": 20,
                # "fontFamily": 'Arial',
                # "backgroundColor": "#e3e3e3",  #背景颜色
                # "padding": [2, 4],
                # "borderRadius": 2,
                },
        },
    ),
)
# 自己设置颜色
# pie.set_colors(['red', 'blue', 'black', 'green', 'orange', 'yellow'])

pie.render(pic_dir+"lmg"+str(n)+"_pie.html") #降水量 海拔 积雪深度

# # # # # # https://zhuanlan.zhihu.com/p/126306394
# # # # # # https://blog.csdn.net/zc666ying/article/details/105080212.
#标签设置 参考以下
# https://blog.csdn.net/H_biubiu/article/details/108099714 
# https://blog.csdn.net/m0_46629123/article/details/119854037 