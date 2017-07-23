#! /usr/bin/env python3

import sys
import re


def main(args):
   csv = open(args[-1], 'r')
   for arg in args[0:-1]:
       pos = parsearg(arg)
       extractdata(pos)


def parsearg(arg):
    columnnum = None
    rownum = None
    regex = re.compile(r'(\d+)([cr])((\d+)([cr]))?')
    mo = regex.search(arg)
    if mo.group(2) == 'c':
        columnnum = mo.group(1)
        if mo.group(3) is not None and mo.group(5) == 'r':
            rownum = mo.group(4)
    elif mo.group(2) == 'r':
        rownum = mo.group(1)
        if mo.group(3) is not None and mo.group(5) == 'c':
            columnnum = mo.group(4)
    return {'column': columnnum, 'row': rownum}


def extractdata(pos):
    pass


if __name__ == '__main__':
    main(sys.argv[1:])
