import numpy as np
import time

import AI
import Battle
import Constants as c
import User

nBattles = 10

startTime = time.time()

# Create AI or User
blueAI = AI.AI()
redAI = AI.AI()

# Initialize win counter
blueWins = 0
redWins = 0

# Play many battles
for iBattles in range(0, nBattles):
  
  # Initialize each battle
  battle = Battle.Battle()
  battle.blue.setTeam(c.t2)
  battle.red.setTeam(c.t1)

  # Run each battle
  while battle.running:
    switch = 0
    move = blueAI.getMove()
    battle.blue.setNextMove(switch, move)
    move = redAI.getMove()
    battle.red.setNextMove(switch, move)
    battle.progress()
  
  # Count the winner
  if battle.winner == 0:
    blueWins += 1
  if battle.winner == 1:
    redWins += 1
  
  # Print some progress notice
  if True:
    print('# = ' + str(iBattles))

print('Runtime: %d seconds' % (time.time() - startTime))
#