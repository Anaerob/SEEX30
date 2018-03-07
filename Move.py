import numpy as np

import Constants as c

class Move:
  def __init__(self, index, state = None):
    
    ### Constants
    
    self.name = c.MN[index]
    self.stats = c.MS[index, :]
    self.modifiers = c.MM[index, :]
    
    # For clarity in code
    self.power = self.stats[0]
    self.accuracy = self.stats[1]
    self.PP = self.stats[2]
    
    ### State
    
    if state is None:
      # Current PP
      self.cPP = self.PP
    else:
      self.setState(state)
  
  def setState(self, state):
    self.cPP = state
  
  def getState(self):
    return self.cPP
  
  def getInput(self):
    return np.array([self.cPP / self.PP])
  
  def printSelf(self):
    print('   ' + self.name + ': ' + str(self.cPP) + ' / ' + str(self.PP) + ' PP')
#