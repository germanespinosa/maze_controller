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
        elif command == "start_experiment":
            experiment_name = qs[1]
            if len(qs) > 2 and qs[2].isnumeric():
                duration = int(qs[2])
                return self.habitat.start_experiment(experiment_name, duration).json()
            else:
                return self.habitat.start_experiment(experiment_name).json()
        elif command == "finish_experiment":
            return self.habitat.finish_experiment().json()
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
