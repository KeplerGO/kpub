"""Creates beautiful visualizations of the publication database."""
import datetime
import numpy as np
from astropy import log

from matplotlib import pyplot as pl
import matplotlib.patheffects as path_effects
import matplotlib as mpl

from . import SCIENCES

# Configure the aesthetics
mpl.rcParams["figure.figsize"] = (10, 6)
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
                 dpi=200,
                 extrapolate=True,
                 mission='both',
                 colors=["#3498db", "#27ae60", "#95a5a6"]):
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

    mission : str
        'kepler', 'k2', or 'both'

    colors : list of str
        Define the facecolor for [kepler, k2, extrapolation]
    """
    # Obtain the dictionary which provides the annual counts
    current_year = datetime.datetime.now().year
    counts = db.get_annual_publication_count(year_begin=first_year, year_end=current_year)

    # Now make the actual plot
    fig = pl.figure()
    ax = fig.add_subplot(111)
    if mission != 'k2':
        pl.bar(np.array(list(counts['kepler'].keys())),
               list(counts['kepler'].values()),
               label='Kepler',
               facecolor=colors[0],
               width=barwidth)
    if mission != 'kepler':
        if mission == 'k2':
            bottom = None
        else:
            bottom = list(counts['kepler'].values())
        pl.bar(np.array(list(counts['k2'].keys())),
               list(counts['k2'].values()),
               bottom=bottom,
               label='K2-Based Publications',
               facecolor=colors[1],
               width=barwidth)
    # Also plot the extrapolated prediction for the current year
    if extrapolate:
        now = datetime.datetime.now()
        fraction_of_year_passed = float(now.strftime("%-j")) / 365.2425
        if mission == 'both':
            current_total = (counts['kepler'][current_year] +
                             counts['k2'][current_year])
        else:
            current_total = counts[mission][current_year]
        expected = (1/fraction_of_year_passed - 1) * current_total
        pl.bar(current_year,
               expected,
               bottom=current_total,
               label='Extrapolation',
               facecolor=colors[2],
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


def plot_science_piechart(db, output_fn="kpub-piechart.pdf", dpi=200):
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
    pl.legend(handles=patches,
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


def plot_author_count(db,
                      output_fn='kpub-author-count.pdf',
                      first_year=2008,
                      dpi=200,
                      colors=["#3498db", "#27ae60", "#95a5a6"]):
    """Plots a line chart showing the number of authors over time.

    Parameters
    ----------
    db : `PublicationDB` object
        Data to plot.

    output_fn : str
        Output filename of the plot.

    first_year : int
        What year should the plot start?

    dpi : float
        Output resolution.

    colors : list of str
        Define the facecolor for [kepler, k2, extrapolation]
    """
    # Obtain the dictionary which provides the annual counts
    current_year = datetime.datetime.now().year

    # Now make the actual plot
    fig = pl.figure()
    ax = fig.add_subplot(111)

    cumulative_years = []
    paper_counts = []
    author_counts, first_author_counts = [], []
    k2_count, kepler_count = [], []
    for year in range(first_year - 1, current_year):
        cumulative_years.append(year)
        metrics = db.get_metrics(cumulative_years)
        paper_counts.append(metrics['publication_count'])
        author_counts.append(metrics['author_count'])
        first_author_counts.append(metrics['first_author_count'])
        k2_count.append(metrics['k2_count'])
        kepler_count.append(metrics['kepler_count'])

    # +1 because the stats for all of e.g. 2018 should show at Jan 1, 2019
    ax.plot([y+1 for y in cumulative_years], paper_counts, label="Kepler & K2 publications", lw=9)
    #ax.plot(cumulative_years, author_counts, label="Unique authors", lw=6)
    ax.plot([y+1 for y in cumulative_years], first_author_counts, label="Unique first authors", lw=3)

    # Aesthetics
    #pl.title("Kepler & K2's scientific output over time")
    pl.ylabel("Cumulative count")
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    pl.xticks(range(first_year - 1, current_year + 1))
    pl.xlim([first_year + 0.5, current_year + 0.5])
    pl.ylim([0, 1.05*np.max(paper_counts)])
    pl.legend(bbox_to_anchor=(0.03, 0.95, 0.95, 0.),
              loc="upper left",
              ncol=1,
              borderaxespad=0.,
              handlelength=1.5,
              frameon=True)
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
    pl.tight_layout(rect=(0, 0, 1, 0.98), h_pad=1.5)
    log.info("Writing {}".format(output_fn))
    pl.savefig(output_fn, dpi=dpi)
    pl.close()



if __name__ == "__main__":
    plot_by_year()
    plot_science_piechart()
