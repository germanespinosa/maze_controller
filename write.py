import sys
f = open(sys.argv[1], "w")
while (True):
    s = sys.stdin.readline()
    f.write(s)
    f.flush()
    s = s.upper()
    sys.stdout.write(s)
    sys.stdout.flush()