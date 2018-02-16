import numpy as np

import Battle
import Constants as c

nBattles = 100000

blueTactics = np.arange(7)
redTactics = np.arange(7)

file = open('simulation.txt', 'w')

for b in np.nditer(blueTactics):
  for r in np.nditer(redTactics):
    
    blueWins = 0
    redWins = 0
    for iBattles in range(0, nBattles):
      
      battle = Battle.Battle()
      battle.blue.setTeam(c.t2)
      battle.red.setTeam(c.t1)
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
      
      if battle.winner == 0:
        blueWins += 1
      if battle.winner == 1:
        redWins += 1
      
      if iBattles % 1000 == 0 and iBattles != 0:
        print('bt = ' + str(b) + ', rt = ' + str(r) + ', # ' + str(iBattles))
    
    file.write('bt = ' + str(b) + ', rt = ' + str(r) + ', bw = ' + str(blueWins) + ', rw = ' + str(redWins) + '\n')

file.close()
#