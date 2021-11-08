import sys
import json
from remote import Remote, Result
from datetime import datetime

class Console:
    def __init__(self, address="0.0.0.0:8081", stderr=sys.stderr):
        if (':' in address):
            self.port = address.split(":")[1]
        else:
            self.port = "8081"
        self.commands = {}
        with open("commands.config") as f:
            self.commands = json.load(f)
        self.error_message = "Command '%s' not found"
        self.stderr = stderr
        self.habitat_remote = Remote(address)

    def print_error(self, *args, **kwargs):
      print(*args, file=self.stderr, **kwargs)

    def console_output(self, result):
        if result.code:
            self.print_error(result.message)
        else:
            print(result.message)

    def start_server(self):
        self.console_output(self.habitat_remote.start_server())

    def process_command(self, cmd):
        parts = cmd.split(" ")
        if len(parts) == 0 or cmd.strip() == "":
            return
        command = parts[0]
        if command not in self.commands:
            print(self.error_message % command)
            return
        params = ""
        first = True
        param_index = 1
        if len(parts) - 1 > len(self.commands[command]["parameters"]):
            print("Too many parameters (received %s, expected %s)." %(len(parts) - 1, len(self.commands[command]["parameters"])))
            self.help(command)
            return
        for param_name in self.commands[command]["parameters"].keys():
            param = self.commands[command]["parameters"][param_name]
            if len(parts) > param_index:
                if not first:
                    params += ","
                first = False
                if param["type"] == "string":
                    params += '"'
                params += parts[param_index]
                if param["type"] == "string":
                    params += '"'
                param_index += 1
            else:
                if param["mandatory"]:
                    print("missing mandatory parameter '%'" % param_name)
        eval("self.%s(%s)" % (command, params))

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
        print("Maze help")
        print("---------")
        print("Command %s: %s" % (command_name, self.commands[command_name]["description"]))
        print("parameters:")
        usage = command_name
        for param_name in self.commands[command_name]["parameters"].keys():
            parameter = self.commands[command_name]["parameters"][param_name]
            print ("\t%s: type '%s' %s - %s" % (param_name, parameter["type"], "optional" if not parameter["mandatory"] else "mandatory", parameter["description"]))
            usage += " " + ("[" if not parameter["mandatory"] else "") + param_name + ( "]" if not parameter["mandatory"] else "" )
        print("usage: %s\n" % usage)

    def open_door(self, door_number):
        self.console_output(self.habitat_remote.open_door(door_number))

    def feeder_reached(self, feeder_number):
        self.console_output(self.habitat_remote.feeder_reached(feeder_number))

    def close_door(self, door_number):
        self.console_output(self.habitat_remote.close_door(door_number))

    def start_experiment(self):
        subject_name = input("subject name: ")
        occlusions = input("occlusions configuration: ")
        duration = int(input("duration (in minutes): "))
        suffix = input("experiment identifier: ")
        experiment_name = str(datetime.now().year) + str("%02d" % datetime.now().month) + str("%02d" % datetime.now().day) + "_" + str("%02d" % datetime.now().hour) + str("%02d" % datetime.now().minute) + "_" + subject_name + "_" + occlusions + ("_" + suffix if suffix != "" else "")
        self.console_output(self.habitat_remote.start_experiment(subject_name, experiment_name, occlusions, duration, suffix))

    def start_server(self):
        self.console_output(self.habitat_remote.start_server())

    def update_background(self):
        self.console_output(self.habitat_remote.update_background())

    def test_feeder(self, feeder_number, duration, repetitions, wait_time):
        self.console_output(self.habitat_remote.test_feeder(feeder_number, duration, repetitions, wait_time))

    def finish_experiment(self):
        self.console_output(self.habitat_remote.finish_experiment())

    def end(self):
        self.console_output(self.habitat_remote.end())
        quit()

    def status(self):
        self.console_output(self.habitat_remote.status())

    def track(self, agent_name, x, y):
        self.console_output(self.habitat_remote.track(agent_name, x, y))

    def enable_feeder (self, feeder_number):
        self.console_output(self.habitat_remote.enable_feeder(feeder_number))

    def disable_feeder (self, feeder_number):
        self.console_output(self.habitat_remote.disable_feeder(feeder_number))

    def calibrate_door(self, door_number, direction, opening_time, closing_time):
        self.console_output(self.habitat_remote.calibrate_door(door_number, direction, opening_time, closing_time))

    def save_doors_calibration(self):
        self.console_output(self.habitat_remote.save_doors_calibration())

    def load_doors_calibration(self):
        self.console_output(self.habitat_remote.load_doors_calibration())

    def test_door(self, door_number, repetitions):
        self.console_output(self.habitat_remote.test_door(door_number,repetitions))
