import time
from remote import Remote
import requests
import os

os.system("python3 server.py 8081&")
time.sleep(4)
remote = Remote("0.0.0.0:8081")
print (remote.start_experiment("test_remote", 1))
for e in range(3):
    print (remote.feeder_reached(1))
    for x in range(-20, 21):
        print (remote.track("mouse", x, 0))
    print (remote.feeder_reached(2))
print (remote.finish_experiment())
print(remote.end())
