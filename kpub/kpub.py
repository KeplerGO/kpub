"""Build and maintain a database of Kepler/K2 publications.
"""
from __future__ import print_function, division, unicode_literals

# Standard library
import os
import re
import sys
import json
import datetime
import argparse
import sqlite3 as sql

try:
    import ads
except Exception:
    ads = None

# External dependencies
import jinja2
from six.moves import input  # needed to support Python 2
from astropy import log
from astropy.utils.console import ProgressBar

from . import plot, PACKAGEDIR

# Where is the default location of the SQLite database?
DEFAULT_DB = os.path.expanduser("~/.kpub.db")


class Highlight:
    """Defines colors for highlighting words in the terminal."""
    RED = "\033[4;31m"
    GREEN = "\033[4;32m"
    YELLOW = "\033[4;33m"
    BLUE = "\033[4;34m"
    PURPLE = "\033[4;35m"
    CYAN = "\033[4;36m"
    END = '\033[0m'


class PublicationDB(object):
    """Class wrapping the SQLite database containing the publications.

    Parameters
    ----------
    filename : str
        Path to the SQLite database file.
    """
    def __init__(self, filename=DEFAULT_DB):
        self.filename = filename
        self.con = sql.connect(filename)
        pubs_table_exists = self.con.execute(
                                """
                                   SELECT COUNT(*) FROM sqlite_master
                                   WHERE type='table' AND name='pubs';
                                """).fetchone()[0]
        if not pubs_table_exists:
            self.create_table()

    def create_table(self):
        self.con.execute("""CREATE TABLE pubs(
                                id UNIQUE,
                                bibcode UNIQUE,
                                year,
                                month,
                                date,
                                mission,
                                science,
                                json)""")

    def add(self, article, mission="kepler", science="exoplanets"):
        """Adds a single article object to the database.

        Parameters
        ----------
        article : `ads.Article` object.
            The object typically returned by `ads.query`.
        """
        log.debug('Ingesting {}'.format(article.bibcode))
        # Also store the extra metadata in the json string
        month = article.pubdate[0:7]
        article._raw['mission'] = mission
        article._raw['science'] = science
        try:
            cur = self.con.execute("INSERT INTO pubs "
                                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                   [article.id, article.bibcode,
                                    article.year, month, article.pubdate,
                                    mission, science,
                                    json.dumps(article._raw)])
            log.info('Inserted {} row(s).'.format(cur.rowcount))
            self.con.commit()
        except sql.IntegrityError:
            log.warning('{} was already ingested.'.format(article.bibcode))

    def add_interactively(self, article, statusmsg=""):
        """Adds an article by prompting the user for the classification.

        Parameters
        ----------
        article : `ads.Article` object
        """
        # Do not show an article that is already in the database
        if article in self:
            log.warning('{} is already in the database -- skipping.'.format(article.bibcode))
            return

        # First, highlight keywords in the title and abstract
        colors = {'KEPLER': Highlight.BLUE,
                  'KIC': Highlight.BLUE,
                  'KOI': Highlight.BLUE,
                  'K2': Highlight.RED,
                  'EPIC': Highlight.RED,
                  'PLANET': Highlight.YELLOW}
        title = article.title[0]
        try:
            abstract = article.abstract
        except AttributeError:
            abstract = ""

        for word in colors:
            pattern = re.compile(word, re.IGNORECASE)
            title = pattern.sub(colors[word] + word + Highlight.END, title)
            abstract = pattern.sub(colors[word]+word+Highlight.END, abstract)

        # Print paper information to stdout
        print(chr(27) + "[2J")  # Clear screen
        print(statusmsg)
        print(title)
        print('-'*len(title))
        print(abstract)
        print('')
        print('Authors: ' + ', '.join(article.author))
        print('Date: ' + article.pubdate)
        print('Status: ' + str(article.property))
        print('URL: http://adsabs.harvard.edu/abs/' + article.bibcode)
        print('')

        # Prompt the user to classify the paper by mission and science
        print('=> Kepler [1], K2 [2], unrelated [3], or skip [any key]? ', end='')
        prompt = input()
        if prompt == "1":
            mission = "kepler"
        elif prompt == "2":
            mission = "k2"
        elif prompt == "3":
            mission = "unrelated"
        else:
            return
        print(mission)

        # Now classify by science
        science = ""
        if mission != "unrelated":
            print('=> Exoplanets [1] or Astrophysics [2]? ', end='')
            prompt = input()
            if prompt == "1":
                science = "exoplanets"
            elif prompt == "2":
                science = "astrophysics"
            print(science)

        self.add(article, mission=mission, science=science)

    def add_by_bibcode(self, bibcode, interactive=False, **kwargs):
        if ads is None:
            log.error("This action requires the ADS key to be setup.")
            return
        
        q = ads.SearchQuery(q=bibcode)
        for article in q:
            # Data products are sometimes returned as NONARTICLE entries
            if article in self:
                log.warning("{} is already in the db.".format(article.bibcode))
            elif 'NONARTICLE' in article.property:
                log.warning("{} is not an article.".format(article.bibcode))
            else:
                if interactive:
                    self.add_interactively(article)
                else:
                    self.add(article, **kwargs)

    def delete_by_bibcode(self, bibcode):
        cur = self.con.execute("DELETE FROM pubs WHERE bibcode = ?;", [bibcode])
        log.info('Deleted {} row(s).'.format(cur.rowcount))
        self.con.commit()

    def __contains__(self, article):
        count = self.con.execute("SELECT COUNT(*) FROM pubs WHERE id = ?;",
                                 [article.id]).fetchone()[0]
        return bool(count)

    def query(self, mission=None, science=None):
        """Query the database by mission and/or science.

        Returns
        -------
        rows : list
            List of SQLite result rows.
        """
        # Build the query
        if mission is None:
            where = "(mission = 'kepler' OR mission = 'k2') "
        else:
            where = "(mission = '{}') ".format(mission)

        if science is not None:
            where += " AND science = '{}' ".format(science)

        cur = self.con.execute("SELECT year, month, json "
                               "FROM pubs "
                               "WHERE {} "
                               "ORDER BY date DESC; ".format(where))
        return cur.fetchall()

    def to_markdown(self, title="Publications", group_by_month=False, **kwargs):
        """Returns the publication list in markdown format.
        """
        if group_by_month:
            group_idx = 1
        else:
            group_idx = 0  # by year

        import collections
        articles = collections.OrderedDict({})
        for row in self.query(**kwargs):
            group = row[group_idx]
            if group.endswith("-00"):
                group = group[:-3] + "-01"
            if group not in articles:
                articles[group] = []
            articles[group].append(json.loads(row[2]))

        templatedir = os.path.join(PACKAGEDIR, 'templates')
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(templatedir))
        template = env.get_template('template.md')
        markdown = template.render(title=title, articles=articles)
        if sys.version_info >= (3, 0):
            return markdown  # Python 3
        else:
            return markdown.encode("utf-8")  # Python 2

    def plot(self):
        """Saves beautiful plot of the database."""
        for extension in ['pdf', 'png']:
            plot.plot_by_year(self, "kpub-publication-rate.{}".format(extension))
            plot.plot_science_piechart(self, "kpub-piechart.{}".format(extension))


    def update(self, month=None,
               exclude=['keplerian', 'johannes', 'k<sub>2</sub>', "kepler equation",
                        "kepler's equation", "xmm-newton", "kepler's law", "kepler's third law",
                        "kepler problem", "kepler crater", "kepler's supernova", "kepler's snr"]):
        """Query ADS for new publications.

        Parameters
        ----------
        month : str
            Of the form "YYYY-MM".

        exclude : list of str
            Ignore articles if they contain any of the strings given
            in this list. (Case-insensitive.)
        """
        if ads is None:
            log.error("This action requires the ADS key to be setup.")
            return

        if month is None:
            month = datetime.datetime.now().strftime("%Y-%m")

        # First show all the papers with the Kepler funding message in the ack
        log.info("Querying ADS for acknowledgements (month={}).".format(month))
        database = "astronomy"
        qry = ads.SearchQuery(q="""(ack:"Kepler mission"
                                    OR ack:"K2 mission"
                                    OR ack:"Kepler team"
                                    OR ack:"K2 team")
                                   -ack:"partial support from"
                                   pubdate:"{}"
                                   database:"{}"
                                """.format(month, database),
                              rows=9999999999)
        articles = list(qry)
        for idx, article in enumerate(articles):
            statusmsg = ("Showing article {} out of {} that mentions Kepler "
                         "in the acknowledgements.\n\n".format(
                            idx+1, len(articles)))
            self.add_interactively(article, statusmsg=statusmsg)

        # Then search for keywords in the title and abstracts
        log.info("Querying ADS for titles and abstracts (month={}).".format(month))
        qry = ads.SearchQuery(q="""(abs:"Kepler"
                                    OR abs:"K2"
                                    OR abs:"KIC"
                                    OR abs:"EPIC"
                                    OR abs:"KOI"
                                    OR title:"Kepler"
                                    OR title:"K2")
                                   pubdate:"{}"
                                   database:"{}"
                                """.format(month, database),
                              rows=9999999999)
        articles = list(qry)

        for idx, article in enumerate(articles):
            # Ignore articles without abstract
            if not hasattr(article, 'abstract'):
                continue
            abstract_lower = article.abstract.lower()

            ignore = False

            # Ignore articles containing any of the excluded terms
            for term in exclude:
                if term.lower() in abstract_lower:
                    ignore = True

            # Ignore articles already in the database
            if article in self:
                ignore = True

            # Ignore all the unrefereed non-arxiv stuff
            try:
                if "NOT REFEREED" in article.property and article.pub != "ArXiv e-prints":
                    ignore = True
            except AttributeError:
                pass  # no .pub attribute

            # Ignore proposals and cospar abstracts
            if ".prop." in article.bibcode or "cosp.." in article.bibcode:
                ignore = True

            if not ignore:  # Propose to the user
                statusmsg = '(Reviewing article {} out of {}.)\n\n'.format(
                                idx+1, len(articles))
                self.add_interactively(article, statusmsg=statusmsg)
        log.info('Finished reviewing all articles for {}.'.format(month))


