import numpy as np

import Constants as c
import Trainer

class Battle:
  def __init__(self, whiteTeam, blackTeam, printMe, state = None):
    
    ### Constants
    
    self.whiteTeam = whiteTeam
    self.blackTeam = blackTeam
    self.printMe = printMe
    
    ### State
    
    if state is None:
      self.round = 0
      self.running = True
      self.winner = -1
      
      # Initialize trainers White and Black
      self.trainers = [
        Trainer.Trainer('White', self.whiteTeam),
        Trainer.Trainer('Black', self.blackTeam)]
      
    else:
      self.setState(state)
  
  def setState(self, state):
    self.round = state[0]
    self.running = state[1]
    self.winner = state[2]
    
    self.trainers = [
      Trainer.Trainer('White', self.whiteTeam, state[3]),
      Trainer.Trainer('Black', self.blackTeam, state[4])]
  
  def getState(self, isWhite):
    tempState = []
    
    tempState.append(self.round)
    tempState.append(self.running)
    tempState.append(self.winner)
    
    if isWhite:
      tempState.append(self.trainers[0].getState())
      tempState.append(self.trainers[1].getState())
    else:
      tempState.append(self.trainers[1].getState())
      tempState.append(self.trainers[0].getState())
    
    return tempState
  
  def getFeatures(self, isWhite):
    tempFeatures = np.array([])
    
    if isWhite:
      tempFeatures = np.append(tempFeatures, self.trainers[0].getFeatures())
      tempFeatures = np.append(tempFeatures, self.trainers[1].getFeatures())
    else:
      tempFeatures = np.append(tempFeatures, self.trainers[1].getFeatures())
      tempFeatures = np.append(tempFeatures, self.trainers[0].getFeatures())
    
    return tempFeatures
  
  def progress(self):
    if self.printMe:
      print('Round ' + str(self.round + 1) + '!')
    
    # For both trainers
    for iT in range(2):
      
      # Check if an action has been chosen
      if not self.trainers[iT].nextActionSet:
        exit('Trainer ' + self.trainers[iT].name + ' move not set!')
      elif self.trainers[iT].nextMove < 0 or self.trainers[iT].nextMove > 2:
        exit('Trainer ' + self.trainers[iT].name + ' chosen move is illegal!')
      
      # Check if the chosen move has any pp remaining
      elif self.trainers[iT].pokemon[self.trainers[iT].cP - 1].moves[self.trainers[iT].nextMove].cPP <= 0:
        exit('Trainer ' + self.trainers[iT].name + ' chose move with no PP remaining!')
    
    # Determine who strikes first based on speed (coin toss if speed is equal)
    firstTrainer = 0
    if self.trainers[0].pokemon[self.trainers[0].cP - 1].stats['speed'] < self.trainers[1].pokemon[self.trainers[1].cP - 1].stats['speed']:
      firstTrainer = 1
    elif self.trainers[0].pokemon[self.trainers[0].cP - 1].stats['speed'] == self.trainers[1].pokemon[self.trainers[1].cP - 1].stats['speed']:
      # Returns 0 or 1
      if np.random.randint(0, 2) == 0:
        firstTrainer = 1
    
    # Use moves in order, only use second move if Pokemon still active
    if self.printMe:
      print(
        self.trainers[firstTrainer].name + '\'s ' +
        self.trainers[firstTrainer].pokemon[self.trainers[firstTrainer].cP - 1].name + ' used ' +
        self.trainers[firstTrainer].pokemon[self.trainers[firstTrainer].cP - 1].moves[self.trainers[firstTrainer].nextMove].name + '!')
    self.useMove(firstTrainer)
    self.trainers[firstTrainer].resetNextAction()
    if self.trainers[(firstTrainer + 1) % 2].pokemon[self.trainers[(firstTrainer + 1) % 2].cP - 1].cHP > 0:
      if self.printMe:
        print(
          self.trainers[(firstTrainer + 1) % 2].name + '\'s ' +
          self.trainers[(firstTrainer + 1) % 2].pokemon[self.trainers[(firstTrainer + 1) % 2].cP - 1].name + ' used ' +
          self.trainers[(firstTrainer + 1) % 2].pokemon[self.trainers[(firstTrainer + 1) % 2].cP - 1].moves[self.trainers[(firstTrainer + 1) % 2].nextMove].name + '!')
      self.useMove((firstTrainer + 1) % 2)
      self.trainers[(firstTrainer + 1) % 2].resetNextAction()
    
    # Check if either pokemon fainted, proclaim victor (0: white, 1: black)
    for iT in range(2):
      if self.trainers[iT].pokemon[self.trainers[iT].cP - 1].cHP <= 0:
        self.running = False
        self.winner = (iT + 1) % 2
    
    if self.printMe:
      print()
    
    self.round += 1
  
  def useMove(self, t): # t: trainer
    # Deduct PP
    self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextMove].cPP -= 1
    
    # Check if move misses (correctly implements the 1/256 miss bug)
    if np.random.randint(0, 256) >= self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextMove].stats['accuracy']:
      if self.printMe:
        print('  ' +
          self.trainers[t].name + '\'s ' +
          self.trainers[t].pokemon[self.trainers[t].cP - 1].name + ' missed!')
      
    else:
      
      # If the move is a damaging move, calculate and deduct damage
      if self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextMove].stats['power'] != 0:
        
        # If the move is a critical hit, calculate damage with double level and no modifiers
        if np.random.randint(0, 256) < np.floor(self.trainers[t].pokemon[self.trainers[t].cP - 1].base['speed'] / 2):
          damage = self.calculateDamage(
            2 * self.trainers[t].pokemon[self.trainers[t].cP - 1].level,
            self.trainers[t].pokemon[self.trainers[t].cP - 1].stats['attack'],
            self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextMove].stats['power'],
            self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].stats['defense'])
          self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].cHP -= int(damage)
          if self.printMe:
            print('  ' +
              self.trainers[t].name + '\'s ' +
              self.trainers[t].pokemon[self.trainers[t].cP - 1].name +
              ' did ' + str(damage) + ' critical damage!')
        
        # If not a critical hit, normal calculation with modifiers
        else:
          damage = self.calculateDamage(
            self.trainers[t].pokemon[self.trainers[t].cP - 1].level,
            np.floor(
              c.statModifiers[self.trainers[t].statMods['attack']] *
              self.trainers[t].pokemon[self.trainers[t].cP - 1].stats['attack'] / 100),
            self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextMove].stats['power'],
            np.floor(
              c.statModifiers[self.trainers[(t + 1) % 2].statMods['defense']] *
              self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].stats['defense'] / 100))
          self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].cHP -= int(damage)
          if self.printMe:
            print('  ' +
              self.trainers[t].name + '\'s ' +
              self.trainers[t].pokemon[self.trainers[t].cP - 1].name +
              ' did ' + str(damage) + ' damage!')
      
      # If the move is a stat modifying move, modify the stat
      if self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextMove].modifiers['chance'] != 0:
        
        # Loop over all stats (1: Attack, 2: Defense, 3: Special, 4: Speed, 5: Accuracy, 6: Evasion)
        s = ['attack', 'defense']
        for iStat in range(2):
          
          # If the move decreases iStat
          if self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextMove].modifiers[s[iStat]] < 0:
            
            # Try decreasing it (returns True if success, False if at minimum)
            if self.trainers[(t + 1) % 2].modifyStat(s[iStat], self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextMove].modifiers[s[iStat]]):
              if self.printMe:
                print('  ' +
                  self.trainers[(t + 1) % 2].name + '\'s ' +
                  self.trainers[(t + 1) % 2].pokemon[self.trainers[t].cP - 1].name + '\'s stat was reduced!')
              
            elif self.printMe:
              print('  ' +
                self.trainers[(t + 1) % 2].name + '\'s ' +
                self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].name + '\'s stat can\'t be lowered more!')
  
  def calculateDamage(self, l, a, p, d):
    # Calculate raw damage
    factor1 = 2 + np.floor(2 * l / 5)
    factor2 = p * a
    denominator = 50 * d
    unmodified = 2 + np.floor(factor1 * factor2 / denominator)
    
    # Apply random modifier
    rand = np.random.randint(217, 256)
    damage = np.floor(unmodified * rand / 255)
    
    return int(damage)
  
  def printSelf(self):
    print()
    self.trainers[0].printSelf()
    print()
    self.trainers[1].printSelf()
    print()
#