import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

import Constants as c
import Load

def main():
    
    lSweep = ['0.1', '0.2', '0.3', '0.4', '0.5']
    tSweep = ['0.1', '0.2', '0.3', '0.4', '0.5']
    bAvg = Load.loadFloatMatrix('SL_sweepLT_bAvg', len(lSweep), len(tSweep))
    bMax = Load.loadFloatMatrix('SL_sweepLT_bMax', len(lSweep), len(tSweep))
    wAvg = Load.loadFloatMatrix('SL_sweepLT_wAvg', len(lSweep), len(tSweep))
    wMax = Load.loadFloatMatrix('SL_sweepLT_wMax', len(lSweep), len(tSweep))
    
    plt.figure()
    plot = plt.imshow(bAvg, cmap = mpl.cm.Greys, norm = mpl.colors.Normalize(vmin = 0, vmax = 0.8), origin = 'lower')
    cbar = plt.colorbar(plot)
    cbar.ax.set_ylabel('Probability')
    plt.title('bAvg: Probability of Charmander winning \n against a hard coded Squirtle')
    plt.xlabel('Temperature')
    plt.xticks(list(range(len(tSweep))), tSweep)
    plt.ylabel('Learning rate')
    plt.yticks(list(range(len(lSweep))), lSweep)
    
    plt.figure()
    plot = plt.imshow(bMax, cmap = mpl.cm.Greys, norm = mpl.colors.Normalize(vmin = 0, vmax = 0.8), origin = 'lower')
    cbar = plt.colorbar(plot)
    cbar.ax.set_ylabel('Probability')
    plt.title('bMax: Probability of Charmander winning \n against a hard coded Squirtle')
    plt.xlabel('Temperature')
    plt.xticks(list(range(len(tSweep))), tSweep)
    plt.ylabel('Learning rate')
    plt.yticks(list(range(len(lSweep))), lSweep)
    
    plt.figure()
    plot = plt.imshow(wAvg, cmap = mpl.cm.Greys, norm = mpl.colors.Normalize(vmin = 0, vmax = 0.4), origin = 'lower')
    cbar = plt.colorbar(plot)
    cbar.ax.set_ylabel('Probability')
    plt.title('wAvg: Probability of Squirtle winning \n against a hard coded Charmander')
    plt.xlabel('Temperature')
    plt.xticks(list(range(len(tSweep))), tSweep)
    plt.ylabel('Learning rate')
    plt.yticks(list(range(len(lSweep))), lSweep)
    
    plt.figure()
    plot = plt.imshow(wMax, cmap = mpl.cm.Greys, norm = mpl.colors.Normalize(vmin = 0, vmax = 0.4), origin = 'lower')
    cbar = plt.colorbar(plot)
    cbar.ax.set_ylabel('Probability')
    plt.title('wMax: Probability of Squirtle winning \n against a hard coded Charmander')
    plt.xlabel('Temperature')
    plt.xticks(list(range(len(tSweep))), tSweep)
    plt.ylabel('Learning rate')
    plt.yticks(list(range(len(lSweep))), lSweep)
    
    plt.show()

if __name__ == '__main__':
    main()

#