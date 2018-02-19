import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

Z1 = np.array([
  [12660, 52874, 55534, 31513, 75509, 65458, 49793, 31482],
  [2088, 16364, 15560, 8220, 71337, 62327, 46999, 28529],
  [1416, 27669, 21911, 6960, 83685, 80357, 74110, 64639],
  [5380, 39868, 54253, 20518, 85376, 85971, 83401, 75821],
  [905, 2954, 2377, 1144, 31992, 23005, 16492, 11376],
  [1558, 4770, 2232, 826, 44251, 32778, 22403, 15496],
  [3352, 7826, 4876, 1490, 56985, 46353, 33697, 22644],
  [6217, 12436, 9931, 2674, 66201, 59521, 47840, 33575]])
Z2 = np.array([
  [53038, 93179, 94304, 82041, 97735, 96788, 93195, 88120],
  [17687, 53049, 48955, 64680, 58561, 56385, 56492, 51361],
  [29030, 40612, 61983, 48859, 64193, 52802, 29300, 11768],
  [34750, 44561, 40764, 62149, 51959, 73587, 60124, 32338],
  [49142, 62005, 38521, 38816, 56083, 62810, 60473, 45660],
  [98331, 85930, 47647, 42361, 30624, 65686, 45741, 21033],
  [99969, 99622, 98430, 93305, 50728, 78757, 86503, 45450],
  [100000, 99996, 99983, 99840, 98603, 85381, 98981, 87134]])
Z3 = np.array([
  [57459, 96188, 89875, 87882, 72987, 45674, 14687, 3166],
  [10509, 57396, 74602, 78823, 58822, 44517, 19162, 4636],
  [25796, 73192, 49989, 74154, 79143, 69253, 44772, 12805],
  [45499, 39855, 72712, 50046, 74196, 70868, 48018, 14524],
  [5848, 58368, 39529, 72318, 45159, 62973, 73401, 40061],
  [9078, 31638, 63776, 50688, 31109, 45676, 36610, 24851],
  [15816, 21538, 84988, 65990, 31432, 58058, 46919, 16529],
  [25849, 31008, 95171, 86864, 55997, 70928, 81011, 47108]])

Z1 = Z1 / 100000
Z2 = Z2 / 100000
Z3 = Z3 / 100000

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

"""
fig, ax = plt.subplots()

cmap = mpl.cm.cool
norm = mpl.colors.Normalize(vmin = 5, vmax = 10)

cb1 = mpl.colorbar.ColorbarBase(ax, cmap = cmap, norm = norm, orientation = 'horizontal')

cb1.set_label('Some units')
fig.show()
"""