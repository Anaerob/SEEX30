import numpy as np

import Constants as c


class AI:
    
    
    def __init__(self, learningRate, temperature, bias=None, weights=None):
        
        self.learningRate = learningRate
        self.temperature = temperature
        self.bias = np.zeros(c.nOutputs)
        if bias is not None:
            self.bias = bias
        self.weights = np.zeros((c.nOutputs, c.nInputs))
        if weights is not None:
            self.weights = weights
    
    def train(self, input, action, reward):
        
        # Approximate the action value function Q using linear combination
        output = np.dot(self.weights, input) + self.bias
        
        # Update the weights and biases using stochastic gradient descent
        self.bias[action - 1] += self.learningRate * (reward - output[action - 1])
        self.weights[action - 1] += self.learningRate * (reward - output[action - 1]) * input
    
    def getAction(self, input):
        
        # Approximate the action value function Q using linear combination
        output = np.dot(self.weights, input) + self.bias
        
        # Set probability of choosing zero PP move to zero
        if input[1] == 1:
            output[1] = -float('inf')
            
            # Punish this theoretical choice heavily
            self.train(input, 2, -10)
        
        # If the specified temperature is too low,
        # choose the action with maximum Q
        if self.temperature < 0.01:
            choice = c.actions[output.tolist().index(max(output))]
        else:
            
            # Choose action using a probabilistic softmax
            policy = np.exp(output / self.temperature) / np.sum(np.exp(output / self.temperature), axis = 0)
            choice = np.random.choice(c.actions, p = policy)
        
        return choice

#