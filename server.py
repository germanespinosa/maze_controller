from rest import Result
from habitat import Habitat
import web

urls = (
    '/(.*)', 'Server'
)
app = web.application(urls, globals())

app.habitat = Habitat()


class Server:
    def __init__(self):
        global app
        self.habitat = app.habitat

    def GET(self, querystring):
        qs = querystring.split("/")
        command = qs[0]
        if command == "enable_feeder":
            feeder_number = int(qs[1])
            return self.habitat.enable_feeder(feeder_number).json()
        elif command == "open_door":
            door_number = int(qs[1])
            return self.habitat.open_door(door_number)
        elif command == "close_door":
            door_number = int(qs[1])
            return self.habitat.close_door(door_number)
        elif command == "feeder_reached":
            feeder_number = int(qs[1])
            return self.habitat.feeder_reached(feeder_number).json()
        elif command == "test_feeder":
            feeder_number = int(qs[1])
            duration = int(qs[2])
            repetitions = int(qs[3])
            wait_time = int(qs[4])
            return self.habitat.test_feeder(feeder_number, duration, repetitions, wait_time).json()
        elif command == "start_experiment":
            experiment_name = qs[1]
            world_name = qs[2]
            if len(qs) > 3 and qs[3].isnumeric():
                duration = int(qs[3])
                return self.habitat.start_experiment(experiment_name, world_name, duration).json()
            else:
                return self.habitat.start_experiment(experiment_name, world_name).json()
        elif command == "finish_experiment":
            return self.habitat.finish_experiment().json()
        elif command == "save_doors_calibration":
            return self.habitat.save_doors_calibration()
        elif command == "load_doors_calibration":
            return self.habitat.load_doors_calibration()
        elif command == "test_door":
            door_number = int(qs[1])
            repetitions = int(qs[2])
            return self.habitat.test_door(door_number, repetitions)
        elif command == "calibrate_door":
            door_number = int(qs[1])
            direction = int(qs[2])
            opening_time = float(qs[3])
            closing_time = float(qs[4])
            return self.habitat.calibrate_door (door_number, direction, opening_time, closing_time)
        elif command == "track":
            agent = qs[1]
            x = int(qs[2])
            y = int(qs[3])
            return self.habitat.track(agent, x, y).json()
        elif command == "end":
            app.stop()
            return Result (0,"good bye!").json()
        elif command == "status":
            return self.habitat.status().json()
        else:
            return Result(1, "unknown command").json()

if __name__ == "__main__":
    app.run()
