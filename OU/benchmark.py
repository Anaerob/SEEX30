import numpy as np
import time

import Battle
import Constants as c
import Load
import MonteCarloTreeSearchAI
import SoftmaxLinearAI

# Variables
nBattles = 100
nSearch = 10

# Start runtime timer
startTime = time.time()

# Random AI
# np.random.choice(c.actions)

# Hard Coded AI
GGHCAI = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
GRHCAI = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
GBHCAI = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
RGHCAI = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
RRHCAI = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
RBHCAI = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
BGHCAI = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
BRHCAI = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
BBHCAI = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# Softmax Linear AI
GGSLAI = SoftmaxLinearAI.AI(0, 0, Load.loadFloatMatrix('weightsGreenGreen', c.nOutputs, c.nInputs))
GRSLAI = SoftmaxLinearAI.AI(0, 0, Load.loadFloatMatrix('smoothGreenRed', c.nOutputs, c.nInputs))
GBSLAI = SoftmaxLinearAI.AI(0, 0, Load.loadFloatMatrix('smoothGreenBlue', c.nOutputs, c.nInputs))
RGSLAI = SoftmaxLinearAI.AI(0, 0, Load.loadFloatMatrix('smoothRedGreen', c.nOutputs, c.nInputs))
RRSLAI = SoftmaxLinearAI.AI(0, 0, Load.loadFloatMatrix('weightsRedRed', c.nOutputs, c.nInputs))
RBSLAI = SoftmaxLinearAI.AI(0, 0, Load.loadFloatMatrix('smoothRedBlue', c.nOutputs, c.nInputs))
BGSLAI = SoftmaxLinearAI.AI(0, 0, Load.loadFloatMatrix('smoothBlueGreen', c.nOutputs, c.nInputs))
BRSLAI = SoftmaxLinearAI.AI(0, 0, Load.loadFloatMatrix('smoothBlueRed', c.nOutputs, c.nInputs))
BBSLAI = SoftmaxLinearAI.AI(0, 0, Load.loadFloatMatrix('weightsBlueBlue', c.nOutputs, c.nInputs))

# Monte Carlo Tree Search AI
GGMCTSAI = MonteCarloTreeSearchAI.AI(c.team1, c.team1, nSearch)
GRMCTSAI = MonteCarloTreeSearchAI.AI(c.team1, c.team2, nSearch)
GBMCTSAI = MonteCarloTreeSearchAI.AI(c.team1, c.team3, nSearch)
RGMCTSAI = MonteCarloTreeSearchAI.AI(c.team2, c.team1, nSearch)
RRMCTSAI = MonteCarloTreeSearchAI.AI(c.team2, c.team2, nSearch)
RBMCTSAI = MonteCarloTreeSearchAI.AI(c.team2, c.team3, nSearch)
BGMCTSAI = MonteCarloTreeSearchAI.AI(c.team3, c.team1, nSearch)
BRMCTSAI = MonteCarloTreeSearchAI.AI(c.team3, c.team2, nSearch)
BBMCTSAI = MonteCarloTreeSearchAI.AI(c.team3, c.team3, nSearch)

# Start benchmark
print('Start benchmark! [Total number of battles: %d]' % ((9 * 5 * nBattles)))

### ------------- ###
### GREEN V GREEN ###
### ------------- ###

print('Start green V green! [Battles per setup: %d]' % (nBattles))

