import log
from rest import Result
from experiment import Experiment
from doors import Doors
from feeders import Feeders
from pi import Pi

class Habitat:
    def __init__(self):
        self.experiment = Experiment()
        self.doors = Doors()
        self.feeders = Feeders()

    def enable_feeder(self, n):
        return self.feeders.enable(n)

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
        if s.code == 0:
            message = s.message
            for pi in Pi.get_pis():
                message += "\nPi at %s: " % pi.address
                ps = pi.get("status")
                if ps.code:
                    message += "error\n"
                else:
                    message += "ok\n"
                    for door_status in ps.content["door_status"]:
                        message += ("door %d: " % door_status["door_number"]) + door_status["state"] + "\n"
                    message += ("feeder %d: " % ps.content["feeder_status"]["feeder_number"]) + ps.content["feeder_status"]["state"]
            return Result(0, message)
        else:
            return s

    def feeder_reached(self, feeder_number):
        if feeder_number not in [1, 2]:
            return Result(1, "wrong feeder number (%d)" % feeder_number)
        if feeder_number == 1:
            if not self.experiment.is_active():
                self.doors.close(1)
                self.doors.close(2)
                self.doors.close(0)
                self.doors.close(3)
                return self.experiment.finish()
            else:
                self.doors.close(1)
                self.doors.open(2)
                self.doors.close(0)
                self.doors.open(3)
                self.feeders.enable(2)
                return self.experiment.start_episode()
        else:
            self.doors.close(3)
            self.doors.open(0)
            self.doors.close(2)
            self.doors.open(1)
            self.feeders.enable(1)
            return self.experiment.finish_episode()

    def start_experiment(self, experiment_name, duration=0):
        self.experiment = Experiment(experiment_name, duration)
        message = "experiment '%s'" % experiment_name
        if duration > -1:
            message += " for %d minutes" % duration
        self.doors.close(0)
        self.doors.close(1)
        self.doors.close(2)
        self.doors.close(3)
        self.feeders.enable(1)
        return Result(0, message)

    def finish_experiment(self):
        return self.experiment.finish()

    def track(self, agent, x, y):
        return self.experiment.track_agent(agent, {"x": x, "y": y})

