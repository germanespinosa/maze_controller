from pi import Pi
from rest import Result, Call

class Doors:
    def __init__(self):
        self.pis = {}
        for pi in Pi.get_pis():
            ps = pi.get("status")
            if ( ps.code==0 ):
                doors_status = ps.content["door_status"]
                for door_status in doors_status:
                    self.pis[door_status["door_number"]] = pi

    def open(self, door_number):
        if door_number not in self.pis.keys():
            return Result(1, "wrong door number (%d)" % door_number)
        return self.pis[door_number].get("open", [door_number])

    def close(self, door_number):
        if door_number not in self.pis.keys():
            return Result(1, "wrong door number (%d)" % door_number)
        return self.pis[door_number].get("close", [door_number])

    def calibrate(self, door_number, direction, opening_time, closing_time):
        if door_number not in self.pis.keys():
            return Result(1, "wrong door number (%d)" % door_number)
        return self.pis[door_number].get("calibrate_door", [door_number, direction, opening_time, closing_time])

    def save_calibration(self):
        r = ""
        for pi in self.pis.values():
            r = pi.get("save_door_calibration")
        return r

    def load_calibration(self):
        r = ""
        for pi in self.pis.values():
            r = pi.get("load_door_calibration")
        return r

    def test_door(self, door_number, repetitions):
        return self.pis[door_number].get("test_door", [door_number, repetitions])