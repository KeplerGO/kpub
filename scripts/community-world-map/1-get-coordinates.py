"""Obtain the affiliation coordinates of the first authors of K2 papers.

Writes a file called `coordinates.csv`.
"""
import nltk
import time
from tqdm import tqdm
import kpub
from geopy.geocoders import GoogleV3

OUTPUT_FN = 'coordinates.csv'

# Step 1: obtain the first author affiliations from kpub
locations = []
db = kpub.PublicationDB()
all_publications = db.get_all()
for publication in all_publications:
    affiliations = publication['aff']
    # Use the first three authors
    for aff in affiliations:
        # Help the geolocator by only passing on the final components of the address
        aff_suffix = ",".join(aff.split(";")[-1].split(",")[-2:]).strip(" ;,-")
        locations.append(aff_suffix)
unique_locations = nltk.FreqDist(locations)
print("Found {} unique locations".format(len(unique_locations)))


# Step 2: initialize the Google geolocator
from config import API_KEY
geolocator = GoogleV3(api_key=API_KEY)
time.sleep(2)

# Step 3: geolocate all affiliations
out = open(OUTPUT_FN, "w")
out.write("lon,lat,count,name\n")
fd_aff = nltk.FreqDist(locations)
for name, count in tqdm(unique_locations.items()):
    if name == "-" or name == "":
        continue
    try:
        location = geolocator.geocode(name, timeout=10)
        outstring = "{},{},{},{}\n".format(location.longitude, location.latitude, count, name.replace(",", ";"))
        out.write(outstring)
        out.flush()
        print("Success: {} = {}".format(name, outstring))
    except Exception as e:
        print("Warning: failed to geolocate {} (exception: {})".format(name, e))
        pass
    time.sleep(0.3)
out.close()
