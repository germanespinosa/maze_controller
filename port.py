# add parameter messages from maze_controller
# import httpimport
# with httpimport.remote_repo(["messages"], "https://raw.githubusercontent.com/germanespinosa/maze_controller/master/"):
from messages import *
from cellworld_py import Message_server, Message_client, Message
from threading import Thread
from time import sleep
from os import path

#GPIO ACCESS
# from gpiozero import Button, LED
# from adafruit_servokit import ServoKit

class Port:
    def __init__(self, port=6000):
        self.server = Message_server()
        self.server.router.add_route("enable_feeder", self.enable_feeder, Enable_feeder_parameters)
        self.server.router.add_route("disable_feeder", self.disable_feeder, Disable_feeder_parameters)
        self.server.router.add_route("calibrate_feeder", self.calibrate_feeder, Calibrate_feeder)
        self.server.router.add_route("test_feeder", self.test_feeder, Test_feeder_parameters)

        self.server.router.add_route("open_door", self.open_door, Open_door_parameters)
        self.server.router.add_route("close_door", self.open_door, Close_door_parameters)
        self.server.router.add_route("calibrate_door", self.calibrate_door, Calibrate_door_parameters)
        self.server.router.add_route("test_door", self.test_door, Test_door_parameters)

        self.server.router.add_route("status", self.status)
        self.server.router.add_route("end", self.quit)

        #feeders setup
        self.feeding_time = 0.0
        self.feeder_number = 0
        # self.feeder_solenoid = LED(27)
        self.feeder_thread = None
        #self.load_feeder_calibration()
        # if self.feeder_number == 1:
        #     self.feeder_sensor = Button(17)
        # else:
        #     self.feeder_sensor = Button(22)
        self.feeder_enabled = False

        #doors setup
        # self.servos = ServoKit(channels=16)
        self.doors = Door_status_list()
        #self.load_door_calibration()

        self.server.start(port)
        self.active = True

    #feeders

    def feed(self, feeding_time=None):
        if feeding_time is None:
            feeding_time = self.feeding_time
        # self.feeder_solenoid.on()
        sleep(feeding_time)
        # self.feeder_solenoid.off()

    def __feeder_process__(self):
        self.feeder_enabled = True
        while self.feeder_enabled:
            # if not self.feeder_sensor.is_pressed:
            #     Thread(target=self.feed()).start()
            #     habitat_server = Message_client("192.168.137.1", 5000)
            #     habitat_server.connection.send(Message("feeder_reached", Feeder_reached_parameters(feeder_number=self.feeder_number)))
            #     habitat_server.connection.close()
            #     self.feeder_enabled = False
            sleep(.01)

    def enable_feeder(self, params):
        print("enable_feeder", params)
        if params.feeder_number == self.feeder_number:
            return
        self.feeder_thread = Thread(target=self.__feeder_process__)
        while not self.feeder_enabled:
            pass

    def disable_feeder(self, params):
        print("disable_feeder", params)
        if params.feeder_number == self.feeder_number:
            return
        if self.feeder_enabled:
            self.feeder_enabled = False
            self.feeder_thread.join()

    def calibrate_feeder(self, params):
        print("calibrate_feeder", params)
        self.feeding_time = params.feeding_time
        with open("feeder.cal", "w") as f:
            f.write(str(self.feeding_time) + "\n")
            f.write(str(self.feeder_number) + "\n")

    def load_feeder_calibration(self):
        with open("feeder.cal", "r") as f:
            lines = f.readlines()
            self.feeding_time = float(lines[0].replace("\n", ""))
            self.feeder_number = int(lines[1].replace("\n", ""))

    def test_feeder(self, params):
        print("test_feeder", params)
        if params.feeder_number == self.feeder_number:
            return
        for r in params.repetitions:
            self.feed(params.feeding_time)
            sleep(params.wait_time)

    #doors

    def calibrate_door(self, params):
        print("calibrate_door", params)
        if params.door_number not in self.doors:
            return
        self.doors[params.door_number].direction = params.direction
        self.doors[params.door_number].closing_time = params.closing_time
        self.doors[params.door_number].opening_time = params.opening_time

    def load_door_calibration(self, message=None):
        print("load_door_calibration", message)
        for door_number in range(4):
            cal_file_name = "door%d.cal" % door_number
            if path.exists(cal_file_name):
                lines = open(cal_file_name, "r").readlines()
                direction = int(lines[1].replace("\n", ""))
                opening_time = float(lines[2].replace("\n", ""))
                closing_time = float(lines[3].replace("\n", ""))
                self.doors.append(Door_status(door_number, direction, opening_time, closing_time))
            else:
                self.doors.append(Door_status(-1))

    def open_door(self, params):
        print("open_door", params)
        if self.doors[params.door_number].door_number == -1:
            return "failed"  # wrong door number
        door = self.doors[params.door_number]
        if door.status == 1:
            return "ok"  # already opened
        # self.servos.continuous_servo[door.number].throttle = -.5 * door.direction
        sleep(door.opening_time)
        # self.servos.continuous_servo[door.number].throttle = 0
        self.doors[params.door_number].status = 1
        sleep(.2)

    def close_door(self, params):
        print("close_door", params)
        if self.doors[params.door_number].door_number == -1:
            return "failed"  # wrong door number
        door = self.doors[params.door_number]
        if door.status == 0:
            return "ok"  # already closed
        # self.servos.continuous_servo[door.number].throttle = .5 * door.direction
        sleep(door.closing_time)
        # self.servos.continuous_servo[door.number].throttle = 0
        self.doors[params.door_number].status = 1
        sleep(.2)

    def test_door(self, params):
        print("test_door", params)
        if self.doors[params.door_number].door_number == -1:
            return
        for r in range(params.repetitions):
            self.open_door(params)
            self.close_door(params)

    def quit(self, message):
        print("quit", message)
        if self.feeder_enabled:
            self.feeder_enabled = False
            self.feeder_thread.join()
        self.active = False

    def status(self, message):
        print("status", message)
        status = Pi_status()
        status.feeder_enable = self.feeder_enabled
        for door in self.doors:
            if door.number >= 0:
                status.door_status_list.append(door)
        response = Message("status_return", status)
        print("returning", response)
        return response



p = Port()
print("started")
while p.active:
    sleep(1)
    pass
sleep(5)
