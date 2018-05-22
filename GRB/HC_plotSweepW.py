import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

import Load

def main():
    
    nStrategies = 7
    
    results = Load.loadFloatMatrix('HC_sweepW', nStrategies, nStrategies)
    
    plt.figure()
    plot = plt.imshow(results, cmap = mpl.cm.Greys, norm = mpl.colors.Normalize(vmin = 0, vmax = 1), origin = 'lower')
    cbar = plt.colorbar(plot)
    cbar.ax.set_ylabel('Probability')
    plt.title('Probability of Charmander winning over Squirtle')
    plt.xlabel('Number of initial Tail Whip (Squirtle)')
    plt.xticks(list(range(nStrategies)))
    plt.ylabel('Number of initial Growl (Charmander)')
    plt.yticks(list(range(nStrategies)))
    
    plt.show()

if __name__ == '__main__':
    main()

#