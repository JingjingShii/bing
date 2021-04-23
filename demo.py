import json
import os
from mlhub.pkg import ask_password
from geocode import geocode
from mlhub.pkg import mlask, mlcat
import sys

mlcat("Bing Map", """\
Welcome to Bing Maps REST service. This service can find the latitude
and longitude coordinates that correspond to location information provided 
as a query string.
""")

mlask(end="\n")

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

# private file stores credentials including the Bing Maps key required by the geocoding function
PRIVATE_FILE = "private.json"

path = os.path.join(os.getcwd(), PRIVATE_FILE)

if os.path.exists(path):
    with open(path) as f:
        private = json.load(f)
else:
    print("Please run ml configure bing to upload your key.", file=sys.stderr)
    sys.exit(1)

# Read Bing Maps key from private file for authentication through Bing Maps API
if "key" in private:
    BING_MAPS_KEY = private["key"]
else:
    print("There is no key in private.json. Please run ml configure bing to upload your key.", file=sys.stderr)
    sys.exit(1)


mlcat("GEOCODE","""
This part is to generate the latitude and longitude coordinates based
on the query. The result might be several. Here we set the query to
Priceline Pharmacy Albany Creek. In this case, it will generate a pair
of coordinates.
""")

mlask(end="\n")

# ----------------------------------------------------------------------
# If the bing map key is not correct, the user needs to run
# ml configure bing to update key
# ----------------------------------------------------------------------
try:
    location = geocode("Priceline Pharmacy Albany Creek", BING_MAPS_KEY, "0", "5", False)
except Exception as e:
    print("The bing map key is not correct. Please run ml configure bing to update your key.", file=sys.stderr)
    sys.exit(1)


print("Latitude: "+str(location[0][0])+" Longitude: "+str(location[0][1]))

