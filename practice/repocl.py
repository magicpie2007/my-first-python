#! /usr/bin/env python3

import sys
import datetime


def main(args):
    # Parse arguments
    branch, since, until = parse_args(args)

    # Decide output file name
    output_file_name = create_file_name(branch, since, until)


def repository_commit_log(branch, since, until):
    # Convert string to datetime type
    if since is not None:
        date_since = datetime.datetime.strptime(since, '%Y%m%d')
    if until is not None:
        date_until = datetime.datetime.strptime(until, '%Y%m%d')

    # Create repo command
    repo_cmd = "repo forall -p -v -c "
    repo_forall_cmd = "git log " + branch + " "





def create_file_name(branch, since, until):
    branch_name = branch.replace('/', '_')
    return "Commit_log_" + branch_name + '_' + since + '-' + until


def parse_args(args):
    opt = None
    branch = None
    since = None
    until = None
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
        else:
            print("Error: Invalid argument")
            sys.exit(1)
    if opt is not None:
        print("Error: Invalid argument")
        sys.exit(1)
    return branch, since, until




if __name__ == '__main__':
    main(sys.argv[1:])
