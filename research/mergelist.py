#! /usr/bin/env python3

import sys


def main(args):
    file_path1, file_path2, key_column, outfile_path = parse_args(args)
    file1 = open(file_path1, 'r')
    file2 = open(file_path2, 'r')
    if outfile_path is None:
        outfile_path = "./out.csv"
    outfile = open(outfile_path, 'w')

    merge_list(file1, file2, key_column, outfile)


def merge_list(file1, file2, key_column, outfile):
    for line in file1.read():
        values = split_line(line)
        


def split_line(line):
    return line.split(',')


def parse_args(args):
    if len(args) < 3:
        print("Error: Invalid Argument")

    file_path1 = args[0]
    file_path2 = args[1]
    key_column = args[2]
    outfile_path = None

    if len(args) == 4:
        outfile_path = args[3]
    return file_path1, file_path2, key_column, outfile_path


if __name__ == '__main__':
    main(sys.argv[1:])
