import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

import Load

def main():
    
    eSweep = ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6']
    tSweep = ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6']
    results = Load.loadFloatMatrix('MCTS_sweepET', len(tSweep), len(eSweep))
    
    plt.figure()
    plot = plt.imshow(results, cmap = mpl.cm.Greys, norm = mpl.colors.Normalize(vmin = 0, vmax = 1), origin = 'lower')
    cbar = plt.colorbar(plot)
    cbar.ax.set_ylabel('Probability')
    plt.title('Probability of using optimal strategy')
    plt.xlabel('Temperature')
    plt.xticks(list(range(len(tSweep))), tSweep)
    plt.ylabel('Epsilon')
    plt.yticks(list(range(len(eSweep))), eSweep)
    
    plt.show()

if __name__ == '__main__':
    main()

#