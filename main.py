import Battle
import Constants as c

battle = Battle.Battle()

if not battle.setRed(c.t1):
  exit("Red team wrong size")

if not battle.setBlue(c.t2):
  exit("Blue team wrong size")

# while not battle.over:
