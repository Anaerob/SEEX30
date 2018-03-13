import numpy as np
import time

import Battle
import Constants as c
import SoftmaxLinearAI

# Training variables
nTrainHomo = 1000
nTrainHetero = 10000
decay = 0.9
learningRate = 0.1
temperature = 0.1
nPlotPoints = 1000

# Start runtime timer
startTime = time.time()

# Create all nine AI
BlueBlue = SoftmaxLinearAI.AI(learningRate, temperature)
BlueGreen = SoftmaxLinearAI.AI(learningRate, temperature)
BlueRed = SoftmaxLinearAI.AI(learningRate, temperature)
GreenBlue = SoftmaxLinearAI.AI(learningRate, temperature)
GreenGreen = SoftmaxLinearAI.AI(learningRate, temperature)
GreenRed = SoftmaxLinearAI.AI(learningRate, temperature)
RedBlue = SoftmaxLinearAI.AI(learningRate, temperature)
RedGreen = SoftmaxLinearAI.AI(learningRate, temperature)
RedRed = SoftmaxLinearAI.AI(learningRate, temperature)

# Start multi-AI training
print('Start multi-AI training: [Decay: %f, Learning rate: %f, Temperature: %f]' % (decay, learningRate, temperature))

### ----------- ###
### BLUE V BLUE ###
### ----------- ###

print('Start blue V blue: [Battles: %d]' % (nTrainHomo))

plotBlueBlue = open('plotBlueBlue.txt', 'w')

for iTrain in range(nTrainHomo):
  # Save weights for the plot
  if iTrain % int(nTrainHomo / nPlotPoints) == 0:
    for i in range(c.nOutputs):
      for j in range(c.nInputs):
        plotBlueBlue.write(str(BlueBlue.weights[i][j]) + '\n')
  
  battle = Battle.Battle(c.team3, c.team3, False)
  
  whiteFeatures = []
  whiteActions = []
  blackFeatures = []
  blackActions = []
  
  # Run the battle until it's over
  while battle.running:
    whiteFeatures.append(battle.getFeatures(c.amWhite))
    whiteActions.append(BlueBlue.getAction(whiteFeatures[battle.round], temperature))
    battle.trainers[0].setNextAction(whiteActions[battle.round])
    
    blackFeatures.append(battle.getFeatures(c.amBlack))
    blackActions.append(BlueBlue.getAction(blackFeatures[battle.round], temperature))
    battle.trainers[1].setNextAction(blackActions[battle.round])
    
    battle.progress()
  
  # Train the AI based on the results, reward 1 for winning and -1 for losing
  for iRound in range(battle.round):
    BlueBlue.train(whiteFeatures[battle.round - iRound - 1], whiteActions[battle.round - iRound - 1], -2 * (battle.winner - 0.5) * (decay ** iRound))
    BlueBlue.train(blackFeatures[battle.round - iRound - 1], blackActions[battle.round - iRound - 1], 2 * (battle.winner - 0.5) * (decay ** iRound))
  
  # Print progress notice every tenth percent
  if iTrain % int(nTrainHomo / 10) == 0 and iTrain != 0:
    print('Trained ' + str(int(100 * iTrain / nTrainHomo)) + '%')

# Print final notice
print('Trained 100%')

# Save final weights, for plot and use
weightsBlueBlue = open('weightsBlueBlue.txt', 'w')
for i in range(c.nOutputs):
  for j in range(c.nInputs):
    plotBlueBlue.write(str(BlueBlue.weights[i][j]) + '\n')
    weightsBlueBlue.write(str(BlueBlue.weights[i][j]) + '\n')
plotBlueBlue.close()
weightsBlueBlue.close()

### ------------- ###
### GREEN V GREEN ###
### ------------- ###

print('Start green V green: [Battles: %d]' % (nTrainHomo))

plotGreenGreen = open('plotGreenGreen.txt', 'w')

