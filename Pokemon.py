import numpy as np

import Constants as c
import Move

class Pokemon:
  def __init__(self, index, state = None):
    
    ### Constants
    
    self.index = index
    self.name = c.PN[self.index]
    self.base = c.PBS[self.index, :]
    
    ## State variables in the general case but fixed in battle scenarios:
    self.level = 5
    self.effort = np.array([0, 0, 0, 0, 0])
    self.individual = np.array([0, 0, 0, 0, 0])
    # self.stats = [HP, Attack, Defense, Special, Speed]
    self.stats = np.array([0, 0, 0, 0, 0])
    self.calculateStats()
    
    # For clarity in code
    self.HP = self.stats[0]
    self.attack = self.stats[1]
    self.defense = self.stats[2]
    self.special = self.stats[3]
    self.speed = self.stats[4]
    
    # Number of moves
    self.nM = 2
    
    ### State
    
    if state is None:
      # Current HP
      self.cHP = self.HP
      
      # self.moves = [Struggle, Move1, Move2, Move3, Move4]
      self.moves = []
      self.initializeMoves()
      
    else:
      self.setState(state)
  
  def setState(self, state):
    self.cHP = state[0]
    
    moveSet = c.PM[self.index, :]
    self.moves = []
    # Struggle not included in state since infinite PP
    self.moves.append(Move.Move(165))
    
    for iM in range(self.nM):
      self.moves.append(Move.Move(moveSet[iM], state[1][iM]))
    
  def getState(self):
    tempState = []
    
    tempState.append(self.cHP)
    
    tempMoveState = []
    # Struggle not included in state since infinite PP
    for iM in range(1, self.nM + 1): 
      tempMoveState.append(self.moves[iM].getState())
    tempState.append(tempMoveState)
    
    return tempState
  
  def getInput(self):
    tempInput = np.array([self.cHP / self.HP])
    
    for iM in range(1, self.nM + 1):
      tempInput = np.append(tempInput, self.moves[iM].getInput())
    
    return tempInput
  
  def calculateStats(self):
    # Calculate HP
    hpTerm1 = 2 * (self.base[0] + self.individual[0])
    hpTerm2 = np.floor(np.minimum(np.ceil(np.sqrt(self.effort[0])), 255) / 4)
    self.stats[0] = 10 + self.level + np.floor(self.level * (hpTerm1 + hpTerm2) / 100)
    
    # Calculate attack, defense, special and speed
    for i in range(1, 5):
      statTerm1 = 2 * (self.base[i] + self.individual[i])
      statTerm2 = np.floor(np.minimum(np.ceil(np.sqrt(self.effort[i])), 255) / 4)
      self.stats[i] = 5 + np.floor(self.level * (statTerm1 + statTerm2) / 100)
  
  def initializeMoves(self):
    # moves[0] = Struggle
    self.moves.append(Move.Move(165))
    
    # Get predetermined move set from Constants
    moveSet = c.PM[self.index, :]
    
    for iM in range(self.nM):
      self.moves.append(Move.Move(moveSet[iM]))
  
  def generateIndividualValues(self):
    # Same generation as in RBY games
    for iI in range(1, 5):
      self.individual[iI] = np.random.randint(0, 16)
    self.individual[0] = 8 * (self.individual[1] % 2) + 4 * (self.individual[2] % 2) + 1 * (self.individual[3] % 2) + 2 * (self.individual[4] % 2)
  
  def printSelf(self):
    print(' ' + self.name + ':')
    print('  HP: ' + str(self.cHP) + ' / ' + str(self.HP))
    print('  Moves:')
    for iM in range (1, self.nM + 1):
      self.moves[iM].printSelf()
#