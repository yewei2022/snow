# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 10:50:17 2022
# https://www.heywhale.com/mw/project/61be9d024e097300170aaa02

# 出错  因为积雪有多行数据 相同
而这个方法要求矩阵可逆 所以 没法搞
@author: Lenovo
"""

import pandas as pd
import numpy as np
import xarray as xr

#%% 创建一个二维数组 不需要
# 本来想 每年的各站点年降水量做ROF  [40,80] 看了不用了
# year=list(np.arange(1981,2021,1))
# path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station'])
# sta1=sta['station'].tolist()
# a1 = np.zeros((40,80))
# a2 = xr.DataArray(data=a1, dims=['year','station'], coords=[year,sta1])
# # print(a2)
# a3 = pd.DataFrame(a2, columns=sta1, index=year)


#%% 1 数据预处理 将 TC影响下的各年各站点总降水量 出问题 有多行数据 相同

need=pd.read_table("F:\\snow_sts_data\\1981-2020\\snow_pre_gss.txt",
                          sep='\s+',na_values=32700)
need['year']=need['time'].astype(str).str[0:4]
name='time'
pre=need.groupby(by=[name,'station'])['gss'].sum() 
pre1=pre.reset_index()
pre1['station']=pre1['station'].astype(int)
pre2=pre1.pivot(index=name, columns='station', values='gss')
data=pre2.fillna(0)

#%%  写EOF REOF 函数

class Eof():
    '''
    用于进行 EOF 分析的 class.
    为了与说明文档一致,程序中的 EOF 和 PC 以列向量的形式存储.
    但是调用方法时返回的是便于使用的行向量.
    '''
    def __init__(self, data):
        '''
        如果你想求旋转后对应的pcs的话，直接对旋转阵TT取逆然后乘原来pcs阵就可
        不过虽然可以，但没必要，因为你用这些pcs去跟别的求相关，多此一举，
        因为旋转后的载荷阵就反应的相关性
        对数组 X 进行 SVD 分解,并保存含特征值,EOF 和 PC 的数组.
        要求多维数组 data 的第一维为时间维.需要自行做预处理.不允许含有缺测值.
        EOF 和 PC 向量都是用列向量表示的.
        '''
        # 将 data 变形为适合做 EOF 分析的二维数组 X.
        #去气候态
        data = data-np.mean(data,axis=0,keepdims=True)
        self.shape = data.shape
        n = self.shape[0]
        X = data.reshape((n, -1))
        # full_matrices=False 使得 EOF 和 PC 的列数相同.
        # svd 得到的奇异值数组 s 按降序排列.
        L, S, R = np.linalg.svd(X, full_matrices=False)
        # 保存协方差阵的特征值.
        # 由 np.linalg.svd 函数的特性,特征值的个数为 min(X.shape).# 维度:(neigs).
        self.neigs = S.size
        self.EIG = S**2 / n
        # 保存 PC 和 factor 的矩阵.
        # 维度:(X.shape[0], neigs).
        self.PC = L * S # 用到了广播.
        self.FAC = L
        # 保存 EOF 和 loading 的矩阵.
        # 维度:(X.shape[1], neigs)
        self.EOF = R.T
        self.LOD = self.EOF * np.sqrt(self.EIG) # 用到了广播.
    def eigs(self, neigs=None):
        '''
        返回前 neigs 个特征值.
        若不给定参数 neigs,返回所有特征值.
        '''
        return self.EIG[:neigs]
    def pcs(self, npcs=None, scale=False):
        '''
        返回含有前 npcs 个 PC 的数组,每一行对应一个 PC.
        要求 neofs<=neigs.若不给定参数 npcs,返回所有 PC.
        参数 scale 决定是否放缩为 factor.
        '''
        if scale:
            return self.FAC[:, :npcs].T
        else:
            return self.PC[:, :npcs].T
    def resize(self, EOF):
        '''对列排列的数组 EOF 转置,再使其与 data 的空间维度匹配.'''
        array = EOF.T
        # 保留第一维(即有多少个 EOF 向量),再 reshape 成 data 的空间维度.
        shape_new = [-1] + list(self.shape[1:])
        return array.reshape(shape_new)
    def eofs(self, neofs=None, scale=False):
        '''
        返回含前 neofs 个 EOF 的数组,每一行对应一个 EOF.
        要求 neofs<=neigs.若不给定参数 neofs,返回所有 EOF.
        参数 scale 决定是否放缩为 loading.
        '''
        if scale:
            return self.resize(self.LOD[:, :neofs])
        else:
            return self.resize(self.EOF[:, :neofs])
    def fraction(self, neigs=None):
        '''
        计算前 neigs 个特征值的解释率,以百分数为单位.
        若不给定参数 neigs,则对所有特征值进行计算.
        '''
        eigs = self.eigs()
        frac = eigs[:neigs] / eigs.sum() * 100
        return frac
    def north_test(self, neigs=None):
        '''
        利用 North 准则计算前 neigs 个特征值的误差百分比.
        若不给定参数 neigs,则对所有特征值进行计算.
        这里自由度直接采用 data.shape[0].
        '''
        n = self.shape[0]
        eigs = self.eigs()
        deigs = eigs[:neigs] * np.sqrt(2/n)
        dfrac = deigs / eigs.sum() * 100
        return dfrac
    def reconstruct(self, neigs=None):
        '''
        从前 neigs 个模态中重建数据阵 data.
        若不给定参数 neigs,则使用所有模态进行计算.
        '''
        EOF = self.EOF[:, :neigs]
        PC = self.PC[:, :neigs]
        X = PC @ EOF.T
        return X.reshape(self.shape)

    def reofs(self, neof=None, **varimax_kw):
        '''
        利用 loading 来计算 REOF.
        neof 指定用到的 loading 的个数.不给出时则用上全部.
        varimax_kw 能够指定 varimax 函数的关键字.
        '''
        EOF = self.LOD[:, :neof]
        REOF = varimax(EOF, varimax_kw)
        return self.resize(REOF)
    def rfraction(self, reofs):
        '''计算 reofs 对应的解释率,以百分数为单位.'''
        eigs = self.eigs()
        fra = self.fraction()
        bili = np.sum(fra[:m_pcs])/np.sum(fra[:]) #!!! 我把这里改成了m_pcs 
        reofs_new = reofs.reshape((reofs.shape[0], -1))
        rfrac = np.sum(reofs_new**2, axis=1) / np.sum(reofs_new**2, 
                                                      axis=1).sum() *bili* 100
        return rfrac
def varimax(EOF, norm=True, N=1000, eps=10**(-6)):
    '''
    利用 varimax 法旋转给定的列排列的 EOF 数组.
    norm 指示是否做 Kaiser 归一化,N 和 eps 确定迭代次数.
    '''
    p, neofs = EOF.shape# 如果只有一个 EOF,那么没必要旋转.
    #print(EOF)
    if neofs == 1:
        return EOF
    import copy
    U = copy.deepcopy(EOF)
    # 做 Kaiser 行归一化.
    if True:
        h = np.sqrt(np.sum(U**2, axis=1))
    U = U / h[:, None]
    TT = np.eye(neofs)
    d0 = 0
    # 进行迭代,最多 N 次.
    for i in range(N):
        Z = U @ TT
        B = U.T @ (Z**3 - Z @ np.diag(np.ones(p) @ Z**2) / p)
        L, S, R = np.linalg.svd(B)
        TT = L @ R
        d1 = S.sum()
        # 当 d1 与 d0 之间的误差足够小时,迭代结束.
        if np.abs(d1 - d0) < eps * d0:
            break
        else:
            d0 = d1
    U = U @ TT
    # 还原归一化效果
    if norm:
        U = U * h[:,None]
    return U


#%%  做EOF REOF
# 我的理解 先EOF 挑选贡献率70%的主成分 比如说前3个 那么就对前三个做方差极大旋转
# 这样的三个 得出来的解释方差之和 与 EOF是一致的
datavalue = data.values
eof = Eof(datavalue)
fra = eof.fraction()

m_pcs=3
print('EOF特征值: \n{}'.format(eof.eigs()))
print('EOF 主成分size: \n{}'.format(eof.pcs().shape)) 
print('EOF各主成分的解释方差: \n{}'.format(fra)) 
print('EOF前3个主成分的方差累计方差贡献率: \n{}'.format(np.sum(fra[:m_pcs]))) 

reof = eof.reofs(m_pcs)
reoffra = eof.rfraction(reof)
# print('REOF的解释方差: \n{}'.format(reoffra))
# print('REOF前5个主成分的方差累计方差贡献率: \n{}'.format(np.sum(reoffra[:4]))) 
# print('REOF size: \n{}'.format(reof.shape))

# 将解释方差先升序再降序排列 目的是取索引 便于之后取值
sorted_nums = sorted(enumerate(reoffra), key=lambda x: x[1]) 
print('REOF的方差解释率及其索引: \n{}'.format(sorted_nums))
# 返回索引序列 enumerate(sequence, [start=0])
# sorted(iterable,key=None, reverse=False) 
# key=lambda x: x[1] 意味根据redoffra数从小到大返回sorted_nums
idxx = [i[0] for i in sorted_nums] #只取索引
idxx = idxx[::-1]

#%% 插值

#取站号 经纬度
idd = list(data.columns)
path_sta='F:\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
station=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
st0 = station[station.station.isin(idd)]
st1 = st0.sort_values(by='station', ascending=True)
st=st1.reset_index(drop=True)

from metpy.interpolate import inverse_distance_to_grid
from scipy.interpolate import Rbf
lon_min=70
lon_max=105
lat_min=25
lat_max=40
intervl=0.25
lon_grid = np.arange(lon_min, lon_max+intervl, intervl) 
lat_grid = np.arange(lat_min, lat_max+intervl, intervl) 

drawdata = np.zeros((m_pcs,len(lat_grid),len(lon_grid)))
lon_gridmesh, lat_gridmesh = np.meshgrid(lon_grid, lat_grid)

for i in range(len(reof)):
    print(i)
    func = Rbf(st.lon, st.lat, reof[i], function='linear',smooth=2)
    stid_pre = func(lon_gridmesh, lat_gridmesh)
    rbfda = stid_pre
    tm_grid = inverse_distance_to_grid(st.lon,st.lat,reof[i],lon_gridmesh,
                                        lat_gridmesh,r=15,min_neighbors=3)
    drawdata[i] = rbfda


reoffra = reoffra.round(2) # reoffra保留两位小数
print('保留两位小数的解释方差: \n{}'.format(reoffra))

# 将drawdata的因子载荷矩阵 按照解释方差降序重新排列行数据
drawdata = drawdata[idxx]
print('插值后的数据维数-(模态,纬度,经度): \n{}'.format(drawdata.shape))

reoffra = reoffra[idxx]
reof = reof[idxx]

#%% 将数据保存为nc 文件 
# https://blog.csdn.net/qq_44907989/article/details/125907641

import xarray as xr
import numpy as np
from metpy.units import units

ds = xr.Dataset()
# *units.degC 是给气温赋单位，有没有单位都可以，锦上添花的东西

ds['pre'] = (('m_pcs','lat','lon'),drawdata*units('mm'))
ds.coords['m_pcs'] = ('m_pcs',[0,1,2])
ds.coords['lat'] = ('lat',lat_grid)
ds.coords['lon'] = ('lon',lon_grid)
ds.to_netcdf('F:\\snow_sts_data\\REOF\\'+name+'_reof_gss.nc')


fra1=pd.DataFrame(fra, columns=['fra'])
fra1.to_csv("F:\\snow_sts_data\\REOF\\"+name+"_gss_fra.txt",
            index = False,sep=' ')

