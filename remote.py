from rest import Call

class Remote:
    def __init__(self, address):
        self.address = address

    def call (self, action, parameters = []):
        return Call.get(self.address, action, parameters)

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

    def finish_experiment(self):
        return self.call("finish_experiment")

    def track(self, agent, x, y):
        return self.call("track", [agent, x, y])

    def end(self):
        return self.call("end")

