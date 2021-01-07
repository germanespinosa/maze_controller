
commands = dict()

commands["exit"] = dict()
commands["exit"]["description"] = "Quits this console and ends the maze controller"
commands["exit"]["parameters"] = dict()

commands["status"] = dict()
commands["status"]["description"] = "Shows full status of the maze"
commands["status"]["parameters"] = dict()

commands["start"] = dict()
commands["start"]["description"] = "Starts a new experiment"
commands["start"]["parameters"] = dict()
commands["start"]["parameters"]["experiment_name"] = dict()
commands["start"]["parameters"]["experiment_name"]["description"] = "Name of the new experiment"
commands["start"]["parameters"]["experiment_name"]["type"] = "string"
commands["start"]["parameters"]["experiment_name"]["mandatory"] = True
commands["start"]["parameters"]["duration"] = dict()
commands["start"]["parameters"]["duration"]["description"] = "Duration of the experiment in minutes"
commands["start"]["parameters"]["duration"]["type"] = "int"
commands["start"]["parameters"]["duration"]["mandatory"] = False

commands["track"] = dict()
commands["track"]["description"] = "Records the location of an agent during an experiment"
commands["track"]["parameters"] = dict()
commands["track"]["parameters"]["agent_name"] = dict()
commands["track"]["parameters"]["agent_name"]["description"] = "Name of the new experiment"
commands["track"]["parameters"]["agent_name"]["type"] = "string"
commands["track"]["parameters"]["agent_name"]["mandatory"] = True
commands["track"]["parameters"]["x"] = dict()
commands["track"]["parameters"]["x"]["description"] = "x component of the agent's coordinate"
commands["track"]["parameters"]["x"]["type"] = "int"
commands["track"]["parameters"]["x"]["mandatory"] = False
commands["track"]["parameters"]["y"] = dict()
commands["track"]["parameters"]["y"]["description"] = "y component of the agent's coordinate"
commands["track"]["parameters"]["y"]["type"] = "int"
commands["track"]["parameters"]["y"]["mandatory"] = False

commands["end"] = dict()
commands["end"]["description"] = "Ends the current experiment"
commands["end"]["parameters"] = dict()

commands["feeder"] = dict()
commands["feeder"]["description"] = "Activates a water feeder"
commands["feeder"]["parameters"] = dict()
commands["feeder"]["parameters"]["feeder_number"] = dict()
commands["feeder"]["parameters"]["feeder_number"]["description"] = "Number of the feeder to be activated"
commands["feeder"]["parameters"]["feeder_number"]["type"] = "int"
commands["feeder"]["parameters"]["feeder_number"]["mandatory"] = True

commands["open"] = dict()
commands["open"]["description"] = "Opens a door"
commands["open"]["parameters"] = dict()
commands["open"]["parameters"]["door_number"] = dict()
commands["open"]["parameters"]["door_number"]["description"] = "Number of the door to be opened"
commands["open"]["parameters"]["door_number"]["type"] = "int"
commands["open"]["parameters"]["door_number"]["mandatory"] = True

commands["close"] = dict()
commands["close"]["description"] = "Closes a door"
commands["close"]["parameters"] = dict()
commands["close"]["parameters"]["door_number"] = dict()
commands["close"]["parameters"]["door_number"]["description"] = "Number of the door to be closed"
commands["close"]["parameters"]["door_number"]["type"] = "int"
commands["close"]["parameters"]["door_number"]["mandatory"] = True

commands["help"] = dict()
commands["help"]["description"] = "Shows help about available commands"
commands["help"]["parameters"] = dict()
commands["help"]["parameters"]["command_name"] = dict()
commands["help"]["parameters"]["command_name"]["description"] = "Name of the command"
commands["help"]["parameters"]["command_name"]["mandatory"] = False
commands["help"]["parameters"]["command_name"]["type"] = "string"


error_message = "Command '%s' not found"

maze_controller = None

def process_command(cmd, controller):
    global maze_controller
    maze_controller = controller
    parts = cmd.split(" ")
    if len(parts) == 0 or cmd.strip() == "":
        return
    command = parts[0]
    if command not in commands:
        print(error_message % command)
        return
    params = ""
    first = True
    param_index = 1
    if len(parts) - 1 > len(commands[command]["parameters"]):
        print("Too many parameters (received %s, expected %s)." %(len(parts) - 1, len(commands[command]["parameters"])))
        cmd_help(command)
        return
    for param_name in commands[command]["parameters"].keys():
        param = commands[command]["parameters"][param_name]
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
                print ("missing mandatory parameter '%'" % param_name)
    eval("cmd_%s(%s)" % (command, params))


def cmd_help(command_name=""):
    if command_name == "":
        print("Maze help")
        print("---------")
        cmds = sorted(commands.keys())
        for command_name in cmds:
            cmd = commands[command_name]
            print("\t%s: %s" % (command_name, cmd["description"]))
        print("\nFor more details: help [command_name]")
        return
    if command_name not in commands:
        print(error_message % command_name)
        return
    print("Maze help")
    print("---------")
    print("Command %s: %s" % (command_name, commands[command_name]["description"]))
    print("parameters:")
    usage = command_name
    for param_name in commands[command_name]["parameters"].keys():
        parameter = commands[command_name]["parameters"][param_name]
        print ("\t%s: type '%s' %s - %s" % (param_name, parameter["type"], "optional" if not parameter["mandatory"] else "mandatory", parameter["description"]))
        usage += " " + ("[" if not parameter["mandatory"] else "") + param_name + ( "]" if not parameter["mandatory"] else "" )
    print("usage: %s\n" % usage)


def cmd_open(door_number):
    global maze_controller
    maze_controller.open_door(door_number)
    print("opening door %d" % door_number)


def cmd_close(door_number):
    global maze_controller
    maze_controller.close_door(door_number)
    print("closing door %d" % door_number)


def cmd_start(experiment_name, duration = -1):
    global maze_controller
    maze_controller.start_experiment(experiment_name)
    print("starting experiment %s for %d minutes" % (experiment_name, duration))


def cmd_end():
    global maze_controller
    maze_controller.end_experiment()
    print("ending current experiment")


def cmd_exit():
    global maze_controller
    maze_controller.quit()
    print("good bye!")
    quit()


def cmd_status():
    print("all ok")


def cmd_track(agent_name, x, y):
    global maze_controller
    maze_controller.track(agent_name, x, y)


def cmd_feeder (feeder_number):
    global maze_controller
    maze_controller.activate_feeder(feeder_number)
    print("activating feeder %d" % feeder_number)
