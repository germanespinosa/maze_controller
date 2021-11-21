from time import sleep
from agent_tracking import Agent_tracking


def new_step(step):
    print(step)


agt = Agent_tracking("127.0.0.1", 4000, new_step)
print(agt.registered)
if agt.connect():
    while not agt.registered:
        pass
    agt.new_episode("TEST", "TEST", 100, "10_05", "/home/maze")
    sleep(30)
    agt.end_episode()
    agt.stop()


#
# import socket
# import json
# import time
#
#
# running = True
#
# def message_processing(client, callback):
#     global running
#     running = True
#     while running:
#         incoming_data = client.recv(1024).decode()
#         messages = [message for message in incoming_data.split(0, '\x00')]
#         for message in messages:
#             callback(message)
#
#
#
#
# HOST = '127.0.0.1'  # The server's hostname or IP address
# PORT = 4000        # The port used by the server
#
# def get_message(command, content=""):
#     if type(content) is dict:
#         content = json.dumps(content)
#     return json.dumps({'command': command, 'content': content})
#
#
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
#     client.connect((HOST, PORT))
#     client.send(get_message("reset_cameras").encode())
#     data = client.recv(1024).decode()
#     print(data)
#     client.send(get_message("register_consumer").encode())
#     data = client.recv(1024).decode()
#     print(data)
#     nem = { 'subject': "FPP1",
#             'experiment': "ROBOT",
#             'episode': 18,
#             'occlusions': "10_05",
#             'destination_folder': "/home/maze/" }
#     m = get_message("new_episode", nem)
#     print(m)
#     client.send(m.encode())
#     time.sleep(10)
#     client.send(get_message("end_episode").encode())
#     data = client.recv(1024).decode()
#     print(data)
#     client.send(get_message("deregister_consumer").encode())
#     data = client.recv(1024).decode()
#     print(data)
