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
        
        for iAction in range(len(c.actions)):
          # Add an action to the move list
          wTry = list(wMoves)
          wTry.append(c.actions[iAction])
          bTry = list(bMoves)
          bTry.append(c.actions[iAction])
          
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
        if np.random.random() < self.epsilon:
          wQ[0] = 1
          wQ[1] = 1
        
        # Set probability of choosing zero PP move to zero
        # We only need to check stat modifier in scenario 1
        if sim.trainers[0].pokemon[sim.trainers[0].cP - 1].moves[2].cPP == 0:
          wQ[1] = -float('inf')
        
        # Use a very hard Softmax to choose action - useful if two actions are considered equal!
        wPolicy = np.exp(wQ / self.temperature) / np.sum(np.exp(wQ / self.temperature), axis = 0)
        wChoice = np.random.choice(c.actions, p = wPolicy)
        
        if self.printMe:
          print('Q: ' + str(wQ) + ', Policy: ' + str(wPolicy) + ', Choice: ' + str(wChoice))
        
        # Same as for white
        if np.random.random() < self.epsilon:
          bQ[0] = 1
          bQ[1] = 1
        
        if sim.trainers[1].pokemon[sim.trainers[1].cP - 1].moves[2].cPP == 0:
          bQ[1] = -float('inf')
        
        bPolicy = np.exp(bQ / self.temperature) / np.sum(np.exp(bQ / self.temperature), axis = 0)
        bChoice = np.random.choice(c.actions, p = bPolicy)
        
        wMoves.append(wChoice)
        bMoves.append(bChoice)
        
        sim.trainers[0].setNextAction(wChoice)
        sim.trainers[1].setNextAction(bChoice)
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
    
    # Final PP check
    sim = Battle.Battle(self.whiteTeam, self.blackTeam, False, state)
    if sim.trainers[0].pokemon[sim.trainers[0].cP - 1].moves[2].cPP == 0:
      Q[1] = -float('inf')
    
    policy = np.exp(Q / self.temperature) / np.sum(np.exp(Q / self.temperature), axis = 0)
    choice = np.random.choice(c.actions, p = policy)
    
    return choice
#