# import httpimport
# with httpimport.remote_repo(["messages"], "https://raw.githubusercontent.com/germanespinosa/maze_controller/master/"):
from messages import *
from cellworld_py import *
from time import sleep

port = Message_client("192.168.137.1", 6000)
print("sending message")
port.connection.send(Message("status", Open_door_parameters(1)))
print("message sent")
port.start()
print("waiting for response")
while True:
    response = port.connection.pending_messages.get_message("status_result")
    if response:
        break
    sleep(0.01)
print("print response")
print(response)
port.connection.close()

#
# status = Pi_status()
# status.feeder_enable = True
# status.door_status_list.append(Door_status(0, 1, .5, .6, 1))
# status.door_status_list.append(Door_status(3, 1, .4, .7, 0))
#
# print (status)
