import argparse
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

import Load

def plot(title, yName, yLabel):
    
    dSweep = [1, 10, 20, 30, 40, 50]
    y = Load.loadFloatArray('MCTS_sweepD_results/MCTS_sweepD_' + yName, len(dSweep))
    plt.figure()
    plt.plot(dSweep, y, 'x')
    plt.title(title)
    plt.xlabel('Depth')
    plt.ylabel(yLabel)

def main(args):
    
    plotAnything = args.abort or args.loss or args.tie or args.time or args.win
    if args.abort:
        plot('ABORTS OVER DEPTH', 'abort', 'Aborts')
    if args.loss:
        plot('LOSSES OVER DEPTH', 'loss', 'Losses')
    if args.tie:
        plot('TIES OVER DEPTH', 'tie', 'Ties')
    if args.time:
        plot('TIMES OVER DEPTH', 'time', 'Time (s)')
    if args.win:
        plot('WINS OVER DEPTH', 'win', 'Wins')
    if plotAnything:
        plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--abort', action='store_true')
    parser.add_argument('--loss', action='store_true')
    parser.add_argument('--tie', action='store_true')
    parser.add_argument('--time', action='store_true')
    parser.add_argument('--win', action='store_true')
    args = parser.parse_args()
    main(args)

#