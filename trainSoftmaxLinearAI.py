import numpy as np
import time

import Battle
import Constants as c
import SoftmaxLinearAI

# Training variables
nTrain = 1000000
decay = 0.9
learningRate = 0.1
temperature = 0.1

# Start runtime timer
startTime = time.time()

# Define teams
redTeam = c.team2

# Create AI
redAI = SoftmaxLinearAI.AI(learningRate, temperature)

# Prepare for plotting weights
nPlotPoints = 1000
weightPlot = open('weightPlot.txt', 'w')

print('Start: [Battles: %d, Decay: %f, Learning rate: %f, Temperature: %f]' % (nTrain, decay, learningRate, temperature))

for iTrain in range(nTrain):
  
  # Save weights for the plot
  if iTrain % int(nTrain / nPlotPoints) == 0:
    for i in range(c.nOutputs):
      for j in range(c.nInputs):
        weightPlot.write(str(redAI.weights[i][j]) + '\n')
  
  battle = Battle.Battle(redTeam, redTeam, False)
  
  whiteFeatures = []
  whiteActions = []
  blackFeatures = []
  blackActions = []
  
  # Run the battle until it's over
  while battle.running:
    whiteFeatures.append(battle.getFeatures(c.amWhite))
    whiteActions.append(redAI.getAction(whiteFeatures[battle.round], temperature))
    battle.trainers[0].setNextAction(whiteActions[battle.round])
    
    #print('Features: ' + str(whiteFeatures[battle.round]))
    #print('Action: ' + str(whiteActions[battle.round]))
    
    blackFeatures.append(battle.getFeatures(c.amBlack))
    blackActions.append(redAI.getAction(blackFeatures[battle.round], temperature))
    battle.trainers[1].setNextAction(blackActions[battle.round])
    
    battle.progress()
  
  # Train the AI based on the results
  for iRound in range(battle.round):
    if battle.winner == 0:
      redAI.train(whiteFeatures[battle.round - iRound - 1], whiteActions[battle.round - iRound - 1], 1 * (decay ** iRound))
      redAI.train(blackFeatures[battle.round - iRound - 1], blackActions[battle.round - iRound - 1], -1 * (decay ** iRound))
    else:
      redAI.train(whiteFeatures[battle.round - iRound - 1], whiteActions[battle.round - iRound - 1], -1 * (decay ** iRound))
      redAI.train(blackFeatures[battle.round - iRound - 1], blackActions[battle.round - iRound - 1], 1 * (decay ** iRound))
  
  # Print progress notice every percent
  if iTrain % int(nTrain / 100) == 0 and iTrain != 0:
    print('Trained ' + str(int(100 * iTrain / nTrain)) + '%')

# Print final notice
print('Trained 100%')

# Save final weights for the plot
for i in range(c.nOutputs):
  for j in range(c.nInputs):
    weightPlot.write(str(redAI.weights[i][j]) + '\n')
weightPlot.close()

# Save trained weights to file
redFile = open('weightsRed.txt', 'w')
for i in range(c.nOutputs):
  for j in range(c.nInputs):
    redFile.write(str(redAI.weights[i][j]) + '\n')
redFile.close()

# Print runtime
if time.time() - startTime < 60:
  print('Runtime: %d seconds' % (time.time() - startTime))
elif time.time() - startTime > 60 and time.time() - startTime < 3600:
  print('Runtime: %d minutes and %d seconds' % ((time.time() - startTime) / 60, (time.time() - startTime) % 60))
else:
  print('Runtime: %d hours, %d minutes and %d seconds' % ((time.time() - startTime) / 3600, ((time.time() - startTime) % 3600) / 60, (time.time() - startTime) % 60))
#