import numpy as np
import time

import AI
import Battle
import Constants as c

startTime = time.time()

# Define teams
blueTeam = c.t2
redTeam = c.t1

# Create AI or User
blueAI = AI.AI(blueTeam, redTeam)
redAI = AI.AI(redTeam, blueTeam)

print(blueAI.weights)
print(redAI.weights)

blueFile = open('weightsBlue.txt', 'w')
redFile = open('weightsRed.txt', 'w')

decay = 0.9

for iBattle in range(100000):
  battle = Battle.Battle(blueTeam, redTeam, False)
  
  blueInputs = []
  blueActions = []
  redInputs = []
  redActions = []
  
  while battle.running:
    blueInputs.append(battle.getInput(c.blue))
    action = blueAI.qApprox(blueInputs[battle.round])
    blueActions.append(action[1])
    battle.blue.setNextAction(action)
    
    redInputs.append(battle.getInput(c.red))
    action = redAI.qApprox(redInputs[battle.round])
    redActions.append(action[1])
    battle.red.setNextAction(action)
    
    battle.progress()
  
  for iRound in range(battle.round):
    blueAI.train(blueInputs[battle.round - iRound - 1], blueActions[battle.round - iRound - 1], ((battle.winner + 1) % 2) * (decay ** iRound))
    redAI.train(redInputs[battle.round - iRound - 1], redActions[battle.round - iRound - 1], (battle.winner) * (decay ** iRound))

print(blueAI.weights)
print(redAI.weights)

blueFile.write(str(blueAI.weights))
redFile.write(str(redAI.weights))

battle = Battle.Battle(blueTeam, redTeam, True)

while battle.running:
  action = blueAI.qApprox(battle.getInput(c.blue))
  battle.blue.setNextAction(action)
  
  action = redAI.qApprox(battle.getInput(c.red))
  battle.red.setNextAction(action)
  
  battle.progress()

blueFile.close()
redFile.close()

print('Runtime: %d seconds' % (time.time() - startTime))
#