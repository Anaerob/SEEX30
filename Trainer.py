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
      self.statMods = np.array([6, 6, 6])
      
      # For clarity in code
      self.mAttack = self.statMods[1]
      self.mDefense = self.statMods[2]
      
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
    self.statMods = state[0]
    
    self.mAttack = self.statMods[1]
    self.mDefense = self.statMods[2]
    
    self.pokemon = []
    for iP in range(self.nP):
      tempPokemon = Pokemon.Pokemon(self.team[iP], state[1][iP])
      self.pokemon.append(tempPokemon)
  
  def getState(self):
    tempState = []
    
    tempState.append(self.statMods)
    
    tempPokemonState = []
    for iP in range(self.nP):
      tempPokemonState.append(self.pokemon[iP].getState())
    tempState.append(tempPokemonState)
    
    return tempState
  
  def getInput(self):
    tempInput = np.array([])
    
    tempInput = np.append(tempInput, self.mAttack / 12)
    tempInput = np.append(tempInput, self.mDefense / 12)
    
    tempInput = np.append(tempInput, self.pokemon[self.cP - 1].getInput())
    
    for iP in range(self.nP):
      if iP == self.cP - 1:
        continue
      tempInput = np.append(tempInput, self.pokemon[iP].getInput())
    
    return tempInput
  
  def modifyStat(self, stat, modifier):
    if self.statMods[stat] <= 0:
      return False
    
    self.statMods[stat] += modifier
    
    self.mAttack = self.statMods[1]
    self.mDefense = self.statMods[2]
    
    return True
  
  def resetNextAction(self):
    self.nextActionSet = False
    self.nextSwitch = 0
    self.nextMove = 0
  
  def printSelf(self):
    print('Trainer ' + self.name + ' has ' + str(self.nP) + ' Pokemon:')
    for iP in range (self.nP):
      self.pokemon[iP].printSelf()
#