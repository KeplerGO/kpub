import kpub
from kpub.plot import *

import numpy as np
import matplotlib.pyplot as pl


output_fn = 'prediction.png'
YLIM = [0, 2300]

first_year = 2009
current_year = 2017 # datetime.datetime.now().year
kepler_years = range(first_year, current_year+1)
k2_years = range(2014, 2014 + len(kepler_years))


db = kpub.PublicationDB()
counts = db.get_annual_publication_count_cumulative(first_year, k2_years[-1])
counts['k2'][2017] += 10
counts['k2'][2017] += 20
# Extrapolate
fraction_of_year_passed = 1. # int(datetime.datetime.now().strftime('%j')) / 365.
delta = counts['kepler'][current_year] - counts['kepler'][current_year-1]
counts['kepler'][current_year] = counts['kepler'][current_year-1] + (delta / fraction_of_year_passed)
delta = counts['k2'][current_year] - counts['k2'][current_year-1]
counts['k2'][current_year] = counts['k2'][current_year-1] + (delta / fraction_of_year_passed)


fig = pl.figure(figsize=(11, 7))

ax = pl.subplot(211)
pl.plot(kepler_years,
        [counts['kepler'][y] for y in kepler_years],
        "r-",
        label='Kepler',
        color="#2c3e50",
        marker='o')
pl.annotate(s='Start of Kepler\ndata collection', xy=(2009.45, 200), xytext=(0, 40),
            fontsize=18, color='#2c3e50',
            textcoords="offset points",
            ha='center', arrowprops={'width': 4, 'color': '#2c3e50'},)
pl.annotate(s='End of Kepler\ndata collection', xy=(2013.4, 1100), xytext=(0, 40),
            fontsize=18, color='#2c3e50',
            textcoords="offset points",
            ha='center', arrowprops={'width': 4, 'color': '#2c3e50'},)

# Aesthetics
pl.ylabel("# of Kepler\npublications")
ax.get_xaxis().get_major_formatter().set_useOffset(False)
pl.xticks(range(kepler_years[0], kepler_years[-1] + 1))
pl.xlim([kepler_years[0] - .5, kepler_years[-1] + .5])
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
pl.plot(range(2017, 2023),
        [counts['kepler'][y] - 170 for y in kepler_years[3:]],
        "r-",
        label='Kepler',
        color="#2c3e50",
        marker='None',
        lw=1.5,
        linestyle='--')

pl.plot(range(2014, current_year+1),
        [counts['k2'][y] for y in range(2014, current_year+1)],
        "r-",
        label='K2',
        color="#c0392b",
        marker='o')
pl.annotate(s='Start of K2\ndata collection', xy=(2014.45, 200), xytext=(0, 40),
            fontsize=18, color='#c0392b',
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
pl.xticks(range(k2_years[0], k2_years[-1] + 1))
pl.xlim([k2_years[0] - .5, k2_years[-1] + .5])
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
pl.savefig(output_fn, dpi=100)
pl.close()
