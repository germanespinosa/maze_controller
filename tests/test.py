import subprocess
import glob
import sys

processes = {}

for test_file in glob.glob("tests/test_*"):
    test_name = test_file.split("/")[1].replace("test_", "").replace(".py", "")
    processes[test_name] = subprocess.Popen(['python3', test_file], stdout=subprocess.PIPE, stderr=sys.stderr)

print("tests running..")
for test_name in processes.keys():
    print(test_name + " tests : ", end="")
    if processes[test_name].wait() != 0:
        print("fail")
        for output in processes[test_name].stdout.readlines():
            print(str(output.strip())[2:-1])
    else:
        print("success")

print()