def kpub(args=None):
    """Lists the publications in the database in Markdown format."""
    parser = argparse.ArgumentParser(
        description="View the Kepler/K2 publication list in markdown format.")
    parser.add_argument('-f', metavar='dbfile',
                        type=str, default=DEFAULT_DB,
                        help="Location of the Kepler/K2 publication list db. "
                             "Defaults to ~/.kpub.db.")
    parser.add_argument('-e', '--exoplanets', action='store_true',
                        help='Only show exoplanet publications.')
    parser.add_argument('-a', '--astrophysics', action='store_true',
                        help='Only show astrophysics publications.')
    parser.add_argument('-k', '--kepler', action='store_true',
                        help='Only show Kepler publications.')
    parser.add_argument('-2', '--k2', action='store_true',
                        help='Only show K2 publications.')
    parser.add_argument('-m', '--month', action='store_true',
                        help='Group the papers by month rather than year.')
    parser.add_argument('-s', '--save', action='store_true',
                        help='Save the output and plots in the current directory.')
    args = parser.parse_args(args)

    db = PublicationDB(args.f)

    if args.save:
        for bymonth in [True, False]:
            if bymonth:
                suffix = "-by-month"
                title_suffix = " by month"
            else:
                suffix = ""
                title_suffix = ""
            output = db.to_markdown(group_by_month=bymonth,
                                    title="Kepler/K2 publications{}".format(title_suffix))
            filename = 'kpub{}.md'.format(suffix)
            log.info('Writing {}'.format(filename))
            f = open(filename, 'w')
            f.write(output)
            f.close()
            for science in ['exoplanets', 'astrophysics']:
                output = db.to_markdown(group_by_month=bymonth,
                                        science=science,
                                        title="Kepler/K2 {} publications{}".format(science.capitalize(), title_suffix))
                filename = 'kpub-{}{}.md'.format(science, suffix)
                log.info('Writing {}'.format(filename))
                f = open(filename, 'w')
                f.write(output)
                f.close()
            for mission in ['kepler', 'k2']:
                output = db.to_markdown(group_by_month=bymonth,
                                        mission=mission,
                                        title="{} publications{}".format(mission.capitalize(), title_suffix))
                filename = 'kpub-{}{}.md'.format(mission, suffix)
                log.info('Writing {}'.format(filename))
                f = open(filename, 'w')
                f.write(output)
                f.close()
        # Also make plots
        for extension in ['pdf', 'png']:
            plot.plot_by_year(db, "kpub-publication-rate.{}".format(extension))
            plot.plot_science_piechart(db, "kpub-piechart.{}".format(extension))
    else:
        if args.exoplanets and not args.astrophysics:
            science = "exoplanets"
        elif args.astrophysics and not args.exoplanets:
            science = "astrophysics"
        else:
            science = None

        if args.kepler and not args.k2:
            mission = "kepler"
        elif args.k2 and not args.kepler:
            mission = "k2"
        else:
            mission = None
        
        output = db.to_markdown(group_by_month=args.month,
                                mission=mission,
                                science=science)
        from signal import signal, SIGPIPE, SIG_DFL
        signal(SIGPIPE, SIG_DFL)
        print(output)


