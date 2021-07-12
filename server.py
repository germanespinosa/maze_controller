from rest import Result
from habitat import habitat
import web

urls = (
    '/(.*)', 'Server'
)
app = web.application(urls, globals())

print (habitat.current_experiment_video_folder)

class Server:

    def GET(self, querystring):
        global habitat
        qs = querystring.split("/")
        command = qs[0]
        if command == "enable_feeder":
            feeder_number = int(qs[1])
            return habitat.enable_feeder(feeder_number).json()
        elif command == "disable_feeder":
            feeder_number = int(qs[1])
            return habitat.disable_feeder(feeder_number).json()
        elif command == "open_door":
            door_number = int(qs[1])
            return habitat.open_door(door_number)
        elif command == "close_door":
            door_number = int(qs[1])
            return habitat.close_door(door_number)
        elif command == "feeder_reached":
            feeder_number = int(qs[1])
            return habitat.feeder_reached(feeder_number).json()
        elif command == "test_feeder":
            feeder_number = int(qs[1])
            duration = int(qs[2])
            repetitions = int(qs[3])
            wait_time = int(qs[4])
            return habitat.test_feeder(feeder_number, duration, repetitions, wait_time).json()
        elif command == "start_experiment":
            experiment_name = qs[1]
            world_name = qs[2]
            if len(qs) > 3 and qs[3].isnumeric():
                duration = int(qs[3])
                return habitat.start_experiment(experiment_name, world_name, duration).json()
            else:
                return habitat.start_experiment(experiment_name, world_name).json()
        elif command == "finish_experiment":
            return habitat.finish_experiment().json()
        elif command == "update_background":
            return habitat.update_background().json()
        elif command == "save_doors_calibration":
            return habitat.save_doors_calibration()
        elif command == "load_doors_calibration":
            return habitat.load_doors_calibration()
        elif command == "test_door":
            door_number = int(qs[1])
            repetitions = int(qs[2])
            return habitat.test_door(door_number, repetitions)
        elif command == "calibrate_door":
            door_number = int(qs[1])
            direction = int(qs[2])
            opening_time = float(qs[3])
            closing_time = float(qs[4])
            return habitat.calibrate_door (door_number, direction, opening_time, closing_time)
        elif command == "track":
            agent = qs[1]
            x = int(qs[2])
            y = int(qs[3])
            return habitat.track(agent, x, y).json()
        elif command == "end":
            habitat.end()
            app.stop()
            return Result(0, "good bye!").json()
        elif command == "status":
            return habitat.status().json()
        else:
            return Result(1, "unknown command").json()
if __name__ == "__main__":
    app.run()
