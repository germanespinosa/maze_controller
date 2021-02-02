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
        if command == "feeder_reached":
            feeder_number = int(qs[1])
            return self.habitat.feeder_reached(feeder_number)
        elif command == "start":
            experiment_name = qs[1]
            if len(qs) > 2 and qs[2].isnumeric():
                duration = int(qs[2])
                return self.habitat.start_experiment(experiment_name, duration)
            else:
                return self.habitat.start_experiment(experiment_name)
        elif command == "finish":
            return self.habitat.finish_experiment()
        elif command == "track":
            agent = qs[1]
            x = int(qs[2])
            y = int(qs[3])
            return self.habitat.track(agent, x, y)
        elif command == "end":
            app.stop()
            return Result (0,"good bye!")
        elif command == "status":
            return self.habitat.status()
        else:
            return Result(1, "unknown command")

if __name__ == "__main__":
    app.run()
