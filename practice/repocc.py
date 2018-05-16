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
    branch, since, until, interval, regex, inverse_regex = parse_args_for_cc(args)
    output_file_name = create_file_name(branch, since, until, interval,
                                        regex, inverse_regex)
    counting_commit(branch, since, until, interval,
                    regex, inverse_regex, output_file_name)
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
    sorted_index = numpy.argsort(numpy.array(data[1:-1]))

    # Define graph type from pygal
    graph_detail = pygal.HorizontalStackedBar(title='Top 20 Repositories (Commit)')
    graph_summary = pygal.HorizontalStackedBar(title='Top 20 Repositories (Commit)',
                                               show_legend=False)

    # Set x labels
    x_labels_data = []
    for i in sorted_index[-20:]:
        pos = {'column': 1, 'row': i + 1 + 1}
        cell = extractdata.extract(csv_file, pos, 'str')
        csv_file.seek(0)
        x_labels_data.append(cell[0])
    graph_detail.x_labels = tuple(x_labels_data)
    graph_summary.x_labels = tuple(x_labels_data)

    # Add data to graph
    for i in range(1, column_size - 1):
        graph_data = []
        for j in sorted_index[-20:]:
            pos = {'column': i + 1, 'row': j + 1 + 1}
            cell = extractdata.extract(csv_file, pos, 'int')
            csv_file.seek(0)
            graph_data.append(cell[0])
        graph_detail.add(header[i], graph_data)
    graph_summary_data = []

    for i in sorted_index[-20:]:
        pos = {'column': column_size, 'row': i + 1 + 1}
        cell = extractdata.extract(csv_file, pos, 'int')
        csv_file.seek(0)
        graph_summary_data.append(cell[0])
    graph_summary.add('', graph_summary_data)

    graph_detail.render_to_file(output_file_name + '.svg')
    graph_detail.render_to_png(output_file_name + '.png')
    graph_summary.render_to_file(output_file_name + '_summary.svg')
    graph_summary.render_to_png(output_file_name + '_summary.png')


def counting_commit(branch, since, until, interval,
                    regex, inverse_regex, output_file_name):
    # Open the file to write result
    output_file = open(output_file_name + ".csv", 'w')

    # Write header
    num_column = write_header_for_cc(since, until, interval, output_file)

    # Execute counting commit
    executing_counting_commit(branch, since, until, interval,
                              regex, inverse_regex,
                              num_column, output_file)

    # Close
    output_file.close()


def executing_counting_commit(branch, since, until, interval,
                              regex, inverse_regex,
                              num_column, output_file):

    # Create repo command
    repo_cmd = "repo forall -p -v "
    if regex is not None:
        repo_cmd = repo_cmd + "-r " + regex + " "
    if inverse_regex is not None:
        repo_cmd = repo_cmd + "-i " + inverse_regex + " "
    repo_cmd = repo_cmd + "-c "
    repo_forall_cmd = "git_cc " + branch + \
                      " " + since + \
                      " " + until + \
                      " " + interval
    cmd = (repo_cmd + repo_forall_cmd).split()

    exe = subprocess.Popen(cmd, stdout=subprocess.PIPE, encoding='utf-8')

    project = None
    sum_columns = numpy.zeros(num_column - 1, numpy.int32)
    while True:
        polling = exe.poll()
        if polling is not None:
            break
        for line in exe.stdout:
            if line.startswith('project '):
                project = line[len('project '):-1]
            elif line.startswith(','):
                # Sum columns
                line_array = numpy.array(list(map(int, line[1:].split(','))), numpy.int32)
                sum_columns += line_array
                output_line = project + line
                output_file.write(output_line)
            elif line == '' or line == '\n':
                # Do nothing
                continue
            else:
                output_file.write(line)

    # Write sum of each column
    output_file.write('Sum,')
    output_file.write(','.join(list(map(str, sum_columns.tolist()))))
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
    num_column = 1
    while date <= date_until:
        date_adj = date - datetime.timedelta(days=1)
        output_file.write(",%s" % date_adj.strftime('%Y-%m-%d'))
        date = date + delta
        num_column += 1

    if date > date_until:
        output_file.write(",%s" % date_until.strftime('%Y-%m-%d'))
        num_column += 1

    output_file.write(",Sum\n")
    num_column += 1

    return num_column


def create_file_name(branch, since, until, interval, regex, inverse_regex):
    branch_name = branch.replace('/', '_')
    file_name = "Commit_Counts_" + branch_name + \
                '_' + since + '-' + until + '_' + interval
    if regex is not None:
        file_name += '_' + regex.replace('/', '_')
    if inverse_regex is not None:
        file_name += '_wo_' + inverse_regex.replace('/', '_')

    return file_name


def parse_args_for_cc(args):
    opt = None
    branch = None
    since = None
    until = None
    interval = None
    regex_pj = None
    inverse_regex_pj = None
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
        elif opt == 'p' or opt == 'period':
            interval = arg
            opt = None
        elif opt == 'r' or opt == 'regex-pj':
            regex_pj = arg
            opt = None
        elif opt == 'i' or opt == 'inverse-regex-pj':
            inverse_regex_pj = arg
            opt = None
        else:
            print("Error: Invalid argument")
            print_usage()
            sys.exit(1)

    if opt is not None:
        print("Error: Invalid argument")
        print_usage()
        sys.exit(1)
    if branch is None or since is None or until is None\
            or interval is None:
        print("Error: Invalid argument")
        print_usage()
        sys.exit(1)

    return branch, since, until, interval, regex_pj, inverse_regex_pj


def print_usage():
    """Print usage"""
    print("Usage: repocc -b bransh -s start -u until -p interval"
          "              -r regex project -i inverse-regex project")


if __name__ == '__main__':
    main(sys.argv[1:])
