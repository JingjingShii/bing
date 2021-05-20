import requests
import sys
import json
import os
import argparse
import csv
from mlhub.pkg import get_cmd_cwd
from utils import request_priv_info

# ----------------------------------------------------------------------
# The geocoding function that generates a list of potential latitude and longitude
# coordinates lists of the address
# ----------------------------------------------------------------------

def geocode(address, bing_map_key, inclnb="0", maxres="1", google=False):
    result = []
    for item in address:
        loc_res = []

        # Bing Maps API endpoint for Australian addresses
        API_URL = (
            f"http://dev.virtualearth.net/REST/v1/Locations?culture=en-AU&query={item}&inclnb={inclnb}&include=queryParse&maxResults={maxres}&userRegion=AU&key={bing_map_key}")

        # Get JSON response from Bing Maps API
        response = requests.get(API_URL).json()

        # If the estimatedTotal is 1 or more than 1
        if response["resourceSets"][0]['estimatedTotal'] > 0:

            loc_inform = response["resourceSets"][0]["resources"]

            cell = ""
            for item in loc_inform:
                latitude = item["point"]["coordinates"][0]
                longitutde = item["point"]["coordinates"][1]

                if google:
                    link = f"https://maps.google.com/?q={latitude},{longitutde}"
                    cell = str(latitude) + "," + str(longitutde) + "," + link
                else:
                    cell = str(latitude) + "," + str(longitutde)

                loc_res.append(cell)

        else:
            print(
                "No coordinates can be queried for this location. Please make sure you have the correct location.")
            sys.exit(1)

        result.append(loc_res)

    return result


if __name__ == "__main__":
    key = request_priv_info()

    parser = argparse.ArgumentParser(description='Running Bing Map.')

    parser.add_argument('address', type=str, nargs='*',
                        help='The location that want to query.')
    parser.add_argument('--inclnb', '-i', type=int, default=0, required=False,
                        help='Include the neighborhood with the address information. 0 or 1. ')
    parser.add_argument('--maxres', '-m', type=int, default=5, required=False,
                        help='Maximun number of locations to return. The value is between 1-20.')
    parser.add_argument('--google', '-g', type=bool,
                        help='Show the location in the Google Map.')
    parser.add_argument('--to', '-t', type=str,
                        help='Output csv file path. ')
    parser.add_argument('--verbose', '-v', type=bool,
                        help='Print out the result.')
    args = parser.parse_args()

    address = " ".join(args.address)

    path = os.path.join(get_cmd_cwd(), address)

    location_list = []

    if os.path.exists(path):
        # If input is a csv file
        with open(path) as f:
            cf = csv.reader(f)
            for row in cf:
                location_list.append(row[0])
    else:
        # If input is a location string
        location_list.append(address)

    try:
        result = geocode(location_list, key, args.inclnb, args.maxres, args.google)

        # If the output file name is given
        if args.to:
            to = os.path.join(get_cmd_cwd(), args.to)
            with open(to, 'w', newline='') as file:
                writer = csv.writer(file)
                for item in result:
                    writer.writerow(item)

        # If the users want to print out the result
        if args.verbose:
            for item in result:
                print(', '.join(item))

    except Exception as e:
        print("The bing map key is not correct. Please run ml configure bing to update your key", file=sys.stderr)
        sys.exit(1)
