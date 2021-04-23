import requests
import sys
import json
import os
import argparse


# ----------------------------------------------------------------------
# The geocoding function that gets a list of potential latitude and longitude
# coordinates lists of the address
# ----------------------------------------------------------------------

def geocode(address, bing_map_key, inclnb="0", maxres="1", google=False):
    result = []

    # Bing Maps API endpoint for Australian addresses
    API_URL = (
        f"http://dev.virtualearth.net/REST/v1/Locations?culture=en-AU&query={address}&inclnb={inclnb}&include=queryParse&maxResults={maxres}&userRegion=AU&key={bing_map_key}")

    # Get JSON response from Bing Maps API
    response = requests.get(API_URL).json()

    # If the estimatedTotal is 1 or more than 1
    if response["resourceSets"][0]['estimatedTotal'] > 0:

        location_list = response["resourceSets"][0]["resources"]

        for item in location_list:
            result.append(item["point"]["coordinates"])

    else:
        print("No coordinates can be queried for this location. Please make sure you have the correct location.")
        sys.exit(1)

    if google:
        google_out = []
        for item in result:
            link = f"https://maps.google.com/?q={item[0]},{item[1]}"
            google_out.append(link)
        return google_out

    return result


if __name__ == "__main__":
    # private file stores credentials including the Bing Maps key required by the geocoding function
    PRIVATE_FILE = "private.json"
    path = os.path.join(os.getcwd(), PRIVATE_FILE)

    if os.path.exists(path):
        with open(path) as f:
            private = json.load(f)
    else:
        print("Please run ml configure bing to paste your key.", file=sys.stderr)
        sys.exit(1)

    # Read Bing Maps key from private file for authentication through Bing Maps API
    if "key" in private:
        BING_MAPS_KEY = private["key"]
    else:
        print("There is no key in private.json. Please run ml configure bing to upload your key.", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Running Bing Map.')

    parser.add_argument('address', type=str, nargs='+',
                        help='The location that want to query.')
    parser.add_argument('--inclnb', type=int, default=0, required=False,
                        help='Include the neighborhood with the address information. 0 or 1. ')
    parser.add_argument('--maxres', type=int, default=5, required=False,
                        help='Maximun number of locations to return. The value is between 1-20.')
    parser.add_argument('--google', type=bool,
                        help='Show the location in the Google Map.')
    args = parser.parse_args()

    address = " ".join(args.address)

    try:
        location = geocode(address, BING_MAPS_KEY, args.inclnb, args.maxres, args.google)
    except Exception as e:
        print("The bing map key is not correct. Please run ml configure bing to update your key", file=sys.stderr)
        sys.exit(1)

    # Print the latitude and longitude coordinates
    print(location)
