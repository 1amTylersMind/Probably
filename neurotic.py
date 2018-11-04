import os, sys, resource, numpy as np, networkx as nx
import matplotlib.pyplot as plt


def swap(fname, destroy):
    data = []
    for line in open(fname, 'r').readlines():
        data.append(line.replace('\n', ''))
    if destroy:
        os.system('rm '+fname)
    return data


def check_mem_usage():
    """
    Check the current memory usage of program
    :return: Current RAM usage in bytes
    """
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return mem


def bfs(graph, start):
    search = [start]
    meta_search = list()
    path = list()
    while search:
        vertex = search.pop()
        for node in graph[vertex]:
            if node not in meta_search:
                meta_search.append(node)
                search.append(node)
                path.append([vertex, node])
    return path


def dfs(graph, start):
    stacked = [start]
    roots = {start:start}
    path = list()
    while stacked:
        vertex = stacked.pop(-1)
        for node in graph[vertex]:
            if node not in roots:
                roots[node] = vertex
                stacked.append(node)
        path.append([roots[vertex],vertex])
    return path


def trace2graph(trace):

    Hop = 0
    for hop in trace:
        nodes = []
        try:
            print trace[Hop - 1]+" > "+hop
        except IndexError:
            pass
        Hop += 1


def axion():
    g = nx.Graph()

    graph = {'A': ['B', 'C'],
             'B': ['D', 'E'],
             'C': ['F', 'G'],
             'D': ['B'],
             'E': ['B'],
             'F': ['C'],
             'G': ['C']}
    for node in graph:
        g.add_nodes_from(node)
        for edge in graph[node]:
            g.add_edge(node, edge)

    pos = {'A': [0.00, 0.00],  'B': [1.00,1.00],
           'C': [-1.00, 1.00],  'D': [2.00, 3.00],
           'E': [3.00,2.00],  'F':[-2.00, 3.00],
           'G': [-3.00, 2.00]}

    nx.draw(g, pos, with_labels=True)
    plt.show()
    return nx.to_numpy_array(g), graph


def example_traces():
    os.system('ls /media/root >> mounted.txt')
    devs = swap('mounted.txt', destroy=True)
    if 'DB0' in devs:
        print 'Internet Map Database Connected'
        os.system(' ls /media/root/DB0/iMap/traces >> fnames.txt')
        fnames = swap('fnames.txt', True)
        txtFiles = 0
        scans = 0
        traces = 0
        for file in fnames:
            try:
                ext = file.split('.')[1]
                if ext == 'txt':
                    txtFiles += 1
            except IndexError:
                pass
            try:
                scanum = file.split('scan')[1].split('.')[0]
                scans += 1
            except IndexError:
                pass
            try:
                tracenum = file.split('trace')[1].split('.')[0]
                traces += 1
            except IndexError:
                pass

        print str(scans) + " Scans Found"
        print str(traces) + " Traces Found "


def main():
    mem_aware = False
    if '--memory' in sys.argv:
        mem_aware = True
        print "Initial Memory Overhead is: " + str(check_mem_usage()/1000)+' Kb'

    if '-iMap' in sys.argv:
        os.system('python simple_trace.py -manual 8.8.8.8 >> goog.txt')
        trace2goog = swap('goog.txt',True)
        print trace2goog.pop(len(trace2goog)-1)
        trace2graph(trace2goog)

    # Example of a little network
    axi, simple_synapse = axion()

    if mem_aware:
        print "::: " + str(check_mem_usage() / 1000) + " Kb of RAM Used :::"

    # Compare the styles of Breadth and Depths First Searches
    # print bfs(simple_synapse,'A')
    # print dfs(simple_synapse, 'A')
    if mem_aware:
        print "::: " + str(check_mem_usage() / 1000) + " Kb of RAM Used :::"


if __name__ == '__main__':
    main()
