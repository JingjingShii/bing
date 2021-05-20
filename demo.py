import json
import os
from mlhub.pkg import ask_password
from geocode import geocode
from mlhub.pkg import mlask, mlcat
from utils import request_priv_info
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

key = request_priv_info()


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
    location = geocode(["Priceline Pharmacy Albany Creek"], key, "0", "5", False)

except Exception as e:
    print("The bing map key is not correct. Please run ml configure bing to update your key.", file=sys.stderr)
    sys.exit(1)

location = location[0][0]
out = location.split(",")

print("Latitude: "+out[0]+" Longitude: "+out[1])

