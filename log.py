from datetime import datetime
log_filename = "logs/experiment.log"


def start_log(filename):
    global log_filename
    log_filename = "logs/" + filename


def get_sequence():
    try:
        f = open("logs/sequence.log", "r")
        seq = int(f.readline())
        f.close()
    except:
        seq = 0
    seq += 1
    f = open("logs/sequence.log", "w")
    f.write(str(seq))
    return seq


def get_timestamp():
    return str(datetime.now())


def write_log(s):
    global log_filename
    f = open(log_filename, "a")
    line = "%s\t%s\t%s\n" % (get_timestamp(), get_sequence() , s)
    f.write(line)
    f.close()

