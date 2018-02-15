import numpy as np

import Constants as c

class Pokemon:
  def __init__(self, index):
    self.index = index
    self.level = 5
    self.setStats()
    
    self.activeStats = self.stats
    
  
  def setStats(self):
    # get predefined base stats for index
    self.base = c.PBS[self.index, :]
    
    # generate random individual values
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
    
    # initialize effort values to zero
    self.effort = np.array([0, 0, 0, 0, 0])
    
    # initialize stats to zero
    self.stats = np.array([0, 0, 0, 0, 0])
    
    # calculate stats properly based on base stats, individual values, effort values and level
    self.calculateStats()
  
  def calculateStats(self):
    # calculate hit points
    hpTerm1 = 2 * (self.base[0] + self.individual[0])
    hpTerm2 = np.floor(np.minimum(np.ceil(np.sqrt(self.effort[0])), 255) / 4)
    self.stats[0] = 10 + self.level + np.floor(self.level * (hpTerm1 + hpTerm2) / 100)
    
    # calculate attack, defense, special and speed
    for i in range(1, 5):
      statTerm1 = 2 * (self.base[i] + self.individual[i])
      statTerm2 = np.floor(np.minimum(np.ceil(np.sqrt(self.effort[i])), 255) / 4)
      self.stats[i] = 5 + np.floor(self.level * (statTerm1 + statTerm2) / 100)
  
#