from console import Console
import sys
commands = Console("0.0.0.0:8082", stderr=sys.stdout)
print("CONSOLE TEST STARTED")
commands.process_command("start_server")

commands.process_command("test_feeder 2 1000 1 1")
exit(0)

for i in range(3):
    commands.process_command("open_door " + str(i))
for i in range(3):
    commands.process_command("close_door " + str(i))

commands.process_command("start_server")
commands.process_command("start_experiment test_condole 1")
for e in range(3):
    commands.process_command("feeder_reached 1")
    for x in range(-20, 21):
        commands.process_command("track mouse %d 0" % x)
    commands.process_command("feeder_reached 2")
commands.process_command("finish_experiment")
commands.process_command("end")

