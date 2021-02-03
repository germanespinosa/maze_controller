from experiment import Experiment
from console_input import console_input
import time
from commands import Commands

time.sleep(2)
print("Maze controller console")
print("-----------------------")
print("type help for more information on available commands")
commands = Commands("")
cmd = ""
while cmd!="exit":
    cmd = console_input("maze" + (":" + experiment.name if experiment.is_active() else ""))
    commands.process_command(cmd)
