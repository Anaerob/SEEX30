import numpy as np


class AI:
    
    
    def __init__(self, learningRate, temperature, bias=None, weights=None):
        
        self.learningRate = learningRate
        self.temperature = temperature
        self.bias = np.zeros(2)
        if bias is not None:
            self.bias = bias
        self.weights = np.zeros((2, 2))
        if weights is not None:
            self.weights = weights
    
    def train(self, input, action, reward):
        
        # Approximate the action value function Q using linear combination
        output = np.dot(self.weights, input) + self.bias
        
        # Update the weights and biases using stochastic gradient descent
        self.bias[action] += self.learningRate * (reward - output[action])
        self.weights[action] += (self.learningRate
            * (reward - output[action]) * input)
    
    def getAction(self, input):
        
        actions = [0, 1]
        
        # Approximate the action value function Q using linear combination
        output = np.dot(self.weights, input) + self.bias
        
        # If the specified temperature is too low,
        # choose the action with maximum Q
        if self.temperature < 0.01:
            choice = actions[output.tolist().index(max(output))]
        else:
            
            # Choose action using a probabilistic softmax
            policy = (np.exp(output / self.temperature)
                / np.sum(np.exp(output / self.temperature), axis = 0))
            choice = np.random.choice(actions, p = policy)
        
        return choice

#