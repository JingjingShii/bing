import json
import os
from mlhub.pkg import ask_password
from geocode import geocode

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

print(geocode("anu", BING_MAPS_KEY))

