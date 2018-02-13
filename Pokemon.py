import numpy as np

import Constants as c

class Pokemon:
  def __init__(self, index):
    self.base = c.BS[1, :]
    self.individual = np.array([0,
      np.random.randint(0, 16),
      np.random.randint(0, 16),
      np.random.randint(0, 16),
      np.random.randint(0, 16)])
    if self.individual[1] % 2 != 0:
      self.individual[0] += 8
    if self.individual[2] % 2 != 0:
      self.individual[0] += 4
    if self.individual[3] % 2 != 0:
      self.individual[0] += 1
    if self.individual[4] % 2 != 0:
      self.individual[0] += 2
    self.effort = np.array([0, 0, 0, 0, 0])
    self.level = 5
    self.stats = np.array([0, 0, 0, 0, 0])
    
    self.calculateStats()
    
  def calculateStats(self):
    hpTerm1 = 2 * (self.base[0] + self.individual[0])
    hpTerm2 = np.floor(np.minimum(np.ceil(np.sqrt(self.effort[0])), 255) / 4)
    self.stats[0] = 10 + self.level + np.floor(self.level * (hpTerm1 + hpTerm2) / 100)
    
    for i in range(1, 5):
      statTerm1 = 2 * (self.base[i] + self.individual[i])
      statTerm2 = np.floor(np.minimum(np.ceil(np.sqrt(self.effort[i])), 255) / 4)
      self.stats[i] = 5 + np.floor(self.level * (statTerm1 + statTerm2) / 100)