for iTrain in range(nTrainHomo):
  # Save weights for the plot
  if iTrain % int(nTrainHomo / nPlotPoints) == 0:
    for i in range(c.nOutputs):
      for j in range(c.nInputs):
        plotGreenGreen.write(str(GreenGreen.weights[i][j]) + '\n')
  
  battle = Battle.Battle(c.team1, c.team1, False)
  
  whiteFeatures = []
  whiteActions = []
  blackFeatures = []
  blackActions = []
  
  # Run the battle until it's over
  while battle.running:
    whiteFeatures.append(battle.getFeatures(c.amWhite))
    whiteActions.append(GreenGreen.getAction(whiteFeatures[battle.round], temperature))
    battle.trainers[0].setNextAction(whiteActions[battle.round])
    
    blackFeatures.append(battle.getFeatures(c.amBlack))
    blackActions.append(GreenGreen.getAction(blackFeatures[battle.round], temperature))
    battle.trainers[1].setNextAction(blackActions[battle.round])
    
    battle.progress()
  
  # Train the AI based on the results, reward 1 for winning and -1 for losing
  for iRound in range(battle.round):
    GreenGreen.train(whiteFeatures[battle.round - iRound - 1], whiteActions[battle.round - iRound - 1], -2 * (battle.winner - 0.5) * (decay ** iRound))
    GreenGreen.train(blackFeatures[battle.round - iRound - 1], blackActions[battle.round - iRound - 1], 2 * (battle.winner - 0.5) * (decay ** iRound))
  
  # Print progress notice every tenth percent
  if iTrain % int(nTrainHomo / 10) == 0 and iTrain != 0:
    print('Trained ' + str(int(100 * iTrain / nTrainHomo)) + '%')

# Print final notice
print('Trained 100%')

# Save final weights, for plot and use
weightsGreenGreen = open('weightsGreenGreen.txt', 'w')
for i in range(c.nOutputs):
  for j in range(c.nInputs):
    plotGreenGreen.write(str(GreenGreen.weights[i][j]) + '\n')
    weightsGreenGreen.write(str(GreenGreen.weights[i][j]) + '\n')
plotGreenGreen.close()
weightsGreenGreen.close()

### --------- ###
### RED V RED ###
### --------- ###

print('Start red V red: [Battles: %d]' % (nTrainHomo))

plotRedRed = open('plotRedRed.txt', 'w')

for iTrain in range(nTrainHomo):
  # Save weights for the plot
  if iTrain % int(nTrainHomo / nPlotPoints) == 0:
    for i in range(c.nOutputs):
      for j in range(c.nInputs):
        plotRedRed.write(str(RedRed.weights[i][j]) + '\n')
  
  battle = Battle.Battle(c.team2, c.team2, False)
  
  whiteFeatures = []
  whiteActions = []
  blackFeatures = []
  blackActions = []
  
  # Run the battle until it's over
  while battle.running:
    whiteFeatures.append(battle.getFeatures(c.amWhite))
    whiteActions.append(RedRed.getAction(whiteFeatures[battle.round], temperature))
    battle.trainers[0].setNextAction(whiteActions[battle.round])
    
    blackFeatures.append(battle.getFeatures(c.amBlack))
    blackActions.append(RedRed.getAction(blackFeatures[battle.round], temperature))
    battle.trainers[1].setNextAction(blackActions[battle.round])
    
    battle.progress()
  
  # Train the AI based on the results, reward 1 for winning and -1 for losing
  for iRound in range(battle.round):
    RedRed.train(whiteFeatures[battle.round - iRound - 1], whiteActions[battle.round - iRound - 1], -2 * (battle.winner - 0.5) * (decay ** iRound))
    RedRed.train(blackFeatures[battle.round - iRound - 1], blackActions[battle.round - iRound - 1], 2 * (battle.winner - 0.5) * (decay ** iRound))
  
  # Print progress notice every tenth percent
  if iTrain % int(nTrainHomo / 10) == 0 and iTrain != 0:
    print('Trained ' + str(int(100 * iTrain / nTrainHomo)) + '%')

# Print final notice
print('Trained 100%')

# Save final weights, for plot and use
weightsRedRed = open('weightsRedRed.txt', 'w')
for i in range(c.nOutputs):
  for j in range(c.nInputs):
    plotRedRed.write(str(RedRed.weights[i][j]) + '\n')
    weightsRedRed.write(str(RedRed.weights[i][j]) + '\n')
plotRedRed.close()
weightsRedRed.close()

### ------------ ###
### BLUE V GREEN ###
### GREEN V BLUE ###
### ------------ ###

print('Start blue V green: [Battles: %d]' % (nTrainHetero))

plotBlueGreen = open('plotBlueGreen.txt', 'w')
plotGreenBlue = open('plotGreenBlue.txt', 'w')

