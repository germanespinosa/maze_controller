import os
import json
from rest import Result
from experiment import Experiment
from doors import Doors
from feeders import Feeders
from pi import Pi
from agent_tracking import Agent_tracking
from datetime import datetime

class Habitat:
    def __init__(self):
        self.videos_folder = "/maze/controller/videos"
        self.current_experiment_video_folder = ""
        self.robot_controller_path = "/maze/agent_tracking/cmake-build-release/robot_controller"
        self.experiment = Experiment()
        self.doors = Doors()
        self.feeders = Feeders()
        self.door_2_open = False
        self.tracker = Agent_tracking("127.0.0.1", 4000, self.process_tracking)

    def process_robot_controller(self, content):
        pass

    def process_tracking(self, content):
        try:
            tracking = json.loads(content)
            frame = tracking["frame"]
            time_stamp = tracking["time_stamp"]
            coordinates = tracking["coordinates"]
            agent = tracking["agent_name"]
            location = tracking["location"]
            rotation = tracking["rotation"]
            data = tracking["data"]
            self.experiment.track_agent(agent, coordinates, location, rotation, frame, time_stamp, data)
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
                episode_number = len(self.experiment.episodes)
                current_episode_video_folder = self.current_experiment_video_folder + "/" + self.experiment.name + "_ep" + ('%02d' % episode_number)
                if not os.path.exists(current_episode_video_folder):
                    os.makedirs(current_episode_video_folder)

                self.tracker.new_episode(self.subject_name, self.sufix, episode_number, self.occlusions, current_episode_video_folder)
                r = self.experiment.start_episode()
                self.experiment.check = self.doors.close
                self.doors.close(1)
                self.doors.open(2)
                self.doors.close(0)
                self.doors.open(3)
                self.feeders.enable(2)
                return r
        else:
            r = self.experiment.finish_episode()
            self.tracker.end_episode()
            self.doors.close(3)
            self.doors.open(0)
            self.doors.close(2)
            self.doors.open(1)
            self.feeders.enable(1)
            return r

    def start_experiment(self, subject_name, experiment_name, occlusions, duration=0, suffix=""):
        self.experiment = Experiment(subject_name, experiment_name, occlusions, duration, suffix)
        self.experiment.start()
        self.subject_name = subject_name
        self.sufix = suffix
        self.occlusions = occlusions
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
        self.tracker.update_backgrounds()
        return Result(0, "Background updated")

    def finish_experiment(self):
        return self.experiment.finish()

    def track(self, agent, x, y): # do better
        return self.experiment.track_agent(agent, {"x": x, "y": y}, {"x": 0, "y": 0})

    def test_door(self, door_number, repetitions):
        return self.doors.test_door(door_number,repetitions)

    def end(self):
        pass

habitat = Habitat()