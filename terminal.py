from experiment import Experiment
from console_input import console_input
import time
from console import Console

time.sleep(2)
print("Maze controller console")
print("-----------------------")
print("type help for more information on available commands")
commands = Console()
commands.process_command("start_server")
cmd = ""
while cmd != "end":
    cmd = console_input("maze:")
    commands.process_command(cmd)
