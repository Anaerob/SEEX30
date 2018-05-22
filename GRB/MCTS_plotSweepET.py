import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

import Load

def main():
    
    eSweep = ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6']
    tSweep = ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6']
    bResults = Load.loadFloatMatrix('MCTS_sweepET_b', len(tSweep), len(eSweep))
    wResults = Load.loadFloatMatrix('MCTS_sweepET_w', len(tSweep), len(eSweep))
    
    plt.figure()
    plot = plt.imshow(bResults, cmap = mpl.cm.Greys, norm = mpl.colors.Normalize(vmin = 0, vmax = 1), origin = 'lower')
    cbar = plt.colorbar(plot)
    cbar.ax.set_ylabel('Probability')
    plt.title('B Probability of using optimal strategy')
    plt.xlabel('Temperature')
    plt.xticks(list(range(len(tSweep))), tSweep)
    plt.ylabel('Epsilon')
    plt.yticks(list(range(len(eSweep))), eSweep)
    
    plt.figure()
    plot = plt.imshow(wResults, cmap = mpl.cm.Greys, norm = mpl.colors.Normalize(vmin = 0, vmax = 1), origin = 'lower')
    cbar = plt.colorbar(plot)
    cbar.ax.set_ylabel('Probability')
    plt.title('W Probability of using optimal strategy')
    plt.xlabel('Temperature')
    plt.xticks(list(range(len(tSweep))), tSweep)
    plt.ylabel('Epsilon')
    plt.yticks(list(range(len(eSweep))), eSweep)
    
    plt.show()

if __name__ == '__main__':
    main()

#