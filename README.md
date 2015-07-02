kpub: Kepler publication database
=================================

`kpub` is a mission-specific tool that enables NASA's Kepler/K2 Guest Observer 
Office to keep track of scientific publications in an easy way. It leverages 
SQLite and the [ADS API](https://github.com/adsabs/adsabs-dev-api)
(using [Andy Casey's awesome Python client](https://github.com/andycasey/ads)) 
to create and curate a database that contains the metadata of scientific 
publications related to the Kepler/K2 spacecraft missions.

## Example use

Print a list of Kepler-related exoplanet publications in markdown format:
```
kpub --exoplanets
```

Add a new article to the database using its bibcode:
```
kpub-add 2015arXiv150204715F
```

Remove an article using its bibcode:
```
kpub-delete 2015ApJ...800...46B
```

Search ADS interactively for new Kepler-related articles and try to add them:
```
kpub-update 2015-07
```

For example output, see the `data/output/` sub-directory in this repository.

## Installation

To install the latest version from source:
```
git clone https://github.com/barentsen/kpub.git
cd kpub
python setup.py install
```

Note that the `kpub` tools will use `~/.kpub.db` as the default database file.
This repository contains a recent version
of the database file (`data/kpub.db`),
which you may want to link to the default file as follows:
```
ln -s /path/to/git/repo/data/kpub.db ~/.kpub.db
```

The `kpub-add`and `kpub-update` tools that come with this package require
an api key from NASA ADS labs to retrieve publication meta-data.
You need to follow the installation instructions of the [ads client](https://github.com/andycasey/ads) by @andycasey to make this work.

## Command-line tools

After installation, this package adds the following command-line tools to your path:
* `kpub` prints the list of publications in markdown format;
* `kpub-update` adds new publications by searching ADS (interactive);
* `kpub-add` adds a publication using its ADS bibcode;
* `kpub-delete` deletes a publication using its ADS bibcode;
* `kpub-import` imports bibcodes from a csv file;
* `kpub-export` exports bibcodes to a csv file.

Listed below are the usage instructions for each command:

*kpub*
```
$ kpub --help
usage: kpub [-h] [-f dbfile] [-e] [-a] [-k] [-2] [-m]

View the Kepler/K2 publication list in markdown format.

optional arguments:
  -h, --help          show this help message and exit
  -f dbfile           Location of the Kepler/K2 publication list db. Defaults 
                      to ~/.kpub.db.
  -e, --exoplanets    Only show exoplanet publications.
  -a, --astrophysics  Only show astrophysics publications.
  -k, --kepler        Only show Kepler publications.
  -2, --k2            Only show K2 publications.
  -m, --month         Group the papers by month rather than year.
```

*kpub-update*
```
$ kpub-update --help
usage: kpub-update [-h] [-f dbfile] [month]

Interactively query ADS for new publications.

positional arguments:
  month       Month to query, e.g. 2015-06.

optional arguments:
  -h, --help  show this help message and exit
  -f dbfile   Location of the Kepler/K2 publication list db. Defaults to
              ~/.kpub.db.
```

*kpub-add*
```
$ kpub-add --help
usage: kpub-add [-h] [-f dbfile] bibcode [bibcode ...]

Add a paper to the Kepler/K2 publication list.

positional arguments:
  bibcode     ADS bibcode that identifies the publication.

optional arguments:
  -h, --help  show this help message and exit
  -f dbfile   Location of the Kepler/K2 publication list db. Defaults to
              ~/.kpub.db.
```

*kpub-delete*
```
$ kpub-delete --help
usage: kpub-delete [-h] [-f dbfile] bibcode [bibcode ...]

Deletes a paper from the Kepler/K2 publication list.

positional arguments:
  bibcode     ADS bibcode that identifies the publication.

optional arguments:
  -h, --help  show this help message and exit
  -f dbfile   Location of the Kepler/K2 publication list db. Defaults to
              ~/.kpub.db.
```

*kpub-import*
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
              ~/.kpub.db.
```

*kpub-export*
```
$ kpub-export --help
usage: kpub-export [-h] [-f dbfile]

Export the Kepler/K2 publication list in CSV format.

optional arguments:
  -h, --help  show this help message and exit
  -f dbfile   Location of the Kepler/K2 publication list db. Defaults to
              ~/.kpub.db.
```


## Acknowledgements

This tool is made possible thanks to the efforts made by NASA ADS to
provide a web API, and thanks to the excellent Python client that Andy Casey
(@andycasey) wrote to use the API. Thanks ADS, thanks Andy!
