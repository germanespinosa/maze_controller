import time
import requests
import os

os.system("python3 server.py 8080&")
time.sleep(4)

print("API TEST STARTED")

print (requests.get("http://0.0.0.0:8080/start_experiment/test_api/1").text)
for e in range(3):
    print(requests.get("http://0.0.0.0:8080/feeder_reached/1").text)
    for x in range(-20, 21):
        print(requests.get("http://0.0.0.0:8080/track/mouse/%d/0" % x).text)
    print(requests.get("http://0.0.0.0:8080/feeder_reached/2").text)
print(requests.get("http://0.0.0.0:8080/finish_experiment").text)

print(requests.get("http://0.0.0.0:8080/end").text)

