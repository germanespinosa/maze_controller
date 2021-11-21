from cellworld_py import *


class Enable_feeder_parameters(Json_object):
    def __init__(self, feeder_number=0):
        self.feeder_number = feeder_number


class Disable_feeder_parameters(Json_object):
    def __init__(self, feeder_number=0):
        self.feeder_number = feeder_number


class Feeder_reached_parameters(Json_object):
    def __init__(self, feeder_number=0):
        self.feeder_number = feeder_number


class Test_feeder_parameters(Json_object):
    def __init__(self, feeder_number=0, duration=0, repetitions=0, wait_time=0):
        self.feeder_number = feeder_number
        self.duration = duration
        self.repetitions = repetitions
        self.wait_time = wait_time


class Open_door_parameters(Json_object):
    def __init__(self, door_number=0):
        self.door_number = door_number


class Close_door_parameters(Json_object):
    def __init__(self, door_number=0):
        self.door_number = door_number


class Calibrate_door_parameters(Json_object):
    def __init__(self, door_number=0, direction=0, opening_time=0, closing_time=0):
        self.door_number = door_number
        self.direction = direction
        self.opening_time = opening_time
        self.closing_time = closing_time


class Test_door_parameters(Json_object):
    def __init__(self, door_number=0, repetitions=0):
        self.door_number = door_number
        self.repetitions = repetitions


class Show_occlusions_parameters(Json_object):
    def __init__(self, occlusions_configuration=""):
        self.occlusions_configuration = occlusions_configuration


class Start_experiment_parameters(Json_object):
    def __init__(self, subject_name="", occlusions_configuration="", duration=0, suffix=""):
        self.subject_name = subject_name
        self.occlusions_configuration = occlusions_configuration
        self.duration = duration
        self.suffix = suffix


class Pi_status_result(Json_object):
    def __init__(self, feeder_enabled=False, door_status=Json_list(allowedType=str)):
        self.feeder_enable = feeder_enabled
        self.door_status = door_status

