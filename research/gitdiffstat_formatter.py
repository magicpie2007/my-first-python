#! /usr/bin/env python3

import re


def format(inputpath, outputpath):
    inputfile = open(inputpath, 'r')
    outputfile = open(outputpath, 'w')
    for line in inputfile:
        print(line, end='')
        separated = line.split('|')
        if len(separated) != 2 or 'Bin' in separated[1]:
            continue
        print(separated[0])
        print(separated[1])
        filename = separated[0].strip()
        regex = re.compile(r'\d+')
        mo = regex.search(separated[1])
        changes = mo.group()
        outputline = filename + ',' + changes
        outputfile.writable(outputfile)

    inputfile.close()
    outputfile.close()


if __name__ == '__main__':
    import sys
    format(sys.argv[1], sys.argv[2])


