import numpy as np

import Constants as c
import Pokemon

class Trainer:
  def __init__(self, name, team, state = None):
    
    ### Constants
    
    self.name = name
    self.team = team
    
    ## State variables in the general case but fixed in battle scenarios:
    # Number of Pokemon
    self.nP = 1
    
    ## State variables in the general case but fixed in scenario 1:
    # Currently active Pokemon
    self.cP = 1
    
    ### Next action
    
    # Switch takes precedence over Move
    # Switch: 1 - 6 \ {unavailable Pokemon}
    # Switch: 0 = Not set
    # Move: 1 - 4 \ {unavailable moves}
    # Move: 0 = Struggle (only when no PP remaining for any move)
    self.nextActionSet = False
    self.nextMove = 0
    
    ### State
    
    if state is None:
      # Stat modifiers (only for currently active Pokemon)
      self.statMods = {
        'attack': 6,
        'defense': 6}
      
      # Pokemon
      self.pokemon = []
      for iP in range(self.nP):
        self.pokemon.append(Pokemon.Pokemon(team[iP]))
      
    else:
      self.setState(state)
  
  def setNextAction(self, action):
    if self.nextActionSet:
      exit('[setNextMove]: Move already set!')
    if action < 0 or action > 2:
      exit('[setNextMove]: Illegal move set by Trainer ' + self.name + '!')
    
    self.nextMove = action
    self.nextActionSet = True
  
  def setState(self, state):
    self.statMods = {
      'attack': state[0],
      'defense': state[1]}
    
    self.pokemon = []
    for iP in range(self.nP):
      self.pokemon.append(Pokemon.Pokemon(self.team[iP], state[2][iP]))
  
  def getState(self):
    tempState = []
    
    tempState.append(self.statMods['attack'])
    tempState.append(self.statMods['defense'])
    
    tempPokemonState = []
    for iP in range(self.nP):
      tempPokemonState.append(self.pokemon[iP].getState())
    tempState.append(tempPokemonState)
    
    return tempState
  
  def getFeatures(self):
    tempFeatures = np.array([])
    
    tempFeatures = np.append(tempFeatures, 1 - self.statMods['attack'] / 6)
    tempFeatures = np.append(tempFeatures, 1 - self.statMods['defense'] / 6)
    
    tempFeatures = np.append(tempFeatures, self.pokemon[self.cP - 1].getFeatures())
    
    for iP in range(self.nP):
      if iP == self.cP - 1:
        continue
      tempFeatures = np.append(tempFeatures, self.pokemon[iP].getFeatures())
    
    return tempFeatures
  
  def modifyStat(self, sStat, modifier):
    # Check if the stat can be modified further
    if self.statMods[sStat] <= 0:
      return False
    
    self.statMods[sStat] += modifier
    
    # Make sure the stat isn't modified too many steps
    if self.statMods[sStat] < 0:
      self.statMods[sStat] = 0
    
    return True
  
  def resetNextAction(self):
    self.nextActionSet = False
    self.nextSwitch = 0
    self.nextMove = 0
  
  def printSelf(self):
    print('Trainer ' + self.name + ' has ' + str(self.nP) + ' Pokemon:')
    for iP in range(self.nP):
      self.pokemon[iP].printSelf()
#