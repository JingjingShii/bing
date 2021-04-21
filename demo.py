import json
import os
from mlhub.pkg import ask_password
from geocode import geocode
from mlhub.pkg import mlask, mlcat
import sys

mlcat("Bing Map", """\
Welcome to Bing Maps REST service. This service can find the the latitude
and longitude coordinates that correspond to location information provided 
as a query string.
""")

mlask(end="\n")

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

# config file stores credentials including the Bing Maps key required by the geocoding function
CONFIG_FILE = "config.json"

if not os.path.exists("config.json") or not os.path.getsize("config.json"):
    print("Please paste your bing map key here:")
    map_key = ask_password()
    data = {}
    data["bing_maps_key"] = map_key
    with open("config.json", "w") as outfile:
        json.dump(data, outfile)

# Read credentials from config file
with open(CONFIG_FILE) as f:
    config = json.load(f)

# Read Bing Maps key from config file for authentication through Bing Maps API
BING_MAPS_KEY = config["bing_maps_key"]

mlcat("GEOCODE","""
This part is to get the latitude and longitude coordinates based on the query,
we set the query to Priceline Pharmacy Albany Creek. You will see its coordinates. 
""")

mlask(end="\n")

# ----------------------------------------------------------------------
# If the bing map key is not correct, the content in config.json will
# be erased. The users need to paste their key again.
# ----------------------------------------------------------------------
try:
    location = geocode("Priceline Pharmacy Albany Creek", "0", "5")
except Exception as e:
    print("The bing map key is not correct. Please past it again.")
    file = open("config.json", "r+")
    file.truncate(0)
    file.close()
    sys.exit(1)

print("Latitude: "+str(location[0])+" Longitude: "+str(location[1]))

