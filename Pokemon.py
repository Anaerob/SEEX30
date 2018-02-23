import numpy as np

import Constants as c
import Move

class Pokemon:
  def __init__(self, index, state = None):
    
    ### Constants
    
    self.index = index
    self.name = c.PN[self.index]
    self.base = c.PBS[self.index, :]
    
    # These are state variables in the general case but fixed in battle scenarios:
    self.level = 5
    self.effort = np.array([0, 0, 0, 0, 0])
    
    ### State
    
    if state is None:
      
      # self.stats = [HP, Attack, Defense, Special, Speed]
      self.individual = np.array([0, 0, 0, 0, 0])
      self.generateIndividualValues()
      self.stats = np.array([0, 0, 0, 0, 0])
      self.calculateStats()
      
      # Current HP
      self.cHP = self.stats[0]
      
      # Number of moves
      self.nM = 0
      
      # self.moves = [Struggle, Move1, Move2, Move3, Move4]
      self.moves = []
      self.initializeMoves()
      
      # Non-volatile status conditions
      self.burn = False
      self.freeze = False
      self.paralysis = False
      self.poison = False
      self.badPoison = False
      self.badPoisonTurn = 0
      self.sleep = False
      
      # Volatile status conditions
      self.bound = False
      self.confusion = False
      self.flinch = False
      self.leechSeed = False
      
    else:
      setState(state)
  
  def setState(self, state):
    
    # self.stats = [HP, Attack, Defense, Special, Speed]
    self.individual = state[0] # np.array([0, 0, 0, 0, 0]) + generateIndividualValues()
    self.stats = state[1] # np.array([0, 0, 0, 0, 0]) + calculateStats()
    
    # Current HP
    self.cHP = state[2] # self.stats[0]
    
    # self.moves = [Struggle, Move1, Move2, Move3, Move4]
    moveSet = c.PM[self.index, :]
    self.nM = state[3] # 0
    if self.nM < 1:
      exit('[setState]: Too few moves in move set')
    if self.nM > 4:
      exit('[setState]: Too many moves in move set')
    self.moves = [] # + initializeMoves()
    self.moves.append(Move.Move(165)) # Struggle not included in state since infinite PP
    for iM in range(self.nM):
      tempMove = Move.Move(moveSet[iM], state[4][iM])
      self.moves.append(tempMove)
    
    # Non-volatile status conditions
    self.burn = state[5] # False
    self.freeze = state[6] # False
    self.paralysis = state[7] # False
    self.poison = state[8] # False
    self.badPoison = state[9] # False
    self.badPoisonTurn = state[10] # 0
    self.sleep = state[11] # False
    
    # Volatile status conditions
    self.bound = state[12] # False
    self.confusion = state[13] # False
    self.flinch = state[14] # False
    self.leechSeed = state[15] # False
  
  def getState(self, state):
    
    # Put everything in tempState and return it
    tempState = []
    
    tempState.append(self.individual)
    tempState.append(self.stats)
    
    tempState.append(self.cHP)
    
    tempState.append(self.nM)
    tempMoveState = []
    for iM in range(1, self.nM + 1): # Don't include Struggle since it has infinite PP
      tempMoveState.append(self.moves[iM].getState())
    tempState.append(tempMoveState)
    
    # Non-volatile status conditions
    tempState.append(self.burn)
    tempState.append(self.freeze)
    tempState.append(self.paralysis)
    tempState.append(self.poison)
    tempState.append(self.badPoison)
    tempState.append(self.badPoisonTurn)
    tempState.append(self.sleep)
    
    # Volatile status conditions
    tempState.append(self.bound)
    tempState.append(self.confusion)
    tempState.append(self.flinch)
    tempState.append(self.leechSeed)
    
    return tempState
  
  def calculateStats(self):
    # calculate hit points
    hpTerm1 = 2 * (self.base[0] + self.individual[0])
    hpTerm2 = np.floor(np.minimum(np.ceil(np.sqrt(self.effort[0])), 255) / 4)
    self.stats[0] = 10 + self.level + np.floor(self.level * (hpTerm1 + hpTerm2) / 100)
    
    # calculate attack, defense, special and speed
    for i in range(1, 5):
      statTerm1 = 2 * (self.base[i] + self.individual[i])
      statTerm2 = np.floor(np.minimum(np.ceil(np.sqrt(self.effort[i])), 255) / 4)
      self.stats[i] = 5 + np.floor(self.level * (statTerm1 + statTerm2) / 100)
  
  def initializeMoves(self):
    # moves[0] = Struggle
    self.moves.append(Move.Move(165))
    
    # Get predetermined move set from Constants
    moveSet = c.PM[self.index, :]
    
    for iM in range(moveSet.size):
      if moveSet[iM] != 0:
        self.nM += 1
    
    if self.nM < 1:
      exit('[initializeMoves]: Too few moves in move set')
    if self.nM > 4:
      exit('[initializeMoves]: Too many moves in move set')
    
    for iM in range(self.nM):
      tempMove = Move.Move(moveSet[iM])
      self.moves.append(tempMove)
  
  def generateIndividualValues(self):
    for iI in range(1, 5):
      self.individual[iI] = np.random.randint(0, 16)
    self.individual[0] = 8 * (self.individual[1] % 2) + 4 * (self.individual[2] % 2) + 1 * (self.individual[3] % 2) + 2 * (self.individual[4] % 2)
  
  def printSelf(self):
    print(' ' + self.name + ':')
    print('  HP: ' + str(self.activeStats[0]) + ' / ' + str(self.stats[0]))
    print('  Moves:')
    for iM in range (0, self.nM):
      self.moves[iM].printSelf()
#