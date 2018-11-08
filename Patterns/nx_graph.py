import os, sys, resource

CEND   = '\33[0m'
CBOLD  = '\33[1m'
CITAL  = '\33[3m'
CWHBLK = '\33[7m'
CBLINK = '\33[5m'
CRED   = '\33[31m'
CPURP  = '\33[35m'
CGREEN = '\33[92m'
CBLUE  = '\33[34m'
CBROWN = '\33[46m'
CREDBG = '\33[41m'
CBLKBG = '\33[100m'


def check_mem_usage():
    """
    Check the current memory usage of program
    :return: Current RAM usage in bytes
    """
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return mem


def swap(fname,destroy):
    data = []
    for line in open(fname, 'r').readlines():
        data.append(line.replace('\n',''))
    if destroy:
        os.system('rm '+fname)
    return data


def sample_callback(sample):
    data = {}
    pkt = 0
    for line in sample:
        packet = []
        try:
            packet.append(line.split('>')[0].replace(' ',''))
            packet.append(line.split('>')[1].split(': ')[0])
            packet.append(line.split('ttl ')[1])
        except IndexError:
            pass
        try:
            packet.append(line.split('[')[1].split(']')[0])
        except IndexError:
            pass
        if 'ARP' in line.split(',')[0].split(' '):
            packet.append("ARP")
        if len(packet) >= 3:
            data[pkt] = packet
            pkt += 1
            print CBOLD+CBLUE+str(packet)+CEND
        else:
            print CBOLD+CRED+str(line.split(','))+CEND
    return data


def monitor(NSamples):
    os.system('clear')
    capt = 0
    while capt <= NSamples:
        os.system('tcpdump -c 10 -vv >> tcp.txt')
        traffic = swap('tcp.txt', True)
        sample_callback(traffic)
        capt += 1


print CITAL+" Initial Memory Consumption: " + str(check_mem_usage()/1000) + "Kb"+CEND
monitor(1)