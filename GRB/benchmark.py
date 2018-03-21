import numpy as np
import time

import Battle
import Constants as c
import Load
import MonteCarloTreeSearchAI
import RandomAI
import SoftmaxLinearAI

# Variables
nBattles = 1000
nSearch = 100
temperature = 0.1

# Start runtime timer
startTime = time.time()

# Initialize results file
results = open('benchmark.txt', 'w')

# RandomAI
RAI = RandomAI.AI()

# Start benchmark
print('Start benchmark! [Total number of battles: %d, Monte Carlo Tree Search depth: %d]' % ((9 * 6 * nBattles), nSearch))

for iSetup in range(9):

  # Do setup specific stuff
  if iSetup == 0:
    print('Start green V green! [Battles per setup: %d]' % (nBattles))
    
    results.write('###\n')
    results.write('### green V green\n')
    results.write('###\n\n')
    
    # Teams
    teams = [c.team1, c.team1]
    
    # Hard Coded AI
    WHCAI = [2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
    BHCAI = [2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
    
    # Softmax Linear AI
    SLAI = SoftmaxLinearAI.AI(0, temperature, Load.loadFloatMatrix('weightsGreenGreen', c.nOutputs, c.nInputs))
    
    # Monte Carlo Tree Search AI
    MCTSAI = MonteCarloTreeSearchAI.AI(c.team1, c.team1, nSearch)
  
  elif iSetup == 1:
    print('Start red V red! [Battles per setup: %d]' % (nBattles))
    
    results.write('###\n')
    results.write('### red V red\n')
    results.write('###\n\n')
    
    # Teams
    teams = [c.team2, c.team2]
    
    # Hard Coded AI
    WHCAI = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
    BHCAI = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
    
    # Softmax Linear AI
    SLAI = SoftmaxLinearAI.AI(0, temperature, Load.loadFloatMatrix('weightsRedRed', c.nOutputs, c.nInputs))
    
    # Monte Carlo Tree Search AI
    MCTSAI = MonteCarloTreeSearchAI.AI(c.team2, c.team2, nSearch)
    
  elif iSetup == 2:
    print('Start blue V blue! [Battles per setup: %d]' % (nBattles))
    
    results.write('###\n')
    results.write('### blue V blue\n')
    results.write('###\n\n')
    
    # Teams
    teams = [c.team3, c.team3]
    
    # Hard Coded AI
    WHCAI = [2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
    BHCAI = [2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
    
    # Softmax Linear AI
    SLAI = SoftmaxLinearAI.AI(0, temperature, Load.loadFloatMatrix('weightsBlueBlue', c.nOutputs, c.nInputs))
    
    # Monte Carlo Tree Search AI
    MCTSAI = MonteCarloTreeSearchAI.AI(c.team3, c.team3, nSearch)
    
  elif iSetup == 3:
    print('Start green V red! [Battles per setup: %d]' % (nBattles))
    
    results.write('###\n')
    results.write('### green V red\n')
    results.write('###\n\n')
    
    # Teams
    teams = [c.team1, c.team2]
    
    # Hard Coded AI
    WHCAI = [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
    BHCAI = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
    
    # Softmax Linear AI
    SLAI = SoftmaxLinearAI.AI(0, temperature, Load.loadFloatMatrix('smoothGreenRed', c.nOutputs, c.nInputs))
    
    # Monte Carlo Tree Search AI
    MCTSAI = MonteCarloTreeSearchAI.AI(c.team2, c.team1, nSearch)
    
  elif iSetup == 4:
    print('Start green V blue! [Battles per setup: %d]' % (nBattles))
    
    results.write('###\n')
    results.write('### green V blue\n')
    results.write('###\n\n')
    
    # Teams
    teams = [c.team1, c.team3]
    
    # Hard Coded AI
    WHCAI = [2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
    BHCAI = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
    
    # Softmax Linear AI
    SLAI = SoftmaxLinearAI.AI(0, temperature, Load.loadFloatMatrix('smoothGreenBlue', c.nOutputs, c.nInputs))
    
    # Monte Carlo Tree Search AI
    MCTSAI = MonteCarloTreeSearchAI.AI(c.team3, c.team1, nSearch)
    
  elif iSetup == 5:
    print('Start red V green! [Battles per setup: %d]' % (nBattles))
    
    results.write('###\n')
    results.write('### red V green\n')
    results.write('###\n\n')
    
    # Teams
    teams = [c.team2, c.team1]
    
    # Hard Coded AI
    WHCAI = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
    BHCAI = [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
    
    # Softmax Linear AI
    SLAI = SoftmaxLinearAI.AI(0, temperature, Load.loadFloatMatrix('smoothRedGreen', c.nOutputs, c.nInputs))
    
    # Monte Carlo Tree Search AI
    MCTSAI = MonteCarloTreeSearchAI.AI(c.team1, c.team2, nSearch)
    
  elif iSetup == 6:
    print('Start red V blue! [Battles per setup: %d]' % (nBattles))
    
    results.write('###\n')
    results.write('### red V blue\n')
    results.write('###\n\n')
    
    # Teams
    teams = [c.team2, c.team3]
    
    # Hard Coded AI
    WHCAI = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
    BHCAI = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
    
    # Softmax Linear AI
    SLAI = SoftmaxLinearAI.AI(0, temperature, Load.loadFloatMatrix('smoothRedBlue', c.nOutputs, c.nInputs))
    
    # Monte Carlo Tree Search AI
    MCTSAI = MonteCarloTreeSearchAI.AI(c.team3, c.team2, nSearch)
    
  elif iSetup == 7:
    print('Start blue V green! [Battles per setup: %d]' % (nBattles))
    
    results.write('###\n')
    results.write('### blue V green\n')
    results.write('###\n\n')
    
    # Teams
    teams = [c.team3, c.team1]
    
    # Hard Coded AI
    WHCAI = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
    BHCAI = [2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
    
    # Softmax Linear AI
    SLAI = SoftmaxLinearAI.AI(0, temperature, Load.loadFloatMatrix('smoothBlueGreen', c.nOutputs, c.nInputs))
    
    # Monte Carlo Tree Search AI
    MCTSAI = MonteCarloTreeSearchAI.AI(c.team1, c.team3, nSearch)
    
  elif iSetup == 8:
    print('Start blue V red! [Battles per setup: %d]' % (nBattles))
    
    results.write('###\n')
    results.write('### blue V red\n')
    results.write('###\n\n')
    
    # Teams
    teams = [c.team3, c.team2]
    
    # Hard Coded AI
    WHCAI = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
    BHCAI = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
    
    # Softmax Linear AI
    SLAI = SoftmaxLinearAI.AI(0, temperature, Load.loadFloatMatrix('smoothBlueRed', c.nOutputs, c.nInputs))
    
    # Monte Carlo Tree Search AI
    MCTSAI = MonteCarloTreeSearchAI.AI(c.team2, c.team3, nSearch)
    
  HCHC = 0
  SLR = 0
  SLHC = 0
  SLMCTS = 0
  MCTSR = 0
  MCTSHC = 0
  MCTSSL = 0
  tactsSL = {}
  tactsMCTS = {}
  for iBattle in range(nBattles):
    
    ###
    ### 1:
    ### White: Hard Coded, Black: Hard Coded
    ###
    
    battle = Battle.Battle(teams[0], teams[1], False)
    while battle.running:
      battle.trainers[0].setNextAction(WHCAI[battle.round])
      
      battle.trainers[1].setNextAction(BHCAI[battle.round])
      
      battle.progress()
    
    # Count white wins
    HCHC += (battle.winner + 1) % 2
    
    ###
    ### 2:
    ### White: Softmax Linear, Black: Random
    ###
    
    battle = Battle.Battle(teams[0], teams[1], False)
    stringSL = ''
    while battle.running:
      actionSL = SLAI.getAction(battle.getFeatures(c.amWhite))
      stringSL += str(actionSL)
      battle.trainers[0].setNextAction(actionSL)
      
      battle.trainers[1].setNextAction(RAI.getAction(battle.trainers[1].pokemon[battle.trainers[1].cP - 1].moves[2].cPP))
      
      battle.progress()
    
    # Count white wins
    SLR += (battle.winner + 1) % 2
    
    if stringSL in tactsSL:
      tactsSL[stringSL] += 1
    else:
      tactsSL[stringSL] = 1
    
    ###
    ### 3:
    ### White: Softmax Linear, Black: Hard Coded
    ###
    
    battle = Battle.Battle(teams[0], teams[1], False)
    stringSL = ''
    while battle.running:
      actionSL = SLAI.getAction(battle.getFeatures(c.amWhite))
      stringSL += str(actionSL)
      battle.trainers[0].setNextAction(actionSL)
      
      battle.trainers[1].setNextAction(BHCAI[battle.round])
      
      battle.progress()
    
    # Count white wins
    SLHC += (battle.winner + 1) % 2
    
    if stringSL in tactsSL:
      tactsSL[stringSL] += 1
    else:
      tactsSL[stringSL] = 1
    
    ###
    ### 4:
    ### White: Softmax Linear, Black: Monte Carlo Tree Search
    ###
    
    battle = Battle.Battle(teams[0], teams[1], False)
    stringSL = ''
    stringMCTS = ''
    while battle.running:
      actionSL = SLAI.getAction(battle.getFeatures(c.amWhite))
      stringSL += str(actionSL)
      battle.trainers[0].setNextAction(actionSL)
      
      actionMCTS = MCTSAI.getAction(battle.getState(c.amBlack))
      stringMCTS += str(actionMCTS)
      battle.trainers[1].setNextAction(actionMCTS)
      
      battle.progress()
    
    # Count white wins
    SLMCTS += (battle.winner + 1) % 2
    # Count black wins
    MCTSSL += battle.winner
    
    if stringSL in tactsSL:
      tactsSL[stringSL] += 1
    else:
      tactsSL[stringSL] = 1
    if stringMCTS in tactsMCTS:
      tactsMCTS[stringMCTS] += 1
    else:
      tactsMCTS[stringMCTS] = 1
    
    ###
    ### 5:
    ### White: Random, Black: Monte Carlo Tree Search
    ###
    
    battle = Battle.Battle(teams[0], teams[1], False)
    stringMCTS = ''
    while battle.running:
      battle.trainers[0].setNextAction(RAI.getAction(battle.trainers[0].pokemon[battle.trainers[0].cP - 1].moves[2].cPP))
      
      actionMCTS = MCTSAI.getAction(battle.getState(c.amBlack))
      stringMCTS += str(actionMCTS)
      battle.trainers[1].setNextAction(actionMCTS)
      
      battle.progress()
    
    # Count black wins
    MCTSR += battle.winner
    
    if stringMCTS in tactsMCTS:
      tactsMCTS[stringMCTS] += 1
    else:
      tactsMCTS[stringMCTS] = 1
    
    ###
    ### 6:
    ### White: Hard Coded, Black: Monte Carlo Tree Search
    ###
    
    battle = Battle.Battle(teams[0], teams[1], False)
    stringMCTS = ''
    while battle.running:
      battle.trainers[0].setNextAction(WHCAI[battle.round])
      
      actionMCTS = MCTSAI.getAction(battle.getState(c.amBlack))
      stringMCTS += str(actionMCTS)
      battle.trainers[1].setNextAction(actionMCTS)
      
      battle.progress()
    
    # Count black wins
    MCTSHC += battle.winner
    
    if stringMCTS in tactsMCTS:
      tactsMCTS[stringMCTS] += 1
    else:
      tactsMCTS[stringMCTS] = 1
    
    # Print progress notice every tenth percent
    if iBattle % int(nBattles / 10) == 0 and iBattle != 0:
      print('Battled ' + str(int(100 * iBattle / nBattles)) + '%')
  
  results.write('# Hard Coded:\n')
  results.write('V Hard Coded: ' + str(100 * HCHC / nBattles) + '% wins\n\n')
  
  valuesSL = sorted(tactsSL.values(), reverse = True)
  results.write('## Softmax Linear:\n\n')
  results.write('# Three most common strategies: \n')
  results.write('\'' + list(tactsSL.keys())[list(tactsSL.values()).index(valuesSL[0])] + '\' at ' + str(100 * valuesSL[0] / np.sum(valuesSL)) + '%\n')
  results.write('\'' + list(tactsSL.keys())[list(tactsSL.values()).index(valuesSL[1])] + '\' at ' + str(100 * valuesSL[1] / np.sum(valuesSL)) + '%\n')
  results.write('\'' + list(tactsSL.keys())[list(tactsSL.values()).index(valuesSL[2])] + '\' at ' + str(100 * valuesSL[2] / np.sum(valuesSL)) + '%\n\n')
  
  results.write('# Win percentages: \n')
  results.write('V Random: ' + str(100 * SLR / nBattles) + '% wins\n')
  results.write('V Hard Coded: ' + str(100 * SLHC / nBattles) + '% wins\n')
  results.write('V Monte Carlo Tree Search: ' + str(100 * SLMCTS / nBattles) + '% wins\n\n')
  
  valuesMCTS = sorted(tactsMCTS.values(), reverse = True)
  results.write('## Monte Carlo Tree Search:\n\n')
  results.write('# Three most common strategies: \n')
  results.write('\'' + list(tactsMCTS.keys())[list(tactsMCTS.values()).index(valuesMCTS[0])] + '\' at ' + str(100 * valuesMCTS[0] / np.sum(valuesMCTS)) + '%\n')
  results.write('\'' + list(tactsMCTS.keys())[list(tactsMCTS.values()).index(valuesMCTS[1])] + '\' at ' + str(100 * valuesMCTS[1] / np.sum(valuesMCTS)) + '%\n')
  results.write('\'' + list(tactsMCTS.keys())[list(tactsMCTS.values()).index(valuesMCTS[2])] + '\' at ' + str(100 * valuesMCTS[2] / np.sum(valuesMCTS)) + '%\n\n')
  
  results.write('# Win percentages: \n')
  results.write('V Random: ' + str(100 * MCTSR / nBattles) + '% wins\n')
  results.write('V Hard Coded: ' + str(100 * MCTSHC / nBattles) + '% wins\n')
  results.write('V Softmax Linear: ' + str(100 * MCTSSL / nBattles) + '% wins\n\n')

results.close()

# Print runtime
if time.time() - startTime < 60:
  print('Runtime: %d seconds' % (time.time() - startTime))
elif time.time() - startTime > 60 and time.time() - startTime < 3600:
  print('Runtime: %d minutes and %d seconds' % ((time.time() - startTime) / 60, (time.time() - startTime) % 60))
else:
  print('Runtime: %d hours, %d minutes and %d seconds' % ((time.time() - startTime) / 3600, ((time.time() - startTime) % 3600) / 60, (time.time() - startTime) % 60))
#