import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

import Constants as c
import Load

def main():
    
    nPlotPoints = 1001
    nTrain = 10000
    
    x = np.linspace(0, nTrain, nPlotPoints)
    xLine = np.linspace(0, nTrain, 2)
    bBias = Load.loadFloatMatrix('SL_bBias_plot', nPlotPoints, c.nOutputs)
    bBiasSmooth = Load.loadFloatArray('SL_bBias_smooth', c.nOutputs)
    bWeights = Load.loadFloatMatrix('SL_bWeights_plot', nPlotPoints, c.nOutputs * c.nInputs)
    bWeightsSmooth = Load.loadFloatArray('SL_bWeights_smooth', c.nOutputs * c.nInputs)
    wBias = Load.loadFloatMatrix('SL_wBias_plot', nPlotPoints, c.nOutputs)
    wBiasSmooth = Load.loadFloatArray('SL_wBias_smooth', c.nOutputs)
    wWeights = Load.loadFloatMatrix('SL_wWeights_plot', nPlotPoints, c.nOutputs * c.nInputs)
    wWeightsSmooth = Load.loadFloatArray('SL_wWeights_smooth', c.nOutputs * c.nInputs)
    
    plt.figure()
    plt.plot(x, bBias, linewidth = 0.5)
    plt.plot(x, bWeights, linewidth = 0.5)
    plt.plot(xLine, [bBiasSmooth, bBiasSmooth], ':')
    plt.plot(xLine, [bWeightsSmooth, bWeightsSmooth], ':')
    plt.title('Weight values during training \n Charmander')
    plt.xlabel('Number of trained battles')
    plt.ylabel('Weight values')
    
    plt.figure()
    plt.plot(x, wBias, linewidth = 0.5)
    plt.plot(x, wWeights, linewidth = 0.5)
    plt.plot(xLine, [wBiasSmooth, wBiasSmooth], ':')
    plt.plot(xLine, [wWeightsSmooth, wWeightsSmooth], ':')
    plt.title('Weight values during training \n Squirtle')
    plt.xlabel('Number of trained battles')
    plt.ylabel('Weight values')
    
    plt.show()

if __name__ == '__main__':
    main()

#