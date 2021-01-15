import threading
import web
import log
from console_input import console_input
import json
from door_control import open_door, close_door, activate_feeder, init_doors
from datetime import datetime

feeder_counters = [0, 0]

experiment = [False, "", datetime.now(), -1]

urls = (
    '/(.*)', 'maze_control'
)
app = web.application(urls, globals())

init_doors()


def response (code, message):
    return {"code": code, "message": message}



class maze_control:
    def activate_feeder(self, n):
        if n not in [1, 2]:
            return response(1, "wrong feeder number (%d)" % n)
        activate_feeder(n)
        return response(0, "feeder %d activated" % n)

    def open_door(self, n):
        if n not in [1, 2, 3, 4]:
            return response(1, "wrong door number (%d)" % n)
        open_door(n)
        return response(0, "door %d opened" % n)

    def close_door(self, n):
        if n not in [1, 2, 3, 4]:
            return response(1, "wrong door number (%d)" % n)
        close_door(n)
        return response(0, "door %d opened" % n)

    def quit(self):
        global app
        app.stop()
        return response(0, "good bye!")

    def status(self):
        if experiment[0]:
            code = 0
            if experiment[3] > 0:
                n = experiment[3] * 60 - (datetime.now() - experiment[2]).seconds
                if n <= 0:
                    message = "experiment %s finishing" % experiment[1]
                else:
                    message = "experiment %s in progress" % experiment[1]
                    message += "(%d seconds remaining)" % n
            else:
                message = "experiment %s in progress" % experiment[1]
        else:
            code = 1
            message = "no active experiment"

        import pi_status
        for address in pi_status.pi_addresses:
            message += "\nPi at %s: " % address
            ps = pi_status.get_status(address)
            message += "ok\n"
            for door_status in ps["door_status"]:
                message += ("door %d: " % door_status["door_number"]) + door_status["state"] + "\n"
            message += ("feeder %d: " % ps["feeder_status"]["feeder_number"]) + ps["feeder_status"]["state"]

        return response(code, message)

    def feeder(self, feeder_number):
        if feeder_number not in [1, 2]:
            return response(1, "wrong feeder number (%d)" % feeder_number)
        feeder_counters[feeder_number - 1] += 1
        log.write_log("feeder %d reached (%d)" % (feeder_number, feeder_counters[feeder_number - 1]))
        message = ""
        if feeder_number == 1:
            if experiment[0]:
                print(experiment)
                if experiment[3] > 0:
                    n = experiment[3] * 60 - (datetime.now() - experiment[2]).seconds
                    print(n)
                    if n <= 0:
                        experiment[0] = False
            if experiment[0]:
                self.close_door(1)
                self.open_door(2)
                self.close_door(0)
                self.open_door(3)
                self.activate_feeder(2)
                message = "feeder 2 activated"
            else:
                self.close_door(1)
                self.close_door(2)
                self.close_door(0)
                self.close_door(3)
                message = 'ended experiment ' + experiment[1]
                log.write_log(message)
        else:
            self.close_door(3)
            self.open_door(0)
            self.close_door(2)
            self.open_door(1)
            self.activate_feeder(1)
            message = "feeder 1 activated"

        return response(0, message)

    def start_experiment(self, experiment_name, duration=-1):
        experiment[0] = True
        experiment[1] = experiment_name
        experiment[2] = datetime.now()
        experiment[3] = duration
        for feeder_index in range(len(feeder_counters)):
            feeder_counters[feeder_index] = 0
        log.start_log(experiment[1] + ".log")
        message = 'started experiment %s' % experiment[1]
        if duration > -1:
            message += " for %d minutes" % duration
        log.write_log(message)
        self.close_door(0)
        self.close_door(1)
        self.close_door(2)
        self.close_door(3)
        self.activate_feeder(1)
        return response(0, message)

    def end_experiment(self):
        experiment[0] = False
        message = 'ending experiment ' + experiment[1]
        return response(0, message)

    def track(self, agent, x, y):
        message = 'agent %s location recorded at coordinates: (%d,%d)' % (agent, x, y)
        log.write_log('{"agent":"%s","coordinates":{"x":%d,"y":%d}}' % (agent, x, y))
        return response(0, message)

    def GET(self, querystring):
        qs = querystring.split("/")
        command = qs[0]
        if command == "feeder":
            feeder_number = int(qs[1])
            return json.dumps(self.feeder(feeder_number))
        elif command == "start":
            experiment_name = qs[1]
            if len(qs) > 2 and qs[2].isnumeric():
                duration = int(qs[2])
                return json.dumps(self.start_experiment(experiment_name,duration))
            else:
                return json.dumps(self.start_experiment(experiment_name))
        elif command == "end":
            return json.dumps(self.end_experiment())
        elif command == "track":
            agent = qs[1]
            x = qs[2]
            y = qs[3]
            return json.dumps(self.track(agent, x, y))
        else:
            return 'unknown command'


def console():
    import time
    import commands
    mc = maze_control()
    time.sleep(2)
    print("Maze controller console")
    print("-----------------------")
    print("type help for more information on available commands")
    while True:
        cmd = console_input("maze" + (":" + experiment[1] if experiment[0] else ""))
        commands.process_command(cmd, mc)


if __name__ == "__main__":
    th = threading.Thread(target=console)
    th.start()
    app.run()
