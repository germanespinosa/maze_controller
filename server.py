# install cellworld_py
import httpimport
with httpimport.remote_repo(["cellworld_py_setup"], "https://raw.githubusercontent.com/germanespinosa/cellworld_py/master/"):
    import cellworld_py_setup
cellworld_py_setup.install(version="1.1", force=True)


from habitat import habitat
from rest import Result
import web

urls = ('/(.*)', 'Server')

app = web.application(urls, globals())

print(habitat.current_experiment_video_folder)

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
        elif command == "show_occlusions":
            occlusions_configuration = qs[1]
            return habitat.show_occlusions(occlusions_configuration).json()
        elif command == "hide_occlusions":
            return habitat.hide_occlusions().json()
        elif command == "test_feeder":
            feeder_number = int(qs[1])
            duration = int(qs[2])
            repetitions = int(qs[3])
            wait_time = int(qs[4])
            return habitat.test_feeder(feeder_number, duration, repetitions, wait_time).json()
        elif command == "start_experiment":
            subject_name = qs[1]
            occlusions = qs[2]
            duration = int(qs[3]) * 60
            suffix = qs[4]
            return habitat.start_experiment(subject_name, occlusions, duration, suffix).json()
        elif command == "finish_experiment":
            return habitat.finish_experiment().json()
        elif command == "connect_tracking":
            return habitat.connect_tracking().json()
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
        elif command == "end":
            app.stop()
            return Result(0, "good bye!").json()
        elif command == "status":
            return habitat.status().json()
        else:
            return Result(1, "unknown command").json()


if __name__ == "__main__":
    app.run()
