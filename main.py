import numpy as np
import time

import AI
import Battle
import Constants as c
import User

nBattles = 1

startTime = time.time()

# Define teams
blueTeam = c.t2
redTeam = c.t1

# Create AI or User
blueAI = AI.AI(blueTeam, redTeam)
redAI = AI.AI(redTeam, blueTeam)

# Initialize win counter
blueWins = 0
redWins = 0


# Play many battles
for iBattles in range(0, nBattles):
  
  # Initialize each battle
  battle = Battle.Battle(blueTeam, redTeam, True)
  battle.printSelf()
  # Run each battle
  while battle.running:
    action = blueAI.getAction(battle.getState(c.blue))
    battle.blue.setNextAction(action)
    action = redAI.getAction(battle.getState(c.red))
    battle.red.setNextAction(action)
    battle.progress()
    battle.printSelf()
  
  # Count the winner
  if battle.winner == 0:
    blueWins += 1
    print('Trainer Blue wins!')
  if battle.winner == 1:
    redWins += 1
    print('Trainer Red wins!')

print('Runtime: %d seconds' % (time.time() - startTime))
#