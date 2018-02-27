import numpy as np

import Battle

class AI:
  def __init__(self, myTeam, opTeam):
    self.x = 1
    self.recursionStart = 100
    self.recursionEnd = 10 # **2 = 16
    
    self.myTeam = myTeam
    self.opTeam = opTeam
  
  def simpleMCS(self, nSim, state, policy = None):
    # [3]: trainers, [0]: blue (this AI PoV) trainer, [8]: pokemon, [3][0][6]: current pokemon, [4]: moves, [i]: move number i (move1 -> i = 0 etc)
    if state[3][0][8][state[3][0][6]][4][0] == 0 and state[3][0][8][state[3][0][6]][4][1] == 0:
      return 0
    elif state[3][0][8][state[3][0][6]][4][0] == 0:
      return 2
    elif state[3][0][8][state[3][0][6]][4][1] == 0:
      return 1
    
    wins = [0, 0]
    
    for iAction in range(2):
      for iSim in range(nSim):
        sim = Battle.Battle([self.myTeam, self.opTeam], False, state)
        
        sim.blue.setNextMove(0, iAction + 1)
        sim.red.setNextMove(0, np.random.randint(1, 3))
        sim.progress()
        
        while sim.running:
          if sim.blue.pokemon[sim.blue.cP].moves[1].cPP == 0 and sim.blue.pokemon[sim.blue.cP].moves[2].cPP == 0:
            sim.blue.setNextMove(0, 0)
          elif sim.blue.pokemon[sim.blue.cP].moves[1].cPP == 0:
            sim.blue.setNextMove(0, 2)
          elif sim.blue.pokemon[sim.blue.cP].moves[2].cPP == 0:
            sim.blue.setNextMove(0, 1)
          else:
            sim.blue.setNextMove(0, np.random.randint(1, 3))
          if sim.red.pokemon[sim.red.cP].moves[1].cPP == 0 and sim.red.pokemon[sim.red.cP].moves[2].cPP == 0:
            sim.red.setNextMove(0, 0)
          elif sim.red.pokemon[sim.red.cP].moves[1].cPP == 0:
            sim.red.setNextMove(0, 2)
          elif sim.red.pokemon[sim.red.cP].moves[2].cPP == 0:
            sim.red.setNextMove(0, 1)
          else:
            sim.red.setNextMove(0, np.random.randint(1, 3))
          sim.progress()
        
        wins[iAction] += (sim.winner + 1) % 2
    
    #print(wins)
    return [0, 1 + wins.index(max(wins))]
  
  def simpleMCSRecursion(self, nSim, state):
    # [3]: trainers, [0]: blue (this AI PoV) trainer, [8]: pokemon, [3][0][6]: current pokemon, [4]: moves, [i]: move number i (move1 -> i = 0 etc)
    if state[3][0][8][state[3][0][6]][4][0] == 0 and state[3][0][8][state[3][0][6]][4][1] == 0:
      return 0
    elif state[3][0][8][state[3][0][6]][4][0] == 0:
      return 2
    elif state[3][0][8][state[3][0][6]][4][1] == 0:
      return 1
    
    blueRecAI = AI(self.myTeam, self.opTeam)
    redRecAI = AI(self.opTeam, self.myTeam)
    
    wins = [0, 0]
    
    for iAction in range(2):
      for iSim in range(nSim):
        sim = Battle.Battle([self.myTeam, self.opTeam], False, state)
        
        sim.blue.setNextMove(0, iAction + 1)
        sim.red.setNextMove(0, np.random.randint(1, 3))
        sim.progress()
        
        while sim.running:
          if sim.blue.pokemon[sim.blue.cP].moves[1].cPP == 0 and sim.blue.pokemon[sim.blue.cP].moves[2].cPP == 0:
            sim.blue.setNextMove(0, 0)
          elif sim.blue.pokemon[sim.blue.cP].moves[1].cPP == 0:
            sim.blue.setNextMove(0, 2)
          elif sim.blue.pokemon[sim.blue.cP].moves[2].cPP == 0:
            sim.blue.setNextMove(0, 1)
          else:
            if nSim > self.recursionEnd ** 2:
              move = blueRecAI.simpleMCSRecursion(int(nSim / self.recursionEnd), sim.getState(False))
            else:
              move = blueRecAI.simpleMCS(self.recursionEnd, sim.getState(False))
            sim.blue.setNextMove(move[0], move[1])
          if sim.red.pokemon[sim.red.cP].moves[1].cPP == 0 and sim.red.pokemon[sim.red.cP].moves[2].cPP == 0:
            sim.red.setNextMove(0, 0)
          elif sim.red.pokemon[sim.red.cP].moves[1].cPP == 0:
            sim.red.setNextMove(0, 2)
          elif sim.red.pokemon[sim.red.cP].moves[2].cPP == 0:
            sim.red.setNextMove(0, 1)
          else:
            if nSim > self.recursionEnd ** 2:
              move = redRecAI.simpleMCSRecursion(int(nSim / self.recursionEnd), sim.getState(True))
            else:
              move = redRecAI.simpleMCS(self.recursionEnd, sim.getState(True))
            sim.red.setNextMove(move[0], move[1])
          sim.progress()
        
        wins[iAction] += (sim.winner + 1) % 2
    
    if nSim == self.recursionStart:
      print(wins)
    return [0, 1 + wins.index(max(wins))]
  
  def getMove(self, state = None):
    if state == None:
      return [0, np.random.randint(1, 3)]
      
    else:
      return self.simpleMCSRecursion(self.recursionStart, state)
    # MCTS first implementation try:
    """else:
      
      nBattles = 10
      dPlays = {}
      dWins = {}
      
      for iBattle in range(nBattles):
        moves = []
        battleSim = Battle.Battle([self.myTeam, self.opTeam], state)
        
        while battleSim.running:
          move = np.random.randint(1, 3)
          moves.append(move)
          
          battleSim.blue.setNextMove(0, move)
          battleSim.red.setNextMove(0, np.random.randint(1, 3))
          battleSim.progress()
        
        string = ''
        i = 0
        for i in range(len(moves)):
          string += str(moves[i])
          if string in dPlays:
            dPlays[string] += 1
            dWins[string] += (battleSim.winner + 1) % 2
          else:
            dPlays[string] = 1
            dWins[string] = (battleSim.winner + 1) % 2
            break
        print('dPlays: ' + str(dPlays))
        print('dWins: ' + str(dWins))"""
#