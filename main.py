import numpy as np
import time

import Battle
import Constants as c
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
redAI = SoftmaxLinearAI.AI(weightsRed)
blueAI = SoftmaxLinearAI.AI()

# Run a battle to see the performance of the AI.
battle = Battle.Battle(redTeam, redTeam, True)
while battle.running:
  battle.white.setNextAction(redAI.getAction(battle.getInput(c.amWhite), 0.01))
  battle.black.setNextAction(redAI.getAction(battle.getInput(c.amBlack), 0.01))
  battle.progress()

#