def kpub_plot(args=None):
    """Creates beautiful plots of the database."""
    parser = argparse.ArgumentParser(
        description="Creates beautiful plots of the database.")
    parser.add_argument('-f', metavar='dbfile',
                        type=str, default=DEFAULT_DB,
                        help="Location of the Kepler/K2 publication list db. "
                             "Defaults to ~/.kpub.db.")
    args = parser.parse_args(args)

    PublicationDB(args.f).plot()


def kpub_update(args=None):
    """Interactively query ADS for new publications."""
    parser = argparse.ArgumentParser(
        description="Interactively query ADS for new publications.")
    parser.add_argument('-f', metavar='dbfile',
                        type=str, default=DEFAULT_DB,
                        help="Location of the Kepler/K2 publication list db. "
                             "Defaults to ~/.kpub.db.")
    parser.add_argument('month', nargs='?', default=None,
                        help='Month to query, e.g. 2015-06.')
    args = parser.parse_args(args)

    PublicationDB(args.f).update(month=args.month)


def kpub_add(args=None):
    """Add a publication with a known ADS bibcode."""
    parser = argparse.ArgumentParser(
        description="Add a paper to the Kepler/K2 publication list.")
    parser.add_argument('-f', metavar='dbfile',
                        type=str, default=DEFAULT_DB,
                        help="Location of the Kepler/K2 publication list db. "
                             "Defaults to ~/.kpub.db.")
    parser.add_argument('bibcode', nargs='+',
                        help='ADS bibcode that identifies the publication.')
    args = parser.parse_args(args)

    db = PublicationDB(args.f)
    for bibcode in args.bibcode:
        db.add_by_bibcode(bibcode, interactive=True)


