import os
import sys

from geocode import geocode
from mlhub.pkg import mlask, mlcat
from mlhub.utils import get_private

mlcat("Bing Map", """\
Welcome to Bing Maps REST service. This service can find the latitude
and longitude coordinates that correspond to location information provided
as a query string.
""")

mlask(end="\n")

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

# Private file stores credentials including the Bing Maps key required
# by the geocoding function

PRIVATE_FILE = "private.json"

path = os.path.join(os.getcwd(), PRIVATE_FILE)

private_dic = get_private(path, "bing")

# Read Bing Maps key from private file for authentication through Bing
# Maps API

if "key" in private_dic:
    BING_MAPS_KEY = private_dic["key"]
else:
    print("There is no key in private.json. " +
          "Please run ml configure bing to upload your key.",
          file=sys.stderr)
    sys.exit(1)


mlcat("GEOCODE", """\
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
    location = geocode("Priceline Pharmacy Albany Creek", BING_MAPS_KEY)

except Exception as e:
    print(f"The bing map key is not correct: {e}\n" +
          "Please run ml configure bing to update your key.",
          file=sys.stderr)
    sys.exit(1)

location = location[0]
out = location.split(",")
latlong = out[0].split(":")
bbox = out[1]

print(f"Latitude:  {latlong[0]}\nLongitude: {latlong[1]}\n")
print(f"Bounding Box: {out[1]}\n")
print(f"Confidence: {out[2]}\n\nCode: {out[3]}\n\nType: {out[4]}\n")
print(f"Address: {','.join(out[5:])}")
print("")
