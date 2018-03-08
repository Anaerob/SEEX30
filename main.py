import numpy as np
import time

import Battle
import Constants as c
import MonteCarloTreeSearchAI
import SoftmaxLinearAI

# Load weights
weightsRedFile = open('weightsRed.txt', 'r')

weightsRed = []
for i in range(c.nOutputs):
  temp = []
  for j in range(c.nInputs):
    temp.append(float(weightsRedFile.readline()))
  weightsRed.append(temp)

weightsRed = np.array(weightsRed)

# Define teams
greenTeam = c.team1
redTeam = c.team2
blueTeam = c.team3

# Create AI
greenAI = SoftmaxLinearAI.AI()
redSLAI = SoftmaxLinearAI.AI(weightsRed)
redMCTSAI = MonteCarloTreeSearchAI.AI(redTeam, redTeam, 1000)
blueAI = SoftmaxLinearAI.AI()

# Run a battle to see the performance of the AI.
battle = Battle.Battle(redTeam, redTeam, True)
while battle.running:
  battle.white.setNextAction(redSLAI.getAction(battle.getInput(c.amWhite)))
  battle.black.setNextAction(redMCTSAI.getAction(battle.getState(c.amBlack)))
  battle.progress()

#