import numpy as np

import Constants as c
import Trainer

class Battle:
  def __init__(self):
    self.blue = Trainer.Trainer('Blue')
    self.blue.setTeam(c.t2)
    self.over = False
    self.red = Trainer.Trainer('Red')
    self.red.setTeam(c.t1)
  
  def progress(self):
    if self.blue.nextMove == -1:
      exit('Blue move not set')
    if self.red.nextMove == -1:
      exit('Red move not set')
    
    # Compare speed
    blueFirst = True
    if self.blue.pokemon[self.blue.currentPokemon].activeStats[4] < self.red.pokemon[self.red.currentPokemon].activeStats[4]:
      blueFirst = False
    elif self.blue.pokemon[self.blue.currentPokemon].activeStats[4] == self.red.pokemon[self.red.currentPokemon].activeStats[4]:
      if np.random.randint(0, 2) == 0: # returns 0 or 1, 50/50
        blueFirst = False
    
    if blueFirst:
      self.useBlueMove()
      self.useRedMove()
    else:
      self.useRedMove()
      self.useBlueMove()
  
  def useBlueMove(self):
    if np.random.randint(0, 256) >= self.blue.pokemon[self.blue.currentPokemon].moves[self.blue.nextMove].stats[1]:
      print('Blue move missed!')
    else:
      damage = self.calculateDamage(
        self.blue.pokemon[self.blue.currentPokemon].level,
        self.blue.pokemon[self.blue.currentPokemon].stats[1],
        self.blue.pokemon[self.blue.currentPokemon].moves[self.blue.nextMove].stats[0],
        self.red.pokemon[self.red.currentPokemon].stats[2])
      self.red.pokemon[self.red.currentPokemon].activeStats[0] = self.red.pokemon[self.red.currentPokemon].activeStats[0] - damage
      print('Blue move did ' + str(damage) + ' damage!')
  
  def useRedMove(self):
    if np.random.randint(0, 256) >= self.red.pokemon[self.red.currentPokemon].moves[self.red.nextMove].stats[1]:
      print('Red move missed!')
    else:
      print(self.red.pokemon[self.red.currentPokemon].level)
      print(self.red.pokemon[self.red.currentPokemon].stats[1])
      print(self.red.pokemon[self.red.currentPokemon].moves[self.red.nextMove].stats[0])
      print(self.blue.pokemon[self.blue.currentPokemon].stats[2])
      damage = self.calculateDamage(
        self.red.pokemon[self.red.currentPokemon].level,
        self.red.pokemon[self.red.currentPokemon].stats[1],
        self.red.pokemon[self.red.currentPokemon].moves[self.red.nextMove].stats[0],
        self.blue.pokemon[self.blue.currentPokemon].stats[2])
      self.blue.pokemon[self.blue.currentPokemon].activeStats[0] = self.blue.pokemon[self.blue.currentPokemon].activeStats[0] - damage
      print('Red move did ' + str(damage) + ' damage!')
  
  def calculateDamage(self, l, a, p, d): # a, n, c, e
    factor1 = 2 + np.floor(2 * l / 5)
    factor2 = p * a
    denominator = 50 * d
    unmodified = 2 + np.floor(factor1 * factor2 / denominator)
    
    rand = np.random.randint(217, 256)
    damage = np.floor(unmodified * rand / 255)
    return damage
  
  def printSelf(self):
    self.blue.printSelf()
    self.red.printSelf()
#