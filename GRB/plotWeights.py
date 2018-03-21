import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

import Constants as c
import Load

nPlotPoints = 1001
xHomo = np.linspace(0, 10000000, nPlotPoints)
xHomoLine = np.linspace(0, 10000000, 2)
xHetero = np.linspace(0, 1000000, nPlotPoints)
xHeteroLine = np.linspace(0, 1000000, 2)

plotGG = Load.loadFloatMatrix('plotGreenGreen', nPlotPoints, c.nInputs * c.nOutputs)
plotRR = Load.loadFloatMatrix('plotRedRed', nPlotPoints, c.nInputs * c.nOutputs)
plotBB = Load.loadFloatMatrix('plotBlueBlue', nPlotPoints, c.nInputs * c.nOutputs)
plotGR = Load.loadFloatMatrix('plotGreenRed', nPlotPoints, c.nInputs * c.nOutputs)
plotGB = Load.loadFloatMatrix('plotGreenBlue', nPlotPoints, c.nInputs * c.nOutputs)
plotRG = Load.loadFloatMatrix('plotRedGreen', nPlotPoints, c.nInputs * c.nOutputs)
plotRB = Load.loadFloatMatrix('plotRedBlue', nPlotPoints, c.nInputs * c.nOutputs)
plotBG = Load.loadFloatMatrix('plotBlueGreen', nPlotPoints, c.nInputs * c.nOutputs)
plotBR = Load.loadFloatMatrix('plotBlueRed', nPlotPoints, c.nInputs * c.nOutputs)

weightsGG = Load.loadFloatArray('weightsGreenGreen', c.nInputs * c.nOutputs)
weightsRR = Load.loadFloatArray('weightsRedRed', c.nInputs * c.nOutputs)
weightsBB = Load.loadFloatArray('weightsBlueBlue', c.nInputs * c.nOutputs)
weightsGR = Load.loadFloatArray('smoothGreenRed', c.nInputs * c.nOutputs)
weightsGB = Load.loadFloatArray('smoothGreenBlue', c.nInputs * c.nOutputs)
weightsRG = Load.loadFloatArray('smoothRedGreen', c.nInputs * c.nOutputs)
weightsRB = Load.loadFloatArray('smoothRedBlue', c.nInputs * c.nOutputs)
weightsBG = Load.loadFloatArray('smoothBlueGreen', c.nInputs * c.nOutputs)
weightsBR = Load.loadFloatArray('smoothBlueRed', c.nInputs * c.nOutputs)

plt.figure()
plt.plot(xHomo, plotGG, linewidth = 0.5)
plt.plot(xHomoLine, [weightsGG, weightsGG], ':')
plt.title('Weight values during training \n Bulbasaur - Bulbasaur')
plt.xlabel('Number of trained battles')
plt.ylabel('Weight values')

plt.figure()
plt.plot(xHomo, plotRR, linewidth = 0.5)
plt.plot(xHomoLine, [weightsRR, weightsRR], ':')
plt.title('Weight values during training \n Charmander - Charmander')
plt.xlabel('Number of trained battles')
plt.ylabel('Weight values')

plt.figure()
plt.plot(xHomo, plotBB, linewidth = 0.5)
plt.plot(xHomoLine, [weightsBB, weightsBB], ':')
plt.title('Weight values during training \n Squirtle - Squirtle')
plt.xlabel('Number of trained battles')
plt.ylabel('Weight values')

plt.figure()
plt.plot(xHetero, plotGR, linewidth = 0.5)
plt.plot(xHeteroLine, [weightsGR, weightsGR], ':')
plt.title('Weight values during training \n Bulbasaur - Charmander')
plt.xlabel('Number of trained battles')
plt.ylabel('Weight values')

plt.figure()
plt.plot(xHetero, plotRG, linewidth = 0.5)
plt.plot(xHeteroLine, [weightsRG, weightsRG], ':')
plt.title('Weight values during training \n Charmander - Bulbasaur')
plt.xlabel('Number of trained battles')
plt.ylabel('Weight values')

plt.figure()
plt.plot(xHetero, plotRB, linewidth = 0.5)
plt.plot(xHeteroLine, [weightsRB, weightsRB], ':')
plt.title('Weight values during training \n Charmander - Squirtle')
plt.xlabel('Number of trained battles')
plt.ylabel('Weight values')

plt.figure()
plt.plot(xHetero, plotBR, linewidth = 0.5)
plt.plot(xHeteroLine, [weightsBR, weightsBR], ':')
plt.title('Weight values during training \n Squirtle - Charmander')
plt.xlabel('Number of trained battles')
plt.ylabel('Weight values')

plt.figure()
plt.plot(xHetero, plotBG, linewidth = 0.5)
plt.plot(xHeteroLine, [weightsBG, weightsBG], ':')
plt.title('Weight values during training \n Squirtle - Bulbasaur')
plt.xlabel('Number of trained battles')
plt.ylabel('Weight values')

plt.figure()
plt.plot(xHetero, plotGB, linewidth = 0.5)
plt.plot(xHeteroLine, [weightsGB, weightsGB], ':')
plt.title('Weight values during training \n Bulbasaur - Squirtle')
plt.xlabel('Number of trained battles')
plt.ylabel('Weight values')

plt.show()

#