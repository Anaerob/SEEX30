import numpy as np

import Constants as c

class Move:
  def __init__(self, index):
    self.name = c.MN[index]
    self.stats = c.MS[index, :]
    self.activeStats = self.stats
    self.modifier = c.MM[index, :]
  
  def printSelf(self):
    print('   ' + self.name + ': ' + str(self.activeStats[2]) + ' / ' + str(self.stats[2]) + ' PP')
#