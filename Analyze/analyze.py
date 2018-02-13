import numpy as np

class Calculator:
  def initHP(self, b, i, e, l):
    term1 = 2 * (b + i)
    term2 = np.floor(np.minimum(np.ceil(np.sqrt(e)), 255) / 4)
    
    hp = 10 + l + np.floor(l * (term1 + term2) / 100)
    return hp
  
  def initStat(self, b, i, e, l):
    term1 = 2 * (b + i)
    term2 = np.floor(np.minimum(np.ceil(np.sqrt(e)), 255) / 4)
    
    stat = 5 + np.floor(l * (term1 + term2) / 100)
    return stat
  
  def damage(self, p, a, d, l):
    factor1 = 2 + np.floor(2 * l / 5)
    factor2 = p * a
    denominator = 50 * d
    unmodified = 2 + np.floor(factor1 * factor2 / denominator)
    
    #rand = np.random.randint(217, 256)
    rand = 255
    damage = np.floor(unmodified * rand / 255)
    return damage

###

calc = Calculator()
tackle = 35
scratch = 40
level = 5
effort = 0

iBulbasaur = 15
iCharmander = 0
iSquirtle = 0

bBulbasaur = np.array([45, 49, 49, 45])
bCharmander = np.array([39, 52, 43, 65])
bSquirtle = np.array([44, 48, 65, 43])

sBulbasaur = np.array([
  calc.initHP(bBulbasaur[0], iBulbasaur, effort, level),
  calc.initStat(bBulbasaur[1], iBulbasaur, effort, level),
  calc.initStat(bBulbasaur[2], iBulbasaur, effort, level),
  calc.initStat(bBulbasaur[3], iBulbasaur, effort, level)])
sCharmander = np.array([
  calc.initHP(bCharmander[0], iCharmander, effort, level),
  calc.initStat(bCharmander[1], iCharmander, effort, level),
  calc.initStat(bCharmander[2], iCharmander, effort, level),
  calc.initStat(bCharmander[3], iCharmander, effort, level)])
sSquirtle = np.array([
  calc.initHP(bSquirtle[0], iSquirtle, effort, level),
  calc.initStat(bSquirtle[1], iSquirtle, effort, level),
  calc.initStat(bSquirtle[2], iSquirtle, effort, level),
  calc.initStat(bSquirtle[3], iSquirtle, effort, level)])

damage = calc.damage(tackle, sSquirtle[1], 66*sCharmander[2]/100, level)
print(damage)