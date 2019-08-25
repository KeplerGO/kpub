"""Geolocate all Kepler & K2 publications.

Writes a file called `all-coordinates.csv`.
"""
import nltk
import time
from tqdm import tqdm
import kpub
from geopy.geocoders import GoogleV3

OUTPUT_FN = 'all-coordinates.csv'
MEMO = {}

# Initialize the Google geolocator
from config import API_KEY
geolocator = GoogleV3(api_key=API_KEY)
time.sleep(2)


def geolocate(geostring):
    print("Querying {}".format(geostring))
    location = geolocator.geocode(geostring, timeout=10)
    country_short = [c['short_name'] for c in location.raw['address_components']
                     if ('country' in c['types'])][0]
    country_long = [c['long_name'] for c in location.raw['address_components']
                    if ('country' in c['types'])][0]
    return {'lon': location.longitude,
            'lat': location.latitude,
            'geostring': geostring,
            'country_short': country_short,
            'country_long': country_long}



out = open(OUTPUT_FN, "w")
out.write("bibcode,year,pubdate,citation_count,mission,science,lon,lat,country_short,country_long,geostring\n")

# Obtain the first author affiliations from kpub
db = kpub.PublicationDB()
all_publications = db.get_all()
for publication in tqdm(all_publications):
    affiliations = publication['aff']

    aff = affiliations[0]
    # Help the geolocator by only passing on the final components of the address
    geostring = ",".join(aff.split(";")[-1].split(",")[-2:]).strip(" ;,-")
   
    try:
        if len(geostring) > 0:
            if geostring in MEMO:
                gl = MEMO[geostring]
            else:
                time.sleep(0.2)
                gl = geolocate(geostring)
                MEMO[geostring] = gl

            outstring = "{},{},{},{},{},{},{},{},{},{},{}\n".format(
                publication['bibcode'], publication['year'],
                publication['pubdate'], publication['citation_count'],
                publication['mission'], publication['science'],
                gl['lon'], gl['lat'],
                gl['country_short'], gl['country_long'],
                gl['geostring'].replace(",", ";"))

            out.write(outstring)
            out.flush()
    except Exception as e:
        print("Warning: failed to geolocate {} (exception: {})".format(geostring, e))
        pass
    
out.close()
