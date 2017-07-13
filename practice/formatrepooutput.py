#! /usr/bin/env python3


def format(inputpath, outputpath):
    inputfile = open(inputpath, 'r')
    outputfile = open(outputpath, 'w')
    project = None
    for line in inputfile:
        # print(line, end='')
        if line.startswith('project '):
            project = line[len('project '):-1]
        elif line.startswith(','):
            outputline = project + line
            # print(outputline)
            outputfile.write(outputline)
        elif line == '' or line == '\n':
            # Do nothing
            continue
        else:
            # Write line as is.
            outputfile.write(line)

    inputfile.close()
    outputfile.close()


if __name__ == '__main__':
    import sys
    format(sys.argv[1], sys.argv[2])

