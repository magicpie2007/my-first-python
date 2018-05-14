#! /usr/bin/env python3

import sys


def main(args):
    file_path1, file_path2, key_column, outfile_path = parse_args(args)
    if key_column <= 0:
        print("Invalid Argument")
        return
    file1 = open(file_path1, 'r')
    file2 = open(file_path2, 'r')
    if outfile_path is None:
        outfile_path = "./out.csv"
    outfile = open(outfile_path, 'w')

    merge_list(file1, file2, key_column, outfile)

    file1.close()
    file2.close()
    outfile.close()


def merge_list(file1, file2, key_column, outfile):
    # First merge the lines which has the same key into one line, but add also the lines only in file1
    values_a = []
    for line in file1:
        values_a = split_line(line)
        values_b = search_line(file2, key_column, values_a[key_column - 1])
        if values_b is not None:
            if key_column == 1:
                values = values_a + values_b[1:]
            else:
                values = values_a[key_column - 1] + values_a[:key_column - 1] + values_a[key_column:] + \
                         values_b[:key_column - 1] + values_b[key_column:]
        else:
            if key_column == 1:
                values = values_a
            else:
                values = values_a[key_column - 1] + values_a[:key_column - 1] + values_a[key_column:]
        outfile.write(','.join(values) + '\n')

    # Secondary add the lines only in file2
    file2.seek(0)
    i = 0
    values_base = [values_a[key_column - 1]]
    while i < len(values_a) - 1:
        values_base.append('')
        i = i + 1
    i = 0
    for line in file2:
        if not g_found_line_has(i):
            values_tmp = split_line(line)
            if key_column == 1:
                values = values_base + values_tmp[1:]
            else:
                values = values_base + values_a[:key_column - 1] + values_a[key_column:]
            outfile.write(','.join(values) + '\n')
        i = i + 1


g_found_line = []


def search_line(file, search_column, key):
    file.seek(0)
    global g_found_line
    i = 0
    for line in file:
        if not g_found_line_has(i):
            values = split_line(line)
            if values[search_column - 1] == key:
                g_found_line.append(i)
                return values
        i = i + 1
    return None


def g_found_line_has(i):
    global g_found_line
    for line_no in g_found_line:
        if line_no == i:
            return True
    return False


def split_line(line):
    return line.replace('\n', '').split(',')


def parse_args(args):
    if len(args) < 3:
        print("Error: Invalid Argument")
        print_usage()
        exit()

    file_path1 = args[0]
    file_path2 = args[1]
    key_column = int(args[2])
    outfile_path = None

    if len(args) == 4:
        outfile_path = args[3]
    return file_path1, file_path2, key_column, outfile_path


def print_usage():
    """Print usage"""
    print("Usage: mergelist file1 file2 [key column number] [output file]")


if __name__ == '__main__':
    main(sys.argv[1:])
