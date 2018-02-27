import numpy as np
import time

import AI
import Battle
import Constants as c
import User

nBattles = 1

startTime = time.time()

# Create AI or User
teams = [c.t2, c.t1]
blueAI = AI.AI(teams[0], teams[1])
redAI = AI.AI(teams[1], teams[0])

# Initialize win counter
blueWins = 0
redWins = 0


# Play many battles
for iBattles in range(0, nBattles):
  
  # Initialize each battle
  battle = Battle.Battle(teams, True)
  battle.printSelf()
  # Run each battle
  while battle.running:
    move = blueAI.getMove(battle.getState(False))
    battle.blue.setNextMove(move[0], move[1])
    move = redAI.getMove(battle.getState(True))
    battle.red.setNextMove(move[0], move[1])
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