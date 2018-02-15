import numpy as np

import Constants as c
import Pokemon

class Trainer:
  def __init__(self, name):
    self.currentPokemon = 0
    self.name = name
    self.nextMove = -1
    self.numberofPokemon = 0
    self.pokemon = []
  
  def setTeam(self, team):
    # Number of Pokemon in the team
    self.numberofPokemon = team.size
    
    if self.numberofPokemon < 1:
      exit('Too few Pokemon in team')
    if self.numberofPokemon > 6:
      exit('Too many Pokemon in team')
    
    for i in range (0, self.numberofPokemon):
      temp = Pokemon.Pokemon(team[i])
      self.pokemon.append(temp)
  
  def printSelf(self):
    print('Trainer ' + self.name + ' has ' + str(self.numberofPokemon) + ' Pokemon:')
    for i in range (0, self.numberofPokemon):
      self.pokemon[i].printSelf()
#