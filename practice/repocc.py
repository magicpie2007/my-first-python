#! /usr/bin/env python3

import sys
import re
import subprocess
import datetime
import pygal
import practice.extractdata as extractdata
from dateutil.relativedelta import relativedelta
import numpy


def main(args):
    branch, since, until, interval = parse_args_for_cc(args)
    output_file_name = create_file_name(branch, since, until, interval)
    counting_commit(branch, since, until, interval, output_file_name)
    drawing_graph(output_file_name)


def drawing_graph(output_file_name):
    # Open csv file
    csv_file = open(output_file_name + '.csv', 'r')

    # Get header data
    header = csv_file.readline().split(',')
    column_size = len(header)
    csv_file.seek(0)

    # Get the data of Sum column
    pos = {'column': column_size, 'row': None}
    data = extractdata.extract(csv_file, pos, 'int')
    csv_file.seek(0)

    # Sort the data and get its index
    sorted_index = numpy.argsort(numpy.array(data[1:]))

    # Define graph type from pygal
    graph = pygal.HorizontalStackedBar()

    # Set x labels
    x_labels_data = []
    for i in sorted_index[-20:]:
        pos = {'column': 1, 'row': i + 1 + 1}
        cell = extractdata.extract(csv_file, pos, 'str')
        csv_file.seek(0)
        x_labels_data.append(cell[0])
    graph.x_labels = tuple(x_labels_data)

    # Add data to graph
    for i in range(1, column_size - 1):
        graph_data = []
        for j in sorted_index[-20:]:
            pos = {'column': i + 1, 'row': j + 1 + 1}
            cell = extractdata.extract(csv_file, pos, 'int')
            csv_file.seek(0)
            graph_data.append(cell[0])
        graph.add(header[i], graph_data)

    graph.render_to_file(output_file_name + '.svg')


def counting_commit(branch, since, until, interval, output_file_name):
    # Open the file to write result
    output_file = open(output_file_name + ".csv", 'w')

    # Write header
    write_header_for_cc(since, until, interval, output_file)

    # Execute counting commit
    executing_counting_commit(branch, since, until, interval, output_file)

    # Close
    output_file.close()


def executing_counting_commit(branch, since, until, interval, output_file):

    # Create repo command
    repo_cmd = "repo forall -p -v -c "
    repo_forall_cmd = "git_cc " + branch + \
                      " " + since + \
                      " " + until + \
                      " " + interval
    cmd = (repo_cmd + repo_forall_cmd).split()

    exe = subprocess.Popen(cmd, stdout=subprocess.PIPE, encoding='utf-8')

    project = None
    while True:
        polling = exe.poll()
        if polling is not None:
            break
        for line in exe.stdout:
            if line.startswith('project '):
                project = line[len('project '):-1]
            elif line.startswith(','):
                output_line = project + line
                output_file.write(output_line)
            elif line == '' or line == '\n':
                # Do nothing
                continue
            else:
                output_file.write(line)
    exe.stdout.close()


def write_header_for_cc(since, until, interval, output_file):
    date_since = datetime.datetime.strptime(since, '%Y%m%d')
    date_until = datetime.datetime.strptime(until, '%Y%m%d')

    # Parse interval
    regex = re.compile(r'(\d+)([mwd])')
    mo = regex.search(interval)
    if mo.group(1) is None or mo.group(2) is None:
        sys.stderr.write("Error: Invalid argument")
        sys.exit(1)
    interval = {'value': int(mo.group(1)), 'unit': mo.group(2)}

    delta = None
    if interval['unit'] == 'm':
        # datetime.timedelta does not support 'months' value, so use relativedelta module
        delta = relativedelta(months=interval['value'])
    elif interval['unit'] == 'w':
        delta = datetime.timedelta(weeks=interval['value'])
    elif interval['unit'] == 'd':
        delta = datetime.timedelta(days=interval['value'])

    date = date_since + delta
    output_file.write("Project")
    while date <= date_until:
        date_adj = date - datetime.timedelta(days=1)
        output_file.write(",%s" % date_adj.strftime('%Y-%m-%d'))
        date = date + delta

    if date > date_until:
        output_file.write(",%s" % date_until.strftime('%Y-%m-%d'))

    output_file.write(",Sum\n")


def create_file_name(branch, since, until, interval):
    branch_name = branch.replace('/', '_')
    return "Commit_Counts_" + branch_name + \
           '_' + since + '-' + until + '_' + interval


def parse_args_for_cc(args):
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
            # since = datetime.datetime.strptime(arg, '%Y%m%d')
            since = arg
            opt = None
        elif opt == 'u' or opt == 'until' or opt == 'end':
            # until = datetime.datetime.strptime(arg, '%Y%m%d')
            until = arg
            opt = None
        elif opt == 'i' or opt == 'interval':
            interval = arg
            opt = None
        else:
            print("Error: Invalid argument")
            sys.exit(1)
    if opt is not None:
        print("Error: Invalid argument")
        sys.exit(1)
    return branch, since, until, interval


if __name__ == '__main__':
    main(sys.argv[1:])
