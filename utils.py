import os
from mlhub.pkg import get_private

# ----------------------------------------------------------------------
# Request bing map key from user.
# ----------------------------------------------------------------------

def request_priv_info():
    PRIVATE_FILE = "private.json"

    path = os.path.join(os.getcwd(), PRIVATE_FILE)

    private_dic = get_private(path, "bing")

    key = private_dic["Bing Map"]["key"]

    return key
