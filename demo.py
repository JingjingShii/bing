import os
import sys

from geocode import geocode
from mlhub.pkg import mlask, mlcat
from utils import request_priv_info

mlcat("Bing Map", """\
Welcome to Bing Maps REST service. This service can identify the latitude
and longitude coordinates that correspond to the supplied location/address
information.
""")

mlask(end="\n")

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

key = request_priv_info()


mlcat("GEOCODE", """\
Here's an example. We provide the location

    Priceline Pharmacy Albany Creek

and Bing will attempt to match this using its extensive map data.
The result includes the logitude, latitude, and neighbourhood bounding
box, how good the match is, the type of the location, and a clean
address.
""")

mlask(end="\n")

# ----------------------------------------------------------------------
# If the bing map key is not correct, the user needs to run
# ml configure bing to update key
# ----------------------------------------------------------------------
try:
    location = geocode(["Priceline Pharmacy Albany Creek"], key, "0", "5", False)

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
print(f"Confidence: {out[2]}; Code: {out[3]}\n\nType: {out[4]}\n")
print(f"Address: {','.join(out[5:])}")
print("")

mlcat("NEXT", """\
You can use the 'geocode' command to obtain this output for yourself.

      $ ml geocode bing Priceline Pharmacy Albany Creek
""")
