import sys
import json
from rest import Call, Result


class Console:
    def __init__(self, address="0.0.0.0:8081", stderr=sys.stderr):
        if ':' in address:
            self.port = address.split(":")[1]
        else:
            self.port = "8081"
        self.commands = {}
        with open("commands.config") as f:
            self.commands = json.load(f)
        self.error_message = "Command '%s' not found"
        self.stderr = stderr
        self.address = address

    def call(self, action, parameters=[]):
        return Call.get(self.address, action, parameters)

    def print_error(self, *args, **kwargs):
        print(*args, file=self.stderr, **kwargs)

    def console_output(self, result):
        if result.code:
            self.print_error(result.message)
        else:
            print(result.message)

    def process_command(self, cmd):
        parts = cmd.split(" ")
        if len(parts) == 0 or cmd.strip() == "":
            return
        command_str = parts[0]
        if command_str not in self.commands:
            return Result(1, self.error_message % command_str)
        command = self.commands[command_str]
        if command["input_type"] == "console":
            params = parts[1:]
        else:
            params = []
            for key in command["parameters"].keys():
                parameter = command["parameters"][key]
                value = input(parameter["description"] + ": ")
                if value == "" and parameter["mandatory"]:
                    print("Canceled")
                    return
                params.append(value)
        if "confirmation" in command:
            if input(command["confirmation"] + "(Y/n): ").upper() == "N":
                return
        return self.call(command_str, params)

    def help(self, command_name=""):
        if command_name == "":
            print("Maze help")
            print("---------")
            cmds = sorted(self.commands.keys())
            for command_name in cmds:
                cmd = self.commands[command_name]
                print("\t%s: %s" % (command_name, cmd["description"]))
            print("\nFor more details: help [command_name]")
            return
        if command_name not in self.commands:
            print(self.error_message % command_name)
            return
        print("Habitat help")
        print("---------")
        print("Command %s: %s" % (command_name, self.commands[command_name]["description"]))
        print("parameters:")
        usage = command_name
        for param_name in self.commands[command_name]["parameters"].keys():
            parameter = self.commands[command_name]["parameters"][param_name]
            print ("\t%s: type '%s' %s - %s" % (param_name, parameter["type"], "optional" if not parameter["mandatory"] else "mandatory", parameter["description"]))
            usage += " " + ("[" if not parameter["mandatory"] else "") + param_name + ( "]" if not parameter["mandatory"] else "" )
        print("usage: %s\n" % usage)

    def start_server(self):
        self.console_output(self.habitat_remote.start_server())
