import json
import requests

import numpy as np

def get_lat_long(address):
    query_string='https://developers.onemap.sg/commonapi/search?searchVal='+str(address)+'&returnGeom=Y&getAddrDetails=N&pageNum=1'
    resp = requests.get(query_string)
    
    # Check if response is okay
    if resp.status_code != 200:
        return False, np.nan, np.nan

    data = json.loads(resp.content)

    if len(data['results']) > 0:
        data = data['results'][0]
        return True, data['LATITUDE'], data['LONGITUDE']
    else:
        return False, np.nan, np.nan