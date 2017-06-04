"""Creates beautiful visualizations of the publication database."""
import datetime
import numpy as np
from astropy import log

from matplotlib import pyplot as pl
import matplotlib.patheffects as path_effects
import matplotlib as mpl

from . import SCIENCES

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


def plot_by_year(db,
                 output_fn='kpub-publication-rate.pdf',
                 first_year=2009,
                 barwidth=0.75,
                 dpi=100,
                 extrapolate=True):
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

    extrapolate : boolean
        If `True`, extrapolate the publication count in the current year.
    """

    # Obtain the dictionary which provides the annual counts
    current_year = datetime.datetime.now().year
    counts = db.count_by_year(year_begin=first_year, year_end=current_year)

    # Now make the actual plot
    fig = pl.figure()
    ax = fig.add_subplot(111)
    pl.bar(np.array(list(counts['kepler'].keys())),
           counts['kepler'].values(),
           label='Kepler',
           facecolor="#3498db",
           width=barwidth)
    pl.bar(np.array(list(counts['k2'].keys())),
           counts['k2'].values(),
           bottom=counts['kepler'].values(),
           label='K2',
           facecolor="#e74c3c",
           width=barwidth)
    # Also plot the extrapolated prediction for the current year
    if extrapolate:
        now = datetime.datetime.now()
        fraction_of_year_passed = float(now.strftime("%-j")) / 365.2425
        current_total = (counts['kepler'][current_year] +
                         counts['k2'][current_year])
        expected = (1/fraction_of_year_passed - 1) * current_total
        pl.bar(current_year,
               expected,
               bottom=current_total,
               label='Extrapolation',
               facecolor='#95a5a6',
               width=barwidth)

    # Aesthetics
    pl.ylabel("Publications per year")
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    pl.xticks(range(first_year - 1, current_year + 1))
    pl.xlim([first_year - 0.75*barwidth, current_year + 0.75*barwidth])
    pl.legend(bbox_to_anchor=(0.1, 1., 1., 0.),
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
    pl.tight_layout(rect=(0, 0, 1, 0.95), h_pad=1.5)
    log.info("Writing {}".format(output_fn))
    pl.savefig(output_fn, dpi=dpi)
    pl.close()


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
    patches, texts, autotexts = pl.pie(count,
                                       colors=['#f39c12', '#18bc9c'],
                                       autopct="%.0f%%",
                                       startangle=90)
    # Now take care of the aesthetics
    for t in autotexts:
        t.set_fontsize(32)
        t.set_color("white")
        t.set_path_effects([path_effects.Stroke(linewidth=2,
                                                foreground='#333333'),
                            path_effects.Normal()])
    pl.legend(patches,
              labels=["Exoplanets", "Astrophysics"],
              fontsize=22,
              bbox_to_anchor=(0.2, 1.05, 1., 0.),
              loc=3,
              ncol=2,
              borderaxespad=0.,
              handlelength=0.8,
              frameon=False)

    pl.axis('equal')  # required to ensure pie chart has equal aspect ratio
    pl.tight_layout(rect=(0, 0, 1, 0.85), h_pad=1.5)
    log.info("Writing {}".format(output_fn))
    pl.savefig(output_fn, dpi=dpi)
    pl.close()


if __name__ == "__main__":
    plot_by_year()
    plot_science_piechart()
