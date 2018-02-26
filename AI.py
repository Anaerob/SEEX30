import numpy as np

import Battle

class AI:
  def __init__(self, myTeam, opTeam):
    self.x = 1
    
    self.myTeam = myTeam
    self.opTeam = opTeam
  
  def simpleMCS(self, state, policy = None):
    # [3]: trainers, [0]: blue (this AI PoV) trainer, [8]: pokemon, [3][0][6]: current pokemon, [4]: moves, [i]: move number i (move1 -> i = 0 etc)
    if state[3][0][8][state[3][0][6]][4][0] == 0 and state[3][0][8][state[3][0][6]][4][1] == 0:
      return 0
    elif state[3][0][8][state[3][0][6]][4][0] == 0:
      return 2
    elif state[3][0][8][state[3][0][6]][4][1] == 0:
      return 1
    
    nSim = 1000000
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
        
        #sim.printSelf()
        #print((sim.winner + 1) % 2)
        wins[iAction] += (sim.winner + 1) % 2
    print(wins)
    return 1 + wins.index(max(wins))
  
  def getMove(self, state = None):
    if state == None:
      return [0, np.random.randint(1, 3)]
      
    else:
      return [0, self.simpleMCS(state)]
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