from pi import Pi
from rest import Result, Call

class Feeders:
    def __init__(self):
        self.pis = {}
        self.is_enabled = {}
        for pi in Pi.get_pis():
            ps = pi.get("status")
            if ( ps.code==0 ):
                self.pis[ps.content["feeder_status"]["feeder_number"]] = pi


    def enable(self, feeder_number):
        if feeder_number not in self.pis.keys():
            return Result(1, "wrong feeder number (%d)" % feeder_number)
        ps = self.pis[feeder_number].get("status")
        is_enabled = ps.content["feeder_status"]["state"] == "enabled"
        if is_enabled:
            return Result(1, "feeder number (%d) is already enabled" % feeder_number)
        return self.pis[feeder_number].get("enable_feeder", [feeder_number])

    def disable(self, feeder_number):
        if feeder_number not in self.pis.keys():
            return Result(1, "wrong feeder number (%d)" % feeder_number)
        ps = self.pis[feeder_number].get("status")
        is_enabled = ps.content["feeder_status"]["state"] == "disabled"
        if is_enabled:
            return Result(1, "feeder number (%d) is already disabled" % feeder_number)
        return self.pis[feeder_number].get("disable_feeder", [feeder_number])


    def test(self, feeder_number, duration, repetitions, wait_time):
        return self.pis[feeder_number].get("test_feeder", [duration, repetitions, wait_time])
