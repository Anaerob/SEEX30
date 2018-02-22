import numpy as np

import Constants as c
import Move

class Pokemon:
  def __init__(self, index):
    
    ### Constants
    
    self.index = index
    self.level = 5
    self.name = c.PN[self.index]
    
    ### Initialize
    
    # Creates list self.moves = [Move1, Move2, Move3, Move4]
    self.initializeMoves()
    # Creates list self.stats = [HP, Attack, Defense, Special, Speed]
    self.initializeStats()
    
    ### State variables
    
    # Current HP
    self.cHP = self.stats[0]
    
    # Non-volatile status conditions
    self.burn = False
    self.freeze = False
    self.paralysis = False
    self.poison = False
    self.badPoison = [False, 0] # badPoison[1] = turn of infliction
    self.sleep = False
    
    # Volatile status conditions
    self.bound = False
    self.confusion = False
    self.flinch = False
    self.leechSeed = False
  
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
  
  def initializeMoves(self):
    # Make the moves list with moves[0] = Struggle
    self.moves = []
    self.moves.append(Move.Move(165))
    
    # Get predetermined move set from Constants
    moveSet = c.PM[self.index, :]
    # Number of moves
    self.nM = 0
    
    for i in range(0, moveSet.size):
      if moveSet[i] != 0:
        self.nM += 1
    
    if self.nM < 1:
      exit('Too few moves in move set')
    if self.nM > 4:
      exit('Too many moves in move set')
    
    for i in range(0, self.nM):
      tempMove = Move.Move(moveSet[i])
      self.moves.append(tempMove)
  
  def initializeStats(self):
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
  
  def printSelf(self):
    print(' ' + self.name + ':')
    print('  HP: ' + str(self.activeStats[0]) + ' / ' + str(self.stats[0]))
    print('  Moves:')
    for iM in range (0, self.nM):
      self.moves[iM].printSelf()
#