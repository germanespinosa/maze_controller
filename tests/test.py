import subprocess

processes = {}
processes["habitat"] = subprocess.Popen(['python3', 'tests/test_habitat.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
processes["api"] = subprocess.Popen(['python3', 'tests/test_api.py'], stdout=subprocess.PIPE,  stderr=subprocess.STDOUT)
processes["remote"] = subprocess.Popen(['python3', 'tests/test_remote.py'], stdout=subprocess.PIPE,  stderr=subprocess.STDOUT)
processes["console"] = subprocess.Popen(['python3', 'tests/test_console.py'], stdout=subprocess.PIPE,  stderr=subprocess.STDOUT)

print("tests running..")
for test in processes.keys():
    print(test + " tests : ", end="")
    if processes[test].wait() != 0:
        print("fail")
        for output in processes[test].stdout.readlines():
            print(str(output.strip())[2:-1])
    else:
        print("success")

print()

