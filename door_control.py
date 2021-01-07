import log
import requests


def open_door(door):
    log.write_log("opening door %d" % door)
    uri = "http://192.168.137." + ("100" if door in [1, 2] else "200")
    uri += ":8081/open/" + str(door)
    response = requests.get(uri)
    if response.status_code == 200:
        if response.text != "open":
            log.write_log("error opening door %d. Expected state 'open', received state '%s'" % (door, response.text))
        else:
            log.write_log("door %d opened" % door)
    else:
        log.write_log("error opening door %d. status code %d" % (door, response.status_code))


def close_door(door):
    log.write_log("closing door %d" % door)
    uri = "http://192.168.137." + ("100" if door in [1, 2] else "200")
    uri += ":8081/close/" + str(door)
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
    uri = "http://192.168.137." + ("100" if feeder_number == 1 else "200")
    uri += ":8081/feeder/" + str(feeder_number)
    try:
        response = requests.get(uri)
    except:
        log.write_log("failed to connect to " + uri)
        return