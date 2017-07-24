#! /usr/bin/env python3

import sys
import re


def main(args):
    csvfile = open(args[-1], 'r')
    extracttype = args[0]
    for arg in args[1:-1]:
        pos = parsearg(arg)
        data = extract(csvfile, pos, extracttype)
        print(data)
        csvfile.seek(0)

    csvfile.close()


def parsearg(arg):
    columnnum = None
    rownum = None
    regex = re.compile(r'(\d+)([cr])((\d+)([cr]))?')
    mo = regex.search(arg)
    if mo.group(2) == 'c':
        columnnum = int(mo.group(1))
        if mo.group(3) is not None and mo.group(5) == 'r':
            rownum = int(mo.group(4))
    elif mo.group(2) == 'r':
        rownum = int(mo.group(1))
        if mo.group(3) is not None and mo.group(5) == 'c':
            columnnum = int(mo.group(4))
    return {'column': columnnum, 'row': rownum}


def extract(csvfile, pos, extracttype):
    if pos['column'] is not None and pos['row'] is not None:
        raw_data = extract_cell(csvfile, pos['column'], pos['row'])
    elif pos['column'] is not None:
        raw_data = extract_column(csvfile, pos['column'])
    elif pos['row'] is not None:
        raw_data = extract_row(csvfile, pos['row'])
    else:
        print("Error: Invalid argument")
        sys.exit(1)

    data = []
    if extracttype == 'str':
        data = raw_data
    elif extracttype == 'int':
        for item in raw_data:
            try:
                data.append(int(item))
            except ValueError:
                data.append(item)
    elif extracttype == 'float':
        for item in raw_data:
            try:
                data.append(float(item))
            except ValueError:
                data.append(item)

    return data


def extract_cell(csvfile, columnnum, rownum):
    rawdata_column = []
    line_rawdata = csvfile.readlines()[rownum - 1].split(',')
    rawdata_column.append(line_rawdata[columnnum - 1])
    return rawdata_column


def extract_column(csvfile, columnnum):
    rawdata_column = []
    for line in csvfile:
        line_rawdata = line.split(',')
        rawdata_column.append(line_rawdata[columnnum - 1])
    return rawdata_column


def extract_row(csvfile, rownum):
    return csvfile.readlines()[rownum - 1].split(',')


if __name__ == '__main__':
    main(sys.argv[1:])
