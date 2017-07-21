#! /usr/bin/env python3

import datetime, sys, os, re, subprocess, io
from dateutil.relativedelta import relativedelta


def main(args):
    if args[0] == 'cc':
        branch, since, until, interval = parseArgsForCC(args[1:])
        executeCountingCommit(branch, since, until, interval)
    elif args[0] == 'interactive':
        startInteractiveMode()


def startInteractiveMode():
    print('''\
    What do you do ?
      1. Count Number of Commit
      2. Research a specific project
      
      9. Exit
    ''')
    number = input('''\
    Select No.: ''')
    if number == '1':
        startCountingCommit()
    elif number == '2':
        startResearchSpecificProject()
    elif number == '9':
        sys.exit()


def startCountingCommit():
    print('''\
    What do you want to count ?
      1. Total Commits of All Projects
      2. Commits of Each Project
    ''')
    countingMode = input('''\
    Select No.: ''')
    branch = input('''\
    Branch: ''')
    since = input('''\
    Since: ''')
    until = input('''\
    Until: ''')
    interval = input('''\
    Interval: ''')


def startResearchSpecificProject():
    pass


def executeCountingCommit(branch, since, until, interval):
    # Create repo command
    # repo_cmd = ["repo", "forall", "-p", "-v", "-c"]
    repo_cmd = "repo forall -p -v -c "
    # since_opt = "--since=\'%s 00:00:00\' " % since.strftime('%Y-%m-%d')
    # until_opt = "--until=\'%s 23:59:59\'" % until.strftime('%Y-%m-%d')
    # repo_forall_cmd = "git log " +  branch + \
    #                   " --oneline --date=iso --pretty=',%h,%cd,%a,%s' " + \
    #                   since_opt + until_opt
    repo_forall_cmd = "git_cc " + branch + \
                      " " + since.strftime('%Y%m%d') + \
                      " " + until.strftime('%Y%m%d') + \
                      " " + interval
    #repo_cmd.append("\"%s\"" % repo_forall_cmd)
    # repo_cmd.append(repo_forall_cmd.split())
    command = (repo_cmd + repo_forall_cmd).split()
    print(command)

    # Parse interval
    regex = re.compile(r'(\d+)(m|w|d)')
    mo = regex.search(interval)
    if mo.group(1) == None or mo.group(2) == None:
        print("Error: Invalid argumnet")
        sys.exit(1)
    interval = {'value': int(mo.group(1)), 'unit': mo.group(2)}

    delta = None
    if interval['unit'] == 'm':
        # delta = datetime.timedelta(months=interval['value'])
        delta = relativedelta(months=interval['value'])
    elif interval['unit'] == 'w':
        delta = datetime.timedelta(weeks=interval['value'])
    elif interval['unit'] == 'd':
        delta = datetime.timedelta(days=interval['value'])

    date = since + delta
    # print("Project", end='')
    while date <= until:
        date_adj = date - datetime.timedelta(days=1)
        print(",%s" % date_adj.strftime('%Y-%m-%d'), end='')
        date = date + delta

    if date > until:
        print(",%s" % until.strftime('%Y-%m-%d'), end='')

    print(",Sum")

    exe = subprocess.Popen(command, stdout=subprocess.PIPE, encoding='utf-8')
    #test_cmd = ["cat", "android_o_commit_count_research_01_20160801_20170630_1m.txt"]
    #exe = subprocess.Popen(test_cmd, stdout=subprocess.PIPE, encoding='utf-8')
    project = None
    while True:
        polling = exe.poll()
        if polling != None:
            print("Already subprocess is terminated: " + str(polling))
            break
        #outs, err = exe.communicate()
        #if outs == None:
        #    break
        #outs_str = outs.decode('utf-8')
        # for line in exe.stdout:
        print("!!! PORING !!!")
        for line in exe.stdout:
            #linestr = str(line)
            # print('org: ' + line, end='')
            if line.startswith('project '):
                project = line[len('project '):-1]
            elif line.startswith(','):
                outputline = project + line
                print(outputline, end='')
                #outputfile.write(outputline)
            elif line == '' or line == '\n':
                # Do nothing
                continue
            else:
                print(line, end='')
                #outputfile.write(outputline)


def parseArgsForCC(args):
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
            since = datetime.datetime.strptime(arg, '%Y%m%d')
            opt = None
        elif opt == 'u' or opt =='until' or opt == 'end':
            until = datetime.datetime.strptime(arg, '%Y%m%d')
            opt = None
        elif opt == 'i' or opt == 'interval':
            interval = arg
            opt = None
        else:
            print("Error: Invalid argument")
            sys.exit(1)
    if opt != None:
        print("Error: Invalid argument")
        sys.exit(1)
    return branch, since, until, interval


if __name__ == '__main__':
    main(sys.argv[1:])

