import numpy as np

import Constants as c

class Move:
  def __init__(self, index, state = None):
    
    ### Constants
    
    self.name = c.MN[index]
    self.stats = c.MS[index, :]
    self.modifiers = c.MM[index, :]
    
    ### State
    
    if state is None:
      self.cPP = self.stats[2]
    else:
      setState(state)
  
  def setState(self, state):
    self.cPP = state
  
  def getState(self):
    return self.cPP
  
  def printSelf(self):
    print('   ' + self.name + ': ' + str(self.cPP) + ' / ' + str(self.stats[2]) + ' PP')
#