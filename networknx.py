import os, sys, time, resource, networkx as nx
import matplotlib.pyplot as plt
from scapy.all import *


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


def get_public_ip():
    os.system('GET https://api.ipify.org?format=json >> ip.txt')
    myPublicIP = swap('ip.txt', True).pop().split('ip":"')[1].split('"}')[0]
    print myPublicIP
    return myPublicIP


def run():
    running = True
    traffic = {}
    while running:
        try:
            os.system('python networknx.py -r >> nx.txt')
            nxtraff = swap('nx.txt', True)
            pkt = 0
            for line in nxtraff:
                packet = line.split('/')
                try:
                    data = [packet[0],packet[1],packet[2]]
                    pkt += 1
                    traffic[pkt] = data
                except IndexError:
                    pass
                '''
                Split by NIC / TYPE/ TRANSPORT /DATA
                '''
        except KeyboardInterrupt:
            running = False
            exit(0)


def main():
    if '-m' in sys.argv:
        print "Initial Memory Overhead is: " + str(check_mem_usage() / 1000) + " Kb"

    if '-r' in sys.argv:  # Recursive
        stank = sniff(5)
        stank.summary()
        if '-h' in sys.argv:
            print "*#----------------#*"
            stank.hexdump()
    if 'run' in sys.argv:
        run()


if __name__ == '__main__':
    main()
