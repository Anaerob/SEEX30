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
    
    # Check if a legal action has been chosen
    for iT in range(2):
      if not self.trainers[iT].nextActionSet:
        exit('[progress]: Trainer ' + self.trainers[iT].name + ' move not set!')
      elif self.trainers[iT].nextAction[0] < 0 or self.trainers[iT].nextAction[0] > 6:
        exit('[progress]: Trainer ' + self.trainers[iT].name + '\'s chosen switch is illegal!')
      elif self.trainers[iT].nextAction[1] < 0 or self.trainers[iT].nextAction[1] > 4:
        exit('[progress]: Trainer ' + self.trainers[iT].name + '\'s chosen move is illegal!')
      
      # Check if the chosen move has any pp remaining
      #elif self.trainers[iT].pokemon[self.trainers[iT].cP - 1].moves[self.trainers[iT].nextAction[1]].cPP <= 0:
        #exit('[progress]: Trainer ' + self.trainers[iT].name + ' chose move with no PP remaining!')
    
    wSwitch = self.trainers[0].nextAction[0] > 0
    bSwitch = self.trainers[1].nextAction[0] > 0
    
    # Carry out switches before moves
    if wSwitch and bSwitch:
      firstTrainer = np.random.randint(2)
      self.switch(firstTrainer)
      self.trainers[firstTrainer].resetNextAction()
      self.switch((firstTrainer + 1) % 2)
      self.trainers[(firstTrainer + 1) % 2].resetNextAction()
    elif wSwitch:
      self.switch(0)
      self.trainers[0].resetNextAction()
      self.useMove(1)
      self.trainers[1].resetNextAction()
    elif bSwitch:
      self.switch(1)
      self.trainers[1].resetNextAction()
      self.useMove(0)
      self.trainers[0].resetNextAction()
    
    # If no switches, use moves
    else:
      # Flooring after division by 100 * 100 omitted because not neccessary for comparison
      wSpeed = c.PS[self.trainers[0].pokemon[self.trainers[0].cP - 1].index][4]
        * c.statMods[self.trainers[0].speedMod]
        * (100 - 25 * self.trainers[0].pokemon[self.trainers[0].cP - 1].paralyzed)
      bSpeed = c.PS[self.trainers[1].pokemon[self.trainers[1].cP - 1].index][4]
        * c.statMods[self.trainers[1].speedMod]
        * (100 - 25 * self.trainers[1].pokemon[self.trainers[1].cP - 1].paralyzed)
      
      # Determine who strikes first based on speed (coin toss if speed is equal)
      firstTrainer = 0
      if wSpeed < bSpeed:
        firstTrainer = 1
      elif wSpeed == bSpeed:
        firstTrainer = np.random.randint(2)
      
      # Use moves in order, only use second move if Pokemon still active
      self.useMove(firstTrainer)
      self.trainers[firstTrainer].resetNextAction()
      if self.trainers[(firstTrainer + 1) % 2].pokemon[self.trainers[(firstTrainer + 1) % 2].cP - 1].cHP > 0:
        self.useMove((firstTrainer + 1) % 2)
        self.trainers[(firstTrainer + 1) % 2].resetNextAction()
    
    # REWRITE: ENDING CONDITIONS
    
    self.round += 1
  
  def useMove(self, t): # t: trainer
    if self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextAction[1]].index == 65:
      self.useDrillPeck(t)
    
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
  
  def useDrillPeck(self, t):
    
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