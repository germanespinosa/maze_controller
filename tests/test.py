import subprocess
import glob

processes = {}

for test_file in glob.glob("tests/*"):
    test_name = test_file.split("/")[1].replace("test_","").replace(".py","")
    processes[test_name] = subprocess.Popen(['python3', test_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

print("tests running..")
for test in processes.keys():
    print(test_name + " tests : ", end="")
    if processes[test].wait() != 0:
        print("fail")
        for output in processes[test].stdout.readlines():
            print(str(output.strip())[2:-1])
    else:
        print("success")

print()

