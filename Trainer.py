import numpy as np

import Constants as c
import Pokemon

class Trainer:
  def __init__(self, name, team, state = None):
    
    ### Constants
    
    self.name = name
    self.team = team
    
    ### Next action
    
    # Switch takes precedence over Move
    # Switch: 1 - 6 \ {unavailable Pokemon}, 0: not set
    # Move 1 - 4 \ {unavailable moves}, 0: struggle (no PP remaining for any move)
    self.nextActionSet = False
    self.nextSwitch = 0
    self.nextMove = 0
    
    ### State
    
    if state is None:
      
      # Stat modifiers (only for currently active Pokemon)
      self.mAttack = 6
      self.mDefense = 6
      self.mSpecial = 6
      self.mSpeed = 6
      self.mAccuracy = 6
      self.mEvasion = 6
      
      # Currently active Pokemon
      self.cP = 0
      
      # Pokemon
      self.nP = self.team.size
      if self.nP < 1:
        exit('[Trainer]: Too few Pokemon in team')
      if self.nP > 6:
        exit('[Trainer]: Too many Pokemon in team')
      self.pokemon = []
      for iP in range(self.nP):
        tempPokemon = Pokemon.Pokemon(team[iP])
        self.pokemon.append(tempPokemon)
      
    else:
      self.setState(state)
  
  def setNextMove(self, switch, move):
    if self.nextActionSet:
      exit('[setNextMove]: Move already set!')
    if switch < 0 or switch > self.nP or move < 0 or move > self.pokemon[self.cP].nM:
      exit('[setNextMove]: Illegal move set by Trainer ' + self.name + '!')
    
    if switch == 0 and move == 0: # Struggle
      self.nextSwitch = switch
      self.nextMove = move
      self.nextActionSet = True
    elif switch > 0 and switch <= self.nP: # Switch
      self.nextSwitch = switch
      self.nextMove = 0
      self.nextActionSet = True
    elif move > 0 and move <= self.pokemon[self.cP].nM: # Move
      self.nextSwitch = 0
      self.nextMove = move
      self.nextActionSet = True
  
  def setState(self, state):
    self.mAttack = state[0]
    self.mDefense = state[1]
    self.mSpecial = state[2]
    self.mSpeed = state[3]
    self.mAccuracy = state[4]
    self.mEvasion = state[5]
    
    self.cP = state[6]
    
    self.nP = state[7]
    self.pokemon = []
    for iP in range(self.nP):
      tempPokemon = Pokemon.Pokemon(self.team[iP], state[8][iP])
      self.pokemon.append(tempPokemon)
  
  def getState(self):
    # Put everything in tempState and return it
    tempState = []
    
    tempState.append(self.mAttack)
    tempState.append(self.mDefense)
    tempState.append(self.mSpecial)
    tempState.append(self.mSpeed)
    tempState.append(self.mAccuracy)
    tempState.append(self.mEvasion)
    
    tempState.append(self.cP)
    
    tempState.append(self.nP)
    
    tempPokemonState = []
    for iP in range(self.nP):
      tempPokemonState.append(self.pokemon[iP].getState())
    tempState.append(tempPokemonState)
    
    return tempState
  
  def resetNextMove(self):
    self.nextActionSet = False
    self.nextSwitch = 0
    self.nextMove = 0
  
  def printSelf(self):
    print('Trainer ' + self.name + ' has ' + str(self.nP) + ' Pokemon:')
    for iP in range (self.nP):
      self.pokemon[iP].printSelf()
#