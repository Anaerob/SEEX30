import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

import Load

def main()
    
    dSweep = ['5', '10', '15', '20', '25']
    sSweep = ['200', '400', '600', '800', '1000']
    results = Load.loadFloatMatrix('MCTS_sweepDS_strategy', len(dSweep), len(sSweep))
    
    plt.figure()
    plot = plt.imshow(results, cmap = mpl.cm.Greys, norm = mpl.colors.Normalize(vmin = 0, vmax = 1), origin = 'lower')
    cbar = plt.colorbar(plot)
    cbar.ax.set_ylabel('Probability')
    plt.title('Probability of using optimal strategy')
    plt.xlabel('Search')
    plt.xticks(list(range(len(sSweep))), sSweep)
    plt.ylabel('Depth')
    plt.yticks(list(range(len(dSweep))), dSweep)
    
    plt.show()

if __name__ == '__main__'
    main()

#