import numpy as np
import time

import Battle
import Constants as c

nBattles = 100000

blueTactics = np.arange(8)
redTactics = np.arange(8)

startTime = time.time()

# For each of the three team matchups
for iTeam in range(0, 3):

  # Open a log file and a results file
  if iTeam == 0:
    logFile = open('log1.txt', 'w')
    logFile.write('trainer blue = charmander, trainer red = bulbasaur\n')
    
    resFile = open('results1.txt', 'w')
  elif iTeam == 1:
    logFile = open('log2.txt', 'w')
    logFile.write('trainer blue = squirtle, trainer red = charmander\n')
    
    resFile = open('results2.txt', 'w')
  elif iTeam == 2:
    logFile = open('log3.txt', 'w')
    logFile.write('trainer blue = bulbasaur, trainer red = squirtle\n')
    
    resFile = open('results3.txt', 'w')
  
  resFile.write('np.array([\n')
  
  # For each number of initial weakening moves (double for loop: blue and red)
  for b in np.nditer(blueTactics):
    
    resFile.write('  [')
    for r in np.nditer(redTactics):
      
      # Initialize win counter
      blueWins = 0
      redWins = 0
      
      # Play many battles
      for iBattles in range(0, nBattles):
        
        # Initialize each battle
        battle = Battle.Battle()
        if iTeam == 0:
          battle.blue.setTeam(c.t2)
          battle.red.setTeam(c.t1)
        elif iTeam == 1:
          battle.blue.setTeam(c.t3)
          battle.red.setTeam(c.t2)
        elif iTeam == 2:
          battle.blue.setTeam(c.t1)
          battle.red.setTeam(c.t3)
        
        # Run each battle
        while battle.running:
          if battle.round < b:
            battle.blue.nextMove = 2
          else:
            battle.blue.nextMove = 1
          if battle.round < r:
            battle.red.nextMove = 2
          else:
            battle.red.nextMove = 1
          battle.progress()
        
        # Count the winner
        if battle.winner == 0:
          blueWins += 1
        if battle.winner == 1:
          redWins += 1
        
        # Print some progress notice
        if iBattles % 10000 == 0 and iBattles != 0:
          print('b = ' + str(b) + ', r = ' + str(r) + ', # = ' + str(iBattles))
      
      # Write the log and results, print some progress
      print('b = ' + str(b) + ', r = ' + str(r) + ': Finished')
      logFile.write('b = ' + str(b) + ', r = ' + str(r) + ', blue wins = ' + str(blueWins) + ', red wins = ' + str(redWins) + '\n')
      if r == 7 and b == 7:
        resFile.write(str(redWins) + ']])')
      elif r == 7:
        resFile.write(str(redWins) + '],\n')
      else:
        resFile.write(str(redWins) + ', ')

  # Close the files
  logFile.close()
  resFile.close()

print('Runtime: %d seconds' % (time.time() - startTime))
#