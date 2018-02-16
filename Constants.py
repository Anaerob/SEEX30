import numpy as np

testArray = np.array([[0, 1], [10, 11]])

statReduction = np.array([100, 66, 50, 40, 33, 28, 25])
statIncrement = np.array([100, 150, 200, 250, 300, 350, 400])
statModifiers = np.array([25, 28, 33, 40, 50, 66, 100, 150, 200, 250, 300, 350, 400]) # [6] = 100

# Pokemon

# names
PN = ['0',
  'Bulbasaur', '2', '3',
  'Charmander', '5', '6',
  'Squirtle', '8', '9']

# base stats [0: hp, 1: attack, 2: defense, 3: special, 4: speed]
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

# moves [0: move 1, 1: move 2, 2: move 3, 3: move 4]
PM = np.array([[0, 0, 0, 0],
  [2, 3, 0, 0], # bulbasaur
  [0, 0, 0, 0],
  [0, 0, 0, 0],
  [1, 3, 0, 0], # charmander
  [0, 0, 0, 0],
  [0, 0, 0, 0],
  [2, 4, 0, 0], # squirtle
  [0, 0, 0, 0],
  [0, 0, 0, 0]])

# Moves

# names
MN = ['Struggle',
  'Scratch',
  'Tackle',
  'Growl',
  'Tail Whip']

# stats [0: power, 1: accuracy, 2: pp]
MS = np.array([[50, 256, 10], # struggle 165
  [40, 255, 35], # scratch 10
  [35, 242, 35], # tackle 33
  [0, 255, 40], # growl 45
  [0, 255, 35]]) # tail whip 39

# modifiers [0: chance, 1: attack, 2: defense, 3: special, 4: speed]
MM = np.array([[0, 0, 0, 0, 0], # struggle 165
  [0, 0, 0, 0, 0], # scratch
  [0, 0, 0, 0, 0], # tackle
  [256, -1, 0, 0, 0], # growl
  [256, 0, -1, 0, 0]]) # tail whip

# recoil [0: percent recoil damage]
MR = np.array([[50],
  [0],
  [0],
  [0],
  [0]])
# scenario 1 specific

# teams
t1 = np.array([1])
t2 = np.array([4])
t3 = np.array([7])

# scenario 2 specific

# teams
team = np.array([3, 6, 9])

#