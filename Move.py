import numpy as np

import Constants as c

class Move:
  def __init__(self, index):
    self.name = c.MN[index]
    self.stats = c.MS[index, :]
    self.cPP = self.stats[2]
    self.modifiers = c.MM[index, :]
  
  def printSelf(self):
    print('   ' + self.name + ': ' + str(self.cPP) + ' / ' + str(self.stats[2]) + ' PP')
#