"""Categorize publications into fine-grained categories
"""
from pprint import pprint
import pandas as pd
import kpub

FILENAME = "k2-categories.csv"

CATEGORIES = {
              'as': 'Asteroseismology',
              'ga': 'Galactic Archaeology',
              'wd': 'White Dwarfs',
              'cv': 'Cataclysmic Variables',
              'eb': 'Eclipsing Binaries',
              'ac': 'Stellar Flares & Activity',
              'ro': 'Stellar Rotation',
              'yo': 'Young stars',
              'cl': 'Clusters',
              'ss': 'Solar System Science',
              'ca': 'Catalogs',
              'da': 'Data Analysis',
              'ed': 'Exoplanet Discovery',
              'ec': 'Exoplanet Characterization',
              'ml': 'Microlensing',
              'sn': 'Supernovae',
              'ag': 'AGN',
              'va': 'Classical Pulsators',
              'ot': 'Others'
              }


if __name__ == "__main__":
    # Read in existing db
    try:
        catdb = pd.read_csv(FILENAME, names=["bibcode", "cat"])
        classified_bibcodes = catdb.bibcode.values
    except FileNotFoundError:
        classified_bibcodes = []

    # Open db in append mode
    out = open(FILENAME, 'a')

    db = kpub.PublicationDB()
    pubs = db.get_all(mission="k2")
    for idx, pub in enumerate(pubs):
        # Skip articles already categorizes
        if pub['bibcode'] in classified_bibcodes:
            continue

        # Clear screen and show the article
        print(chr(27) + "[2J")
        print("Article {} out of {}".format(idx+1, len(pubs)))
        kpub.display_abstract(pub)

        # Prompt the user to classify the paper
        print("Categories:")
        pprint(CATEGORIES)
        while True:
            print("=> Enter code: ", end="")
            prompt = input()
            if prompt not in CATEGORIES.keys():
                print("Error: invalid category")
            else:
                out.write("{},{}\n".format(pub['bibcode'], prompt))
                out.flush()
                break

    out.close()
