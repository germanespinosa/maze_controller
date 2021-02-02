from pi import Pi
from rest import Result, Call

class Feeders:
    def __init__(self):
        self.pis = {}
        for pi in Pi.get_pis():
            ps = pi.get("status")
            if ( ps.code==0 ):
                self.pis[ps.content["feeder_status"]["feeder_number"]] = pi

    def enable(self, feeder_number):
        if feeder_number not in self.pis.keys():
            return Result(1, "wrong feeder number (%d)" % feeder_number)
        return self.pis[feeder_number].get("enable_feeder", [feeder_number])
