import numpy as np

import Battle
import Constants as c

battle = Battle.Battle()

battle.trainers[0].setTeam(c.t2)
battle.trainers[1].setTeam(c.t1)

battle.printSelf()

while battle.running:
  battle.blue.nextMove = 2
  battle.red.nextMove = 1
  battle.progress()
  # battle.printSelf()

battle.printSelf()