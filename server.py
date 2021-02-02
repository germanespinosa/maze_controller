import web
import json
import habitat

urls = (
    '/(.*)', 'Server'
)
app = web.application(urls, globals())
app.habitat = habitat.Control()
class Server:
    def GET(self, querystring):
        qs = querystring.split("/")
        command = qs[0]
        if command == "feeder_reached":
            feeder_number = int(qs[1])
            return json.dumps(self.feeder_reached(feeder_number))
        elif command == "start":
            experiment_name = qs[1]
            if len(qs) > 2 and qs[2].isnumeric():
                duration = int(qs[2])
                return json.dumps(self.start_experiment(experiment_name,duration))
            else:
                return json.dumps(self.start_experiment(experiment_name))
        elif command == "end":
            return json.dumps(self.end_experiment())
        elif command == "track":
            agent = qs[1]
            x = int(qs[2])
            y = int(qs[3])
            return json.dumps(self.track(agent, x, y))
        else:
            return 'unknown command'

app.run()
