import numpy as np

import Pokemon

class Battle:
  def __init__(self):
    self.blue = []
    self.over = False
    self.red = []
    
  
  def setBlue(self, team):
    # Number of Pokemon in the team
    number = team.size
    if number < 1 or number > 6:
      return False
    
    for i in range (0, number):
      temp = Pokemon.Pokemon(team[i])
      self.blue.append(temp)
    
    return True
  
  def setRed(self, team):
    # Number of Pokemon in the team
    number = team.size
    if number < 1 or number > 6:
      return False
    
    for i in range (0, number):
      temp = Pokemon.Pokemon(team[i])
      self.red.append(temp)
    
    return True
  
#