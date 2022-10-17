import pygmt
import shapefile
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

minlon, maxlon = 107., 130.
minlat, maxlat = 18., 45.

# Load sample earth relief data
grid = pygmt.datasets.load_earth_relief(resolution="30s", region=[minlon, maxlon, minlat, maxlat])
region = [minlon, maxlon, minlat, maxlat]

land = grid * pygmt.grdlandmask(region=region, 
     spacing="30s", 
     maskvalues=[0, 1], 
     resolution="f")

wet = grid * pygmt.grdlandmask(region=region, 
     spacing="30s", 
     maskvalues=[1, "NaN"], 
     resolution="f")

frame =  ["xa1f0.25","ya1f0.25", "z2000+lmeters", "wSEnZ"]

cmap=plt.get_cmap('Greens')
newcolors=cmap(np.linspace(0, 1, 256))
newcmap = ListedColormap(newcolors[57:245])

pygmt.makecpt(
        cmap="gray",
        series=f'-6000/4000/100',
        continuous=True
    )

fig = pygmt.Figure()

fig.grdview(
    grid=land,
    region=[minlon, maxlon, minlat, maxlat, 0, 4000],
    perspective=[165, 30],
    frame=frame,
    projection="M15c",
    zsize="4c",
    surftype="i",
    plane="0+gazure",
    shading=0,
    # Set the contour pen thickness to "1p"
    contourpen="1p",
    cmap="grayC",
)

fig.colorbar(perspective=True, frame=["a2000", "x+l'Elevation in (m)'", "y+lm"])

fig.basemap(
    perspective=True,
    rose="jTL+w3c+l+o-2c/-1c" #map directional rose at the top left corner 

)

fig.plot3d(
    x = 113.61,
    y = 34.76,
    z = 0,
    style='a0.1i',
    color='white',
    pen='purple',
    label='Zhengzhou',
    zsize="4c",
    perspective=True,

)

fig.coast(
    perspective=[165, 30, 0],
    shorelines="1p,black",
)

CHN='/Users/luoyh23/Documents/Henan/core_plot/gadm36_CHN_shp/gadm36_CHN_1.shp'
file = shapefile.Reader(CHN)
records = file.records
records
border_shape = file 
border = border_shape.shapes()

#npro = len(border)
#for i in range(0,npro):

border_points = border[11].points
x0,y0=zip(*border_points)
print(len(x0))
z0 = np.zeros(len(x0))

fig.plot3d(
    x = x0,
    y = y0,
    z = z0,
    style='c0.01i',
    color='purple',
    pen='purple',
    zsize="2c",
    perspective=True,
)

border_points = border[9].points
x0,y0=zip(*border_points)
print(len(x0))
z0 = np.zeros(len(x0))

fig.plot3d(
    x = x0,
    y = y0,
    z = z0,
    style='c0.01i',
    color='purple',
    pen='purple',
    zsize="2c",
    perspective=True,
)

#fig.grdview(
#    grid=wet,
#    region=[minlon, maxlon, minlat, maxlat, 0, 4000],
#    perspective=[150, 30],
#    projection="M15c",
#    zsize="4c",
#    surftype="i",
#    plane="0+gazure",
#    shading=0,
#    # Set the contour pen thickness to "1p"
#    contourpen="1p",
#    cmap="seafloor",
#)



#fig.readshapefile(CHN,'states',drawbounds=True)
#fig.coast(borders=["1/0.5p,black", "2/0.5p,red", "3/0.5p,blue"], land="gray")

#fig.colorbar(perspective=True, frame=["a2000", "x+l'Elevation in (m)'", "y+lm"])
fig.savefig("HN_3d.png", crop=True, dpi=300)