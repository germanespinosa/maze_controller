import json
from rest import Call

class Pi:
    def __init__(self, address):
        self.address = address

    def get(self, action, params=[]):
        return Call.get(self.address, action, params)

    def get_addresses():
        addresses = []
        with open("pis", "r") as f:
            addresses = json.load(f)
        return addresses

    def get_pis():
        pis = []
        for address in Pi.get_addresses():
            pis.append(Pi(address))
        return pis
