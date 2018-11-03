import numpy as np, matplotlib.pyplot as plt, matplotlib.animation as animation
import time, resource


def check_mem_usage():
    """
    Check the current memory usage of program
    :return: Current RAM usage in bytes
    """
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return mem


def random_flips(N):
    coin = {1: 'Heads', 0: 'Tails'}
    game = {'Heads': 0, 'Tails': 0}
    flips = np.random.randint(0, 2, N)
    reel = []
    start = time.time()
    for toss in flips:
        game[coin[toss]] += 1
        reel.append([game['Heads'], game['Tails']])
    return game


def coin_flip_experiment(flips):
    games = list()
    hdata = []
    tdata = []
    start = time.time()
    for flip in flips:
        game = random_flips(flip)
        hdata.append(game['Heads'])
        tdata.append(game['Tails'])
        games.append(game)
    print "\t\tDONE"
    print "[" + str(time.time() - start) + " s Elapsed]"
    print "HEADS | TAILS | % HEADS"
    for game in games:
        ratioH = float((game['Heads']) * 1000 / (game['Heads'] + game['Tails'])) / 1000
        out = str(int(game['Heads'])) + "   |   " + str(int(game['Tails'])) +\
                                        "   |   " + str(ratioH)
        print out
    return games, hdata, tdata


def visualize_experiment(games, heads, tails):
    data = []
    for graph in games:
        ratio = float(graph['Heads']*1000)/float(graph['Tails']*1000)
        data.append(ratio)

    f, (ax0, ax1) = plt.subplots(2,1, sharex=True)

    ax0.plot(np.array(data))
    ax0.plot(np.ones((len(data))))
    ax1.plot(np.log10(np.array(heads)),label='Heads')
    ax1.plot(np.log10(np.array(tails)),label='Tails')
    ax1.legend()
    ax0.set_xlabel('Coin Flip Experiments')
    ax0.set_ylabel('Ratio Heads/Tails')
    ax1.set_xlabel('experiments')
    ax1.set_ylabel('log10(flips)')
    plt.show()


def main():
    """
    I want to watch how the distribution of heads and tails,
    for a simulated coinflip, will evolve over time.
    The Question is ... will it converge?
    """

    mem_before_experiment = check_mem_usage()

    print str(float(mem_before_experiment * 1000) / 1000000) + " Mb Used (Total)"

    flips = [25,50,80,150,250,575,750,875,1000,2000,3000,4000,5000,7500,10000,
             12500, 15000, 20000]
    games, heads, tails= coin_flip_experiment(flips)

    mem_after_experiment = check_mem_usage()

    print str(float(mem_after_experiment * 1000) / 1000000) + " Mb Used (Total)"

    mem_used = mem_after_experiment - mem_before_experiment

    print str(np.sum(np.array(flips)))+" Coin Flips Simulated [" + \
          str(float(1000*mem_used/1000000)) + " kb of RAM used]"

    visualize_experiment(games, heads, tails)


if __name__ == '__main__':
    main()