def kpub_delete(args=None):
    """Deletes a publication using its ADS bibcode."""
    parser = argparse.ArgumentParser(
        description="Deletes a paper from the Kepler/K2 publication list.")
    parser.add_argument('-f', metavar='dbfile',
                        type=str, default=DEFAULT_DB,
                        help="Location of the Kepler/K2 publication list db. "
                             "Defaults to ~/.kpub.db.")
    parser.add_argument('bibcode', nargs='+',
                        help='ADS bibcode that identifies the publication.')
    args = parser.parse_args(args)

    db = PublicationDB(args.f)
    for bibcode in args.bibcode:
        db.delete_by_bibcode(bibcode)


def kpub_import(args=None):
    """Import publications from a csv file.

    The csv file must contain entries of the form "bibcode,mission,science".
    The actual metadata of each publication will be grabbed using the ADS API,
    hence this routine may take 10-20 minutes to complete.
    """
    parser = argparse.ArgumentParser(
        description="Batch-import papers into the Kepler/K2 publication list "
                    "from a CSV file. The CSV file must have three columns "
                    "(bibcode,mission,science) separated by commas. "
                    "For example: '2004ApJ...610.1199G,kepler,astrophysics'.")
    parser.add_argument('-f', metavar='dbfile',
                        type=str, default=DEFAULT_DB,
                        help="Location of the Kepler/K2 publication list db. "
                             "Defaults to ~/.kpub.db.")
    parser.add_argument('csvfile',
                        help="Filename of the csv file to ingest.")
    args = parser.parse_args(args)

    db = PublicationDB(args.f)
    for line in ProgressBar(open(args.csvfile, 'r').readlines()):
        col = line.split(',')  # Naive csv parsing
        db.add_by_bibcode(col[0], mission=col[1], science=col[2].strip())


def kpub_export(args=None):
    """Export the bibcodes and classifications in CSV format."""
    parser = argparse.ArgumentParser(
        description="Export the Kepler/K2 publication list in CSV format.")
    parser.add_argument('-f', metavar='dbfile',
                        type=str, default=DEFAULT_DB,
                        help="Location of the Kepler/K2 publication list db. "
                             "Defaults to ~/.kpub.db.")
    args = parser.parse_args(args)

    db = PublicationDB(args.f)
    cur = db.con.execute("SELECT bibcode, mission, science "
                         "FROM pubs ORDER BY bibcode;")
    for row in cur.fetchall():
        print('{0},{1},{2}'.format(row[0], row[1], row[2]))


if __name__ == '__main__':
    pass
