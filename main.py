import numpy as np
import time

import Battle
import Constants as c
import Load
import MonteCarloTreeSearchAI
import SoftmaxLinearAI

weightsRed = Load.loadFloatMatrix('weightsRed', c.nOutputs, c.nInputs)

# Define teams
greenTeam = c.team1
redTeam = c.team2
blueTeam = c.team3

# Create AI
redSLAI = SoftmaxLinearAI.AI(0, 0.1, weightsRed)
redMCTSAI = MonteCarloTreeSearchAI.AI(redTeam, redTeam, 1000)

# Run a battle to see the performance of the AI.
battle = Battle.Battle(redTeam, redTeam, True)
while battle.running:
  battle.white.setNextAction(redSLAI.getAction(battle.getInput(c.amWhite)))
  battle.black.setNextAction(redMCTSAI.getAction(battle.getState(c.amBlack)))
  battle.progress()
  print(battle.getInput(c.amWhite))

#