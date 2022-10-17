# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 21:45:12 2022
用 xeofs 做 EOF REOF
@author: Lenovo
"""


"""
https://www.heywhale.com/mw/project/626e867a9405f9001759e3e0
https://github.com/nicrie/xeofs
"""
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
from cartopy.crs import Robinson, PlateCarree
import cartopy.crs as ccrs
from xeofs.xarray import EOF, Rotator


sns.set_context('paper')

file_path="F:\\snow_practice\\era5.geopotential.19790101.nc"
sst0 = xr.open_dataset(file_path)

ssta=sst0.z.sel(level=500)


#%%
# Perform the actual analysis

# (1) Standard EOF without regularization
model_var = EOF(ssta, dim=['time'], weights='coslat')
model_var.solve()
# (2) Varimax-rotated EOF analysis
rot_var = Rotator(model_var, n_rot=50, power=1)
reofs=rot_var.eofs()
rpcs=rot_var.pcs()
reofs_var=reofs.varianceFraction(neigs=None)

#%% 绘图

mode = 1 
proj = PlateCarree() 
kwargs = {     
    'cmap' : 'RdBu',     
    'vmin' : -.05,     
    'vmax': .05,    
    'transform': proj,     
    'add_colorbar': False 
}  
fig = plt.figure(figsize=(7.3, 6)) 
fig.subplots_adjust(wspace=0) 
gs = GridSpec(1, 4, figure=fig, width_ratios=[1, 1, 1, 1]) 
ax = [fig.add_subplot(gs[0, i], projection=proj) for i in range(4)] 

# ax_pc = fig.add_subplot(gs[1, :])  
# # PC 
# rpcs.sel(mode=mode).plot(ax=ax_pc) 
# ax_pc.set_xlabel('') 
# ax_pc.set_title('')  

# EOFs 
for i, (a, reof) in enumerate(zip(ax, reofs)):     
    a.coastlines(color='.5')     
    reofs.sel(mode=mode).plot(ax=a, **kwargs)     
    a.set_xticks([])     
    a.set_yticks([])     
    a.set_xlabel('')     
    a.set_ylabel('')     
    a.set_title('Mode {:}'.format(i+1)) 
ax[0].set_ylabel('EOFs')
 
# fig.suptitle('Mode {:}'.format(mode)) 

plt.savefig('F:\\snow_practice\\rotated_eof.jpg', dpi=1000)
