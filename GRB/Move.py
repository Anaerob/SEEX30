import numpy as np

import Constants as c

class Move:
  def __init__(self, index, state = None):
    
    ### Constants
    
    self.index = index
    self.name = c.MN[self.index]
    self.stats = {
      'power': c.MS[self.index][0],
      'accuracy': c.MS[self.index][1],
      'PP': c.MS[self.index][2]}
    self.modifiers = {
      'chance': c.MM[self.index][0],
      'attack': c.MM[self.index][1],
      'defense': c.MM[self.index][2],
      'special': c.MM[self.index][3],
      'speed': c.MM[self.index][4]}
    
    ### State
    
    if state is None:
      # Current PP
      self.cPP = self.stats['PP']
    else:
      self.setState(state)
  
  def setState(self, state):
    self.cPP = state
  
  def getState(self):
    return self.cPP
  
  def getFeatures(self):
    return np.array([(self.cPP < 4) * (1 - self.cPP / 4)])
  
  def printSelf(self):
    print('   ' + self.name + ': ' + str(self.cPP) + ' / ' + str(self.stats['PP']) + ' PP')
#