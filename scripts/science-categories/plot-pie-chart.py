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
       textprops={'fontsize': 20, 'weight': 'bold'})
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
pl.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
pl.savefig("k2-science-piechart.png")
pl.close("all")
