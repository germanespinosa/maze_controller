import time
from habitat import Habitat
from remote import Remote

import requests
import os
os.system("python3 server.py &")

h = Habitat()
print (h.start_experiment("test", 1))
for e in range(3):
    print (h.feeder_reached(1))
    for x in range(-20, 21):
        time.sleep(.1)
        print (h.track("mouse", x, 0))
    print (h.feeder_reached(2))
print (h.finish_experiment())

print("API TEST STARTED")

print (requests.get("http://0.0.0.0:8080/start_experiment/test_api/1").text)
for e in range(3):
    print(requests.get("http://0.0.0.0:8080/feeder_reached/1").text)
    for x in range(-20, 21):
        time.sleep(.1)
        print(requests.get("http://0.0.0.0:8080/track/mouse/%d/0" % x).text)
    print(requests.get("http://0.0.0.0:8080/feeder_reached/2").text)
print(requests.get("http://0.0.0.0:8080/finish_experiment").text)

print("REMOTE TEST STARTED")

remote = Remote("0.0.0.0:8080")

print (remote.start_experiment("test_remote", 1))
for e in range(3):
    print (remote.feeder_reached(1))
    for x in range(-20, 21):
        time.sleep(.1)
        print (remote.track("mouse", x, 0))
    print (remote.feeder_reached(2))
print (remote.finish_experiment())


print(requests.get("http://0.0.0.0:8080/end").text)
