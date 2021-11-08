import socket
import json
from threading import Thread

class Agent_tracking:
    def __init__(self, ip, port, call_back=None):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))
        self.send_message("register_consumer")
        if call_back:
            self.running = True
            self.thread = Thread(target=Agent_tracking.process, args=(self, call_back))
            self.thread.start()

    def send_message(self, command, content=""):
        if type(content) is dict:
            content = json.dumps(content)
        self.client.send(json.dumps({'command': command, 'content': content}).encode())

    def new_episode(self, subject_name, sufix, episode_number, occlusions, folder):
        self.send_message("new_episode", {'subject': subject_name,
               'experiment': sufix,
               'episode': episode_number,
               'occlusions': occlusions,
               'destination_folder': folder})

    def end_episode(self):
        self.send_message("end_episode")

    def reset_cameras(self):
        self.send_message("reset_cameras")

    def update_backgrounds(self):
        self.send_message("update_background")

    @staticmethod
    def process(agent_tracking, call_back):
        while agent_tracking.running:
            data = agent_tracking.client.recv(8192).decode()

            for message_str in data.split('\x00'):
                if message_str:
                    try:
                        message = json.loads(message_str)
                        if "command" in message:
                            if message["command"] == "step":
                                call_back(message["content"])
                    finally:
                        pass

    def stop(self):
        self.send_message("deregister_consumer")
        self.running = False
        self.app.terminate()
