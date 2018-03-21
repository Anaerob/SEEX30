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

hardcoded = open('hardcoded.txt', 'w')

WGG = np.sum(compGG, axis = 1) / nTacts
hardcoded.write('green v green: ' + str(WGG.tolist().index(np.min(WGG))) + '\n')
# BGG = np.sum(compGG, axis = 0) / nTacts
# print('green v green black: ' + str(BGG.tolist().index(np.max(BGG))))

WRR = np.sum(compRR, axis = 1) / nTacts
hardcoded.write('red v red: ' + str(WRR.tolist().index(np.min(WRR))) + '\n')
# BRR = np.sum(compRR, axis = 0) / nTacts
# print('red v red black: ' + str(BRR.tolist().index(np.max(BRR))))

WBB = np.sum(compBB, axis = 1) / nTacts
hardcoded.write('blue v blue: ' + str(WBB.tolist().index(np.min(WBB))) + '\n')
# BBB = np.sum(compBB, axis = 0) / nTacts
# print('blue v blue black: ' + str(BBB.tolist().index(np.max(BBB))))

WGR = np.sum(compGR, axis = 1) / nTacts
hardcoded.write('green v red: ' + str(WGR.tolist().index(np.min(WGR))) + '\n')
BGR = np.sum(compGR, axis = 0) / nTacts
hardcoded.write('red v green: ' + str(BGR.tolist().index(np.max(BGR))) + '\n')

WRB = np.sum(compRB, axis = 1) / nTacts
hardcoded.write('red v blue: ' + str(WRB.tolist().index(np.min(WRB))) + '\n')
BRB = np.sum(compRB, axis = 0) / nTacts
hardcoded.write('blue v red: ' + str(BRB.tolist().index(np.max(BRB))) + '\n')

WBG = np.sum(compBG, axis = 1) / nTacts
hardcoded.write('blue v green: ' + str(WBG.tolist().index(np.min(WBG))) + '\n')
BBG = np.sum(compBG, axis = 0) / nTacts
hardcoded.write('green v blue: ' + str(BBG.tolist().index(np.max(BBG))) + '\n')

"""

# All white growl = 0 probabilitites
print(compGG[0])

# Average probability for white growl = 0
print(np.sum(compGG[0]) / nTacts)

# Average probability for all white growl #
avgProbWGG = np.sum(compGG, axis = 1) / nTacts
print(avgProbWGG)

# Pick the minimum, as it's the probability of black winning
print(np.min(avgProbWGG))

# The index of the minimum = best pick for white number of growls
print(avgProbWGG.tolist().index(np.min(avgProbWGG)))

# axis = 1 summerar en rad i taget

""

# Average probability for all black growl #
avgProbBGG = np.sum(compGG, axis = 0) / nTacts
print(avgProbBGG)

# Pick the maximum, as it's the probability of black winning
print(np.max(avgProbBGG))

# The index of the maximum = best pick for black number of growls
print(avgProbBGG.tolist().index(np.max(avgProbBGG)))

"""

