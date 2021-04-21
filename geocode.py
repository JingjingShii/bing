import requests
import sys
import json
import os
from mlhub.pkg import ask_password

# config file stores credentials including the Bing Maps key required by the geocoding function
CONFIG_FILE = "config.json"

# Input argument should be a single address
assert len(sys.argv) >= 1, "Please supply an address for geocoding."

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


# The geocoding function that gets latitude and longitude coordinates of the address
def geocode(address, bing_maps_key):
    # Bing Maps API endpoint for Australian addresses
    API_URL = "http://dev.virtualearth.net/REST/v1/Locations?culture=en-AU"

    # Build query string
    query_string = (
            API_URL
            + "&query="
            + address
            + "&inclnb=1&include=queryParse&userRegion=AU&key="
            + bing_maps_key
    )
    # Get JSON response from Bing Maps API
    response = requests.get(query_string).json()
    # Get the latitude and longitude coordinates from the JSON response
    coords = response["resourceSets"][0]["resources"][0]["point"]["coordinates"]

    return coords


if __name__ == "__main__":
    # Read the input address
    address = " ".join(sys.argv[1:])

    # Perform geocoding on the address to get its latitude and longitude coordinates
    coords = geocode(address, BING_MAPS_KEY)

    # Print the latitude and longitude coordinates
    print(coords)
