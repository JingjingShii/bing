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
CONFIG_FILE = "private.json"

path = os.path.join(os.getcwd(), "private.json")

if not os.path.getsize("private.json"):

    msg = "Please paste your bing map key here:"

    msg_saved = """
    That information has been saved into the file:

        {}
    """.format(path)

    msg_request = f"""\
Bing Map key is required to access this service (and to run this command).
See the README for details of a free key. If you have a key
then please paste the key here. 
"""
    print(msg_request, file=sys.stderr)
    map_key = ask_password(prompt=msg)
    data = {}

    if len(map_key) >0:
        data["bing_maps_key"] = map_key
        with open("private.json", "w") as outfile:
            json.dump(data, outfile)
        print(msg_saved, file=sys.stderr)

# Read credentials from config file
with open(CONFIG_FILE) as f:
    config = json.load(f)

# Read Bing Maps key from config file for authentication through Bing Maps API
BING_MAPS_KEY = config["bing_maps_key"]

mlcat("GEOCODE","""
This part is to generate the latitude and longitude coordinates based
on the query. The result might be several. Here we set the query to
Priceline Pharmacy Albany Creek. In this case, it will generate a pair
of coordinates.
""")

mlask(end="\n")

# ----------------------------------------------------------------------
# If the bing map key is not correct, the content in private.json will
# be erased. The users need to paste their key again.
# ----------------------------------------------------------------------
try:
    location = geocode("Priceline Pharmacy Albany Creek", BING_MAPS_KEY, "0", "5", False)

except Exception as e:
    print("The bing map key is not correct. Please run and paste the key again.")
    file = open("private.json", "r+")
    file.truncate(0)
    file.close()
    sys.exit(1)


print("Latitude: "+str(location[0][0])+" Longitude: "+str(location[0][1]))

