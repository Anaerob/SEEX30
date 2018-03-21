import numpy as np

import Constants as c

class Move:
  def __init__(self, index, state = None):
    
    ### Constants
    
    self.index = index
    self.name = c.MN[self.index]
    
    ### State
    
    if state is None:
      # Current PP
      self.cPP = c.MS[self.index][2]
    else:
      self.setState(state)
  
  def setState(self, state):
    self.cPP = state
  
  def getState(self):
    return self.cPP
  
  def getFeatures(self):
    return np.array([(self.cPP < 4) * (1 - self.cPP / 4)])
  
  def printSelf(self):
    print('   ' + self.name + ': ' + str(self.cPP) + ' / ' + str(c.MS[self.index][2]) + ' PP')
#