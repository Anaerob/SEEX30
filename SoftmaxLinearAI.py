import numpy as np

import Constants as c

class AI:
  def __init__(self, weights = None):
    self.learningRate = 0.1
    self.temperature = 0.1
    
    if weights is None:
      self.weights = np.zeros((c.nOutputs, c.nInputs)) # scenario 1: 10 in, 2 out
    else:
      self.weights = weights
  
  def train(self, input, action, reward):
    # baseline = np.sum(np.dot(self.weights, input))/2
    
    # For action 0
    if action == 1:
      self.weights[0] += self.learningRate * (reward - np.dot(self.weights[0], input)) * input
    
    # For action 1
    if action == 2:
      self.weights[1] += self.learningRate * (reward - np.dot(self.weights[1], input)) * input
  
  def getAction(self, input, temperature = None):
    # List of all actions
    actions = [1, 2]
    
    # Linear combination of inputs and weights
    output = np.dot(self.weights, input)
    
    if temperature is None:
      # Softmax with default temperature to decide the policy probabilities
      policy = np.exp(output / self.temperature) / np.sum(np.exp(output / self.temperature), axis = 0)
      
      # Choose based on policy
      choice = np.random.choice(actions, p = policy)
      
    elif temperature < 0.005:
      # This is where softmax starts to blow up, use a hardmax instead
      choice = actions[output.tolist().index(max(output))]
      
    else:
      # Softmax with given temperature to decide the policy probabilities
      policy = np.exp(output / temperature) / np.sum(np.exp(output / temperature), axis = 0)
      
      # Choose based on policy
      choice = np.random.choice(actions, p = policy)
    
    # Don't choose illegal moves
    if input[3] == 0 and input[4] == 0:
      choice = 0
    elif input[4] == 0:
      choice = 1
    elif input[3] == 0:
      choice = 2
    
    return choice
  
#