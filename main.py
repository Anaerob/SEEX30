import numpy as np
import time

import AI
import Battle
import Constants as c
import User

nBattles = 1

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
  teams = []
  teams.append(c.t2)
  teams.append(c.t1)
  battle = Battle.Battle(teams) # TODO: TEAMS
  
  # Run each battle
  while battle.running:
    switch = 0
    move = blueAI.getMove()
    battle.blue.setNextMove(switch, move)
    move = redAI.getMove()
    battle.red.setNextMove(switch, move)
    battle.progress()
    battle.printSelf()
    
    if battle.round == 5:
      battleState = battle.getState()
  
  # Count the winner
  if battle.winner == 0:
    blueWins += 1
  if battle.winner == 1:
    redWins += 1
  
  # Print some progress notice
  if True:
    print('# = ' + str(iBattles))

teams = []
teams.append(c.t2)
teams.append(c.t1)
battle2 = Battle.Battle(teams, battleState)

while battle2.running:
  switch = 0
  move = blueAI.getMove()
  battle2.blue.setNextMove(switch, move)
  move = redAI.getMove()
  battle2.red.setNextMove(switch, move)
  battle2.progress()
  battle2.printSelf()

# Count the winner
if battle2.winner == 0:
  blueWins += 1
if battle2.winner == 1:
  redWins += 1

# Print some progress notice
if True:
  print('# = ' + str(123))

print('Runtime: %d seconds' % (time.time() - startTime))
#