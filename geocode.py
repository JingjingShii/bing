import requests
import sys
import json
import os
import argparse
import csv


# ----------------------------------------------------------------------
# The geocoding function that gets a list of potential latitude and longitude
# coordinates lists of the address
# ----------------------------------------------------------------------

def geocode(address, bing_map_key, to, inclnb="0", maxres="1", google=False):

    to_path = os.path.join(os.getcwd(), to)

    with open(to_path, 'w', newline='') as file:

        writer = csv.writer(file)

        for item in address:
            result = []

            # Bing Maps API endpoint for Australian addresses
            API_URL = (
                f"http://dev.virtualearth.net/REST/v1/Locations?culture=en-AU&query={item}&inclnb={inclnb}&include=queryParse&maxResults={maxres}&userRegion=AU&key={bing_map_key}")

            # Get JSON response from Bing Maps API
            response = requests.get(API_URL).json()

            # If the estimatedTotal is 1 or more than 1
            if response["resourceSets"][0]['estimatedTotal'] > 0:

                loc_list = response["resourceSets"][0]["resources"]

                cell = ""
                for item in loc_list:
                    latitude = item["point"]["coordinates"][0]
                    longitutde = item["point"]["coordinates"][1]

                    if google:
                        link = f"https://maps.google.com/?q={latitude},{longitutde}"
                        cell = str(latitude) + "," + str(longitutde) + "," + link
                    else:
                        cell = str(latitude) + "," + str(longitutde)

                    result.append(cell)

            else:
                print(
                    "No coordinates can be queried for this location. Please make sure you have the correct location.")
                sys.exit(1)

            writer.writerow(result)


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

    # If the input is a csv file

    location_list = []

    if os.path.exists(address):
        with open("/Users/Jingjing/Desktop/test.csv") as f:
            cf = csv.reader(f)
            for row in cf:
                location_list.append(row[0])
    else:
        location_list.append(address)

    try:
        geocode(location_list, BING_MAPS_KEY, args.to, args.inclnb, args.maxres, args.google)
        if args.verbose:
            to_path = os.path.join(os.getcwd(), args.to)
            with open(to_path) as f:
                csv_reader = csv.reader(f, delimiter=',')
                for item in csv_reader:
                    print(item)

    except Exception as e:
        print("The bing map key is not correct. Please run ml configure bing to update your key", file=sys.stderr)
        sys.exit(1)

    # Print the latitude and longitude coordinates
    # print(location)
