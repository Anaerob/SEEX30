import numpy as np

import Constants as c
import Move

class Pokemon:
  def __init__(self, index, state = None):
    
    ### Constants
    
    self.index = index
    self.name = c.PN[self.index]
    self.base = {
      'HP': c.PBS[self.index][0],
      'attack': c.PBS[self.index][1],
      'defense': c.PBS[self.index][2],
      'special': c.PBS[self.index][3],
      'speed': c.PBS[self.index][4]}
    
    ## State variables in the general case but fixed in battle scenarios:
    self.level = 5
    self.effort = {
      'HP': 0,
      'attack': 0,
      'defense': 0,
      'special': 0,
      'speed': 0}
    self.individual = {
      'HP': 0,
      'attack': 0,
      'defense': 0,
      'special': 0,
      'speed': 0}
    self.stats = {}
    self.calculateStats()
    # Number of moves
    self.nM = 2
    
    ### State
    
    if state is None:
      # Current HP
      self.cHP = self.stats['HP']
      
      # self.moves = [Struggle, Move1, Move2, Move3, Move4]
      self.moves = []
      self.initializeMoves()
      
    else:
      self.setState(state)
  
  def setState(self, state):
    self.cHP = state[0]
    
    self.moves = []
    
    moveSet = c.PM[self.index]
    
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
  
  def getFeatures(self):
    tempFeatures = np.array([self.cHP / self.stats['HP']])
    
    for iM in range(1, self.nM + 1):
      tempFeatures = np.append(tempFeatures, self.moves[iM].getFeatures())
    
    return tempFeatures
  
  def calculateStats(self):
    # Calculate HP
    hpTerm1 = 2 * (self.base['HP'] + self.individual['HP'])
    hpTerm2 = np.floor(np.minimum(np.ceil(np.sqrt(self.effort['HP'])), 255) / 4)
    self.stats['HP'] = 10 + self.level + np.floor(self.level * (hpTerm1 + hpTerm2) / 100)
    
    # Calculate attack, defense, special and speed
    s = ['attack', 'defense', 'special', 'speed']
    for iStat in range(4):
      statTerm1 = 2 * (self.base[s[iStat]] + self.individual[s[iStat]])
      statTerm2 = np.floor(np.minimum(np.ceil(np.sqrt(self.effort[s[iStat]])), 255) / 4)
      self.stats[s[iStat]] = 5 + np.floor(self.level * (statTerm1 + statTerm2) / 100)
  
  def initializeMoves(self):
    # moves[0] = Struggle
    self.moves.append(Move.Move(165))
    
    # Get predetermined move set from Constants
    moveSet = c.PM[self.index]
    
    for iM in range(self.nM):
      self.moves.append(Move.Move(moveSet[iM]))
  
  def printSelf(self):
    print(' ' + self.name + ':')
    print('  HP: ' + str(self.cHP) + ' / ' + str(self.stats['HP']))
    print('  Moves:')
    for iM in range (1, self.nM + 1):
      self.moves[iM].printSelf()
#