for iTrain in range(nTrainHetero):
  # Save weights for the plot
  if iTrain % int(nTrainHetero / nPlotPoints) == 0:
    for i in range(c.nOutputs):
      for j in range(c.nInputs):
        plotBlueGreen.write(str(BlueGreen.weights[i][j]) + '\n')
        plotGreenBlue.write(str(GreenBlue.weights[i][j]) + '\n')
  
  battle = Battle.Battle(c.team3, c.team1, False)
  
  whiteFeatures = []
  whiteActions = []
  blackFeatures = []
  blackActions = []
  
  # Run the battle until it's over
  while battle.running:
    whiteFeatures.append(battle.getFeatures(c.amWhite))
    whiteActions.append(BlueGreen.getAction(whiteFeatures[battle.round], temperature))
    battle.trainers[0].setNextAction(whiteActions[battle.round])
    
    blackFeatures.append(battle.getFeatures(c.amBlack))
    blackActions.append(GreenBlue.getAction(blackFeatures[battle.round], temperature))
    battle.trainers[1].setNextAction(blackActions[battle.round])
    
    battle.progress()
  
  # Train the AI based on the results, reward 1 for winning and -1 for losing
  for iRound in range(battle.round):
    BlueGreen.train(whiteFeatures[battle.round - iRound - 1], whiteActions[battle.round - iRound - 1], -2 * (battle.winner - 0.5) * (decay ** iRound))
    GreenBlue.train(blackFeatures[battle.round - iRound - 1], blackActions[battle.round - iRound - 1], 2 * (battle.winner - 0.5) * (decay ** iRound))
  
  # Print progress notice every tenth percent
  if iTrain % int(nTrainHetero / 10) == 0 and iTrain != 0:
    print('Trained ' + str(int(100 * iTrain / nTrainHetero)) + '%')

# Print final notice
print('Trained 100%')

# Save final weights, for plot and use
weightsBlueGreen = open('weightsBlueGreen.txt', 'w')
weightsGreenBlue = open('weightsGreenBlue.txt', 'w')
for i in range(c.nOutputs):
  for j in range(c.nInputs):
    plotBlueGreen.write(str(BlueGreen.weights[i][j]) + '\n')
    plotGreenBlue.write(str(GreenBlue.weights[i][j]) + '\n')
    weightsBlueGreen.write(str(BlueGreen.weights[i][j]) + '\n')
    weightsGreenBlue.write(str(GreenBlue.weights[i][j]) + '\n')
plotBlueGreen.close()
plotGreenBlue.close()
weightsBlueGreen.close()
weightsGreenBlue.close()

### ----------- ###
### GREEN V RED ###
### RED V GREEN ###
### ----------- ###

print('Start green V red: [Battles: %d]' % (nTrainHetero))

plotGreenRed = open('plotGreenRed.txt', 'w')
plotRedGreen = open('plotRedGreen.txt', 'w')

for iTrain in range(nTrainHetero):
  # Save weights for the plot
  if iTrain % int(nTrainHetero / nPlotPoints) == 0:
    for i in range(c.nOutputs):
      for j in range(c.nInputs):
        plotGreenRed.write(str(GreenRed.weights[i][j]) + '\n')
        plotRedGreen.write(str(RedGreen.weights[i][j]) + '\n')
  
  battle = Battle.Battle(c.team1, c.team2, False)
  
  whiteFeatures = []
  whiteActions = []
  blackFeatures = []
  blackActions = []
  
  # Run the battle until it's over
  while battle.running:
    whiteFeatures.append(battle.getFeatures(c.amWhite))
    whiteActions.append(GreenRed.getAction(whiteFeatures[battle.round], temperature))
    battle.trainers[0].setNextAction(whiteActions[battle.round])
    
    blackFeatures.append(battle.getFeatures(c.amBlack))
    blackActions.append(RedGreen.getAction(blackFeatures[battle.round], temperature))
    battle.trainers[1].setNextAction(blackActions[battle.round])
    
    battle.progress()
  
  # Train the AI based on the results, reward 1 for winning and -1 for losing
  for iRound in range(battle.round):
    GreenRed.train(whiteFeatures[battle.round - iRound - 1], whiteActions[battle.round - iRound - 1], -2 * (battle.winner - 0.5) * (decay ** iRound))
    RedGreen.train(blackFeatures[battle.round - iRound - 1], blackActions[battle.round - iRound - 1], 2 * (battle.winner - 0.5) * (decay ** iRound))
  
  # Print progress notice every tenth percent
  if iTrain % int(nTrainHetero / 10) == 0 and iTrain != 0:
    print('Trained ' + str(int(100 * iTrain / nTrainHetero)) + '%')

