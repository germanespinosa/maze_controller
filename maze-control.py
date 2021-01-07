import threading
import web
import log
from console_input import console_input

from door_control import open_door, close_door, activate_feeder

feeder_counters = [0, 0]

experiment = [False, ""]

urls = (
    '/(.*)', 'maze_control'
)
app = web.application(urls, globals())

class maze_control:

    def activate_feeder(self, n):
        activate_feeder (n)

    def open_door(self, n):
        open_door(n)

    def close_door(self, n):
        close_door(n)

    def quit(self):
        global app
        app.stop()

    def feeder(self, feeder_number):
        feeder_counters[feeder_number - 1] += 1
        log.write_log("feeder %d reached (%d)" % (feeder_number, feeder_counters[feeder_number - 1]))
        if feeder_number == 1:
            if experiment[0]:
                self.close_door(1)
                self.open_door(2)
                self.close_door(0)
                self.open_door(3)
                self.activate_feeder(2)
            else:
                self.close_door(1)
                self.close_door(2)
                self.close_door(0)
                self.close_door(3)
                log.write_log('ended experiment ' + experiment[1])
        else:
            self.close_door(3)
            self.open_door(0)
            self.close_door(2)
            self.open_door(1)
            self.activate_feeder(1)

    def start_experiment(self, experiment_name):
        experiment[0] = True
        experiment[1] = experiment_name
        for feeder_index in range(len(feeder_counters)):
            feeder_counters[feeder_index] = 0
        log.start_log(experiment[1] + ".log")
        log.write_log('started experiment ' + experiment[1])
        self.close_door(0)
        self.close_door(1)
        self.close_door(2)
        self.close_door(3)
        self.activate_feeder(1)

    def end_experiment(self):
        experiment[0] = False

    def track(self, agent, x, y):
        log.write_log('{"agent":"%s","coordinates":{"x":%d,"y":%d}}' % (agent, x, y))

    def GET(self, querystring):
        qs = querystring.split("/")
        command = qs[0]
        if command == "feeder":
            feeder_number = int(qs[1])
            self.feeder(feeder_number)
        elif command == "start":
            experiment_name = qs[1]
            self.start_experiment(experiment_name)
            return 'started experiment ' + experiment[1]
        elif command == "end":
            self.end_experiment()
        elif command == "track":
            agent = qs[1]
            x = qs[2]
            y = qs[3]
            self.track(agent, x, y)
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
