import json
from rest import Result
from datetime import datetime
from world import World
from map import Map

class Experiment:
    def __init__(self, name="", world_name="", duration_minutes=0):
        self.name = name
        self.active = False
        if world_name != "":
            self.world = World("hexa_" + world_name)
            self.map = Map(self.world)
        self.duration = duration_minutes * 60
        self.start_time = datetime.now()
        self.end_time = None
        self.agents_locations = {}
        self.trajectories = []
        self.current_episode_start_time = None
        self.episodes = []

    def start(self):
        self.active = True


    def active_episode(self):
        return not self.current_episode_start_time is None

    def start_episode(self):
        self.agents_locations = {}
        self.current_episode_start_time = datetime.now()
        self.episodes.append({"trajectories": [], "start_time": str(self.current_episode_start_time), "time_stamp": ( self.current_episode_start_time-self.start_time).total_seconds()})
        return Result(0, "episode %d started" % len(self.episodes))

    def write(self):
        e = {"name": self.name, "start_time": str(self.start_time), "duration": self.duration}
        e["episodes"] = self.episodes
        if (self.end_time):
            e["end_time"] = str(self.end_time)
        with open("logs/" + self.name + ".json", 'w') as outfile:
            json.dump(e, outfile)

    def finish_episode(self):
        if not self.active_episode():
            return Result(1,"there is not any active episode")
        self.episodes[-1]["end_time"] = str(datetime.now())
        self.current_episode_start_time = None
        self.write()
        return Result(0, "episode %d finished" % len(self.episodes))

    def track_agent(self, agent, coordinates, location, frame=-1, time_stamp=None):
        if not self.active_episode():
            return Result(1, "there is not any active episode")
        if agent in self.agents_locations and self.agents_locations[agent] == coordinates:
            return Result (1, "duplicated coordinates given")
        if self.world and self.map.cell(coordinates)["occluded"]:
            return Result(0, "Coordinates correspond to an occluded cell")
        else:
            self.agents_locations[agent] = coordinates
            if time_stamp is None:
                time_stamp = (datetime.now() - self.current_episode_start_time).total_seconds()
            step = {"time_stamp": time_stamp, "agent_name": agent, "coordinates": coordinates, "location": location, "frame": frame}
            self.episodes[-1]["trajectories"].append(step)
            if self.check:
                if agent == "mouse" and coordinates != {"x": -20, "y": 0}:
                    self.check(2)
                    self.check = None
            return Result(0, "%s coordinates recorded" % agent, step)

    def running_time(self):
        date_diff = datetime.now() - self.start_time
        return date_diff.seconds

    def remaining_time(self):
        return self.duration - self.running_time()

    def is_active(self):
        if self.active:
            if self.duration:
                if self.remaining_time() > 0:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    def status(self):
        if self.is_active():
            if self.duration:
                n = self.remaining_time()
                if n <= 0:
                    message = "experiment %s finishing" % self.name
                else:
                    message = "experiment %s in progress" % self.name
                    message += "(%d seconds remaining)" % n
            else:
                message = "experiment %s in progress" % self.name
        else:
            message = "no active experiment"
        return Result(0, message)

    def __repr__(self):
        return self.status()

    def experiment_ended(self):
        self.finish_episode()
        self.end_time = datetime.now()
        self.active = False

    def finish(self):
        self.active = False
        return Result(0, "experiment %s finished" % self.name)
