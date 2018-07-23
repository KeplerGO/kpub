"""Plot the K2 community coordinates using basemap.
"""
import matplotlib.pyplot as pl
from mpl_toolkits.basemap import Basemap
import pandas

df = pandas.read_csv("coordinates.csv")

fig = pl.figure(figsize=(16, 9))
ax = fig.add_axes([0.02, 0.03, 0.96, 0.89])
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
pl.title("Location of K2 paper authors", fontsize=30, y=1.02)
ax.text(1, 0.01, 'Last update: 2018 Jul 5',
        horizontalalignment='right',
        verticalalignment='top',
        transform=ax.transAxes,
        fontsize=14)
pl.savefig("k2-authors-world-map.png")
pl.savefig("k2-authors-world-map.pdf")
pl.close("all")
