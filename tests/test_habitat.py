import time
from habitat import Habitat

h = Habitat()
print (h.start_experiment("test", 1))
for e in range(3):
    print (h.feeder_reached(1))
    for x in range(-20, 21):
        print (h.track("mouse", x, 0))
    print (h.feeder_reached(2))
print (h.finish_experiment())

print("ALL TEST FINISHED OK")
