import numpy as np
import Pokemon

class Battle:
  def __init__(self):
    x = 0
    self.red = []
    self.blue = []
  
  def setRed(self, team):
    # Number of Pokemon in the team
    number = team.size
    # if less than 1 or more than 6, cast exception?
    
    for i in range (0, number):
      temp = Pokemon.Pokemon(team[i])
      self.red.append(temp)
    
    # print(self.red[0].stats)
    
  def setBlue(self, team):
    # Number of Pokemon in the team
    number = team.size
    # if less than 1 or more than 6, cast exception?
    
    for i in range (0, number):
      temp = Pokemon.Pokemon(team[i])
      self.blue.append(temp)
    
    # print(self.blue)