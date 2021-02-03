import time
from habitat import Habitat
from remote import Remote
from commands import Commands
import requests
import os

os.system("python3 server.py 8082&")
time.sleep(4)

commands = Commands("0.0.0.0:8082")
print("CONSOLE TEST STARTED")
print (commands.process_command("start_experiment test_condole 1"))
for e in range(3):
    print(commands.process_command("feeder_reached 1"))
    for x in range(-20, 21):
        print(commands.process_command("track mouse %d 0" % x))
    print(commands.process_command("feeder_reached 2"))
print(commands.process_command("finish_experiment"))
print(commands.process_command("end"))

