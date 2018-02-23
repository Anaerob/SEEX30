import numpy as np

import Constants as c
import Pokemon

class Trainer:
  def __init__(self, name):
    
    ### Constants
    
    self.name = name
    
    ### State variables
    
    ## Stat modifiers (only for currently active Pokemon)
    self.mAttack = 6
    self.mDefense = 6
    self.mSpecial = 6
    self.mSpeed = 6
    self.mAccuracy = 6
    self.mEvasion = 6
    
    ## Pokemon
    self.pokemon = []
    # Currently active Pokemon
    self.cP = 0 
    
    ### Next action
    
    # Switch takes precedence over Move
    # Switch: 1 - 6 \ {unavailable Pokemon}, 0: not set
    # Move 1 - 4 \ {unavailable moves}, 0: struggle (no PP remaining for any move)
    self.nextActionSet = False
    self.nextSwitch = 0
    self.nextMove = 0
  
  def setNextMove(self, switch, move):
    if switch < 0 or switch > self.nP or move < 0 or move > self.pokemon[self.cP].nM:
      exit('Illegal move set by Trainer ' + self.name + '!')
    
    if switch == 0 and move == 0: # Struggle
      self.nextSwitch = switch
      self.nextMove = move
      self.nextActionSet = True
    elif switch > 0 and switch <= 6: # Switch
      self.nextSwitch = switch
      self.nextMove = 0
      self.nextActionSet = True
    elif move > 0 and move <= 4: # Move
      self.nextSwitch = 0
      self.nextMove = move
      self.nextActionSet = True
  
  def resetNextMove(self):
    self.nextActionSet = False
    self.nextSwitch = 0
    self.nextMove = 0
  
  def setTeam(self, team):
    # Number of Pokemon in the team
    self.nP = team.size
    
    if self.nP < 1:
      exit('Too few Pokemon in team')
    if self.nP > 6:
      exit('Too many Pokemon in team')
    
    for iP in range (0, self.nP):
      tempPokemon = Pokemon.Pokemon(team[iP])
      self.pokemon.append(tempPokemon)
  
  def printSelf(self):
    print('Trainer ' + self.name + ' has ' + str(self.nP) + ' Pokemon:')
    for iP in range (0, self.nP):
      self.pokemon[iP].printSelf()
#