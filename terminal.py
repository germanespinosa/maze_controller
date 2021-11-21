from console_input import console_input
from console import Console

print("Habitat controller console")
print("-----------------------")
print("type help for more information on available commands")
commands = Console()
cmd = ""
commands.process_command("connect_tracking")
while cmd != "end":
    cmd = console_input("habitat:")
    r = commands.process_command(cmd)
    if r.code == 0:
        print(r.message)
    else:
        commands.print_error(r.message)