SLR = 0
SLHC = 0
SLMCTS = 0
MCTSR = 0
MCTSHC = 0
for iBattle in range(nBattles):
  # White: Softmax Linear, Black: Random
  battle = Battle.Battle(c.team1, c.team1, False)
  while battle.running:
    battle.trainers[0].setNextAction(GGSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(np.random.choice(c.actions))
    battle.progress()
  SLR += (battle.winner + 1) % 2
  
  # White: Softmax Linear, Black: Hard Coded
  battle = Battle.Battle(c.team1, c.team1, False)
  while battle.running:
    battle.trainers[0].setNextAction(GGSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(GGHCAI[battle.round])
    battle.progress()
  SLHC += (battle.winner + 1) % 2
  
  # White: Softmax Linear, Black: Monte Carlo Tree Search
  battle = Battle.Battle(c.team1, c.team1, False)
  while battle.running:
    battle.trainers[0].setNextAction(GGSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(GGMCTSAI.getAction(battle.getState(c.amBlack)))
    battle.progress()
  SLMCTS += (battle.winner + 1) % 2
  
  # White: Monte Carlo Tree Search, Black: Random
  battle = Battle.Battle(c.team1, c.team1, False)
  while battle.running:
    battle.trainers[0].setNextAction(GGMCTSAI.getAction(battle.getState(c.amWhite)))
    battle.trainers[1].setNextAction(np.random.choice(c.actions))
    battle.progress()
  MCTSR += (battle.winner + 1) % 2
  
  # White: Monte Carlo Tree Search, Black: Hard Coded
  battle = Battle.Battle(c.team1, c.team1, False)
  while battle.running:
    battle.trainers[0].setNextAction(GGMCTSAI.getAction(battle.getState(c.amWhite)))
    battle.trainers[1].setNextAction(GGHCAI[battle.round])
    battle.progress()
  MCTSHC += (battle.winner + 1) % 2
  
  # Print progress notice every tenth percent
  if iBattle % int(nBattles / 10) == 0 and iBattle != 0:
    print('Battled ' + str(int(100 * iBattle / nBattles)) + '%')

print('green V green finished!')
print('Softmax Linear results: [Random: %d wins, Hard Code: %d wins, Monte Carlo Tree Search: %d wins]' % (SLR, SLHC, SLMCTS))
print('Monte Carlo Tree Search results: [Random: %d wins, Hard Code: %d wins, Softmax Linear: %d wins]' % (MCTSR, MCTSHC, (nBattles - SLMCTS)))

### --------- ###
### RED V RED ###
### --------- ###

print('Start red V red! [Battles per setup: %d]' % (nBattles))

SLR = 0
SLHC = 0
SLMCTS = 0
MCTSR = 0
MCTSHC = 0
for iBattle in range(nBattles):
  # White: Softmax Linear, Black: Random
  battle = Battle.Battle(c.team2, c.team2, False)
  while battle.running:
    battle.trainers[0].setNextAction(RRSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(np.random.choice(c.actions))
    battle.progress()
  SLR += (battle.winner + 1) % 2
  
  # White: Softmax Linear, Black: Hard Coded
  battle = Battle.Battle(c.team2, c.team2, False)
  while battle.running:
    battle.trainers[0].setNextAction(RRSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(RRHCAI[battle.round])
    battle.progress()
  SLHC += (battle.winner + 1) % 2
  
  # White: Softmax Linear, Black: Monte Carlo Tree Search
  battle = Battle.Battle(c.team2, c.team2, False)
  while battle.running:
    battle.trainers[0].setNextAction(RRSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(RRMCTSAI.getAction(battle.getState(c.amBlack)))
    battle.progress()
  SLMCTS += (battle.winner + 1) % 2
  
  # White: Monte Carlo Tree Search, Black: Random
  battle = Battle.Battle(c.team2, c.team2, False)
  while battle.running:
    battle.trainers[0].setNextAction(RRMCTSAI.getAction(battle.getState(c.amWhite)))
    battle.trainers[1].setNextAction(np.random.choice(c.actions))
    battle.progress()
  MCTSR += (battle.winner + 1) % 2
  
  # White: Monte Carlo Tree Search, Black: Hard Coded
  battle = Battle.Battle(c.team2, c.team2, False)
  while battle.running:
    battle.trainers[0].setNextAction(RRMCTSAI.getAction(battle.getState(c.amWhite)))
    battle.trainers[1].setNextAction(RRHCAI[battle.round])
    battle.progress()
  MCTSHC += (battle.winner + 1) % 2
  
  # Print progress notice every tenth percent
  if iBattle % int(nBattles / 10) == 0 and iBattle != 0:
    print('Battled ' + str(int(100 * iBattle / nBattles)) + '%')

print('red V red finished!')
print('Softmax Linear results: [Random: %d wins, Hard Code: %d wins, Monte Carlo Tree Search: %d wins]' % (SLR, SLHC, SLMCTS))
print('Monte Carlo Tree Search results: [Random: %d wins, Hard Code: %d wins, Softmax Linear: %d wins]' % (MCTSR, MCTSHC, (nBattles - SLMCTS)))

### ----------- ###
### BLUE V BLUE ###
### ----------- ###

print('Start blue V blue! [Battles per setup: %d]' % (nBattles))

SLR = 0
SLHC = 0
SLMCTS = 0
MCTSR = 0
MCTSHC = 0
for iBattle in range(nBattles):
  # White: Softmax Linear, Black: Random
  battle = Battle.Battle(c.team3, c.team3, False)
  while battle.running:
    battle.trainers[0].setNextAction(BBSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(np.random.choice(c.actions))
    battle.progress()
  SLR += (battle.winner + 1) % 2
  
  # White: Softmax Linear, Black: Hard Coded
  battle = Battle.Battle(c.team3, c.team3, False)
  while battle.running:
    battle.trainers[0].setNextAction(BBSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(BBHCAI[battle.round])
    battle.progress()
  SLHC += (battle.winner + 1) % 2
  
  # White: Softmax Linear, Black: Monte Carlo Tree Search
  battle = Battle.Battle(c.team3, c.team3, False)
  while battle.running:
    battle.trainers[0].setNextAction(BBSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(BBMCTSAI.getAction(battle.getState(c.amBlack)))
    battle.progress()
  SLMCTS += (battle.winner + 1) % 2
  
  # White: Monte Carlo Tree Search, Black: Random
  battle = Battle.Battle(c.team3, c.team3, False)
  while battle.running:
    battle.trainers[0].setNextAction(BBMCTSAI.getAction(battle.getState(c.amWhite)))
    battle.trainers[1].setNextAction(np.random.choice(c.actions))
    battle.progress()
  MCTSR += (battle.winner + 1) % 2
  
  # White: Monte Carlo Tree Search, Black: Hard Coded
  battle = Battle.Battle(c.team3, c.team3, False)
  while battle.running:
    battle.trainers[0].setNextAction(BBMCTSAI.getAction(battle.getState(c.amWhite)))
    battle.trainers[1].setNextAction(BBHCAI[battle.round])
    battle.progress()
  MCTSHC += (battle.winner + 1) % 2
  
  # Print progress notice every tenth percent
  if iBattle % int(nBattles / 10) == 0 and iBattle != 0:
    print('Battled ' + str(int(100 * iBattle / nBattles)) + '%')

print('blue V blue finished!')
print('Softmax Linear results: [Random: %d wins, Hard Code: %d wins, Monte Carlo Tree Search: %d wins]' % (SLR, SLHC, SLMCTS))
print('Monte Carlo Tree Search results: [Random: %d wins, Hard Code: %d wins, Softmax Linear: %d wins]' % (MCTSR, MCTSHC, (nBattles - SLMCTS)))

### ----------- ###
### GREEN V RED ###
### ----------- ###

print('Start green V red! [Battles per setup: %d]' % (nBattles))

SLR = 0
SLHC = 0
SLMCTS = 0
MCTSR = 0
MCTSHC = 0
for iBattle in range(nBattles):
  # White: Softmax Linear, Black: Random
  battle = Battle.Battle(c.team1, c.team2, False)
  while battle.running:
    battle.trainers[0].setNextAction(GRSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(np.random.choice(c.actions))
    battle.progress()
  SLR += (battle.winner + 1) % 2
  
  # White: Softmax Linear, Black: Hard Coded
  battle = Battle.Battle(c.team1, c.team2, False)
  while battle.running:
    battle.trainers[0].setNextAction(GRSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(RGHCAI[battle.round])
    battle.progress()
  SLHC += (battle.winner + 1) % 2
  
  # White: Softmax Linear, Black: Monte Carlo Tree Search
  battle = Battle.Battle(c.team1, c.team2, False)
  while battle.running:
    battle.trainers[0].setNextAction(GRSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(RGMCTSAI.getAction(battle.getState(c.amBlack)))
    battle.progress()
  SLMCTS += (battle.winner + 1) % 2
  
  # White: Monte Carlo Tree Search, Black: Random
  battle = Battle.Battle(c.team1, c.team2, False)
  while battle.running:
    battle.trainers[0].setNextAction(GRMCTSAI.getAction(battle.getState(c.amWhite)))
    battle.trainers[1].setNextAction(np.random.choice(c.actions))
    battle.progress()
  MCTSR += (battle.winner + 1) % 2
  
  # White: Monte Carlo Tree Search, Black: Hard Coded
  battle = Battle.Battle(c.team1, c.team2, False)
  while battle.running:
    battle.trainers[0].setNextAction(GRMCTSAI.getAction(battle.getState(c.amWhite)))
    battle.trainers[1].setNextAction(RGHCAI[battle.round])
    battle.progress()
  MCTSHC += (battle.winner + 1) % 2
  
  # Print progress notice every tenth percent
  if iBattle % int(nBattles / 10) == 0 and iBattle != 0:
    print('Battled ' + str(int(100 * iBattle / nBattles)) + '%')

print('green V red finished!')
print('Softmax Linear results: [Random: %d wins, Hard Code: %d wins, Monte Carlo Tree Search: %d wins]' % (SLR, SLHC, SLMCTS))
print('Monte Carlo Tree Search results: [Random: %d wins, Hard Code: %d wins, Softmax Linear: %d wins]' % (MCTSR, MCTSHC, (nBattles - SLMCTS)))

### ------------ ###
### GREEN V BLUE ###
### ------------ ###

print('Start green V blue! [Battles per setup: %d]' % (nBattles))

SLR = 0
SLHC = 0
SLMCTS = 0
MCTSR = 0
MCTSHC = 0
for iBattle in range(nBattles):
  # White: Softmax Linear, Black: Random
  battle = Battle.Battle(c.team1, c.team3, False)
  while battle.running:
    battle.trainers[0].setNextAction(GBSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(np.random.choice(c.actions))
    battle.progress()
  SLR += (battle.winner + 1) % 2
  
  # White: Softmax Linear, Black: Hard Coded
  battle = Battle.Battle(c.team1, c.team3, False)
  while battle.running:
    battle.trainers[0].setNextAction(GBSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(BGHCAI[battle.round])
    battle.progress()
  SLHC += (battle.winner + 1) % 2
  
  # White: Softmax Linear, Black: Monte Carlo Tree Search
  battle = Battle.Battle(c.team1, c.team3, False)
  while battle.running:
    battle.trainers[0].setNextAction(GBSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(BGMCTSAI.getAction(battle.getState(c.amBlack)))
    battle.progress()
  SLMCTS += (battle.winner + 1) % 2
  
  # White: Monte Carlo Tree Search, Black: Random
  battle = Battle.Battle(c.team1, c.team3, False)
  while battle.running:
    battle.trainers[0].setNextAction(GBMCTSAI.getAction(battle.getState(c.amWhite)))
    battle.trainers[1].setNextAction(np.random.choice(c.actions))
    battle.progress()
  MCTSR += (battle.winner + 1) % 2
  
  # White: Monte Carlo Tree Search, Black: Hard Coded
  battle = Battle.Battle(c.team1, c.team3, False)
  while battle.running:
    battle.trainers[0].setNextAction(GBMCTSAI.getAction(battle.getState(c.amWhite)))
    battle.trainers[1].setNextAction(BGHCAI[battle.round])
    battle.progress()
  MCTSHC += (battle.winner + 1) % 2
  
  # Print progress notice every tenth percent
  if iBattle % int(nBattles / 10) == 0 and iBattle != 0:
    print('Battled ' + str(int(100 * iBattle / nBattles)) + '%')

print('green V blue finished!')
print('Softmax Linear results: [Random: %d wins, Hard Code: %d wins, Monte Carlo Tree Search: %d wins]' % (SLR, SLHC, SLMCTS))
print('Monte Carlo Tree Search results: [Random: %d wins, Hard Code: %d wins, Softmax Linear: %d wins]' % (MCTSR, MCTSHC, (nBattles - SLMCTS)))

### ----------- ###
### RED V GREEN ###
### ----------- ###

print('Start red V green! [Battles per setup: %d]' % (nBattles))

SLR = 0
SLHC = 0
SLMCTS = 0
MCTSR = 0
MCTSHC = 0
for iBattle in range(nBattles):
  # White: Softmax Linear, Black: Random
  battle = Battle.Battle(c.team2, c.team1, False)
  while battle.running:
    battle.trainers[0].setNextAction(RGSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(np.random.choice(c.actions))
    battle.progress()
  SLR += (battle.winner + 1) % 2
  
  # White: Softmax Linear, Black: Hard Coded
  battle = Battle.Battle(c.team2, c.team1, False)
  while battle.running:
    battle.trainers[0].setNextAction(RGSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(GRHCAI[battle.round])
    battle.progress()
  SLHC += (battle.winner + 1) % 2
  
  # White: Softmax Linear, Black: Monte Carlo Tree Search
  battle = Battle.Battle(c.team2, c.team1, False)
  while battle.running:
    battle.trainers[0].setNextAction(RGSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(GRMCTSAI.getAction(battle.getState(c.amBlack)))
    battle.progress()
  SLMCTS += (battle.winner + 1) % 2
  
  # White: Monte Carlo Tree Search, Black: Random
  battle = Battle.Battle(c.team2, c.team1, False)
  while battle.running:
    battle.trainers[0].setNextAction(RGMCTSAI.getAction(battle.getState(c.amWhite)))
    battle.trainers[1].setNextAction(np.random.choice(c.actions))
    battle.progress()
  MCTSR += (battle.winner + 1) % 2
  
  # White: Monte Carlo Tree Search, Black: Hard Coded
  battle = Battle.Battle(c.team2, c.team1, False)
  while battle.running:
    battle.trainers[0].setNextAction(RGMCTSAI.getAction(battle.getState(c.amWhite)))
    battle.trainers[1].setNextAction(GRHCAI[battle.round])
    battle.progress()
  MCTSHC += (battle.winner + 1) % 2
  
  # Print progress notice every tenth percent
  if iBattle % int(nBattles / 10) == 0 and iBattle != 0:
    print('Battled ' + str(int(100 * iBattle / nBattles)) + '%')

print('red V green finished!')
print('Softmax Linear results: [Random: %d wins, Hard Code: %d wins, Monte Carlo Tree Search: %d wins]' % (SLR, SLHC, SLMCTS))
print('Monte Carlo Tree Search results: [Random: %d wins, Hard Code: %d wins, Softmax Linear: %d wins]' % (MCTSR, MCTSHC, (nBattles - SLMCTS)))

### ---------- ###
### RED V BLUE ###
### ---------- ###

print('Start red V blue! [Battles per setup: %d]' % (nBattles))

SLR = 0
SLHC = 0
SLMCTS = 0
MCTSR = 0
MCTSHC = 0
for iBattle in range(nBattles):
  # White: Softmax Linear, Black: Random
  battle = Battle.Battle(c.team2, c.team3, False)
  while battle.running:
    battle.trainers[0].setNextAction(RBSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(np.random.choice(c.actions))
    battle.progress()
  SLR += (battle.winner + 1) % 2
  
  # White: Softmax Linear, Black: Hard Coded
  battle = Battle.Battle(c.team2, c.team3, False)
  while battle.running:
    battle.trainers[0].setNextAction(RBSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(BRHCAI[battle.round])
    battle.progress()
  SLHC += (battle.winner + 1) % 2
  
  # White: Softmax Linear, Black: Monte Carlo Tree Search
  battle = Battle.Battle(c.team2, c.team3, False)
  while battle.running:
    battle.trainers[0].setNextAction(RBSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(BRMCTSAI.getAction(battle.getState(c.amBlack)))
    battle.progress()
  SLMCTS += (battle.winner + 1) % 2
  
  # White: Monte Carlo Tree Search, Black: Random
  battle = Battle.Battle(c.team2, c.team3, False)
  while battle.running:
    battle.trainers[0].setNextAction(RBMCTSAI.getAction(battle.getState(c.amWhite)))
    battle.trainers[1].setNextAction(np.random.choice(c.actions))
    battle.progress()
  MCTSR += (battle.winner + 1) % 2
  
  # White: Monte Carlo Tree Search, Black: Hard Coded
  battle = Battle.Battle(c.team2, c.team3, False)
  while battle.running:
    battle.trainers[0].setNextAction(RBMCTSAI.getAction(battle.getState(c.amWhite)))
    battle.trainers[1].setNextAction(BRHCAI[battle.round])
    battle.progress()
  MCTSHC += (battle.winner + 1) % 2
  
  # Print progress notice every tenth percent
  if iBattle % int(nBattles / 10) == 0 and iBattle != 0:
    print('Battled ' + str(int(100 * iBattle / nBattles)) + '%')

print('red V blue finished!')
print('Softmax Linear results: [Random: %d wins, Hard Code: %d wins, Monte Carlo Tree Search: %d wins]' % (SLR, SLHC, SLMCTS))
print('Monte Carlo Tree Search results: [Random: %d wins, Hard Code: %d wins, Softmax Linear: %d wins]' % (MCTSR, MCTSHC, (nBattles - SLMCTS)))

### ------------ ###
### BLUE V GREEN ###
### ------------ ###

print('Start blue V green! [Battles per setup: %d]' % (nBattles))

SLR = 0
SLHC = 0
SLMCTS = 0
MCTSR = 0
MCTSHC = 0
for iBattle in range(nBattles):
  # White: Softmax Linear, Black: Random
  battle = Battle.Battle(c.team3, c.team1, False)
  while battle.running:
    battle.trainers[0].setNextAction(BGSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(np.random.choice(c.actions))
    battle.progress()
  SLR += (battle.winner + 1) % 2
  
  # White: Softmax Linear, Black: Hard Coded
  battle = Battle.Battle(c.team3, c.team1, False)
  while battle.running:
    battle.trainers[0].setNextAction(BGSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(GBHCAI[battle.round])
    battle.progress()
  SLHC += (battle.winner + 1) % 2
  
  # White: Softmax Linear, Black: Monte Carlo Tree Search
  battle = Battle.Battle(c.team3, c.team1, False)
  while battle.running:
    battle.trainers[0].setNextAction(BGSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(GBMCTSAI.getAction(battle.getState(c.amBlack)))
    battle.progress()
  SLMCTS += (battle.winner + 1) % 2
  
  # White: Monte Carlo Tree Search, Black: Random
  battle = Battle.Battle(c.team3, c.team1, False)
  while battle.running:
    battle.trainers[0].setNextAction(BGMCTSAI.getAction(battle.getState(c.amWhite)))
    battle.trainers[1].setNextAction(np.random.choice(c.actions))
    battle.progress()
  MCTSR += (battle.winner + 1) % 2
  
  # White: Monte Carlo Tree Search, Black: Hard Coded
  battle = Battle.Battle(c.team3, c.team1, False)
  while battle.running:
    battle.trainers[0].setNextAction(BGMCTSAI.getAction(battle.getState(c.amWhite)))
    battle.trainers[1].setNextAction(GBHCAI[battle.round])
    battle.progress()
  MCTSHC += (battle.winner + 1) % 2
  
  # Print progress notice every tenth percent
  if iBattle % int(nBattles / 10) == 0 and iBattle != 0:
    print('Battled ' + str(int(100 * iBattle / nBattles)) + '%')

print('blue V green finished!')
print('Softmax Linear results: [Random: %d wins, Hard Code: %d wins, Monte Carlo Tree Search: %d wins]' % (SLR, SLHC, SLMCTS))
print('Monte Carlo Tree Search results: [Random: %d wins, Hard Code: %d wins, Softmax Linear: %d wins]' % (MCTSR, MCTSHC, (nBattles - SLMCTS)))

### ---------- ###
### BLUE V RED ###
### ---------- ###

print('Start blue V red! [Battles per setup: %d]' % (nBattles))

SLR = 0
SLHC = 0
SLMCTS = 0
MCTSR = 0
MCTSHC = 0
for iBattle in range(nBattles):
  # White: Softmax Linear, Black: Random
  battle = Battle.Battle(c.team3, c.team2, False)
  while battle.running:
    battle.trainers[0].setNextAction(BRSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(np.random.choice(c.actions))
    battle.progress()
  SLR += (battle.winner + 1) % 2
  
  # White: Softmax Linear, Black: Hard Coded
  battle = Battle.Battle(c.team3, c.team2, False)
  while battle.running:
    battle.trainers[0].setNextAction(BRSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(RBHCAI[battle.round])
    battle.progress()
  SLHC += (battle.winner + 1) % 2
  
  # White: Softmax Linear, Black: Monte Carlo Tree Search
  battle = Battle.Battle(c.team3, c.team2, False)
  while battle.running:
    battle.trainers[0].setNextAction(BRSLAI.getAction(battle.getFeatures(c.amWhite)))
    battle.trainers[1].setNextAction(RBMCTSAI.getAction(battle.getState(c.amBlack)))
    battle.progress()
  SLMCTS += (battle.winner + 1) % 2
  
  # White: Monte Carlo Tree Search, Black: Random
  battle = Battle.Battle(c.team3, c.team2, False)
  while battle.running:
    battle.trainers[0].setNextAction(BRMCTSAI.getAction(battle.getState(c.amWhite)))
    battle.trainers[1].setNextAction(np.random.choice(c.actions))
    battle.progress()
  MCTSR += (battle.winner + 1) % 2
  
  # White: Monte Carlo Tree Search, Black: Hard Coded
  battle = Battle.Battle(c.team3, c.team2, False)
  while battle.running:
    battle.trainers[0].setNextAction(BRMCTSAI.getAction(battle.getState(c.amWhite)))
    battle.trainers[1].setNextAction(RBHCAI[battle.round])
    battle.progress()
  MCTSHC += (battle.winner + 1) % 2
  
  # Print progress notice every tenth percent
  if iBattle % int(nBattles / 10) == 0 and iBattle != 0:
    print('Battled ' + str(int(100 * iBattle / nBattles)) + '%')

print('blue V red finished!')
print('Softmax Linear results: [Random: %d wins, Hard Code: %d wins, Monte Carlo Tree Search: %d wins]' % (SLR, SLHC, SLMCTS))
print('Monte Carlo Tree Search results: [Random: %d wins, Hard Code: %d wins, Softmax Linear: %d wins]' % (MCTSR, MCTSHC, (nBattles - SLMCTS)))

# Print runtime
if time.time() - startTime < 60:
  print('Runtime: %d seconds' % (time.time() - startTime))
elif time.time() - startTime > 60 and time.time() - startTime < 3600:
  print('Runtime: %d minutes and %d seconds' % ((time.time() - startTime) / 60, (time.time() - startTime) % 60))
else:
  print('Runtime: %d hours, %d minutes and %d seconds' % ((time.time() - startTime) / 3600, ((time.time() - startTime) % 3600) / 60, (time.time() - startTime) % 60))
#