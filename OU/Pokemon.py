import numpy as np

import Constants as c
import Move

class Pokemon:
  def __init__(self, index, state = None):
    
    ### Constants
    
    self.index = index
    self.name = c.PN[self.index]
    
    # Number of moves
    self.nM = 4
    
    ### State
    
    if state is None:
      # Current HP
      self.cHP = c.PS[self.index][0]
      
      # Status conditions
      self.frozen = False
      self.paralyzed = False
      self.sleeping = False
      
      # self.moves = [Struggle, Move1, Move2, Move3, Move4]
      self.moves = [Move.Move(165)]
      
      # Get moves using predetermined move set from Constants
      for iM in range(self.nM):
        self.moves.append(Move.Move(c.PM[self.index][iM]))
      
    else:
      self.setState(state)
  
  def setState(self, state):
    self.cHP = state[0]
    
    self.frozen = state[1]
    self.paralyzed = state[2]
    self.sleeping = state[3]
    
    self.moves = [Move.Move(165)]
    
    for iM in range(self.nM):
      self.moves.append(Move.Move(c.PM[self.index][iM], state[4][iM]))
    
  def getState(self):
    tempState = [self.cHP]
    
    tempState.append(self.frozen)
    tempState.append(self.paralyzed)
    tempState.append(self.sleeping)
    
    tempMoveState = []
    for iM in range(self.nM):
      tempMoveState.append(self.moves[iM + 1].getState())
    tempState.append(tempMoveState)
    
    return tempState
  
  def getFeatures(self):
    tempFeatures = np.array([self.cHP / c.PS[self.index][0]])
    
    tempFeatures = np.append(tempFeatures, int(self.frozen))
    tempFeatures = np.append(tempFeatures, int(self.paralyzed))
    tempFeatures = np.append(tempFeatures, int(self.sleeping))
    
    for iM in range(self.nM):
      tempFeatures = np.append(tempFeatures, self.moves[iM + 1].getFeatures())
    
    return tempFeatures
  
  def printSelf(self):
    print(' ' + self.name + ':')
    print('  HP: ' + str(self.cHP) + ' / ' + str(c.PS[self.index][0]))
    if self.cHP == 0:
      print('  Fainted!')
    else:
      if self.frozen:
        print('  Frozen!')
      if self.paralyzed:
        print('  Paralyzed!')
      if self.sleeping:
        print('  Sleeping!')
      print('  Moves:')
      for iM in range (1, self.nM + 1):
        self.moves[iM].printSelf()
#