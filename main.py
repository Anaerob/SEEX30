import numpy as np

import Battle
import Constants as c

battle = Battle.Battle()

battle.printSelf()

while not battle.over:
  battle.blue.nextMove = 0
  battle.red.nextMove = 0
  battle.progress()
  battle.printSelf()