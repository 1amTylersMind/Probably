import os, sys


def swap(fname,destroy):
    data = []
    for line in open(fname,'r').readlines():
        data.append(line.replace('\n',''))
    if destroy:
        os.system('rm '+ fname)
    return data


def trace(dest):
    trace = {}
    os.system('traceroute '+dest+" >> trace.txt")
    raw_trace = swap('trace.txt', True)
    hop = 1
    for line in raw_trace:
        try:
            trace[hop] = line.split(str(hop)+' ')[1].split(' (')[0].replace(' * ','')
            print trace[hop]
            hop += 1
        except IndexError:
            pass
    print str(hop) + " Hops to "+dest


def parse_trace(fname):
    raw_trace = swap(fname,False)
    hop = 1
    for line in raw_trace:
        try:
            trace[hop] = line.split(str(hop) + ' ')[1].split(' (')[0].replace('* ', '')
            print trace[hop]
            hop += 1
        except IndexError:
            pass
    print str(hop) + " Hops to " + trace[hop]


def detailed_trace_data(fname):
    raw_data = swap(fname,False)


def main():
    if '-manual' in sys.argv:
        trace(sys.argv[2])

    if '-parse' in sys.argv:
        parse_trace(sys.argv[2])

    if '-analyze' in sys.argv:
        detailed_trace_data(sys.argv[2])


if __name__ == '__main__':
    main()


