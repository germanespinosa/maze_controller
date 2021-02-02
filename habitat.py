import log
from rest import Result
from experiment import Experiment
from doors import Doors
from feeders import Feeders
from pi import Pi

import requests
import json

class Habitat:
    def __init__(self):
        self.experiment = Experiment()
        self.doors = Doors()
        self.feeders = Feeders()

    def activate_feeder(self, n):
        return self.feeders.activate(n)

    def open_door(self, n):
        return self.doors.open(n)

    def close_door(self, n):
        return self.doors.close(n)

    def quit(self):
        global app
        app.stop()
        return Result(0, "good bye!")

    def status(self):
        s = self.experiment.status()
        for pi in Pi.get_pis():
            message += "\nPi at %s: " % address
            ps = pi.get("status")
            message += "ok\n"
            for door_status in ps["door_status"]:
                message += ("door %d: " % door_status["door_number"]) + door_status["state"] + "\n"
            message += ("feeder %d: " % ps["feeder_status"]["feeder_number"]) + ps["feeder_status"]["state"]
        return Result(0, message)

    def feeder_reached(self, feeder_number):
        print (self.experiment)
        if feeder_number not in [1, 2]:
            return response(1, "wrong feeder number (%d)" % feeder_number)
        feeder_counters[feeder_number - 1] += 1
        log.write_log("feeder %d reached (%d)" % (feeder_number, feeder_counters[feeder_number - 1]))
        message = ""
        if feeder_number == 1:
            if self.experiment[0]:
                print(self.experiment)
                if self.experiment[3] > 0:
                    n = self.experiment[3] * 60 - (datetime.now() - self.experiment[2]).seconds
                    if n <= 0:
                        self.experiment[0] = False
            if self.experiment[0]:
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
                message = 'ended experiment ' + self.experiment[1]
        else:
            self.close_door(3)
            self.open_door(0)
            self.close_door(2)
            self.open_door(1)
            self.activate_feeder(1)
            message = "feeder 1 activated"
        return Result(0, message)

    def start_experiment(self, experiment_name, duration=0):
        self.experiment = Experiment(experiment_name, duration)
        log.start_log(self.experiment[1] + ".log")
        message = 'started experiment %s' % experiment_name
        if duration > -1:
            message += " for %d minutes" % duration
        self.close_door(0)
        self.close_door(1)
        self.close_door(2)
        self.close_door(3)
        self.activate_feeder(1)
        return Result(0, message)

    def end_experiment(self):
        self.experiment.finish()
        return Result(0, message)

    def track(self, agent, x, y):
        self.experiment.track_agent(agent, {"x": x, "y": y})
        return Result(0, message)

class Remote:
    def __init__(self, address):
        self.address = address

    def call (self, action, parameters = []):
        uri = self.address + "/" + action + "/" + "/".join([str(p) for p in parameters])
        return from_response(Call.get(address, action, parameters))

    def activate_feeder(self, n):
        return self.call("activate_feeder", [n])

    def open_door(self, n):
        return self.call("open_door", [n])

    def close_door(self, n):
        return self.call("close_door", [n])

    def quit(self):
        return self.call("quit")

    def status(self):
        return self.call("status")

    def feeder_reached(self, feeder_number):
        return self.call("feeder_reached", [feeder_number])

    def start_experiment(self, experiment_name, duration=0):
        return self.call("start_experiment", [experiment_name, duration])

    def end_experiment(self):
        return self.call("end_experiment")

    def track(self, agent, x, y):
        return self.call("track", [agent, x, y])
