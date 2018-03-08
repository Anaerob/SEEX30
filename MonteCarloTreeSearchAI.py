import numpy as np

import Battle
import Constants as c

class AI:
  def __init__(self, whiteTeam, blackTeam, nSearch):
    self.nSearch = nSearch
    self.epsilon = 0.05
    self.temperature = 0.01
    self.printMe = False
    
    self.whiteTeam = whiteTeam
    self.blackTeam = blackTeam
  
  def getAction(self, state):
    # List of all actions
    actions = [1, 2]
    
    # Initialize the dictionaries
    wPlayed = {}
    wWins = {}
    bPlayed = {}
    bWins = {}
    
    for iSearch in range(self.nSearch):
      
      # Initialize a simulation starting from the given state
      sim = Battle.Battle(self.whiteTeam, self.blackTeam, False, state)
      wMoves = []
      bMoves = []
      
      while sim.running:
        
        # Build Q for all actions by checking tree, or exploring if not in tree
        wQ = np.array([])
        bQ = np.array([])
        
        for iAction in range(len(actions)):
          # Add an action to the move list
          wTry = list(wMoves)
          wTry.append(actions[iAction])
          bTry = list(bMoves)
          bTry.append(actions[iAction])
          
          # Build a string used to check dictionary
          wString = ''
          bString = ''
          for iTry in range(len(wTry)):
            wString += str(wTry[iTry])
            bString += str(bTry[iTry])
          
          if self.printMe:
            print('Try: ' + str(wTry) + ', String: ' + str(wString))
          
          if wString in wPlayed:
            # If it's already in the tree, add the win probability to Q
            wQ = np.append(wQ, wWins[wString] / wPlayed[wString])
          else:
            # If not, explore by setting a very high probability for picking
            wQ = np.append(wQ, 1.1)
          
          # Same as for white
          if bString in bPlayed:
            bQ = np.append(bQ, bWins[bString] / bPlayed[bString])
          else:
            bQ = np.append(bQ, 1.1)
        
        # Epsilon-greedy with softmax as simulation policy
        if np.random.random() > self.epsilon:
          # Use a very hard Softmax to choose action - useful if two actions are considered equal!
          wPolicy = np.exp(wQ / self.temperature) / np.sum(np.exp(wQ / self.temperature), axis = 0)
          wChoice = np.random.choice(actions, p = wPolicy)
          
          if self.printMe:
            print('Q: ' + str(wQ) + ', Policy: ' + str(wPolicy) + ', Choice: ' + str(wChoice))
          
        else:
          wChoice = actions[np.random.randint(len(actions))]
        
        # Same as for white
        if np.random.random() > self.epsilon:
          bPolicy = np.exp(bQ / self.temperature) / np.sum(np.exp(bQ / self.temperature), axis = 0)
          bChoice = np.random.choice(actions, p = bPolicy)
          
        else:
          bChoice = actions[np.random.randint(len(actions))]
        
        wMoves.append(wChoice)
        bMoves.append(bChoice)
        
        sim.white.setNextAction(wChoice)
        sim.black.setNextAction(bChoice)
        sim.progress()
      
      # Update and extend the search tree
      wString = ''
      for i in range(len(wMoves)):
        wString += str(wMoves[i])
        bString += str(bMoves[i])
        if wString in wPlayed:
          wPlayed[wString] += 1
          wWins[wString] += (sim.winner + 1) % 2
        else:
          wPlayed[wString] = 1
          wWins[wString] = (sim.winner + 1) % 2
          break
      
      # Same as for white
      bString = ''
      for i in range(len(bMoves)):
        if bString in bPlayed:
          bPlayed[bString] += 1
          bWins[bString] += sim.winner
        else:
          bPlayed[bString] = 1
          bWins[bString] = sim.winner
          break
    
    # Use a very hard Softmax to choose action
    Q = np.array([wWins['1'] / wPlayed['1'], wWins['2'] / wPlayed['2']])
    policy = np.exp(Q / self.temperature) / np.sum(np.exp(Q / self.temperature), axis = 0)
    choice = np.random.choice(actions, p = policy)
    
    return choice
#