import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

import Constants as c
import Load

weightsGG = Load.loadFloatMatrix('plotGreenGreen', 1001, 20)
weightsGR = Load.loadFloatMatrix('plotGreenRed', 1001, 20)
weightsGB = Load.loadFloatMatrix('plotGreenBlue', 1001, 20)
weightsRG = Load.loadFloatMatrix('plotRedGreen', 1001, 20)
weightsRR = Load.loadFloatMatrix('plotRedRed', 1001, 20)
weightsRB = Load.loadFloatMatrix('plotRedBlue', 1001, 20)
weightsBG = Load.loadFloatMatrix('plotBlueGreen', 1001, 20)
weightsBR = Load.loadFloatMatrix('plotBlueRed', 1001, 20)
weightsBB = Load.loadFloatMatrix('plotBlueBlue', 1001, 20)
x = np.linspace(0, 10000000, 1001)

figGG = plt.figure()
plot = plt.plot(x, weightsGG, linewidth = 0.5)
plt.title('Bulbasaur VS Bulbasaur: Evolution of weights during training')
plt.xlabel('Number of trained battles')
plt.ylabel('Weights')

figGR = plt.figure()
plot = plt.plot(x, weightsGR, linewidth = 0.5)
plt.title('Bulbasaur VS Charmander: Evolution of weights during training')
plt.xlabel('Number of trained battles')
plt.ylabel('Weights')

figGB = plt.figure()
plot = plt.plot(x, weightsGB, linewidth = 0.5)
plt.title('Bulbasaur VS Squirtle: Evolution of weights during training')
plt.xlabel('Number of trained battles')
plt.ylabel('Weights')

figRG = plt.figure()
plot = plt.plot(x, weightsRG, linewidth = 0.5)
plt.title('Charmander VS Bulbasaur: Evolution of weights during training')
plt.xlabel('Number of trained battles')
plt.ylabel('Weights')

figRR = plt.figure()
plot = plt.plot(x, weightsRR, linewidth = 0.5)
plt.title('Charmander VS Charmander: Evolution of weights during training')
plt.xlabel('Number of trained battles')
plt.ylabel('Weights')

figRB = plt.figure()
plot = plt.plot(x, weightsRB, linewidth = 0.5)
plt.title('Charmander VS Squirtle: Evolution of weights during training')
plt.xlabel('Number of trained battles')
plt.ylabel('Weights')

figBG = plt.figure()
plot = plt.plot(x, weightsBG, linewidth = 0.5)
plt.title('Squirtle VS Bulbasaur: Evolution of weights during training')
plt.xlabel('Number of trained battles')
plt.ylabel('Weights')

figBR = plt.figure()
plot = plt.plot(x, weightsBR, linewidth = 0.5)
plt.title('Squirtle VS Charmander: Evolution of weights during training')
plt.xlabel('Number of trained battles')
plt.ylabel('Weights')

figBB = plt.figure()
plot = plt.plot(x, weightsBB, linewidth = 0.5)
plt.title('Squirtle VS Squirtle: Evolution of weights during training')
plt.xlabel('Number of trained battles')
plt.ylabel('Weights')



plt.show()

"""

fig1 = plt.figure()
plot = plt.imshow(Z3, cmap = mpl.cm.seismic, norm = mpl.colors.Normalize(vmin = 0, vmax = 1), origin = 'lower')
#cp = plt.contourf(R, B, Z1, cmap = mpl.cm.seismic, norm = mpl.colors.Normalize(vmin = 0, vmax = 1))
cbar = plt.colorbar(plot)
cbar.ax.set_ylabel('Probability of Red winning')
# plt.clabel(cp, inline = True, fontsize = 10)
plt.title('Red (Squirtle) Vs. Blue (Bulbasaur)')
plt.xlabel('Reds number of initial weakening moves')
plt.ylabel('Blues number of initial weakening moves')
plt.show()

""

fig, ax = plt.subplots()

cmap = mpl.cm.cool
norm = mpl.colors.Normalize(vmin = 5, vmax = 10)

cb1 = mpl.colorbar.ColorbarBase(ax, cmap = cmap, norm = norm, orientation = 'horizontal')

cb1.set_label('Some units')
fig.show()
"""