kpub: Kepler publication database
=================================

`kpub` is a mission-specific tool that enables the Kepler/K2 Guest Observer Office to keep track of scientific publications in an easy way. It leverages the [ADS API]() and [SQLite]() to create and manage a self-contained database that contains the metadata of literature articles related to NASA's Kepler/K2 spacecraft missions.

Installation
------------
Install the latest version from source as follows:
```
git clone https://github.com/barentsen/kpub.git
cd kpub
python setup.py install
```

Using kpub
----------
The following command-line tools are available after installation:
* `kpub`: shows the list of publications in Markdown format.
* `kpub-add`: add a publication with a known ADS bibcode (interactive).
* `kpub-update`: add new publications from ADS (interactive).
* `kpub-import`: import publications from a csv file.
* `kpub-export`: export publications to a csv file.
