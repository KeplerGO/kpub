"""Creates beautiful visualizations of the publication database."""
import datetime
import sqlite3 as sql

import numpy as np
from astropy import log

from matplotlib import pyplot as plt
import matplotlib.patheffects as path_effects
import matplotlib as mpl

import kpub

# Configure the aesthetics
mpl.rcParams["figure.figsize"] = (8.485, 6)
mpl.rcParams["interactive"] = False
mpl.rcParams["lines.antialiased"] = True
# Patches
mpl.rcParams["patch.linewidth"] = 0.5
mpl.rcParams["patch.facecolor"] = "348ABD"
mpl.rcParams["patch.edgecolor"] = "eeeeee"
mpl.rcParams["patch.antialiased"] = True
# Font
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["font.size"] = 16
mpl.rcParams["font.sans-serif"] = "Open Sans"
mpl.rcParams["text.color"] = "333333"
# Axes
mpl.rcParams["axes.facecolor"] = "ecf0f1"
mpl.rcParams["axes.edgecolor"] = "bdc3c7"
mpl.rcParams["axes.linewidth"] = 1.0
mpl.rcParams["axes.grid"] = False
mpl.rcParams["axes.titlesize"] = "x-large"
mpl.rcParams["axes.labelsize"] = "x-large"
mpl.rcParams["axes.labelweight"] = "normal"
mpl.rcParams["axes.labelcolor"] = "333333"
mpl.rcParams["axes.axisbelow"] = True
mpl.rcParams["axes.unicode_minus"] = True
# Ticks
mpl.rcParams["xtick.color"] = "333333"
mpl.rcParams["ytick.color"] = "333333"
mpl.rcParams["xtick.major.size"] = 0
mpl.rcParams["ytick.major.size"] = 0
# Grid
mpl.rcParams["grid.color"] = "bdc3c7"
mpl.rcParams["grid.linestyle"] = "-"
mpl.rcParams["grid.linewidth"] = 1


MISSIONS = ['kepler', 'k2']
SCIENCES = ['exoplanets', 'astrophysics']


def quarterly_count(db, mission="k2", start="2015-01", stop="2015-04"):
    cur = db.con.execute("""SELECT COUNT(*) FROM pubs 
                            WHERE mission = ? 
                            AND month >= ?
                            AND month < ?;""",
                            [mission, start, stop])
    rows = list(cur.fetchall())
    return rows[0][0]


if __name__ == "__main__":
    barwidth = 0.75
    output_fn = "kpub-first-quarters.pdf"
    dpi = 200
    ymax = 35
    yticks = [0, 10, 20, 30]

    db = kpub.PublicationDB()

    # First collect the data
    k1_labels = ["2009/1", "2009/2", "2009/3", "2009/4", "2010/1", "2010/2", "2010/3", "2010/4"]
    k1_start =  ["2009-01", "2009-04", "2009-07", "2009-10", "2010-01", "2010-04", "2010-07", "2010-10"]
    k1_stop =   ["2009-04", "2009-07", "2009-10", "2010-01", "2010-04", "2010-07", "2010-10", "2011-01"]
    k1_counts = []
    for idx, label in enumerate(k1_labels):
        count = quarterly_count(db, mission="kepler", start=k1_start[idx], stop=k1_stop[idx])
        k1_counts.append(count)

    k2_labels = ["2014/1", "2014/2", "2014/3", "2014/4", "2015/1", "2015/2", "2015/3", "2015/4"]
    k2_start =  ["2014-01", "2014-04", "2014-07", "2014-10", "2015-01", "2015-04", "2015-07", "2015-10"]
    k2_stop =   ["2014-04", "2014-07", "2014-10", "2015-01", "2015-04", "2015-07", "2015-10", "2016-01"]
    k2_counts = []
    for idx, label in enumerate(k2_labels):
        count = quarterly_count(db, mission="k2", start=k2_start[idx], stop=k2_stop[idx])
        k2_counts.append(count)

    # Now make the actual plot
    fig = plt.figure()
    plt.subplots_adjust(left=0.12, right=0.98,
                        bottom=0.15, top=0.98,
                        hspace=0.2)

    ax = fig.add_subplot(211)
    plt.bar(np.arange(len(k1_counts)) - 0.5 * barwidth,
            k1_counts,
            facecolor="#3498db",
            width=barwidth,
            label="First Kepler publications")
    # Aesthetics
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    plt.xticks(range(len(k1_counts)), k1_labels)
    plt.xlim([0 - 0.75*barwidth, len(k1_counts) - 1 + 0.75*barwidth])
    plt.legend(loc="upper left", frameon=True)
    plt.yticks(yticks)
    plt.ylim([0, ymax])
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
    ax.set_ylabel("Number of publications")
    ax.yaxis.set_label_coords(-0.06, -.15)


    ax = fig.add_subplot(212)
    plt.bar(np.arange(len(k2_counts)) - 0.5 * barwidth,
            k2_counts,
            facecolor="#e74c3c",
            width=barwidth,
            label="First K2 publications")
    # Aesthetics
    #plt.ylabel("Number of publications")
    plt.xlabel("Quarter")
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    plt.xticks(range(len(k2_counts)), k2_labels)
    plt.xlim([0 - 0.75*barwidth, len(k2_counts) - 1 + 0.75*barwidth])
    plt.legend(loc="upper left", frameon=True)
    plt.yticks(yticks)
    plt.ylim([0, ymax])
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

    #plt.tight_layout(h_pad=1.5)
    log.info("Writing {}".format(output_fn))
    plt.savefig(output_fn, dpi=dpi)
    plt.close()


