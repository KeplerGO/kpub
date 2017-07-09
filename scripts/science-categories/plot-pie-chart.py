import pandas as pd
import matplotlib.pyplot as pl
#import seaborn as sns

from categorize import CATEGORIES

FLAT = ["#1abc9c", "#2ecc71", "#3498db", "#9b59b6",
"#f1c40f", "#e67e22", "#e74c3c", 
"#16a085", "#27ae60", "#2980b9", "#8e44ad",
         "#f39c12", "#d35400", "#c0392b"]

FLAT = ["#2ecc71", "#27ae60"]

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

labels = [CATEGORIES[lab] for lab in myorder]
sizes = [counts[lab] for lab in myorder]

#sizes = counts.values

fig1, ax = pl.subplots(figsize=(16, 9))
ax.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=145,
       counterclock=False, colors=FLAT,
       pctdistance=0.8, labeldistance=1.1,
       textprops={'fontsize': 20, 'weight': 'bold'})
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
pl.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
pl.savefig("k2-science-piechart.png")
