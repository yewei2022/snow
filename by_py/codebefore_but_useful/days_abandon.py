# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 19:08:36 2022

一些降雪统计中暂时用不上的代码
@author: Lenovo
"""

import pandas as pd

need=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_pre_gss.txt",
                          sep='\s+',na_values=32700)

#%% branch3 计算 step # 不同海拔高度下的降雪日数所占比例 无用

# need.drop(['lon','lat','dailypre','gss','gss_inc','tc_id'],axis=1,inplace=True)

# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','alti'])

# # 添加位置信息 法一  循环添加  海拔，因为index不唯一，不能通过index直接concat
# alti=[]
# for i in need.station.tolist():
#     alti.append(sta.loc[sta["station"] == i,['alti']])
# alti_df = pd.concat(alti,ignore_index=True)
# need1=pd.concat([need,alti_df],axis=1)
# days_alti1=need1[need1['alti'] <3000.]
# days_alti2=need1[(need1['alti']>=3000.)&(need1['alti']<3500.)]
# days_alti3=need1[(need1['alti']>=3500.)&(need1['alti']<4000.)]
# days_alti4=need1[(need1['alti']>=4000.)&(need1['alti']<4500.)]
# days_alti5=need1[(need1['alti']>=4500.)&(need1['alti']<5000.)]

# # 测试不同海拔高度的站点本身有多少个
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# need1=pd.read_table(path_sta,sep = ",",usecols=['station','alti'])

# days_alti1=need1[need1['alti'] <3000.]
# days_alti2=need1[(need1['alti']>=3000.)&(need1['alti']<3500.)]
# days_alti3=need1[(need1['alti']>=3500.)&(need1['alti']<4000.)]
# days_alti4=need1[(need1['alti']>=4000.)&(need1['alti']<4500.)]
# days_alti5=need1[(need1['alti']>=4500.)&(need1['alti']<5000.)]

#%% branch3 计算 step # 不同pre gss等级站点所占总站点数比例 无用

# #不同gss站点所占比例
# grade01=need[(need['gss_inc'] >0.)&(need['gss_inc'] < 3.)]
# # grade1_ratio=format(len(grade01)/len(need)*100,'.1f') #换算成百分率
# grade02=need[(need['gss_inc'] >= 3.)&(need['gss_inc'] < 5.)]
# grade03=need[(need['gss_inc'] >= 5.)&(need['gss_inc'] < 8.)]
# grade04=need[need['gss_inc'] >= 8.]

# #不同pre站点所占比例
# grade01=need[need['dailypre'] < 2.5]
# # grade1_ratio=format(len(grade01)/len(need)*100,'.1f') #换算成百分率
# grade02=need[(need['dailypre'] >= 2.5)&(need['dailypre'] < 5.)]
# grade03=need[(need['dailypre'] >= 5.)&(need['dailypre'] < 10.)]
# grade04=need[need['dailypre'] >= 10.]



#%% branch3 计算 step # 不同pre等级的海拔高度 不用打开step1 无用

# need=pd.read_table("F:\\snow_sts_data\\percentile\\snow_pre_label.txt",
#                           sep='\s+',na_values=32700)
# #添加海拔
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','alti'])
# # 添加海拔信息 法一  循环添加  海拔，因为index不唯一，不能通过index直接concat
# alti=[]
# for i in need.station.tolist():
#     ii=int(i)
#     alti.append(sta.loc[sta["station"] == ii,['alti']])
# alti_df = pd.concat(alti,ignore_index=True)
# need1=pd.concat([need,alti_df],axis=1)

# grade01=need1[need1['pre_grd_label']==1]
# grade02=need1[need1['pre_grd_label']==2]
# grade03=need1[need1['pre_grd_label']==3]
# grade04=need1[need1['pre_grd_label']==4]
# grade01.reset_index(drop=True,inplace=True)
# grade02.reset_index(drop=True,inplace=True)
# grade03.reset_index(drop=True,inplace=True)
# grade04.reset_index(drop=True,inplace=True)
# grade_alti=pd.concat([grade01['alti'],grade02['alti'],grade03['alti'],
#                       grade04['alti']],axis=1)
# grade_alti.columns=['Grade1','Grade2','Grade3','Grade4']

# grade_alti.to_csv("F:\\snow_sts_data\\percentile\\pre_grade_alti.txt",
#                     index = False,sep=' ',na_rep=32700) 

# # # grade1_ratio=format(len(grade01)/len(need)*100,'.1f') #将某个值换算成百分率



#%% branch3 计算 step # 不同gss等级的海拔高度 不用打开step1  无用

# need=pd.read_table("F:\\snow_sts_data\\percentile\\snow_gss_label.txt",
#                           sep='\s+',na_values=32700)
# #添加海拔
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','alti'])
# # 添加海拔信息 法一  循环添加  海拔，因为index不唯一，不能通过index直接concat
# alti=[]
# for i in need.station.tolist():
#     ii=int(i)
#     alti.append(sta.loc[sta["station"] == ii,['alti']])
# alti_df = pd.concat(alti,ignore_index=True)
# need1=pd.concat([need,alti_df],axis=1)

# grade01=need1[need1['gss_grd_label']==1]
# grade02=need1[need1['gss_grd_label']==2]
# grade03=need1[need1['gss_grd_label']==3]
# grade04=need1[need1['gss_grd_label']==4]
# grade01.reset_index(drop=True,inplace=True)
# grade02.reset_index(drop=True,inplace=True)
# grade03.reset_index(drop=True,inplace=True)
# grade04.reset_index(drop=True,inplace=True)
# grade_alti=pd.concat([grade01['alti'],grade02['alti'],grade03['alti'],
#                       grade04['alti']],axis=1)
# grade_alti.columns=['Grade1','Grade2','Grade3','Grade4']

# grade_alti.to_csv("F:\\snow_sts_data\\percentile\\gss_grade_alti.txt",
#                     index = False,sep=' ',na_rep=32700) 



#%% branch4 画图 不同等级降雪，不同海拔高度饼图 无用

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

