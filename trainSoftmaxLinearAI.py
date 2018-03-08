import numpy as np
import time

import Battle
import Constants as c
import SoftmaxLinearAI

# Training variables
nTrain = 10000000
decay = 0.9
temperature = 0.1

# Start runtime timer
startTime = time.time()

# Define teams
greenTeam = c.team1
redTeam = c.team2
blueTeam = c.team3

# Create AI
# greenAI = SoftmaxLinearAI.AI()
redAI = SoftmaxLinearAI.AI()
blueAI = SoftmaxLinearAI.AI()

print('Start: [Battles: %d, Decay: %f, Temperature: %f]' % (nTrain, decay, temperature))

progressFile = open('progress.txt', 'w')

prevWeights = redAI.weights.copy()

for iTrain in range(nTrain):
  battle = Battle.Battle(redTeam, redTeam, False)
  
  whiteInputs = []
  whiteActions = []
  blackInputs = []
  blackActions = []
  
  # Run the battle until it's over
  while battle.running:
    whiteInputs.append(battle.getInput(c.amWhite))
    whiteActions.append(redAI.getAction(whiteInputs[battle.round], temperature))
    battle.white.setNextAction(whiteActions[battle.round])
    
    blackInputs.append(battle.getInput(c.amBlack))
    blackActions.append(redAI.getAction(blackInputs[battle.round], temperature))
    battle.black.setNextAction(blackActions[battle.round])
    
    battle.progress()
  
  # Train the AI based on the results
  for iRound in range(battle.round):
    if battle.winner == 0:
      redAI.train(whiteInputs[battle.round - iRound - 1], whiteActions[battle.round - iRound - 1], 1 * (decay ** iRound))
      redAI.train(blackInputs[battle.round - iRound - 1], blackActions[battle.round - iRound - 1], -1 * (decay ** iRound))
    else:
      redAI.train(whiteInputs[battle.round - iRound - 1], whiteActions[battle.round - iRound - 1], -1 * (decay ** iRound))
      redAI.train(blackInputs[battle.round - iRound - 1], blackActions[battle.round - iRound - 1], 1 * (decay ** iRound))
  
  # Print progress notice
  if iTrain % int(nTrain / 100) == 0 and iTrain != 0:
    print('Trained ' + str(int(100 * iTrain / nTrain)) + '%')
    progressFile.write('Total delta: ' + str(np.sum(np.absolute(redAI.weights - prevWeights))) + '\n')
    progressFile.write('Weights = ' + str(redAI.weights) + '\n\n')
    prevWeights = redAI.weights.copy()

print('Trained 100%')

# Save weights to file
redFile = open('weightsRed.txt', 'w')
for i in range(c.nOutputs):
  for j in range(c.nInputs):
    redFile.write(str(redAI.weights[i][j]) + '\n')
redFile.close()

progressFile.close()

# make minutes if > 60s, hours if > 60min
print('Runtime: %d seconds' % (time.time() - startTime))
#