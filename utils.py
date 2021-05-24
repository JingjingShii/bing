import os
from mlhub.pkg import get_private

# ----------------------------------------------------------------------
# Request bing map key from user.
# ----------------------------------------------------------------------

def request_priv_info():
    PRIVATE_FILE = "private.json"

    path = os.path.join(os.getcwd(), PRIVATE_FILE)

    values = get_private(path, "bing", "Bing Map")

    key = values[0]

    return key
