import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

import Load

nTacts = 7

compGG = Load.loadFloatMatrix('compGreenGreen', nTacts, nTacts)
compRR = Load.loadFloatMatrix('compRedRed', nTacts, nTacts)
compBB = Load.loadFloatMatrix('compBlueBlue', nTacts, nTacts)
compGR = Load.loadFloatMatrix('compGreenRed', nTacts, nTacts)
compRB = Load.loadFloatMatrix('compRedBlue', nTacts, nTacts)
compBG = Load.loadFloatMatrix('compBlueGreen', nTacts, nTacts)

figGG = plt.figure()
plot = plt.imshow(compGG, cmap = mpl.cm.Greys, norm = mpl.colors.Normalize(vmin = 0, vmax = 1), origin = 'lower')
cbar = plt.colorbar(plot)
cbar.ax.set_ylabel('Probability of Black winning')
plt.title('Probability of winning \n White (Bulbasaur) - Black (Bulbasaur)')
plt.xlabel('Black: number of initial Growl')
plt.xticks(list(range(nTacts)))
plt.ylabel('White: number of initial Growl')
plt.yticks(list(range(nTacts)))

figRR = plt.figure()
plot = plt.imshow(compRR, cmap = mpl.cm.Greys, norm = mpl.colors.Normalize(vmin = 0, vmax = 1), origin = 'lower')
cbar = plt.colorbar(plot)
cbar.ax.set_ylabel('Probability of Black winning')
plt.title('Probability of winning \n White (Charmander) - Black (Charmander)')
plt.xlabel('Black: number of initial Growl')
plt.xticks(list(range(nTacts)))
plt.ylabel('White: number of initial Growl')
plt.yticks(list(range(nTacts)))

figBB = plt.figure()
plot = plt.imshow(compBB, cmap = mpl.cm.Greys, norm = mpl.colors.Normalize(vmin = 0, vmax = 1), origin = 'lower')
cbar = plt.colorbar(plot)
cbar.ax.set_ylabel('Probability of Black winning')
plt.title('Probability of winning \n White (Squirtle) - Black (Squirtle)')
plt.xlabel('Black: number of initial Tail Whip')
plt.xticks(list(range(nTacts)))
plt.ylabel('White: number of initial Tail Whip')
plt.yticks(list(range(nTacts)))

figGR = plt.figure()
plot = plt.imshow(compGR, cmap = mpl.cm.Greys, norm = mpl.colors.Normalize(vmin = 0, vmax = 1), origin = 'lower')
cbar = plt.colorbar(plot)
cbar.ax.set_ylabel('Probability of Black winning')
plt.title('Probability of winning \n White (Bulbasaur) - Black (Charmander)')
plt.xlabel('Black: number of initial Growl')
plt.xticks(list(range(nTacts)))
plt.ylabel('White: number of initial Growl')
plt.yticks(list(range(nTacts)))

figRB = plt.figure()
plot = plt.imshow(compRB, cmap = mpl.cm.Greys, norm = mpl.colors.Normalize(vmin = 0, vmax = 1), origin = 'lower')
cbar = plt.colorbar(plot)
cbar.ax.set_ylabel('Probability of Black winning')
plt.title('Probability of winning \n White (Charmander) - Black (Squirtle)')
plt.xlabel('Black: number of initial Tail Whip')
plt.xticks(list(range(nTacts)))
plt.ylabel('White: number of initial Growl')
plt.yticks(list(range(nTacts)))

figBG = plt.figure()
plot = plt.imshow(compBG, cmap = mpl.cm.Greys, norm = mpl.colors.Normalize(vmin = 0, vmax = 1), origin = 'lower')
cbar = plt.colorbar(plot)
cbar.ax.set_ylabel('Probability of Black winning')
plt.title('Probability of winning \n White (Squirtle) - Black (Bulbasaur)')
plt.xlabel('Black: number of initial Growl')
plt.xticks(list(range(nTacts)))
plt.ylabel('White: number of initial Tail Whip')
plt.yticks(list(range(nTacts)))

plt.show()

#