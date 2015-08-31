"""Creates beautiful visualizations of the publication database."""
import datetime
import sqlite3 as sql

import numpy as np
from astropy import log

from matplotlib import pyplot as plt
import matplotlib.patheffects as path_effects
import matplotlib as mpl

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


def plot_by_year(db,
                 output_fn='kpub-publication-rate.pdf',
                 first_year=2009,
                 barwidth=0.75,
                 dpi=100):
    """Plots a bar chart showing the number of publications per year.

    Parameters
    ----------
    db : `PublicationDB` object
        Data to plot.

    output_fn : str
        Output filename of the plot.

    first_year : int
        What year should the plot start?

    barwidth : float
        Aesthetics -- how wide are the bars?

    dpi : float
        Output resolution.
    """
    current_year = datetime.datetime.now().year

    # Initialize a dictionary to contain the data to plot
    counts = {}
    for mission in MISSIONS:
        counts[mission] = {}
        for year in range(first_year, current_year + 1):
            counts[mission][year] = 0

        cur = db.con.execute("SELECT year, COUNT(*) FROM pubs "
                          "WHERE mission = ? "
                          "AND year >= '2009' "
                          "GROUP BY year;",
                          [mission])
        rows = list(cur.fetchall())
        for row in rows:
            counts[mission][int(row[0])] = row[1]

    # Now make the actual plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.bar(np.array(list(counts['kepler'].keys())) - 0.5*barwidth,
            counts['kepler'].values(),
            label='Kepler',
            facecolor="#2980b9",
            width=barwidth)
    plt.bar(np.array(list(counts['k2'].keys())) - 0.5*barwidth,
            counts['k2'].values(),
            bottom=counts['kepler'].values(),
            label='K2',
            facecolor="#c0392b",
            width=barwidth)
    # Also plot the extrapolated precition for the current year
    now = datetime.datetime.now()
    fraction_of_year_passed = float(now.strftime("%-j")) / 365.2425
    current_total = (counts['kepler'][current_year] +
                     counts['k2'][current_year])
    expected = (1/fraction_of_year_passed - 1) * current_total
    plt.bar(current_year - 0.5*barwidth,
            expected,
            bottom=current_total,
            label='Extrapolation',
            facecolor='gray',
            width=barwidth)

    # Aesthetics
    plt.ylabel("Number of publications")
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    plt.xticks(range(first_year - 1, current_year + 1))
    plt.xlim([first_year - 0.75*barwidth, current_year + 0.75*barwidth])
    plt.legend(bbox_to_anchor=(0.1, 1., 1., 0.),
               loc=3,
               ncol=3,
               borderaxespad=0.,
               handlelength=0.8,
               frameon=False)
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
    plt.tight_layout(rect=(0, 0, 1, 0.95), h_pad=1.5)
    log.info("Writing {}".format(output_fn))
    plt.savefig(output_fn, dpi=dpi)
    plt.close()


def plot_science_piechart(db, output_fn="kpub-piechart.pdf", dpi=100):
    """Plots a piechart showing exoplanet vs astrophysics publications.

    Parameters
    ----------
    db : `PublicationDB` object
        Data to plot.

    output_fn : str
        Output filename of the plot.

    dpi : float
        Output resolution.
    """
    count = []
    for science in SCIENCES:
        cur = db.con.execute("SELECT COUNT(*) FROM pubs "
                          "WHERE science = ?;", [science])
        rows = list(cur.fetchall())
        count.append(rows[0][0])

    # Plot the pie chart
    patches, texts, autotexts = plt.pie(count,
                                        colors=['#f39c12', '#16a085'],
                                        autopct="%.0f%%",
                                        startangle=90)
    # Now take care of the aesthetics
    for t in autotexts:
        t.set_fontsize(32)
        t.set_color("white")
        t.set_path_effects([path_effects.Stroke(linewidth=2,
                                                foreground='#333333'),
                            path_effects.Normal()])
    plt.legend(patches,
               labels=["Exoplanets", "Astrophysics"],
               fontsize=22,
               bbox_to_anchor=(0.2, 1.05, 1., 0.),
               loc=3,
               ncol=2,
               borderaxespad=0.,
               handlelength=0.8,
               frameon=False)

    plt.axis('equal')  # required to ensure pie chart has equal aspect ratio
    plt.tight_layout(rect=(0, 0, 1, 0.85), h_pad=1.5)
    log.info("Writing {}".format(output_fn))
    plt.savefig(output_fn, dpi=dpi)
    plt.close()


if __name__ == "__main__":
    plot_by_year()
    plot_science_piechart()
