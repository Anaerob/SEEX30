import numpy as np

testArray = np.array([[0, 1], [10, 11]])

statReduction = np.array([100, 66, 50, 40, 33, 28, 25])
statIncrement = np.array([100, 150, 200, 250, 300, 350, 400])

# Pokemon

# base stats
PBS = np.array([[0, 0, 0, 0, 0],
  [45, 49, 49, 65, 45], # bulbasaur
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [39, 52, 43, 50, 65], # charmander
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [44, 48, 65, 50, 43], # squirtle
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0]])

# moves
PM = np.array([[0, 0, 0, 0],
  [1, 3, 0, 0], # bulbasaur
  [0, 0, 0, 0],
  [0, 0, 0, 0],
  [2, 3, 0, 0], # charmander
  [0, 0, 0, 0],
  [0, 0, 0, 0],
  [1, 4, 0, 0], # squirtle
  [0, 0, 0, 0],
  [0, 0, 0, 0]])

# Moves

# stats
MS = np.array([[0, 0, 0],
  [40, 100, 35], # scratch
  [35, 95, 35], # tackle
  [0, 100, 40], # growl
  [0, 100, 35]]) # tail whip

# modifiers
MM = np.array([[0, 0, 0, 0],
  [0, 0, 0, 0], # scratch
  [0, 0, 0, 0], # tackle
  [-1, 0, 0, 0], # growl
  [0, -1, 0, 0]]) # tail whip

# scenario 1 specific

# teams
t1 = np.array([1])
t2 = np.array([4])
t3 = np.array([7])

# scenario 2 specific

# teams
team = np.array([3, 6, 9])

#