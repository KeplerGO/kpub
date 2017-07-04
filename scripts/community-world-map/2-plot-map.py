"""Plot the K2 community coordinates using basemap.
"""
import matplotlib.pyplot as pl
from mpl_toolkits.basemap import Basemap
import pandas

df = pandas.read_csv("coordinates.csv")

fig = pl.figure(figsize=(16, 9))
ax = fig.add_axes([0.02, 0.03, 0.96, 0.94])
ax.set_facecolor('white')
m = Basemap(projection='kav7',
            lon_0=-90, lat_0=0,
            resolution="l", fix_aspect=False)
m.drawcountries(color='#7f8c8d', linewidth=1.)
m.drawstates(color='#bdc3c7', linewidth=0.5)
m.drawcoastlines(color='#7f8c8d', linewidth=1.)
m.fillcontinents('#ecf0f1', zorder=0)
x, y = m(df['lon'].values, df['lat'].values)
m.scatter(x, y, marker="x", color="red", lw=2.5, s=100, zorder=999)
pl.savefig("k2-authors-world-map.png")
pl.savefig("k2-authors-world-map.pdf")

"""
fig = pl.figure(figsize=(16, 9))
ax = fig.add_axes([0.05,0.05,0.9,0.9])

m = Basemap(projection='cyl',
                           llcrnrlon=-134, llcrnrlat=23,
                           urcrnrlon=-57, urcrnrlat=53,
                           resolution="l", fix_aspect=False)
#m.drawcoastlines()
m.drawcountries(color='#7f8c8d', linewidth=1.)
m.drawstates(color='#bdc3c7', linewidth=0.5)
m.drawcoastlines(color='#7f8c8d', linewidth=1.)
m.fillcontinents('#ecf0f1', zorder=0)
m.scatter(df['lon'], df['lat'], marker="x", color="red", lw=2.5, s=100, zorder=999)
#ax.set_title('K2 Author Affiliations')
#pl.tight_layout()
#pl.show()
pl.savefig("k2-authors-usa.png")


m = Basemap(projection='cyl',
                           llcrnrlon=-15, llcrnrlat=35,
                           urcrnrlon=28, urcrnrlat=62,
                           resolution="l", fix_aspect=False)
#m.drawcoastlines()
m.drawcountries(color='#7f8c8d', linewidth=1.)
m.drawstates(color='#bdc3c7', linewidth=0.5)
m.drawcoastlines(color='#7f8c8d', linewidth=1.)
m.fillcontinents('#ecf0f1', zorder=0)
m.scatter(df['lon'], df['lat'], marker="x", color="red", lw=2.5, s=100, zorder=999)
#ax.set_title('K2 Author Affiliations')
#pl.tight_layout()
#pl.show()
pl.savefig("k2-authors-europe.png")
"""

"""
fig = pl.figure(figsize=(16, 9))
ax = fig.add_axes([0.05,0.05,0.9,0.9])
m = Basemap(projection='cyl',
                           llcrnrlon=-25, llcrnrlat=-52,
                           urcrnrlon=180, urcrnrlat=80,
                           resolution="l", fix_aspect=False)
m.drawcountries(color='#7f8c8d', linewidth=1.)
m.drawstates(color='#bdc3c7', linewidth=0.5)
m.drawcoastlines(color='#7f8c8d', linewidth=1.)
m.fillcontinents('#ecf0f1', zorder=0)
m.scatter(df['lon'], df['lat'], marker="x", color="red", lw=2.5, s=100, zorder=999)
pl.savefig("k2-authors-asia.png")
"""

pl.close("all")