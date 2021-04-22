import requests
import sys
import json
import os
from mlhub.pkg import ask_password
import argparse

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


# ----------------------------------------------------------------------
# The geocoding function that gets a list of potential latitude and longitude
# coordinates lists of the address
# ----------------------------------------------------------------------

def geocode(address, inclnb="0", maxres="1"):
    result = []

    # Bing Maps API endpoint for Australian addresses
    API_URL = (f'http://dev.virtualearth.net/REST/v1/Locations?culture=en-AU&query={address}&inclnb={inclnb}&include=queryParse&maxResults={maxres}&userRegion=AU&key={BING_MAPS_KEY}')

    # Get JSON response from Bing Maps API
    response = requests.get(API_URL).json()

    print(response)

    # If the result is 1 or more than 1
    if response["resourceSets"][0]['estimatedTotal'] > 0:

        location_list = response["resourceSets"][0]["resources"]

        for item in location_list:
            result.append(item["point"]["coordinates"])

    else:
        print("No coordinates can be queried for this location. Please make sure you have the correct location.")
        sys.exit(1)

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Running Bing Map.')

    parser.add_argument('address', type=str, nargs='+',
                        help='The location that want to query.')
    parser.add_argument('--inclnb', type=int, default=0, required=False,
                        help='Include the neighborhood with the address information. 0 or 1. ')
    parser.add_argument('--maxres', type=int, default=5, required=False,
                        help='Maximun number of locations to return. The value is between 1-20.')
    args = parser.parse_args()

    address = " ".join(args.address)
    # Perform geocoding on the address to get its latitude and longitude coordinates
    coords = geocode(address, args.inclnb, args.maxres)

    # Print the latitude and longitude coordinates
    print(coords)
