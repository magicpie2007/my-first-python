#! /usr/bin/env python3

import datetime, sys, os, re

def main(args):
    print(parseargs(args))

def parseargs(args):
    opt = None
    branch = None
    since = None
    until = None
    interval = None
    for arg in args:
        # Extract option key
        if arg.startswith('-'):
            opt = arg[1:]
            continue
        elif arg.startswith('--'):
            opt = arg[2:]
            continue

        # Extract option value
        if opt == 'b' or opt == 'branch':
            branch = arg
        elif opt == 's' or opt == 'since' or opt == 'start':
            start = datetime.datetime.strptime(arg, '%Y%m%d')
            opt = None
        elif opt == 'u' or opt =='until' or opt == 'end':
            until = datetime.datetime.strptime(arg, '%Y%m%d')
            opt = None
        elif opt == 'i' or opt == 'interval':
            regex = re.compile(r'(\d+)(m|w|d)')
            mo = regex.search(arg)
            if mo.group(1) == None or mo.group(2) == None:
                print("Error: Invalid argumnet")
                sys.exit(1)
            interval = {'value': mo.group(1), 'unit': mo.group(2)}
            opt = None
        else:
            print("Error: Invalid argument")
            sys.exit(1)
    if opt != None:
        print("Error: Invalid argument")
        sys.exit(1)
    return branch, start, until, interval


if __name__ == '__main__':
    main(sys.argv[1:])

