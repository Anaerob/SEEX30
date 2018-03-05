import numpy as np

import Constants as c
import Trainer

class Battle:
  def __init__(self, blueTeam, redTeam, printMe, state = None):
    
    ### Constants
    
    self.blueTeam = blueTeam
    self.redTeam = redTeam
    self.printMe = printMe
    
    ### State
    
    if state is None:
      self.round = 0
      self.running = True
      self.winner = -1
      
      # Initialize both trainers Red and Blue
      self.blue = Trainer.Trainer('Blue', self.blueTeam)
      self.red = Trainer.Trainer('Red', self.redTeam)
      
      # Put both trainers in a list to avoid double code
      self.trainers = [self.blue, self.red]
      #self.trainers.append(self.blue)
      #self.trainers.append(self.red)
    
    else:
      self.setState(state)
  
  def setState(self, state):
    self.round = state[0]
    self.running = state[1]
    self.winner = state[2]
    
    self.blue = Trainer.Trainer('Blue', self.blueTeam, state[3][0])
    self.red = Trainer.Trainer('Red', self.redTeam, state[3][1])
    
    self.trainers = []
    self.trainers.append(self.blue)
    self.trainers.append(self.red)
  
  def getState(self, isBlue):
    # Put everything in tempState and return it
    tempState = []
    
    tempState.append(self.round)
    tempState.append(self.running)
    tempState.append(self.winner)
    
    tempTrainerState = []
    for iT in range(2):
      if isBlue:
        tempTrainerState.append(self.trainers[iT].getState())
      else:
        tempTrainerState.append(self.trainers[(iT + 1) % 2].getState())
      
    tempState.append(tempTrainerState)
    
    return tempState
  
  def getInput(self, isBlue):
    tempInput = np.array([])
    
    if isBlue:
      tempInput = np.append(tempInput, self.blue.getInput())
      tempInput = np.append(tempInput, self.red.getInput())
    else:
      tempInput = np.append(tempInput, self.red.getInput())
      tempInput = np.append(tempInput, self.blue.getInput())
    
    return tempInput
  
  def progress(self):
    
    # For both trainers
    for iT in range(0, 2):
      
      # Check if an action has been chosen
      if not self.trainers[iT].nextActionSet:
        exit('Trainer ' + self.trainers[iT].name + ' move not set!')
      elif self.trainers[iT].nextMove < 0 or self.trainers[iT].nextMove > 4:
        exit('Trainer ' + self.trainers[iT].name + ' chosen move is illegal!')
      
      # Check if the chosen move has any pp remaining
      elif self.trainers[iT].pokemon[self.trainers[iT].cP].moves[self.trainers[iT].nextMove].cPP <= 0:
        exit('Trainer ' + self.trainers[iT].name + ' chose move with no PP remaining!')
    
    # Determine who strikes first based on speed (coin toss if speed is equal)
    ### TODO: fix "active" speed, fix paralysis
    firstTrainer = 0
    if self.trainers[0].pokemon[self.trainers[0].cP].stats[4] < self.trainers[1].pokemon[self.trainers[1].cP].stats[4]:
      firstTrainer = 1
    elif self.trainers[0].pokemon[self.trainers[0].cP].stats[4] == self.trainers[1].pokemon[self.trainers[1].cP].stats[4]:
      if np.random.randint(0, 2) == 0: # returns 0 or 1, 50/50
        firstTrainer = 1
    
    # Use moves in order, only use second move if Pokemon still active
    self.useMove(firstTrainer)
    self.trainers[firstTrainer].resetNextAction()
    if self.trainers[(firstTrainer + 1) % 2].pokemon[self.trainers[(firstTrainer + 1) % 2].cP].cHP > 0:
      self.useMove((firstTrainer + 1) % 2)
      self.trainers[(firstTrainer + 1) % 2].resetNextAction()
    
    # Check if either pokemon fainted
    for iT in range(0, 2):
      if self.trainers[iT].pokemon[self.trainers[iT].cP].cHP <= 0:
        self.running = False
        self.winner = (iT + 1) % 2
    
    # Increment round counter
    self.round += 1
  
  def useMove(self, t): # t: trainer
    
    # Deduct PP
    self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextMove].cPP -= 1
    
    # Check if move misses (correctly implements the 1/256 miss bug)
    ### TODO: Implement accuracy/evasion
    if np.random.randint(0, 256) >= self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextMove].stats[1]:
      if self.printMe:
        print(
          self.trainers[t].name + '\'s ' +
          self.trainers[t].pokemon[self.trainers[t].cP].name + '\'s ' +
          self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextMove].name + ' missed!')
    else:
      
      # If the move is a damaging move, calculate and deduct damage
      if self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextMove].stats[0] != 0:
        
        # If the move is a critical hit, calculate damage with double level and no modifiers
        if np.random.randint(0, 256) < np.floor(self.trainers[t].pokemon[self.trainers[t].cP].stats[4] / 2):
          damage = self.calculateDamage(
            2 * self.trainers[t].pokemon[self.trainers[t].cP].level,
            self.trainers[t].pokemon[self.trainers[t].cP].stats[1],
            self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextMove].stats[0],
            self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP].stats[2])
          self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP].cHP -= int(damage)
          if self.printMe:
            print(
              self.trainers[t].name + '\'s ' +
              self.trainers[t].pokemon[self.trainers[t].cP].name + '\'s ' +
              self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextMove].name +
              ' did ' + str(damage) + ' critical damage!')
        
        # If not, normal calculation with modifiers
        else:
          damage = self.calculateDamage(
            self.trainers[t].pokemon[self.trainers[t].cP].level,
            np.floor(
              c.statModifiers[self.trainers[t].mAttack] *
              self.trainers[t].pokemon[self.trainers[t].cP].stats[1] / 100),
            self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextMove].stats[0],
            np.floor(
              c.statModifiers[self.trainers[(t + 1) % 2].mDefense] *
              self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP].stats[2] / 100))
          self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP].cHP -= int(damage)
          if self.printMe:
            print(
              self.trainers[t].name + '\'s ' +
              self.trainers[t].pokemon[self.trainers[t].cP].name + '\'s ' +
              self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextMove].name +
              ' did ' + str(damage) + ' damage!')
      
      # If the move is a stat modifying move, modify the stat
      if self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextMove].modifiers[0] != 0:
        
        # If the move decreases the attack stat
        if self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextMove].modifiers[1] < 0:
          
          # If the opponents attack is at minimum, don't lower it further
          ### TODO: write lowering method that checks this
          if self.trainers[(t + 1) % 2].mAttack == 0:
            if self.printMe:
              print(
                self.trainers[(t + 1) % 2].name + '\'s ' +
                self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP].name + '\'s attack can\'t be lowered more!')
          
          # Else, lower it
          else:
            self.trainers[(t + 1) % 2].mAttack += self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextMove].modifiers[1]
            if self.printMe:
              print(
                self.trainers[t].name + '\'s ' +
                self.trainers[t].pokemon[self.trainers[t].cP].name + '\'s ' +
                self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextMove].name +
                ' reduced ' + self.trainers[(t + 1) % 2].name + '\'s attack!')
        
        # If the move decreases the defense stat
        if self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextMove].modifiers[2] < 0:
          
          # If the opponents defense is at minimum, don't lower it further
          if self.trainers[(t + 1) % 2].mDefense == 0:
            if self.printMe:
              print(
                self.trainers[(t + 1) % 2].name + '\'s ' +
                self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP].name + '\'s defense can\'t be lowered more!')
          
          # Else, lower it
          else:
            self.trainers[(t + 1) % 2].mDefense += self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextMove].modifiers[2]
            if self.printMe:
              print(
                self.trainers[t].name + '\'s ' +
                self.trainers[t].pokemon[self.trainers[t].cP].name + '\'s ' +
                self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextMove].name +
                ' reduced ' + self.trainers[(t + 1) % 2].name + '\'s defense!')
  
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