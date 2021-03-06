import requests
import json
import sys
global base_uri
base_uri = "https://raw.githubusercontent.com/germanespinosa/cellworld_data/master/"

def get_resource(resource_type, key0, *argv ):
    resource_uri = base_uri + resource_type + "/" + key0
    for arg in argv:
        resource_uri += "." + arg
    response = requests.get(resource_uri)
    print("URI:" + resource_uri,file=sys.stderr)
    return json.loads(response.text)