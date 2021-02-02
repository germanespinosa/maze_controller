import time
from habitat import Habitat
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

print(" TEST REMOTE STARTED")

print (requests.get("http://0.0.0.0:8080/start/test_remote/1").text)
for e in range(3):
    print(requests.get("http://0.0.0.0:8080/feeder_reached/1").text)
    for x in range(-20, 21):
        time.sleep(.1)
        print(requests.get("http://0.0.0.0:8080/track/mouse/%d/0" % x).text)
    print(requests.get("http://0.0.0.0:8080/feeder_reached/2").text)
print(requests.get("http://0.0.0.0:8080/finish").text)
print(requests.get("http://0.0.0.0:8080/end").text)

