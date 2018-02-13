import numpy as np

import Constants as c

class Pokemon:
  def __init__(self, index):
    self.B = c.BS[1, :]
    self.I = np.array([
      np.random.randint(0, 16),
      np.random.randint(0, 16),
      np.random.randint(0, 16),
      np.random.randint(0, 16),
      np.random.randint(0, 16)])
    self.E = np.array([0, 0, 0, 0, 0])
    self.level = 5