kpub: Kepler publication database
=================================

`kpub` is a mission-specific tool that enables NASA's Kepler/K2 Guest Observer Office to keep track of scientific publications in an easy way. It leverages the [ADS API](https://github.com/andycasey/ads) and SQLite to curate a database that contains the metadata of scientific publications related to the Kepler/K2 spacecraft missions.

## Example use

Generate a list of exoplanet-related publications in markdown format:
```
kpub --exoplanets > exoplanet-publications.md
```

Add a new article to the database using its bibcode:
```
kpub-add 2015arXiv150204715F
```

Remove an article from the list using its bibcode:
```
kpub-delete 2015ApJ...800...46B
```

Search ADS for new Kepler-related articles published in July 2015,
and interactively classify them:
```
kpub-update 2015-07
```

For example output, see the files in the `data/output/` directory
of this repository.

## Installation

To install the latest version from source:
```
git clone https://github.com/barentsen/kpub.git
cd kpub
python setup.py install
```

Note that `kpub` will use `~/.kpub.db` as the default database file.
This repository contains a recent version
of the database file (`data/kpub.db`);
you may want to link this to the default file as follows:
```
ln -s /path/to/git/repo/data/kpub.db ~/.kpub.db
```

## Using kpub

After installation, this package adds the following command-line tools to your path:
* `kpub` prints the list of publications in markdown format;
* `kpub-update` adds new publications by searching ADS (interactive);
* `kpub-add` adds a publication using its ADS bibcode;
* `kpub-delete` deletes a publication using its ADS bibcode;
* `kpub-import` imports bibcodes from a csv file;
* `kpub-export` exports bibcodes to a csv file.

Listed below are the usage instructions for each command:

### kpub
```
$ kpub --help
usage: kpub [-h] [-f dbfile] [-e] [-a] [-k] [-2] [-m]

View the Kepler/K2 publication list in markdown format.

optional arguments:
  -h, --help          show this help message and exit
  -f dbfile           Location of the Kepler/K2 publication list db.Defaults
                      to kpub.db in the package dir.
  -e, --exoplanets    Only show exoplanet publications.
  -a, --astrophysics  Only show astrophysics publications.
  -k, --kepler        Only show Kepler publications.
  -2, --k2            Only show K2 publications.
  -m, --month         Group the papers by month rather than year.
```

### kpub-update
```
$ kpub-update --help
usage: kpub-update [-h] [-f dbfile] [month]

Interactively query ADS for new publications.

positional arguments:
  month       Month to query, e.g. 2015-06.

optional arguments:
  -h, --help  show this help message and exit
  -f dbfile   Location of the Kepler/K2 publication list db.Defaults to
              kpub.db in the package dir.
```

### kpub-add
```
$ kpub-add --help
usage: kpub-add [-h] [-f dbfile] bibcode [bibcode ...]

Add a paper to the Kepler/K2 publication list.

positional arguments:
  bibcode     ADS bibcode that identifies the publication.

optional arguments:
  -h, --help  show this help message and exit
  -f dbfile   Location of the Kepler/K2 publication list db.Defaults to
              kpub.db in the package dir.
```

### kpub-delete
```
$ kpub-delete --help
usage: kpub-delete [-h] [-f dbfile] bibcode [bibcode ...]

Deletes a paper from the Kepler/K2 publication list.

positional arguments:
  bibcode     ADS bibcode that identifies the publication.

optional arguments:
  -h, --help  show this help message and exit
  -f dbfile   Location of the Kepler/K2 publication list db.Defaults to
              kpub.db in the package dir.
```

### kpub-import
```
$ kpub-import --help 
usage: kpub-import [-h] [-f dbfile] csvfile

Batch-import papers into the Kepler/K2 publication list from a CSV file. The
CSV file must have three columns (bibcode,mission,science) separated by
commas. For example: '2004ApJ...610.1199G,kepler,astrophysics'.

positional arguments:
  csvfile     Filename of the csv file to ingest.

optional arguments:
  -h, --help  show this help message and exit
  -f dbfile   Location of the Kepler/K2 publication list db. Defaults to
              kpub.db in the package dir.
```

### kpub-export
```
$ kpub-export --help
usage: kpub-export [-h] [-f dbfile]

Export the Kepler/K2 publication list in CSV format.

optional arguments:
  -h, --help  show this help message and exit
  -f dbfile   Location of the Kepler/K2 publication list db. Defaults to
              kpub.db in the package dir.
```
