"""Make a pie chart plot showing the distribution of K2 papers by science theme.
"""
import pandas as pd
import matplotlib.pyplot as pl

from categorize import CATEGORIES


df = pd.read_csv("k2-categories.csv", names=["bibcode", "category"])

# Simplify the pie chart by mergin certain categories
CATEGORIES['cl'] = "Open Clusters"
df.loc[df.category == 'ro', 'category'] = 'cl'
CATEGORIES['da'] = "Catalogs & Data Analysis"
df.loc[df.category == 'ca', 'category'] = 'da'
CATEGORIES['ot'] = "Extragalactic & Other Science"
df.loc[df.category == 'cv', 'category'] = 'ot'
#CATEGORIES['as'] = "Asteroseismology"
#df.loc[df.category == 'ga', 'category'] = 'as'

counts = df.category.value_counts()
myorder = ['ed', 'ec', 'ml', 'as', 'ga', 'va', 'wd', 'cl', 'eb', 'yo', 'ac', 'ss', 'ot', 'da']
assert(len(myorder) == len(counts.index))

#labels = [CATEGORIES[lab] for lab in counts.index]
#sizes = counts.values
labels = [CATEGORIES[lab] for lab in myorder]
sizes = [counts[lab] for lab in myorder]

fig, ax = pl.subplots(figsize=(16, 9))
ax.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=145,
       counterclock=False, colors=["#2ecc71", "#27ae60"],
       pctdistance=0.8, labeldistance=1.1,
       textprops={'fontsize': 20, 'weight': 'normal'})
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ttl = pl.title("NASA #K2Mission Papers by Science Topic", fontsize=36)
ttl.set_position([.5, 1.05])
ax.text(1, 0.005, 'Last update: 2017 Jul 12',
        horizontalalignment='right',
        verticalalignment='top',
        transform=ax.transAxes,
        fontsize=14)
pl.tight_layout(rect=[0.03, 0.03, 0.97, 0.97])
pl.savefig("k2-science-piechart.png")
pl.close("all")
