kpub: Kepler publication database
=================================

`kpub` is a mission-specific tool that enables NASA's Kepler/K2 Guest Observer Office to keep track of scientific publications in an easy way. It leverages the [ADS API](https://github.com/andycasey/ads) and SQLite to curate a database that contains the metadata of scientific publications related to the Kepler/K2 spacecraft missions.

Installation
------------
To install the latest version from source:
```
git clone https://github.com/barentsen/kpub.git
cd kpub
python setup.py install
```

Using kpub
----------
After installation, this package adds the following command-line tools to your path:
* `kpub` prints the list of publications in markdown format;
* `kpub-update` adds new publications by searching ADS (interactive);
* `kpub-add` adds a publication using its ADS bibcode;
* `kpub-delete` deletes a publication using its ADS bibcode;
* `kpub-import` imports bibcodes from a csv file;
* `kpub-export` exports bibcodes to a csv file.

Listed below are the detailed usage instructions:


