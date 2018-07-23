import kpub
from kpub.plot import *

import numpy as np
import matplotlib.pyplot as pl


output_fn = 'prediction.png'
YLIM = [0, 2500]

first_year = 2009
current_year = 2018 # datetime.datetime.now().year
kepler_years = range(first_year, current_year+1)
k2_years = range(2014, 2014 + len(kepler_years))


db = kpub.PublicationDB()
counts = db.get_annual_publication_count_cumulative(first_year - 1, k2_years[-1])

# Correct for missing part of current year
#counts['kepler'][2018] += 0.5*(counts['kepler'][2018] - counts['kepler'][2017])
#counts['k2'][2018] += 0.5*(counts['k2'][2018] - counts['k2'][2017])

# Extrapolate
fraction_of_year_passed = 1. # int(datetime.datetime.now().strftime('%j')) / 365.
delta = counts['kepler'][current_year] - counts['kepler'][current_year-1]
counts['kepler'][current_year] = counts['kepler'][current_year-1] + (delta / fraction_of_year_passed)
delta = counts['k2'][current_year] - counts['k2'][current_year-1]
counts['k2'][current_year] = counts['k2'][current_year-1] + (delta / fraction_of_year_passed)


fig = pl.figure(figsize=(11, 7))

ax = pl.subplot(211)
pl.plot([2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2018.5],
        [counts['kepler'][y] for y in range(2008, 2019)],
        "r-",
        label='Kepler',
        color="#2c3e50",
        marker='o')
pl.annotate(s='Start of Kepler\ndata collection', xy=(2009.5, 250), xytext=(0, 40),
            fontsize=16, color='#2c3e50',
            textcoords="offset points",
            ha='center', arrowprops={'width': 4, 'color': '#2c3e50'},)
pl.annotate(s='End of Kepler\ndata collection', xy=(2013.4, 900), xytext=(0, 40),
            fontsize=16, color='#2c3e50',
            textcoords="offset points",
            ha='center', arrowprops={'width': 4, 'color': '#2c3e50'},)

# Aesthetics
pl.ylabel("# of Kepler\npublications")
ax.get_xaxis().get_major_formatter().set_useOffset(False)
pl.xticks(range(kepler_years[0], kepler_years[-1] + 2))
pl.xlim([kepler_years[0] - .5, kepler_years[-1] + 1.5])
pl.yticks([0, 1000, 2000])
pl.ylim(YLIM)
# Disable spines
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
# Only show bottom and left ticks
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
# Only show horizontal grid lines
ax.grid(axis='y')


ax = pl.subplot(212)

#pl.plot(range(2014, current_year+7),
#        [counts['kepler'][y-5] for y in range(2014, current_year+7)],
#        "r-",
#        label='Kepler',
#        color="#3498db",
#        marker='o')

# Dashed extrapolation
pl.plot([2018, 2019, 2020, 2021, 2022, 2023, 2023.5],
        [counts['kepler'][y] - 240 for y in kepler_years[3:]],
        "r-",
        label='Kepler',
        color="#2c3e50",
        marker='None',
        lw=1.5,
        linestyle='--')

pl.plot([2014, 2015, 2016, 2017, 2018, 2018.5],
        [counts['k2'][y] for y in range(2013, current_year+1)],
        "r-",
        label='K2',
        color="#c0392b",
        marker='o')
pl.annotate(s='Start of K2\ndata collection', xy=(2014.5, 250), xytext=(0, 40),
            fontsize=16, color='#c0392b',
            textcoords="offset points",
            ha='center', arrowprops={'width': 4, 'color': '#c0392b'},)
#pl.annotate(s='End of K2\ndata collection', xy=(2019., 1100), xytext=(0, 40),
#            fontsize=18, color='#e74c3c',
#            textcoords="offset points",
#            ha='center', arrowprops={'width': 4, 'color': '#e74c3c'},)
"""
pl.arrow(2019, 500, 1, 0, width=50, length_includes_head=True,
    facecolor='black', alpha=1)
"""
#pl.annotate("", xy=(2021, 800), xytext=(2019., 800),
#            textcoords="data",
#            arrowprops={'width': 4, 'color': '#000000'},
#            )
#pl.text(2019, 700, "Proposed K2\ncommunity\nsupport", va='top', ha='left')

# Aesthetics
pl.ylabel("# of K2\npublications")
ax.get_xaxis().get_major_formatter().set_useOffset(False)
pl.xticks(range(k2_years[0], k2_years[-1] + 2))
pl.xlim([k2_years[0] - .5, k2_years[-1] + 1.5])
pl.yticks([0, 1000, 2000])
pl.ylim(YLIM)
# Disable spines
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
# Only show bottom and left ticks
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
# Only show horizontal grid lines
ax.grid(axis='y')

pl.xlabel("Year")

pl.tight_layout(rect=(0, 0, 1, 0.98), h_pad=1.5)
log.info("Writing {}".format(output_fn))
pl.savefig(output_fn, dpi=200)
pl.close()
