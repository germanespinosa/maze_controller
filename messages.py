from cellworld_py import Json_object, Json_list


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
    def __init__(self, feeder_number=0, feeding_time=0, repetitions=0, wait_time=0):
        self.feeder_number = feeder_number
        self.feeding_time = feeding_time
        self.repetitions = repetitions
        self.wait_time = wait_time


class Open_door_parameters(Json_object):
    def __init__(self, door_number=0):
        self.door_number = door_number


class Close_door_parameters(Json_object):
    def __init__(self, door_number=0):
        self.door_number = door_number


class Calibrate_feeder(Json_object):
    def __init__(self, feeder_number=0, feeding_time=0.0):
        self.feeder_number = feeder_number
        self.feeding_time = feeding_time


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


class Door_status(Json_object):
    def __init__(self, number=0, direction=0, opening_time=0.0, closing_time=0.0, status=0):
        self.number = number
        self.direction = direction
        self.opening_time = opening_time
        self.closing_time = closing_time
        self.status = status


class Door_status_list(Json_list):
    def __init__(self, iterable=None):
        Json_list.__init__(self, iterable, allowedType=Door_status)


class Pi_status(Json_object):
    def __init__(self, feeder_enabled=False, door_status_list=Door_status_list()):
        self.feeder_enable = feeder_enabled
        self.door_status_list = door_status_list

