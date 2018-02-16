import numpy as np

import Constants as c
import Trainer

class Battle:
  def __init__(self):
    self.blue = Trainer.Trainer('Blue')
    self.red = Trainer.Trainer('Red')
    self.running = True
  
  def progress(self):
    # Check if both players have set their moves
    if self.blue.nextMove == -1:
      exit('Blue move not set')
    if self.red.nextMove == -1:
      exit('Red move not set')
    
    # Check if the chosen move has any pp remaining
    if self.blue.pokemon[self.blue.currentPokemon].moves[self.blue.nextMove].activeStats[2] <= 0:
      exit('Blue chose move with no PP remaining!')
    if self.red.pokemon[self.red.currentPokemon].moves[self.red.nextMove].activeStats[2] <= 0:
      exit('Red chose move with no PP remaining!')
    
    # Determine who strikes first based on speed (coin toss if speed is equal)
    blueFirst = True
    if self.blue.pokemon[self.blue.currentPokemon].activeStats[4] < self.red.pokemon[self.red.currentPokemon].activeStats[4]:
      blueFirst = False
    elif self.blue.pokemon[self.blue.currentPokemon].activeStats[4] == self.red.pokemon[self.red.currentPokemon].activeStats[4]:
      if np.random.randint(0, 2) == 0: # returns 0 or 1, 50/50
        blueFirst = False
    
    # Use moves in order, abort if first move ends battle
    if blueFirst:
      self.useBlueMove()
      self.blue.nextMove = -1
      if self.red.pokemon[self.red.currentPokemon].activeStats[0] > 0:
        self.useRedMove()
        self.red.nextMove = -1
      else:
        self.running = False
    else:
      self.useRedMove()
      self.red.nextMove = -1
      if self.blue.pokemon[self.blue.currentPokemon].activeStats[0] > 0:
        self.useBlueMove()
        self.blue.nextMove = -1
      else:
        self.running = False
    
    # Check if either pokemon fainted
    if self.blue.pokemon[self.blue.currentPokemon].activeStats[0] <= 0 or self.red.pokemon[self.red.currentPokemon].activeStats[0] <= 0:
      self.running = False
  
  def useBlueMove(self):
    # Deduct PP
    self.blue.pokemon[self.blue.currentPokemon].moves[self.blue.nextMove].activeStats[2] -= 1
    
    # Check if move misses
    if np.random.randint(0, 256) >= self.blue.pokemon[self.blue.currentPokemon].moves[self.blue.nextMove].stats[1]:
      print('Blue move missed!')
    else:
      # If the move is a damaging move, calculate and deduct damage
      if self.blue.pokemon[self.blue.currentPokemon].moves[self.blue.nextMove].stats[0] != 0:
        damage = self.calculateDamage(
          self.blue.pokemon[self.blue.currentPokemon].level,
          np.floor(
            c.statModifiers[self.blue.pokemon[self.blue.currentPokemon].statModifiers[1]] *
            self.blue.pokemon[self.blue.currentPokemon].stats[1] / 100),
          self.blue.pokemon[self.blue.currentPokemon].moves[self.blue.nextMove].stats[0],
          np.floor(
            c.statModifiers[self.red.pokemon[self.red.currentPokemon].statModifiers[2]] *
            self.red.pokemon[self.red.currentPokemon].stats[2] / 100))
        self.red.pokemon[self.red.currentPokemon].activeStats[0] = self.red.pokemon[self.red.currentPokemon].activeStats[0] - damage
        print('Blue move did ' + str(damage) + ' damage!')
      
      # If the move is a stat modifying move, modify the stat
      if self.blue.pokemon[self.blue.currentPokemon].moves[self.blue.nextMove].modifiers[0] != 0:
        if self.blue.pokemon[self.blue.currentPokemon].moves[self.blue.nextMove].modifiers[1] != 0:
          self.red.pokemon[self.red.currentPokemon].statModifiers[1] += self.blue.pokemon[self.blue.currentPokemon].moves[self.blue.nextMove].modifiers[1]
          print('Blue move reduced Reds attack!')
        if self.blue.pokemon[self.blue.currentPokemon].moves[self.blue.nextMove].modifiers[2] != 0:
          self.red.pokemon[self.red.currentPokemon].statModifiers[2] += self.blue.pokemon[self.blue.currentPokemon].moves[self.blue.nextMove].modifiers[2]
          print('Blue move reduced Reds defense!')
  
  def useRedMove(self):
    # Deduct PP
    self.red.pokemon[self.red.currentPokemon].moves[self.red.nextMove].activeStats[2] -= 1
    
    # Check if move misses
    if np.random.randint(0, 256) >= self.red.pokemon[self.red.currentPokemon].moves[self.red.nextMove].stats[1]:
      print('Red move missed!')
    else:
      # If the move is a damaging move, calculate and deduct damage
      if self.red.pokemon[self.red.currentPokemon].moves[self.red.nextMove].stats[0] != 0:
        damage = self.calculateDamage(
          self.red.pokemon[self.red.currentPokemon].level,
          np.floor(
            c.statModifiers[self.red.pokemon[self.red.currentPokemon].statModifiers[1]] *
            self.red.pokemon[self.red.currentPokemon].stats[1] / 100),
          self.red.pokemon[self.red.currentPokemon].moves[self.red.nextMove].stats[0],
          np.floor(
            c.statModifiers[self.blue.pokemon[self.blue.currentPokemon].statModifiers[2]] *
            self.blue.pokemon[self.blue.currentPokemon].stats[2] / 100))
        self.blue.pokemon[self.blue.currentPokemon].activeStats[0] = self.blue.pokemon[self.blue.currentPokemon].activeStats[0] - damage
        print('Red move did ' + str(damage) + ' damage!')
      
      # If the move is a stat modifying move, modify the stat
      if self.red.pokemon[self.red.currentPokemon].moves[self.red.nextMove].modifiers[0] != 0:
        if self.red.pokemon[self.red.currentPokemon].moves[self.red.nextMove].modifiers[1] != 0:
          self.blue.pokemon[self.blue.currentPokemon].statModifiers[1] += self.red.pokemon[self.red.currentPokemon].moves[self.red.nextMove].modifiers[1]
          print('Red move reduced Blues attack!')
        if self.red.pokemon[self.red.currentPokemon].moves[self.red.nextMove].modifiers[2] != 0:
          self.blue.pokemon[self.blue.currentPokemon].statModifiers[2] += self.red.pokemon[self.red.currentPokemon].moves[self.red.nextMove].modifiers[2]
          print('Red move reduced Blues defense!')
  
  def calculateDamage(self, l, a, p, d): # a, n, c, e
    # Calculate raw damage
    factor1 = 2 + np.floor(2 * l / 5)
    factor2 = p * a
    denominator = 50 * d
    unmodified = 2 + np.floor(factor1 * factor2 / denominator)
    
    # Apply random modifier
    rand = np.random.randint(217, 256)
    damage = np.floor(unmodified * rand / 255)
    
    return damage
  
  def printSelf(self):
    print()
    self.blue.printSelf()
    print()
    self.red.printSelf()
    print()
#