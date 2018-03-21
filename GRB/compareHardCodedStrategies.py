import numpy as np
import time

import Battle
import Constants as c

# Training variables
nBattles = 100000
nTacts = 7

# Start runtime timer
startTime = time.time()

# Construct tactics matrix
# Both Tackle and Scratch has 35 PP
allDamage = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
tacts = [allDamage.copy()]
for i in range(nTacts - 1):
  allDamage.insert(0, 2)
  tacts.append(allDamage.copy())

# Start multi-AI training
print('Start comparison! [Number of strategy combos: %d, Total number of battles: %d]' % ((nTacts ** 2), (6 * nBattles * nTacts ** 2)))

### ------------- ###
### GREEN V GREEN ###
### ------------- ###

print('Start green V green! [Battles per strategy combo: %d]' % (nBattles))

compGreenGreen = open('compGreenGreen.txt', 'w')

for iTacts in range(nTacts):
  for jTacts in range(nTacts):
    # Print progress notice
    if not(iTacts == 0 and jTacts == 0):
      print('Battled ' + str(int(100 * (iTacts * nTacts + jTacts) / (nTacts ** 2))) + '%')
    
    # Initialize win counter
    blackWins = 0
    
    # Play many battles
    for iBattle in range(nBattles):
      # Initialize each battle
      battle = Battle.Battle(c.team1, c.team1, False)
      
      # Run each battle
      while battle.running:
        battle.trainers[0].setNextAction(tacts[iTacts][battle.round])
        battle.trainers[1].setNextAction(tacts[jTacts][battle.round])
        battle.progress()
      
      # Count the winner
      blackWins += battle.winner
    
    # Write the results to file
    compGreenGreen.write(str(blackWins / nBattles) + '\n')
compGreenGreen.close()

### --------- ###
### RED V RED ###
### --------- ###

print('Start red V red! [Battles per strategy combo: %d]' % (nBattles))

compRedRed = open('compRedRed.txt', 'w')

for iTacts in range(nTacts):
  for jTacts in range(nTacts):
    # Print progress notice
    if not(iTacts == 0 and jTacts == 0):
      print('Battled ' + str(int(100 * (iTacts * nTacts + jTacts) / (nTacts ** 2))) + '%')
    
    # Initialize win counter
    blackWins = 0
    
    # Play many battles
    for iBattle in range(nBattles):
      # Initialize each battle
      battle = Battle.Battle(c.team2, c.team2, False)
      
      # Run each battle
      while battle.running:
        battle.trainers[0].setNextAction(tacts[iTacts][battle.round])
        battle.trainers[1].setNextAction(tacts[jTacts][battle.round])
        battle.progress()
      
      # Count the winner
      blackWins += battle.winner
    
    # Write the results to file
    compRedRed.write(str(blackWins / nBattles) + '\n')
compRedRed.close()

### ----------- ###
### BLUE V BLUE ###
### ----------- ###

print('Start blue V blue! [Battles per strategy combo: %d]' % (nBattles))

compBlueBlue = open('compBlueBlue.txt', 'w')

for iTacts in range(nTacts):
  for jTacts in range(nTacts):
    # Print progress notice
    if not(iTacts == 0 and jTacts == 0):
      print('Battled ' + str(int(100 * (iTacts * nTacts + jTacts) / (nTacts ** 2))) + '%')
    
    # Initialize win counter
    blackWins = 0
    
    # Play many battles
    for iBattle in range(nBattles):
      # Initialize each battle
      battle = Battle.Battle(c.team3, c.team3, False)
      
      # Run each battle
      while battle.running:
        battle.trainers[0].setNextAction(tacts[iTacts][battle.round])
        battle.trainers[1].setNextAction(tacts[jTacts][battle.round])
        battle.progress()
      
      # Count the winner
      blackWins += battle.winner
    
    # Write the results to file
    compBlueBlue.write(str(blackWins / nBattles) + '\n')
