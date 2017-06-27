# date control utils

from datetime import datetime
from datetime import timedelta


def weekincrement(d, f = "%Y-%m-%d"):
    dt = datetime.strptime(d, f)
    dt = dt + timedelta(days=7)
    ret = dt.strftime(f)
    print(ret)
    return ret


if __name__ == "__main__":
    import sys
    argv = sys.argv
    argc = len(sys.argv)
    if argc == 2:
        weekincrement(argv[1])
    elif argc == 3:
        weekincrement(argv[1], argv[2])
    else:
        print("Invalid arguments")

