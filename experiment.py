import json
from datetime import datetime

class Experiment:
    def __init__(self, name="", duration_minutes=0):
        self.active = True
        self.name = name
        self.duration = duration_minutes * 60
        self.start_time = datetime.now()
        self.agents_locations = {}
        self.trajectories = []
        self.current_episode_start_time = None
        self.episodes = []

    def start_episode(self):
        self.agents_locations = {}
        self.current_episode_start_time = datetime.now()
        self.episodes.append({"trajectories": [], "time_stamp": ( self.current_episode_start_time-self.start_time).microseconds/1000})

    def finish_episode(self):
        if not self.current_episode_start_time:
            return
        self.episodes[-1]["end_time"] = str(datetime.now())
        e = {"name": self.name, "start_time": str(self.start_time), "duration": self.duration}
        e["episodes"] = self.episodes
        with open("logs/" + self.name + ".json", 'w') as outfile:
            json.dump(e, outfile)
        self.current_episode_start_time = None

    def track_agent(self, agent, location):
        if agent in self.agents_locations and self.agents_locations[agent] == location:
            return
        self.agents_locations[agent] = location
        self.episodes[-1]["trajectories"].append({"time_stamp": (datetime.now()-self.current_episode_start_time).microseconds/1000, "agent_name": agent, "coordinates": location})

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
        return message

    def __repr__(self):
        return self.status()

    def finish(self):
        self.finish_episode()
        self.active = False