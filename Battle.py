import numpy as np

import Constants as c
import Trainer

class Battle:
  def __init__(self):
    # Initialize both trainers Red and Blue
    self.blue = Trainer.Trainer('Blue')
    self.red = Trainer.Trainer('Red')
    
    # Put both trainers in a list to avoid double code
    self.trainers = []
    self.trainers.append(self.blue)
    self.trainers.append(self.red)
    self.running = True
  
  def progress(self):
    # For both trainers
    for i in range(0, 2):
      # Check if an action has been chosen
      if self.trainers[i].nextMove == -1:
        exit('Trainer ' + self.trainers[i].name + ' move not set!')
      
      # Check if the chosen move has any pp remaining
      elif self.trainers[i].pokemon[self.trainers[i].currentPokemon].moves[self.trainers[i].nextMove].activeStats[2] <= 0:
        exit('Trainer ' + self.trainers[i].name + ' chose move with no PP remaining!')
    
    # Determine who strikes first based on speed (coin toss if speed is equal)
    firstTrainer = 0
    if self.trainers[0].pokemon[self.trainers[0].currentPokemon].activeStats[4] < self.trainers[1].pokemon[self.trainers[1].currentPokemon].activeStats[4]:
      firstTrainer = 1
    elif self.trainers[0].pokemon[self.trainers[0].currentPokemon].activeStats[4] == self.trainers[1].pokemon[self.trainers[1].currentPokemon].activeStats[4]:
      if np.random.randint(0, 2) == 0: # returns 0 or 1, 50/50
        firstTrainer = 1
    
    # Use moves in order, only use second move if Pokemon still active
    self.useMove(firstTrainer)
    self.trainers[firstTrainer].nextMove = -1
    if self.trainers[(firstTrainer + 1) % 2].pokemon[self.trainers[(firstTrainer + 1) % 2].currentPokemon].activeStats[0] > 0:
      self.useMove((firstTrainer + 1) % 2)
      self.trainers[(firstTrainer + 1) % 2].nextMove = -1
    
    # Check if either pokemon fainted
    for i in range(0, 2):
      if self.trainers[i].pokemon[self.trainers[i].currentPokemon].activeStats[0] <= 0:
        self.running = False
  
  def useMove(self, trainer):
    # Deduct PP
    self.trainers[trainer].pokemon[self.trainers[trainer].currentPokemon].moves[self.trainers[trainer].nextMove].activeStats[2] -= 1
    
    # Check if move misses (correctly implements the 1/256 miss bug)
    if np.random.randint(0, 256) >= self.trainers[trainer].pokemon[self.trainers[trainer].currentPokemon].moves[self.trainers[trainer].nextMove].stats[1]:
      print(
        self.trainers[trainer].name + '\'s ' +
        self.trainers[trainer].pokemon[self.trainers[trainer].currentPokemon].name + '\'s ' +
        self.trainers[trainer].pokemon[self.trainers[trainer].currentPokemon].moves[self.trainers[trainer].nextMove].name + ' missed!')
    else:
      # If the move is a damaging move, calculate and deduct damage
      if self.trainers[trainer].pokemon[self.trainers[trainer].currentPokemon].moves[self.trainers[trainer].nextMove].stats[0] != 0:
        damage = self.calculateDamage(
          self.trainers[trainer].pokemon[self.trainers[trainer].currentPokemon].level,
          np.floor(
            c.statModifiers[self.trainers[trainer].pokemon[self.trainers[trainer].currentPokemon].statModifiers[1]] *
            self.trainers[trainer].pokemon[self.trainers[trainer].currentPokemon].stats[1] / 100),
          self.trainers[trainer].pokemon[self.trainers[trainer].currentPokemon].moves[self.trainers[trainer].nextMove].stats[0],
          np.floor(
            c.statModifiers[self.trainers[(trainer + 1) % 2].pokemon[self.trainers[(trainer + 1) % 2].currentPokemon].statModifiers[2]] *
            self.trainers[(trainer + 1) % 2].pokemon[self.trainers[(trainer + 1) % 2].currentPokemon].stats[2] / 100))
        self.trainers[(trainer + 1) % 2].pokemon[self.trainers[(trainer + 1) % 2].currentPokemon].activeStats[0] -= damage
        print(
          self.trainers[trainer].name + '\'s ' +
          self.trainers[trainer].pokemon[self.trainers[trainer].currentPokemon].name + '\'s ' +
          self.trainers[trainer].pokemon[self.trainers[trainer].currentPokemon].moves[self.trainers[trainer].nextMove].name +
          ' did ' + str(damage) + ' damage!')
      
      # If the move is a stat modifying move, modify the stat
      if self.trainers[trainer].pokemon[self.trainers[trainer].currentPokemon].moves[self.trainers[trainer].nextMove].modifiers[0] != 0:
        # Modify the attack stat
        if self.trainers[trainer].pokemon[self.trainers[trainer].currentPokemon].moves[self.trainers[trainer].nextMove].modifiers[1] != 0:
          self.trainers[(trainer + 1) % 2].pokemon[self.trainers[(trainer + 1) % 2].currentPokemon].statModifiers[1] += self.trainers[trainer].pokemon[self.trainers[trainer].currentPokemon].moves[self.trainers[trainer].nextMove].modifiers[1]
          print(
            self.trainers[trainer].name + '\'s ' +
            self.trainers[trainer].pokemon[self.trainers[trainer].currentPokemon].name + '\'s ' +
            self.trainers[trainer].pokemon[self.trainers[trainer].currentPokemon].moves[self.trainers[trainer].nextMove].name +
            ' reduced ' + self.trainers[(trainer + 1) % 2].name + '\'s attack!')
        
        # Modify the defense stat
        if self.trainers[trainer].pokemon[self.trainers[trainer].currentPokemon].moves[self.trainers[trainer].nextMove].modifiers[2] != 0:
          self.trainers[(trainer + 1) % 2].pokemon[self.trainers[(trainer + 1) % 2].currentPokemon].statModifiers[2] += self.trainers[trainer].pokemon[self.trainers[trainer].currentPokemon].moves[self.trainers[trainer].nextMove].modifiers[2]
          print(
            self.trainers[trainer].name + '\'s ' +
            self.trainers[trainer].pokemon[self.trainers[trainer].currentPokemon].name + '\'s ' +
            self.trainers[trainer].pokemon[self.trainers[trainer].currentPokemon].moves[self.trainers[trainer].nextMove].name +
            ' reduced ' + self.trainers[(trainer + 1) % 2].name + '\'s defense!')
  
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