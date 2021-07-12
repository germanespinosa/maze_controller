import os
import json
from rest import Result
from experiment import Experiment
from doors import Doors
from feeders import Feeders
from pi import Pi
from app_comm import App_comm

class Habitat:
    def __init__(self):
        self.videos_folder = "videos"
        self.current_experiment_video_folder = ""
        self.tracking_path = "/maze/agent_tracking/cmake-build-release/agent_tracker"
        self.robot_controller_path = "/maze/agent_tracking/cmake-build-release/robot_controller"
        self.experiment = Experiment()
        self.doors = Doors()
        self.feeders = Feeders()
        self.door_2_open = False
        self.tracker = App_comm([self.tracking_path,
                                 "experiment",
                                 "view"], self.process_tracking)
        self.robot = App_comm([self.robot_controller_path],
                              self.process_robot_controller)

    def process_robot_controller(self, content):
        pass

    def process_tracking(self, content):
        try:
            tracking = json.loads(content)
            frame = tracking["frame"]
            time_stamp = tracking["time_stamp"]
            coordinates = tracking["detection_coordinates"]["coordinates"]
            agent = tracking["detection_coordinates"]["detection_location"]["profile"]["agent_name"]
            location = tracking["detection_coordinates"]["detection_location"]["location"]
            msg = "%s,%f,%f,%f" % (agent, location["x"], location["y"], tracking["theta"])
            self.robot.write(msg)
            self.experiment.track_agent(agent, coordinates, location, frame, time_stamp)
        except:
            pass

    def enable_feeder(self, n):
        return self.feeders.enable(n)

    def disable_feeder(self, n):
        return self.feeders.disable(n)

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
                return self.experiment.experiment_ended()
            else:
                self.tracker.write(self.current_experiment_video_folder + "/" + self.experiment.name + "_ep" + ('%02d' % len(self.experiment.episodes)))
                r = self.experiment.start_episode()
                self.experiment.check = self.doors.close
                self.doors.close(1)
                self.doors.open(2)
                self.doors.close(0)
                self.doors.open(3)
                self.feeders.enable(2)
                return r
        else:
            self.tracker.write("end")
            r = self.experiment.finish_episode()
            self.doors.close(3)
            self.doors.open(0)
            self.doors.close(2)
            self.doors.open(1)
            self.feeders.enable(1)
            return r

    def start_experiment(self, experiment_name, world_name, duration=0):
        self.experiment = Experiment(experiment_name, world_name, duration)
        self.experiment.start()
        if experiment_name != "":
            self.current_experiment_video_folder = self.videos_folder + "/" + experiment_name
            if not os.path.exists(self.current_experiment_video_folder):
                os.makedirs(self.current_experiment_video_folder)
        message = "experiment '%s'" % experiment_name
        if duration > -1:
            message += " for %d minutes" % duration
        self.doors.close(0)
        self.doors.close(1)
        self.doors.close(2)
        self.doors.close(3)
        self.feeders.enable(1)
        return Result(0, message)

    def test_feeder(self, feeder_number, duration, repetitions, wait_time):
        return self.feeders.test(feeder_number, duration, repetitions, wait_time)

    def calibrate_door(self, door_number, direction, opening_time, closing_time):
        return self.doors.calibrate(door_number, direction, opening_time, closing_time)

    def save_doors_calibration(self):
        return self.doors.save_calibration()

    def load_doors_calibration(self):
        return self.doors.load_calibration()

    def update_background(self):
        self.tracker.write("update_background")
        return Result(0, "Background updated")

    def finish_experiment(self):
        return self.experiment.finish()

    def track(self, agent, x, y): # do better
        return self.experiment.track_agent(agent, {"x": x, "y": y}, {"x": 0, "y": 0})

    def test_door(self, door_number, repetitions):
        return self.doors.test_door(door_number,repetitions)

    def end(self):
        self.tracker.write("exit")
        self.tracker.stop()
        self.robot.write("exit")
        self.robot.stop()


habitat = Habitat()