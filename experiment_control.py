import json
from rest import Result
from datetime import datetime
from cellworld_py import Experiment, Episode, Step, Episode_list, Trajectories, check_type, Coordinates


class Experiment_control:

    def __init__(self):
        self.experiment = None
        self.current_episode = None
        self.is_finished = False

    def new_experiment(self, subject_name, occlusions, duration, suffix):
        start_time = datetime.now()
        name = str(start_time.year) + str("%02d" % start_time.month) + str(
            "%02d" % start_time.day) + "_" + str("%02d" % start_time.hour) + str(
            "%02d" % start_time.minute) + "_" + subject_name + "_" + occlusions + (
                              "_" + suffix if suffix != "" else "")
        self.is_finished = False
        self.experiment = Experiment(name, "hexagonal", "cv", occlusions, subject_name, duration, start_time)
        message = "started experiment '%s'" % name
        if duration > -1:
            message += " for %d minutes" % (duration / 60)

        return Result(0, message)

    def start_episode(self):
        self.current_episode = Episode(datetime.now())
        return Result(0, "episode %d started" % (len(self.experiment.episodes)))

    def write(self):
        with open("logs/" + self.experiment.name + ".json", 'w') as outfile:
            outfile.write(str(self.experiment))

    def finish_episode(self):
        if not self.current_episode:
            return Result(1, "there is no active episode")
        self.experiment.episodes.append(self.current_episode)
        self.current_episode = None
        self.write() #saves every episode
        if self.is_finished or self.remaining_time() <= 0:
            self.experiment = None
        return Result(0, "episode finished")

    def track_agent(self, step):
        if not self.current_episode:
            return False
        check_type(step, Step, "incorrect type for step")
        self.current_episode.trajectories.append(step)
        if step.agent_name == "prey" and step.coordinates != Coordinates(-20,0):
            return True
        return False

    def running_time(self):
        date_diff = datetime.now() - self.experiment.start_time
        return date_diff.seconds

    def remaining_time(self):
        return self.experiment.duration - self.running_time()

    def status(self):
        if self.experiment:
            n = self.remaining_time()
            if n <= 0:
                message = "experiment %s finishing" % self.experiment.name
            else:
                message = "experiment %s in progress" % self.experiment.name
                message += "(%d minutes remaining)" % round(n / 60)
        else:
            message = "no active experiment"
        return Result(0, message)

    def __repr__(self):
        return self.status()

    def experiment_ended(self):
        if self.current_episode:
            self.finish_episode()
        self.experiment = None

    def finish(self):
        self.is_finished = True
        return Result(0, "experiment %s finished" % self.experiment.name)
