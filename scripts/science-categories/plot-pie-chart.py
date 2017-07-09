import pandas as pd
import matplotlib.pyplot as pl

from categorize import CATEGORIES

df = pd.read_csv("k2-categories.csv", names=["bibcode", "category"])

# Simplify the pie chart by mergin certain categories
CATEGORIES['cl'] = "Rotation & Clusters"
df.loc[df.category == 'ro', 'category'] = 'cl'
CATEGORIES['da'] = "Catalogs & Data Analysis"
df.loc[df.category == 'ca', 'category'] = 'da'
CATEGORIES['ot'] = "Extragalactic & Other Science"
df.loc[df.category == 'cv', 'category'] = 'ot'
CATEGORIES['as'] = "Asteroseismology"
df.loc[df.category == 'ga', 'category'] = 'as'

counts = df.category.value_counts()


labels = [CATEGORIES[lab] for lab in counts.index]

sizes = counts.values
#explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = pl.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=180, counterclock=False)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
pl.tight_layout()
pl.savefig("k2-piechart.png")