compBlueBlue.close()

### ----------- ###
### GREEN V RED ###
### RED V GREEN ###
### ----------- ###

print('Start green V red! [Battles per strategy combo: %d]' % (nBattles))

compGreenRed = open('compGreenRed.txt', 'w')

for iTacts in range(nTacts):
  for jTacts in range(nTacts):
    # Print progress notice
    if not(iTacts == 0 and jTacts == 0):
      print('Battled ' + str(int(100 * (iTacts * nTacts + jTacts) / (nTacts ** 2))) + '%')
    
    # Initialize win counter
    blackWins = 0
    
    # Play many battles
    for iBattle in range(nBattles):
      # Initialize each battle
      battle = Battle.Battle(c.team1, c.team2, False)
      
      # Run each battle
      while battle.running:
        battle.trainers[0].setNextAction(tacts[iTacts][battle.round])
        battle.trainers[1].setNextAction(tacts[jTacts][battle.round])
        battle.progress()
      
      # Count the winner
      blackWins += battle.winner
    
    # Write the results to file
    compGreenRed.write(str(blackWins / nBattles) + '\n')
compGreenRed.close()

### ---------- ###
### RED V BLUE ###
### BLUE V RED ###
### ---------- ###

print('Start red V blue! [Battles per strategy combo: %d]' % (nBattles))

compRedBlue = open('compRedBlue.txt', 'w')

for iTacts in range(nTacts):
  for jTacts in range(nTacts):
    # Print progress notice
    if not(iTacts == 0 and jTacts == 0):
      print('Battled ' + str(int(100 * (iTacts * nTacts + jTacts) / (nTacts ** 2))) + '%')
    
    # Initialize win counter
    blackWins = 0
    
    # Play many battles
    for iBattle in range(nBattles):
      # Initialize each battle
      battle = Battle.Battle(c.team2, c.team3, False)
      
      # Run each battle
      while battle.running:
        battle.trainers[0].setNextAction(tacts[iTacts][battle.round])
        battle.trainers[1].setNextAction(tacts[jTacts][battle.round])
        battle.progress()
      
      # Count the winner
      blackWins += battle.winner
    
    # Write the results to file
    compRedBlue.write(str(blackWins / nBattles) + '\n')
compRedBlue.close()

### ------------ ###
### BLUE V GREEN ###
### GREEN V BLUE ###
### ------------ ###

print('Start blue V green! [Battles per strategy combo: %d]' % (nBattles))

compBlueGreen = open('compBlueGreen.txt', 'w')

for iTacts in range(nTacts):
  for jTacts in range(nTacts):
    # Print progress notice
    if not(iTacts == 0 and jTacts == 0):
      print('Battled ' + str(int(100 * (iTacts * nTacts + jTacts) / (nTacts ** 2))) + '%')
    
    # Initialize win counter
    blackWins = 0
    
    # Play many battles
    for iBattle in range(nBattles):
      # Initialize each battle
      battle = Battle.Battle(c.team3, c.team1, False)
      
      # Run each battle
      while battle.running:
        battle.trainers[0].setNextAction(tacts[iTacts][battle.round])
        battle.trainers[1].setNextAction(tacts[jTacts][battle.round])
        battle.progress()
      
      # Count the winner
      blackWins += battle.winner
    
    # Write the results to file
    compBlueGreen.write(str(blackWins / nBattles) + '\n')
compBlueGreen.close()

# Print runtime
if time.time() - startTime < 60:
  print('Runtime: %d seconds' % (time.time() - startTime))
elif time.time() - startTime > 60 and time.time() - startTime < 3600:
  print('Runtime: %d minutes and %d seconds' % ((time.time() - startTime) / 60, (time.time() - startTime) % 60))
else:
  print('Runtime: %d hours, %d minutes and %d seconds' % ((time.time() - startTime) / 3600, ((time.time() - startTime) % 3600) / 60, (time.time() - startTime) % 60))
#