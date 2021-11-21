# install cellworld_py
import httpimport
with httpimport.remote_repo(["agent_tracking"], "https://raw.githubusercontent.com/germanespinosa/agent_tracking/master/python/"):
    from agent_tracking import Agent_tracking

import os
from threading import Thread
from rest import Result
from experiment_control import Experiment_control
from doors import Doors
from feeders import Feeders
from pi import Pi


class Habitat:
    def __init__(self):
        self.videos_folder = "/maze/controller/videos"
        self.current_experiment_video_folder = ""
        self.robot_controller_path = "/maze/agent_tracking/cmake-build-release/robot_controller"
        self.experiment_control = Experiment_control()
        self.doors = Doors()
        self.feeders = Feeders()
        self.door_2_open = False
        self.tracker = Agent_tracking()

    def process_tracking(self, step):
        if self.experiment_control.track_agent(step) and self.door_2_open:
            Thread(target=self.doors.close, args=[2]).start()

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
        s = self.experiment_control.status()
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
            if not self.experiment_control.experiment:
                Thread(target=self.doors.close, args=[0]).start()
                Thread(target=self.doors.close, args=[1]).start()
                Thread(target=self.doors.close, args=[2]).start()
                Thread(target=self.doors.close, args=[3]).start()
                return Result(0, "All doors closed")
            else:
                episode_number = len(self.experiment_control.experiment.episodes)
                current_episode_video_folder = self.current_experiment_video_folder + "/" + self.experiment_control.experiment.name + "_ep" + ('%02d' % episode_number)
                if not os.path.exists(current_episode_video_folder):
                    os.makedirs(current_episode_video_folder)
                self.tracker.new_episode(self.subject_name, self.sufix, episode_number, self.occlusions, current_episode_video_folder, True, self.process_tracking)
                self.door_2_open = True
                r = self.experiment_control.start_episode()
                Thread(target=self.doors.close, args=[1]).start()
                Thread(target=self.doors.open, args=[2]).start()
                Thread(target=self.doors.close, args=[0]).start()
                Thread(target=self.doors.open, args=[3]).start()
                self.feeders.enable(2)
                return r
        else:
            r = self.experiment_control.finish_episode()
            self.tracker.end_episode()
            Thread(target=self.doors.close, args=[3]).start()
            Thread(target=self.doors.open, args=[0]).start()
            Thread(target=self.doors.close, args=[2]).start()
            Thread(target=self.doors.open, args=[1]).start()
            self.feeders.enable(1)
            self.tracker.reset_cameras()
            return r

    def start_experiment(self, subject_name, occlusions, duration=0, suffix=""):
        res = self.experiment_control.new_experiment(subject_name, occlusions, duration, suffix)
        if res.code != 0:
            return res
        self.tracker.new_experiment(self.experiment_control.experiment.name)
        self.subject_name = subject_name
        self.sufix = suffix
        self.occlusions = occlusions
        self.current_experiment_video_folder = self.videos_folder + "/" + self.experiment_control.experiment.name
        if not os.path.exists(self.current_experiment_video_folder):
            os.makedirs(self.current_experiment_video_folder)
        Thread(target=self.doors.close, args=[0]).start()
        Thread(target=self.doors.close, args=[1]).start()
        Thread(target=self.doors.close, args=[2]).start()
        Thread(target=self.doors.close, args=[3]).start()
        self.feeders.enable(1)
        return res

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

    def test_door(self, door_number, repetitions):
        return self.doors.test_door(door_number,repetitions)

    @staticmethod
    def show_occlusions(occlusions_configuration):
        if habitat.tracker.show_occlusions(occlusions_configuration):
            return Result(0, "Occlusions updated")
        else:
            return Result(1, "Failed to update occlusions")

    @staticmethod
    def hide_occlusions():
        if habitat.tracker.hide_occlusions():
            return Result(0, "Occlusions updated")
        else:
            return Result(1, "Failed to update occlusions")


habitat = Habitat()