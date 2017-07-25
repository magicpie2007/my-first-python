#! /usr/bin/env python3

import sys
import pygal


def main(args):
    pass


def stacked_bar_graph(graph_title, x_labels, *args, output_file):
    graph = pygal.StackedBar(title=graph_title)
    graph.x_labels = x_labels
    for arg in args:
        graph.add(arg['title'], arg['data'])
    graph.render_to_file(output_file)


if __name__ == '__main__':
    main(sys.argv[1:])
