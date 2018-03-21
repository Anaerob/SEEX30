import numpy as np

import Constants as c
import Move

class Pokemon:
  def __init__(self, index, state = None):
    
    ### Constants
    
    self.index = index
    self.name = c.PN[self.index]
    
    ## State variables in the general case but fixed in battle scenarios:
    
    # Number of moves
    self.nM = 4
    
    ### State
    
    if state is None:
      # Current HP
      self.cHP = c.PS[self.index][0]
      
      self.frozen = False
      self.paralyzed = False
      self.sleeping = False
      
      # self.moves = [Struggle, Move1, Move2, Move3, Move4]
      self.moves = [Move.Move(165)]
      
      # Get predetermined move set from Constants
      moveSet = c.PM[self.index]
      
      for iM in range(self.nM):
        self.moves.append(Move.Move(moveSet[iM]))
      
    else:
      self.setState(state)
  
  def setState(self, state):
    self.cHP = state[0]
    
    self.moves = [Move.Move(165)]
    
    moveSet = c.PM[self.index]
    
    for iM in range(self.nM):
      self.moves.append(Move.Move(moveSet[iM], state[1][iM]))
    
  def getState(self):
    tempState = []
    
    tempState.append(self.cHP)
    
    tempMoveState = []
    for iM in range(self.nM): 
      tempMoveState.append(self.moves[iM + 1].getState())
    tempState.append(tempMoveState)
    
    return tempState
  
  def getFeatures(self):
    tempFeatures = np.array([self.cHP / c.PS[self.index][0]])
    
    for iM in range(self.nM):
      tempFeatures = np.append(tempFeatures, self.moves[iM + 1].getFeatures())
    
    return tempFeatures
  
  def printSelf(self):
    print(' ' + self.name + ':')
    print('  HP: ' + str(self.cHP) + ' / ' + str(c.PS[self.index][0]))
    print('  Moves:')
    for iM in range (1, self.nM + 1):
      self.moves[iM].printSelf()
#