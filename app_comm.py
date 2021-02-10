import subprocess
from threading import Thread

class App_comm:
    def __init__(self, cmd, call_back=None):
        self.app = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        if call_back:
            self.running = True
            self.thread = Thread(target=App_comm.process, args=(self, call_back))
            self.thread.start()

    def write(self, s):
        self.app.stdin.write((s + "\n").encode())
        self.app.stdin.flush()

    def process(app_comm, call_back):
        while app_comm.running:
            content = app_comm.app.stdout.readline().decode().replace("\r", "").replace("\n", "")
            if app_comm.running:
                call_back(content)

    def stop(self):
        self.running = False
        self.app.terminate()
