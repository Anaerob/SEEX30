import numpy as np
import random

pHP = [0, 393, 413, 703, 353, 523, 383]


class AI:
    
    
    def __init__(self, learningRate, temperature, load):
        
        self.learningRate = learningRate
        self.temperature = temperature
        self.moveBias = np.zeros((6, 6, 4))
        self.moveWeights = np.zeros((6, 6, 4, 15))
        self.switchBias = np.zeros((6, 6))
        self.switchWeights = np.zeros((6, 6, 14))
        if load:
            self.load()
    
    def getAction(self, state):
        
        if state[6][0] and not state[4][0]:
            return [0, 0]
        else:
            actions = self.getAllowedActions(state)
            if len(actions) == 1:
                return actions[0]
            else:
                features = self.getFeatures(actions, state)
                output = self.getOutput(actions, features, state)
                
                if self.temperature < 0.01:
                    iChoice = random.choice([i for i, x in enumerate(output) if x == max(output)])
                else:
                    policy = np.exp(output / self.temperature) / np.sum(np.exp(output / self.temperature), axis = 0)
                    iChoice = np.random.choice(list(range(len(actions))), p = policy)
                
                return actions[iChoice]
    
    def getAllowedActions(self, state):
        
        if state[4][0]:
            actions = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0]]
            for iP in range(1, 7):
                if state[14][0][iP] <= 0:
                    actions.remove([iP, 0])
                elif state[3][0] == iP:
                    actions.remove([iP, 0])
        else:
            actions = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [0, 1], [0, 2], [0, 3], [0, 4]]
            for iP in range(1, 7):
                if state[14][0][iP] <= 0:
                    actions.remove([iP, 0])
                elif state[3][0] == iP:
                    actions.remove([iP, 0])
            for iM in range(1, 5):
                if state[15][0][state[3][0] - 1][iM] <= 0:
                    actions.remove([0, iM])
            if len(actions) == 0:
                actions = [[0, 0]]
        return actions
    
    def getFeatures(self, actions, state):
        
        temp = []
        
        for iP in range(1, 7):
            if [iP, 0] in actions:
                temp.append(self.getSwitchFeatures(state, iP))
        for iM in range(1, 5):
            if [0, iM] in actions:
                temp.append(self.getMoveFeatures(state, iM))
        
        return temp
    
    def getMoveFeatures(self, state, move):
        
        lowPP = 4
        
        return np.array([
            state[8][0] / 104,
            state[8][1] / 104,
            (6 - state[9][0]) / 6,
            (6 - state[9][1]) / 6,
            (state[10][0] - 6) / 6,
            (state[10][1] - 6) / 6,
            int(state[11][0][state[3][0]]),
            int(state[11][1][state[3][1]]),
            int(state[12][0][state[3][0]]),
            int(state[12][1][state[3][1]]),
            int(state[13][0][state[3][0]] > 0),
            int(state[13][1][state[3][1]] > 0),
            state[14][0][state[3][0]] / pHP[state[3][0]],
            state[14][1][state[3][1]] / pHP[state[3][1]],
            (state[15][0][state[3][0] - 1][move] < lowPP) * (1 - state[15][0][state[3][0] - 1][move] / lowPP)]) # len = 15, [14]
    
    def getOutput(self, actions, features, state):
        
        temp = np.array([])
        
        for iP in range(1, 7):
            if [iP, 0] in actions:
                temp = np.append(temp, np.dot(self.switchWeights[state[3][1] - 1][iP - 1], features[len(temp)]) + self.switchBias[state[3][1] - 1][iP - 1])
        for iM in range(1, 5):
            if [0, iM] in actions:
                temp = np.append(temp, np.dot(self.moveWeights[state[3][1] - 1][state[3][0] - 1][iM - 1], features[len(temp)]) + self.moveBias[state[3][1] - 1][state[3][0] - 1][iM - 1])
        
        return temp
    
    def getSwitchFeatures(self, state, pokemon):
        
        return np.array([
            state[8][0] / 104,
            state[8][1] / 104,
            (6 - state[9][0]) / 6,
            (6 - state[9][1]) / 6,
            (state[10][0] - 6) / 6,
            (state[10][1] - 6) / 6,
            int(state[11][0][pokemon]),
            int(state[11][1][state[3][1]]),
            int(state[12][0][pokemon]),
            int(state[12][1][state[3][1]]),
            int(state[13][0][pokemon] > 0),
            int(state[13][1][state[3][1]] > 0),
            state[14][0][pokemon] / pHP[pokemon],
            state[14][1][state[3][1]] / pHP[state[3][1]]]) # len = 14, [13]
    
    def load(self):
        
        if not os.path.isdir('LinearNeuralNetworkAI'):
            return False
        if not os.path.isfile('LinearNeuralNetworkAI/moveBias.txt'):
            return False
        if not os.path.isfile('LinearNeuralNetworkAI/moveWeights.txt'):
            return False
        if not os.path.isfile('LinearNeuralNetworkAI/switchBias.txt'):
            return False
        if not os.path.isfile('LinearNeuralNetworkAI/switchWeights.txt'):
            return False
        
        moveBiasFile = open('LinearNeuralNetworkAI/moveBias.txt', 'r')
        moveWeightsFile = open('LinearNeuralNetworkAI/moveWeights.txt', 'r')
        switchBiasFile = open('LinearNeuralNetworkAI/switchBias.txt', 'r')
        switchWeightsFile = open('LinearNeuralNetworkAI/switchWeights.txt', 'r')
        for iO in range(6):
            for iP in range(6):
                self.switchBias[iO][iP] = float(switchBiasFile.readline())
                for iM in range(4):
                    self.moveBias[iO][iP][iM] = float(moveBiasFile.readline())
                    for iF in range(15):
                        self.moveWeights[iO][iP][iM][iF] = float(moveWeightsFile.readline())
                for iF in range(14):
                    self.switchWeights[iO][iP][iF] = float(switchWeightsFile.readline())
        moveBiasFile.close()
        moveWeightsFile.close()
        switchBiasFile.close()
        switchWeightsFile.close()
        
        return True
    
    def save(self):
        
        if not os.path.isdir('LinearNeuralNetworkAI'):
            os.makedirs('LinearNeuralNetworkAI')
        moveBiasFile = open('LinearNeuralNetworkAI/moveBias.txt', 'w')
        moveWeightsFile = open('LinearNeuralNetworkAI/moveWeights.txt', 'w')
        switchBiasFile = open('LinearNeuralNetworkAI/switchBias.txt', 'w')
        switchWeightsFile = open('LinearNeuralNetworkAI/switchWeights.txt', 'w')
        for iO in range(6):
            for iP in range(6):
                switchBiasFile.write(str(self.switchBias[iO][iP]) + '\n')
                for iM in range(4):
                    moveBiasFile.write(str(self.moveBias[iO][iP][iM]) + '\n')
                    for iF in range(15):
                        moveWeightsFile.write(str(self.moveWeights[iO][iP][iM][iF]) + '\n')
                for iF in range(14):
                    switchWeightsFile.write(str(self.switchWeights[iO][iP][iF]) + '\n')
        moveBiasFile.close()
        moveWeightsFile.close()
        switchBiasFile.close()
        switchWeightsFile.close()
    
    def train(self, action, reward, state):
        
        if action != [0, 0]:
            if action[0] == 0:
                features = self.getMoveFeatures(state, action[1])
                output = self.getOutput([action], [features], state)
                self.moveBias[state[3][1] - 1][state[3][0] - 1][action[1] - 1] += self.learningRate * (reward - output[0])
                self.moveWeights[state[3][1] - 1][state[3][0] - 1][action[1] - 1] += self.learningRate * (reward - output[0]) * features
            elif action[1] == 0:
                features = self.getSwitchFeatures(state, action[0])
                output = self.getOutput([action], [features], state)
                self.switchBias[state[3][1] - 1][action[0] - 1] += self.learningRate * (reward - output[0])
                self.switchWeights[state[3][1] - 1][action[0] - 1] += self.learningRate * (reward - output[0]) * features

#