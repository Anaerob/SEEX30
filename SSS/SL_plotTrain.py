import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

import Load

def main():
    
    nBattles = 1000
    nPlotPoints = 1001
    x = np.linspace(0, nBattles, nPlotPoints)
    xLine = np.linspace(0, nBattles, 2)
    bias = Load.loadFloatMatrix('SL_bias_plot', nPlotPoints, 2)
    weights = Load.loadFloatMatrix('SL_weights_plot', nPlotPoints, 2 * 2)
    biasSmooth = Load.loadFloatArray('SL_bias_smooth', 2)
    weightsSmooth = Load.loadFloatArray('SL_weights_smooth', 2 * 2)
    
    plt.figure()
    plt.plot(x, bias, linewidth = 0.5)
    plt.plot(x, weights, linewidth = 0.5)
    plt.plot(xLine, [biasSmooth, biasSmooth], ':')
    plt.plot(xLine, [weightsSmooth, weightsSmooth], ':')
    plt.title('Biases and weights')
    plt.xlabel('Number of trained games')
    plt.ylabel('Weight values')
    
    plt.show()

if __name__ == '__main__':
    main()

#