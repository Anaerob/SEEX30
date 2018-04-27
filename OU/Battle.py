import numpy as np

import Constants as c
import Trainer

class Battle:
  def __init__(self, printMe, state = None):
    
    ### Constants
    
    self.printMe = printMe
    
    ### State
    
    if state is None:
      self.round = 0
      
      self.running = True
      
      self.wForceSwitch = False
      self.bForceSwitch = False
      
      self.wWinner = False
      self.bWinner = False
      self.tie = False
      
      # Initialize trainers White and Black
      self.trainers = [
        Trainer.Trainer('White', self.whiteTeam),
        Trainer.Trainer('Black', self.blackTeam)]
      
    else:
      self.setState(state)
  
  def setState(self, state):
    self.round = state[0]
    self.running = state[1]
    self.wWinner = state[2]
    self.bWinner = state[3]
    self.tie = state[4]
    
    self.trainers = [
      Trainer.Trainer('White', self.whiteTeam, state[5]),
      Trainer.Trainer('Black', self.blackTeam, state[6])]
  
  def getState(self, isWhite):
    tempState = [self.round]
    
    tempState.append(self.running)
    tempState.append(self.wWinner)
    tempState.append(self.bWinner)
    tempState.append(self.tie)
    
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
      # Flooring and division by 100 * 100 omitted because not neccessary for comparison
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
  
  def useMove(self, t):
    # Deduct PP, unless the move is Struggle
    if self.trainers[t].nextAction[1] != 0:
      self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextAction[1]].cPP -= 1
    
    # Check if move misses (1/256 miss bugg included)
    if np.random.randint(256) >= c.MS[self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextMove].index][1]:
      if self.printMe:
        print('  ' +
          self.trainers[t].name + '\'s ' +
          self.trainers[t].pokemon[self.trainers[t].cP - 1].name + ' missed!')
    else:
      if self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextAction[1]].index == 34:
        self.useBodySlam(t)
      elif self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextAction[1]].index == 58:
        self.useIceBeam(t)
      elif self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextAction[1]].index == 63:
        self.useHyperBeam(t)
      elif self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextAction[1]].index == 65:
        self.useDrillPeck(t)
      elif self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextAction[1]].index == 78:
        self.useStunSpore(t)
      elif self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextAction[1]].index == 79:
        self.useSleepPowder(t)
      elif self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextAction[1]].index == 85:
        self.useThunderbolt(t)
      elif self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextAction[1]].index == 86:
        self.useThunderWave(t)
      elif self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextAction[1]].index == 89:
        self.useEarthquake(t)
      elif self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextAction[1]].index == 94:
        self.usePsychic(t)
      elif self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextAction[1]].index == 97:
        self.useAgility(t)
      elif self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextAction[1]].index == 120:
        self.useSelfDestruct(t)
      elif self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextAction[1]].index == 135:
        self.useSoftBoiled(t)
      elif self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextAction[1]].index == 153:
        self.useExplosion(t)
      elif self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextAction[1]].index == 157:
        self.useRockSlide(t)
      elif self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextAction[1]].index == 164:
        self.useSubstitute(t)
      elif self.trainers[t].pokemon[self.trainers[t].cP - 1].moves[self.trainers[t].nextAction[1]].index == 165:
        self.useStruggle(t)
    
      """
      
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
  """
  def useBodySlam(self, t): # Rhydon, Tauros & Snorlax
    level = 100
    
    # Check if critical hit
    if np.random.randint(256) < np.floor(c.PBS[self.trainers[t].pokemon[self.trainers[t].cP - 1].index][4] / 2):
      level = 200
     
    # Calculate base damage
    damage = self.calculateDamage(level,
      c.PS[self.trainers[t].pokemon[self.trainers[t].cP - 1].index][1],
      85,
      c.PS[self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].index][2])
    
    # Not very effective x0.5 against Rhydon
    if self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].index == 112:
      damage = int(damage / 2)
    
    # Same type attack bonus when using Tauros or Snorlax
    if self.trainers[t].pokemon[self.trainers[t].cP - 1].index == 128
      or self.trainers[t].pokemon[self.trainers[t].cP - 1].index == 143:
      damage = int(damage * 1.5)
    
    # Inflict damage
    self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].cHP = 
      int(self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].cHP - damage > 0)
      * (self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].cHP - damage)
    
    # Can't paralyze normal types
    if self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].index == 103
      or self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].index == 112
      or self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].index == 145:
      # 30% chance of paralyzing
      if np.random.randint(256) < 77:
        self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].paralyzed = True
  
  def useIceBeam(self, t): # Chansey & Tauros
    damage = 0
    
    # Check if critical hit & calculate base damage
    if np.random.randint(256) < np.floor(c.PBS[self.trainers[t].pokemon[self.trainers[t].cP - 1].index][4] / 2):
      damage = self.calculateDamage(200,
        c.PS[self.trainers[t].pokemon[self.trainers[t].cP - 1].index][3],
        90,
        c.PS[self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].index][3])
    else:
      damage = self.calculateDamage(100,
        np.floor(c.statMods[self.trainers[t].specialMod] * c.PS[self.trainers[t].pokemon[self.trainers[t].cP - 1].index][3] / 100),
        90,
        np.floor(c.statMods[self.trainers[(t + 1) % 2].specialMod] * c.PS[self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].index][3] / 100))
    
    # Super effective x2 against Exeggutor, Rhydon and Zapdos
    if self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].index == 103
      or self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].index == 112
      or self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].index == 145:
      damage = int(damage * 2)
    
    # Inflict damage
    self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].cHP = 
      int(self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].cHP - damage > 0)
      * (self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].cHP - damage)
    
    # 10% chance of freezing
    if np.random.randint(256) < 26:
      self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].frozen = True
  
  def useHyperBeam(self, t): # Tauros & Snorlax
    level = 100
    
    # Check if critical hit
    if np.random.randint(256) < np.floor(c.PBS[self.trainers[t].pokemon[self.trainers[t].cP - 1].index][4] / 2):
      level = 200
    
    # Calculate base damage
    damage = self.calculateDamage(level,
      c.PS[self.trainers[t].pokemon[self.trainers[t].cP - 1].index][1],
      150,
      c.PS[self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].index][2])
    
    # Not very effective x0.5 against Rhydon
    if self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].index == 112:
      damage = int(damage / 2)
    
    # Same type attack bonus when using Tauros or Snorlax
    damage = int(damage * 1.5)
    
    # Inflict damage
    self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].cHP = 
      int(self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].cHP - damage > 0)
      * (self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].cHP - damage)
    
    # Recharge
    self.recharge = True
  
  def useDrillPeck(self, t): # Zapdos
    level = 100
    
    # Check if critical hit
    if np.random.randint(256) < 50:
      level = 200
    
    # Calculate base damage
    damage = self.calculateDamage(level,
      90,
      85,
      c.PS[self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].index][2])
    
    # Super effective x2 against Exeggutor
    if self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].index == 103:
      damage = int(damage * 2)
    
    # Not very effective x0.5 against Rhydon and Zapdos
    if self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].index == 112
      or self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].index == 145:
      damage = int(damage / 2)
    
    # Same type attack bonus when using Zapdos
    damage = int(damage * 1.5)
    
    # Inflict damage
    self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].cHP = 
      int(self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].cHP - damage > 0)
      * (self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].cHP - damage)
  
  def useStunSpore(self, t): # Exeggutor
    # Paralyze
    self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].paralyzed = True
  
  def useSleepPowder(self, t): # Exeggutor
    # Sleep
    self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].sleeping = True
  
  def useThunderbolt(self, t): # Chansey & Zapdos
    damage = 0
    
    # Check if critical hit & calculate base damage
    if np.random.randint(256) < np.floor(c.PBS[self.trainers[t].pokemon[self.trainers[t].cP - 1].index][4] / 2):
      damage = self.calculateDamage(200,
        c.PS[self.trainers[t].pokemon[self.trainers[t].cP - 1].index][3],
        90,
        c.PS[self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].index][3])
    else:
      damage = self.calculateDamage(100,
        np.floor(c.statMods[self.trainers[t].specialMod] * c.PS[self.trainers[t].pokemon[self.trainers[t].cP - 1].index][3] / 100),
        90,
        np.floor(c.statMods[self.trainers[(t + 1) % 2].specialMod] * c.PS[self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].index][3] / 100))
    
    # Immunity x0 against Rhydon
    if self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].index == 112:
      damage = 0
    
    # Not very effective x0.5 against Exeggutor
    if self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].index == 103:
      damage = int(damage / 2)
    
    # Same type attack bonus when using Zapdos
    if self.trainers[t].pokemon[self.trainers[t].cP - 1].index == 145:
      damage = int(damage * 1.5)
    
    # Inflict damage
    self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].cHP = 
      int(self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].cHP - damage > 0)
      * (self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].cHP - damage)
    
    # Can't paralyze Zapdos
    if self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].index != 145:
      # 10% chance of paralyzing
      if np.random.randint(256) < 26:
        self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP - 1].paralyzed = True
  
  def useThunderWave(self, t): # Chansey % Zapdos
    
  
  def useEarthquake(self, t):
    
  
  def usePsychic(self, t):
    
  
  def useAgility(self, t):
    
  
  def useSelfDestruct(self, t):
    
  
  def useSoftBoiled(self, t):
    
  
  def useExplosion(self, t):
    
  
  def useRockSlide(self, t):
    
  
  def useSubstitute(self, t):
    
  
  def useStruggle(self, t):
    
  
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