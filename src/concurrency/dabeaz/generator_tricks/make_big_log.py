import sys

if len(sys.argv) != 2:
    print("Usage : make_big_log.py repetitions", file=sys.stderr)
    sys.exit(1)

data = open("access.log").read()

with open("big_access.log", "w") as f:
    for i in range(int(sys.argv[1])):
        f.write(data)
