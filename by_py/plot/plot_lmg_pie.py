# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 22:41:38 2023
画不同第一主导因子所占比例 饼图
@author: Lenovo
"""


import pandas as pd
import os

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
df1 = df0.set_index(['station']) #设置索引

# from pyecharts.charts import Pie
# from pyecharts import options as opts
# from pyecharts.globals import ThemeType
# theme = ThemeType.LIGHT #此处 改风格

# # # position=['Grade1: 0<x<2.5','Grade2: 2.5≤x<5','Grade3: 5≤x<10','Grade4: x≥10']
# # # Num0= [len(grade01), len(grade02),len(grade03),len(grade04)]

# position=['Alti<3000','3000≤Alti<3500','3500≤Alti<4000','4000≤Alti<4500',
#           'Alti≥4500']
# Num0= [len(days_alti1), len(days_alti2),len(days_alti3),len(days_alti4),
#         len(days_alti5)]

# # position=['Grade1: 0<x<3','Grade2: 3≤x<5','Grade3: 5≤x<8','Grade4: x≥8']
# # Num0= [len(grade01), len(grade02),len(grade03),len(grade04)]

# Num=list(map(str,Num0))
# data_pair = [list(z) for z in zip(position, Num)]
# pie = Pie(init_opts=opts.InitOpts(theme=theme))
# pie.add(series_name=["Grade"],
#         data_pair=data_pair,
#         center=["48%", "50%"],
#         radius=["30%", "75%"],
#         rosetype= None,
#         itemstyle_opts = None,
#         label_opts=opts.LabelOpts(is_show=True, position="center"))

# #全局设置
# pie.set_global_opts(
#     # #设置标题
#     # title_opts=opts.TitleOpts(
#     #     #名字
#     #     title="",#标题无
#     #     # #组件距离容器左侧的位置
#     #     pos_left="center",
#     #     # #组件距离容器上方的像素值
#     #     pos_top="4%",
#     #     #设置标题颜色
#     #     title_textstyle_opts=opts.TextStyleOpts(color="black"),
#     # ),
#     #图例配置项
#     legend_opts=opts.LegendOpts(
#         orient="vertical", #图例垂直放置
#         pos_top="12%",# 图例位置调整
#         pos_left="8%",
#         textstyle_opts=opts.TextStyleOpts(font_size=18,
#               font_weight=700,color="black")),
# )
# #系列设置
# pie.set_series_opts(
#     tooltip_opts=opts.TooltipOpts(
#         trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
#     ),
#     #设置标签颜色
#     label_opts=opts.LabelOpts(color="black",            # position 标签的位置
#             position="inside",
#             # 回调函数，回调函数格式：
#             # (params: Object|Array) => string
#             # 设置标签的显示样式
#             # formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
#             formatter="{per|{d}%}  ",

#             # 背景颜色
#             background_color='rgba(247,251,245,.0001)',#白色透明色
#             # # 边框颜色
#             # border_color="#aaa",
#             # # 边框宽度
#             # border_width=2,          
#             # # 边框四角弧度
#             # border_radius=4,
#             rich={
#             # "a": {"fontSize": 18,
#             #       "fontWeight": 700,
#             #       "color": "black",
#             #       "lineHeight": 22,
#             #       "align": "center" #对齐方式
#             #       },
            
            
#             # "abg": {
#             #     "fontSize": 18,
#             #     "fontWeight": 700,
#             #     "backgroundColor": "#e3e3e3", 
#             #     "width": "100%",
#             #     "align": "right",
#             #     "height": 22,
#             #     "borderRadius": [4, 4, 0, 0],
#             #      },
            
            
#             # "hr": {
#             #     "fontSize": 18,
#             #     "fontWeight": 700,
#             #     "borderColor": "#aaa",
#             #     "width": "100%",
#             #     "borderWidth": 0.5,
#             #     "height": 0,
#             #     },
            
            
#             # "b": {"fontSize": 18,
#             #       "fontWeight": 700,
#             #       "lineHeight": 33
#             #       },
            
            
#             #百分比
#             "per": {
#                 "color": "black", #字体颜色
#                 "fontSize": 25,# 降雪等级30
#                 "fontWeight": 700,
#                 # "backgroundColor": "#e3e3e3",  #背景颜色
#                 # "padding": [2, 4],
#                 # "borderRadius": 2,
#                 },
#         },
#     ),
# )

# pie.render("F:\\snow_related\\pic\\snow_byTC\\海拔.html") #降水量 海拔 积雪深度

# # # # 参考https://zhuanlan.zhihu.com/p/126306394
# # # # https://blog.csdn.net/zc666ying/article/details/105080212