import json
import log
import requests


pi_addresses = []
with open("pis", "r") as f:
    pi_addresses = json.load(f)


def get_status(pi_address):
    uri = "http://%s" % pi_address
    uri += "/status"
    response = requests.get(uri)
    if response.status_code == 200:
        return json.loads(response.text)["content"]
