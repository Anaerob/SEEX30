import numpy as np

import Constants as c

class AI:
  def __init__(self, learningRate, temperature, weights = None):
    self.learningRate = learningRate
    self.temperature = temperature
    
    if weights is None:
      self.weights = np.zeros((c.nOutputs, c.nInputs))
    else:
      self.weights = weights
  
  def train(self, input, action, reward):
    # baseline = np.sum(np.dot(self.weights, input))/2
    
    # Linear combination of inputs and weights
    output = np.dot(self.weights, input)
    
    self.weights[action - 1] += self.learningRate * (reward - output[action - 1]) * input
  
  def getAction(self, input, temperature = None):
    # Linear combination of inputs and weights
    output = np.dot(self.weights, input)
    
    # Set probability of choosing zero PP move to zero
    # We only need to check stat modifier in scenario 1
    if input[4] == 1:
      output[1] = -float('inf')
    
    if temperature is None:
      if self.temperature < 0.005:
        # This is where softmax starts to blow up, use a hardmax instead
        choice = c.actions[output.tolist().index(max(output))]
      else:
        # Softmax with default temperature to decide the policy probabilities
        policy = np.exp(output / self.temperature) / np.sum(np.exp(output / self.temperature), axis = 0)
        
        # Choose based on policy
        choice = np.random.choice(c.actions, p = policy)
      
    elif temperature < 0.005:
      # This is where softmax starts to blow up, use a hardmax instead
      choice = c.actions[output.tolist().index(max(output))]
      
    else:
      # Softmax with default temperature to decide the policy probabilities
      policy = np.exp(output / temperature) / np.sum(np.exp(output / temperature), axis = 0)
      
      # Choose based on policy
      choice = np.random.choice(c.actions, p = policy)
    
    return choice
  
#