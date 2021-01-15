import json
import log
import requests

door_addresses = {}
feeder_addresses = {}


def new_response (code, message):
    return {"code": code, "message": message}


def init_doors():
    import pi_status
    for address in pi_status.pi_addresses:
        ps = pi_status.get_status(address)
        feeder_addresses[ps["feeder_status"]["feeder_number"]] = address
        doors_status = ps["door_status"]
        for door_status in doors_status:
            door_addresses[door_status["door_number"]] = address


def open_door(door):
    if door not in door_addresses.keys():
        return new_response(1, "wrong door number (%d)" % door)
    uri = "http://%s" % door_addresses[door]
    uri += "/open/" + str(door)
    log.write_log("opening door %d" % door)
    response = requests.get(uri)
    if response.status_code == 200:
        if response.text != "open":
            log.write_log("error opening door %d. Expected state 'open', received state '%s'" % (door, response.text))
        else:
            log.write_log("door %d opened" % door)
    else:
        log.write_log("error opening door %d. status code %d" % (door, response.status_code))


def close_door(door):
    if door not in door_addresses.keys():
        return new_response(1, "wrong door number (%d)" % door)
    uri = "http://%s" % door_addresses[door]
    uri += "/close/" + str(door)
    log.write_log("closing door %d" % door)
    try:
        response = requests.get(uri)
    except:
        log.write_log("failed to connect to " + uri)
        return
    if response.status_code == 200:
        if response.text != "closed":
            log.write_log("error closing door %d. Expected state 'open', received state '%s'" % (door, response.text))
        else:
            log.write_log("door %d closed" % door)
    else:
        log.write_log("error closing door %d. status code %d" % (door, response.status_code))

def activate_feeder(feeder_number):
    if feeder_number not in feeder_addresses.keys():
        return new_response(1, "wrong feeder number (%d)" % feeder_number)
    uri = "http://%s" % feeder_addresses[feeder_number]
    uri += "/enable_feeder"
    try:
        response = requests.get(uri)
    except:
        log.write_log("failed to connect to " + uri)
        return