#! /usr/bin/env python3

import re

def main(args):
    options, inputpath, outputpath = parseargs(args)
    format(inputpath, outputpath, options['counttarget'] == 'dir', options['ignore'])


def parseargs(args):
    inputpath = args[-2]
    outputpath = args[-1]
    otherargs = args[0:-2]
    options = {'counttarget': 'file', 'ignore': None}

    opt = None
    for arg in otherargs:
        # Extract option key
        if arg.startswith('-'):
            opt = arg[1:]
        elif arg.startswith('--'):
            opt = arg[2:]

        if opt == 'd' or opt == 'dir':
            options['counttarget'] = 'dir'
            opt = None
            continue
        elif opt == 'h' or opt == 'help':
            opt = None
            displayhelp()
            sys.exit(0)
        elif opt.startswith('i=') or opt.startswith('ignore='):
            ignore = opt.split('=')
            options['ignore'] = ignore[1].split(',')
            opt = None
            continue
        else:
            continue

        # Extract option value (But now Not use option value)
        print("Error: Invalid argument")
        displayhelp()
        sys.exit(1)

    if opt != None:
        print("Error: Invalid argument")
        displayhelp()
        sys.exit(1)

    return options, inputpath, outputpath


def format(inputpath, outputpath, countdir=False, ignore=None):
    inputfile = open(inputpath, 'r')
    outputfile = open(outputpath, 'w')

    if countdir:
        outputfile.write('Directory,Count\n')
        dirname = None
        changes = 0
        for line in inputfile:
            filename, changesstr = extractdata(line)
            if filename == None or changesstr == None or includeignore(filename, ignore):
                continue

            index = filename.rfind('/')
            tmpdirname = '(Top Directory)'
            if index != -1:
                tmpdirname = filename[0:index]

            if dirname == None:
                dirname = tmpdirname

            if tmpdirname == dirname:
                changes += int(changesstr)
            else:
                outputline = dirname + ',' + str(changes) + '\n'
                outputfile.write(outputline)
                dirname = tmpdirname
                changes = int(changesstr)
        # Finally write data for last directory
        outputline = dirname + ',' + str(changes) + '\n'
        outputfile.write(outputline)

    else:
        outputfile.write('File,Count\n')
        for line in inputfile:
            filename, changes = extractdata(line)
            if filename == None or changes == None or includeignore(filename, ignore):
                continue
            outputfile.write(filename + ',' + changes + '\n')

    inputfile.close()
    outputfile.close()


def extractdata(linestr):
    separated = linestr.split('|')
    if len(separated) != 2 or 'Bin' in separated[1]:
        return None, None
    filename = separated[0].strip()
    regex = re.compile(r'\d+')
    mo = regex.search(separated[1])
    changes = mo.group()
    return filename, changes


def includeignore(str, ignore):
    if ignore == None:
        return False
    for ig in ignore:
        if ig in str:
            return True
    return False


def displayhelp():
    pass


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])


