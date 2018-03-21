import numpy as np

import Constants as c
import Load

# Load all hetero weights
weightsGR = Load.loadFloatMatrix('plotGreenRed', 1001, 20)
weightsGB = Load.loadFloatMatrix('plotGreenBlue', 1001, 20)
weightsRG = Load.loadFloatMatrix('plotRedGreen', 1001, 20)
weightsRB = Load.loadFloatMatrix('plotRedBlue', 1001, 20)
weightsBG = Load.loadFloatMatrix('plotBlueGreen', 1001, 20)
weightsBR = Load.loadFloatMatrix('plotBlueRed', 1001, 20)

# Green V Blue doesn't converge until 600:
del weightsGB[:600]

# Smooth all hetero weights
smoothGR = np.sum(weightsGR, axis = 0) / 1001
smoothGB = np.sum(weightsGB, axis = 0) / (1001 - 600)
smoothRG = np.sum(weightsRG, axis = 0) / 1001
smoothRB = np.sum(weightsRB, axis = 0) / 1001
smoothBG = np.sum(weightsBG, axis = 0) / 1001
smoothBR = np.sum(weightsBR, axis = 0) / 1001

# Save to file
fileGR = open('smoothGreenRed.txt', 'w')
fileGB = open('smoothGreenBlue.txt', 'w')
fileRG = open('smoothRedGreen.txt', 'w')
fileRB = open('smoothRedBlue.txt', 'w')
fileBG = open('smoothBlueGreen.txt', 'w')
fileBR = open('smoothBlueRed.txt', 'w')
for i in range(c.nOutputs * c.nInputs):
  fileGR.write(str(smoothGR[i]) + '\n')
  fileGB.write(str(smoothGB[i]) + '\n')
  fileRG.write(str(smoothRG[i]) + '\n')
  fileRB.write(str(smoothRB[i]) + '\n')
  fileBG.write(str(smoothBG[i]) + '\n')
  fileBR.write(str(smoothBR[i]) + '\n')
fileGR.close()
fileGB.close()
fileRG.close()
fileRB.close()
fileBG.close()
fileBR.close()
