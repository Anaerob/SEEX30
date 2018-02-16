import numpy as np

import Battle
import Constants as c

battle = Battle.Battle()

battle.trainers[0].setTeam(c.t2)
battle.trainers[1].setTeam(c.t1)

battle.printSelf()

for i in range(0, 7):
  battle.blue.nextMove = 2
  battle.red.nextMove = 1
  battle.progress()

while battle.running:
  battle.blue.nextMove = 1
  battle.red.nextMove = 1
  battle.progress()
  # battle.printSelf()

battle.printSelf()