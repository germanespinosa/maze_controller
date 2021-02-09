from console import Console
commands = Console("0.0.0.0:8082")
print("CONSOLE TEST STARTED")
commands.process_command("start_server")
commands.process_command("start_experiment test_condole 1")
for e in range(3):
    commands.process_command("feeder_reached 1")
    for x in range(-20, 21):
        commands.process_command("track mouse %d 0" % x)
    commands.process_command("feeder_reached 2")
commands.process_command("finish_experiment")
commands.process_command("end")

