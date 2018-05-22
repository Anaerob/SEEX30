import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

import Constants as c
import Load

def main():
    
    dSweep = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    win = Load.loadFloatArray('MCTS_sweepD_win', len(dSweep))
    
    plt.figure()
    plt.plot(dSweep, win, 'x')
    plt.title('WINS OVER DEPTH')
    plt.xlabel('Depth')
    plt.ylabel('Wins')
    
    plt.show()

if __name__ == '__main__':
    main()

#