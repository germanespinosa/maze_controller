import sys
from habitat import Habitat

h = Habitat()

#h.test_feeder(1,1000,1,0)

h.start_experiment("test","10_05", 5)

for i in range(4):
    h.close_door(i)

for i in range(4):
    r = h.open_door(i)

for i in range(4):
    r = h.close_door(i)

for e in range(3):
    print (h.feeder_reached(1))
    for x in range(-20, 21):
        print(h.track("mouse", x, 0))
    print(h.feeder_reached(2))
print (h.finish_experiment())

print("ALL TEST FINISHED OK")
