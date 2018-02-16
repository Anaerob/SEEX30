import numpy as np

import Battle
import Constants as c

battle = Battle.Battle()

battle.blue.setTeam(c.t2)
battle.red.setTeam(c.t1)

battle.printSelf()

for i in range(0, 7):
  battle.blue.nextMove = 1
  battle.red.nextMove = 0
  battle.progress()

while battle.running:
  battle.blue.nextMove = 0
  battle.red.nextMove = 0
  battle.progress()
  # battle.printSelf()

battle.printSelf()