# Print final notice
print('Trained 100%')

# Save final weights, for plot and use
weightsGreenRed = open('weightsGreenRed.txt', 'w')
weightsRedGreen = open('weightsRedGreen.txt', 'w')
for i in range(c.nOutputs):
  for j in range(c.nInputs):
    plotGreenRed.write(str(GreenRed.weights[i][j]) + '\n')
    plotRedGreen.write(str(RedGreen.weights[i][j]) + '\n')
    weightsGreenRed.write(str(GreenRed.weights[i][j]) + '\n')
    weightsRedGreen.write(str(RedGreen.weights[i][j]) + '\n')
plotGreenRed.close()
plotRedGreen.close()
weightsGreenRed.close()
weightsRedGreen.close()

### ---------- ###
### RED V BLUE ###
### BLUE V RED ###
### ---------- ###

print('Start red V blue: [Battles: %d]' % (nTrainHetero))

plotRedBlue = open('plotRedBlue.txt', 'w')
plotBlueRed = open('plotBlueRed.txt', 'w')

for iTrain in range(nTrainHetero):
  # Save weights for the plot
  if iTrain % int(nTrainHetero / nPlotPoints) == 0:
    for i in range(c.nOutputs):
      for j in range(c.nInputs):
        plotRedBlue.write(str(RedBlue.weights[i][j]) + '\n')
        plotBlueRed.write(str(BlueRed.weights[i][j]) + '\n')
  
  battle = Battle.Battle(c.team2, c.team3, False)
  
  whiteFeatures = []
  whiteActions = []
  blackFeatures = []
  blackActions = []
  
  # Run the battle until it's over
  while battle.running:
    whiteFeatures.append(battle.getFeatures(c.amWhite))
    whiteActions.append(RedBlue.getAction(whiteFeatures[battle.round], temperature))
    battle.trainers[0].setNextAction(whiteActions[battle.round])
    
    blackFeatures.append(battle.getFeatures(c.amBlack))
    blackActions.append(BlueRed.getAction(blackFeatures[battle.round], temperature))
    battle.trainers[1].setNextAction(blackActions[battle.round])
    
    battle.progress()
  
  # Train the AI based on the results, reward 1 for winning and -1 for losing
  for iRound in range(battle.round):
    RedBlue.train(whiteFeatures[battle.round - iRound - 1], whiteActions[battle.round - iRound - 1], -2 * (battle.winner - 0.5) * (decay ** iRound))
    BlueRed.train(blackFeatures[battle.round - iRound - 1], blackActions[battle.round - iRound - 1], 2 * (battle.winner - 0.5) * (decay ** iRound))
  
  # Print progress notice every tenth percent
  if iTrain % int(nTrainHetero / 10) == 0 and iTrain != 0:
    print('Trained ' + str(int(100 * iTrain / nTrainHetero)) + '%')

# Print final notice
print('Trained 100%')

# Save final weights, for plot and use
weightsRedBlue = open('weightsRedBlue.txt', 'w')
weightsBlueRed = open('weightsBlueRed.txt', 'w')
for i in range(c.nOutputs):
  for j in range(c.nInputs):
    plotRedBlue.write(str(RedBlue.weights[i][j]) + '\n')
    plotBlueRed.write(str(BlueRed.weights[i][j]) + '\n')
    weightsRedBlue.write(str(RedBlue.weights[i][j]) + '\n')
    weightsBlueRed.write(str(BlueRed.weights[i][j]) + '\n')
plotRedBlue.close()
plotBlueRed.close()
weightsRedBlue.close()
weightsBlueRed.close()

# Print runtime
if time.time() - startTime < 60:
  print('Runtime: %d seconds' % (time.time() - startTime))
elif time.time() - startTime > 60 and time.time() - startTime < 3600:
  print('Runtime: %d minutes and %d seconds' % ((time.time() - startTime) / 60, (time.time() - startTime) % 60))
else:
  print('Runtime: %d hours, %d minutes and %d seconds' % ((time.time() - startTime) / 3600, ((time.time() - startTime) % 3600) / 60, (time.time() - startTime) % 60))
#