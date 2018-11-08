"""Plot the K2 community coordinates using basemap.
"""
import matplotlib.pyplot as pl
from mpl_toolkits.basemap import Basemap
import pandas

df = pandas.read_csv("coordinates-only.csv")

fig = pl.figure(figsize=(9*1.618, 9))
ax = fig.add_axes([0.02, 0.03, 0.96, 0.89])
ax.set_facecolor('white')
m = Basemap(projection='kav7',
            lon_0=-90, lat_0=0,
            resolution="l", fix_aspect=False)
m.drawcountries(color='#7f8c8d', linewidth=0.8)
m.drawstates(color='#bdc3c7', linewidth=0.5)
m.drawcoastlines(color='#7f8c8d', linewidth=0.8)
m.fillcontinents('#ecf0f1', zorder=0)
x, y = m(df['lon'].values, df['lat'].values)
m.scatter(x, y, marker="o", color="red", edgecolor='black', lw=0.4, s=15, zorder=999)
#pl.title("Institutions of Kepler paper authors", fontsize=30, y=1.02)
#ax.text(1, 0.01, 'Last update: 2018 Oct 27',
#        horizontalalignment='right',
#        verticalalignment='top',
#        transform=ax.transAxes,
#        fontsize=14)
pl.tight_layout()
pl.savefig("authors-world-map.png")
pl.savefig("authors-world-map.pdf")
pl.close("all")
