import random

statMods = [25, 28, 33, 40, 50, 66, 100, 150, 200, 250, 300, 350, 400]
pAttack = [0, 288, 358, 108, 298, 318, 278]
pDefense = [0, 268, 338, 108, 288, 228, 268]
pSpecial = [0, 348, 188, 308, 238, 228, 348]
pSpeed = [0, 208, 178, 198, 318, 158, 298]
pCrit = [0, 22, 20, 25, 55, 15, 50]
pMoves = [
    [0, 0, 0, 0, 0],
    [0, 5, 6, 10, 14],
    [0, 1, 9, 15, 16],
    [0, 2, 7, 8, 13],
    [0, 1, 2, 3, 9],
    [0, 1, 3, 9, 12],
    [0, 4, 7, 8, 11]]
mAccuracy = [256, 255, 255, 230, 255, 191, 191, 255, 255, 255, 255, 256, 255, 256, 255, 230, 256]


class Sim:
    
    
    def __init__(self, state = None):
        
        if state is None:
            self.round = 0
            self.running = True
            self.win = [False, False]
            self.currentPokemon = [1, 1]
            self.forceSwitch = [False, False]
            self.nextAction = [0, 0]
            self.recharge = [False, False]
            self.remainingPokemon = [6, 6]
            self.substitute = [0, 0]
            self.specialMod = [6, 6]
            self.speedMod = [6, 6]
            self.frozen = [
                [False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False]]
            self.paralyzed = [
                [False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False]]
            self.sleeping = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
            self.currentHP = [
                [0, 393, 413, 703, 353, 523, 383],
                [0, 393, 413, 703, 353, 523, 383]]
            self.currentPP = [
                [
                    [10, 10, 10, 10, 10],
                    [10, 48, 24, 16, 8],
                    [10, 24, 16, 16, 16],
                    [10, 16, 24, 32, 16],
                    [10, 24, 16, 8, 16],
                    [10, 24, 8, 16, 8],
                    [10, 32, 24, 32, 48]],
                [
                    [10, 10, 10, 10, 10],
                    [10, 48, 24, 16, 8],
                    [10, 24, 16, 16, 16],
                    [10, 16, 24, 32, 16],
                    [10, 24, 16, 8, 16],
                    [10, 24, 8, 16, 8],
                    [10, 32, 24, 32, 48]]]
        else:
            self.setState(state)
    
    def setState(self, state):
        
        self.round = state[0]
        self.running = state[1]
        self.win = list(state[2])
        self.currentPokemon = list(state[3])
        self.forceSwitch = list(state[4])
        self.nextAction = list(state[5])
        self.recharge = list(state[6])
        self.remainingPokemon = list(state[7])
        self.substitute = list(state[8])
        self.specialMod = list(state[9])
        self.speedMod = list(state[10])
        self.frozen = [list(state[11][0]), list(state[11][1])]
        self.paralyzed = [list(state[12][0]), list(state[12][1])]
        self.sleeping = [list(state[13][0]), list(state[13][1])]
        self.currentHP = [list(state[14][0]), list(state[14][1])]
        self.currentPP = [
                [
                    [10, 10, 10, 10, 10],
                    list(state[15][0][0]),
                    list(state[15][0][1]),
                    list(state[15][0][2]),
                    list(state[15][0][3]),
                    list(state[15][0][4]),
                    list(state[15][0][5])],
                [
                    [10, 10, 10, 10, 10],
                    list(state[15][1][0]),
                    list(state[15][1][1]),
                    list(state[15][1][2]),
                    list(state[15][1][3]),
                    list(state[15][1][4]),
                    list(state[15][1][5])]]
    
    def getState(self, isPlayer):
        
        t = 1
        o = 0
        if isPlayer:
            t = 0
            o = 1
        
        return [
            self.round,
            self.running,
            [self.win[t], self.win[o]],
            [self.currentPokemon[t], self.currentPokemon[o]],
            [self.forceSwitch[t], self.forceSwitch[o]],
            [self.nextAction[t], self.nextAction[o]],
            [self.recharge[t], self.recharge[o]],
            [self.remainingPokemon[t], self.remainingPokemon[o]],
            [self.substitute[t], self.substitute[o]],
            [self.specialMod[t], self.specialMod[o]],
            [self.speedMod[t], self.speedMod[o]],
            [list(self.frozen[t]), list(self.frozen[o])],
            [list(self.paralyzed[t]), list(self.paralyzed[o])],
            [list(self.sleeping[t]), list(self.sleeping[o])],
            [list(self.currentHP[t]), list(self.currentHP[o])],
            [
                [
                    list(self.currentPP[t][1]),
                    list(self.currentPP[t][2]),
                    list(self.currentPP[t][3]),
                    list(self.currentPP[t][4]),
                    list(self.currentPP[t][5]),
                    list(self.currentPP[t][6])],
                [
                    list(self.currentPP[o][1]),
                    list(self.currentPP[o][2]),
                    list(self.currentPP[o][3]),
                    list(self.currentPP[o][4]),
                    list(self.currentPP[o][5]),
                    list(self.currentPP[o][6])]]]
    
    def progress(self):
        
        if self.forceSwitch[0] or self.forceSwitch[1]:
            r = random.randint(0, 1)
            for iT in range(2):
                t = (iT + r) % 2
                if self.forceSwitch[t]:
                    self.doSwitch(t)
                else:
                    self.nextAction[t] = 0
        else:
            switch = []
            switch.append(self.nextAction[0][0] > 0 and not self.recharge[0])
            switch.append(self.nextAction[1][0] > 0 and not self.recharge[1])
            if switch[0] and switch[1]:
                t = random.randint(0, 1)
                self.doSwitch(t)
                self.doSwitch((t + 1) % 2)
            elif switch[0]:
                self.doSwitch(0)
                self.useMove(1)
            elif switch[1]:
                self.doSwitch(1)
                self.useMove(0)
            else:
                speed = []
                speed.append(
                    pSpeed[self.currentPokemon[0]]
                    * statMods[self.speedMod[0]]
                    * (100 - 75 * self.paralyzed[0][self.currentPokemon[0]]))
                speed.append(
                    pSpeed[self.currentPokemon[1]]
                    * statMods[self.speedMod[1]]
                    * (100 - 75 * self.paralyzed[1][self.currentPokemon[1]]))
                t = int(speed[0] < speed[1])
                if speed[0] == speed[1]:
                    t = random.randint(0, 1)
                
                self.useMove(t)
                if (self.currentHP[t][self.currentPokemon[t]] > 0
                        and self.currentHP[(t + 1) % 2][self.currentPokemon[(t + 1) % 2]] > 0):
                    self.useMove((t + 1) % 2)
                else:
                    self.nextAction[(t + 1) % 2] = 0
            for iT in range(2):
                if self.currentHP[iT][self.currentPokemon[iT]] <= 0:
                    self.forceSwitch[iT] = True
                    self.remainingPokemon[iT] -= 1
                    self.frozen[iT][self.currentPokemon[iT]] = False
                    self.paralyzed[iT][self.currentPokemon[iT]] = False
                    self.sleeping[iT][self.currentPokemon[iT]] = 0
            for iT in range(2):
                if self.remainingPokemon[iT] <= 0:
                    self.running = False
                    self.win[(iT + 1) % 2] = True
            self.round += 1
    
    def doSwitch(self, t):
        
        self.currentPokemon[t] = self.nextAction[t][0]
        self.recharge[t] = False
        self.substitute[t] = 0
        self.specialMod[t] = 6
        self.speedMod[t] = 6
        self.forceSwitch[t] = False
        self.nextAction[t] = 0
    
    def useMove(self, t):
        
        if self.recharge[t]:
            self.recharge[t] = False
        elif self.sleeping[t][self.currentPokemon[t]] > 0:
            self.sleeping[t][self.currentPokemon[t]] -= 1
        elif (not self.frozen[t][self.currentPokemon[t]]
                and (not self.paralyzed[t][self.currentPokemon[t]] or random.randint(0, 255) >= 64)):
            if self.nextAction[t][1] != 0:
                self.currentPP[t][self.currentPokemon[t]][self.nextAction[t][1]] -= 1
            if random.randint(0, 255) < mAccuracy[pMoves[self.currentPokemon[t]][self.nextAction[t][1]]]:
                if pMoves[self.currentPokemon[t]][self.nextAction[t][1]] == 1:
                    self.useBodySlam(t)
                elif pMoves[self.currentPokemon[t]][self.nextAction[t][1]] == 9:
                    self.useEarthquake(t)
                elif pMoves[self.currentPokemon[t]][self.nextAction[t][1]] == 2:
                    self.useIceBeam(t)
                elif pMoves[self.currentPokemon[t]][self.nextAction[t][1]] == 3:
                    self.useHyperBeam(t)
                elif pMoves[self.currentPokemon[t]][self.nextAction[t][1]] == 7:
                    self.useThunderbolt(t)
                elif pMoves[self.currentPokemon[t]][self.nextAction[t][1]] == 8:
                    self.useThunderWave(t)
                elif pMoves[self.currentPokemon[t]][self.nextAction[t][1]] == 4:
                    self.useDrillPeck(t)
                elif pMoves[self.currentPokemon[t]][self.nextAction[t][1]] == 5:
                    self.useStunSpore(t)
                elif pMoves[self.currentPokemon[t]][self.nextAction[t][1]] == 6:
                    self.useSleepPowder(t)
                elif pMoves[self.currentPokemon[t]][self.nextAction[t][1]] == 10:
                    self.usePsychic(t)
                elif pMoves[self.currentPokemon[t]][self.nextAction[t][1]] == 11:
                    self.useAgility(t)
                elif pMoves[self.currentPokemon[t]][self.nextAction[t][1]] == 13:
                    self.useSoftboiled(t)
                elif pMoves[self.currentPokemon[t]][self.nextAction[t][1]] == 15:
                    self.useRockSlide(t)
                elif pMoves[self.currentPokemon[t]][self.nextAction[t][1]] == 16:
                    self.useSubstitute(t)
                elif pMoves[self.currentPokemon[t]][self.nextAction[t][1]] == 12:
                    self.useSelfdestruct(t, True)
                elif pMoves[self.currentPokemon[t]][self.nextAction[t][1]] == 14:
                    self.useExplosion(t, True)
                elif self.nextAction[t][1] == 0:
                    self.useStruggle(t)
            else:
                if pMoves[self.currentPokemon[t]][self.nextAction[t][1]] == 12:
                    self.useSelfdestruct(t, False)
                elif pMoves[self.currentPokemon[t]][self.nextAction[t][1]] == 14:
                    self.useExplosion(t, False)
        self.nextAction[t] = 0
    
    def useStruggle(self, t):
        
        level = 100
        o = (t + 1) % 2
        if random.randint(0, 255) < pCrit[self.currentPokemon[t]]:
            level = 200
        damage = self.calculateDamage(
            level,
            pAttack[self.currentPokemon[t]],
            50,
            pDefense[self.currentPokemon[o]])
        if self.currentPokemon[o] == 2:
            damage = int(damage / 2)
        if self.currentPokemon[t] == 3 or self.currentPokemon[t] == 4 or self.currentPokemon[t] == 5:
            damage = int(damage * 1.5)
        substituteBroke = False
        if self.substitute[o] <= 0:
            self.currentHP[o][self.currentPokemon[o]] -= int(damage)
        else:
            self.substitute[o] -= int(damage)
            if self.substitute[o] <= 0:
                substituteBroke = True
        if not substituteBroke:
            self.currentHP[t][self.currentPokemon[t]] -= int(damage / 2)
    
    def useBodySlam(self, t):
        
        level = 100
        o = (t + 1) % 2
        if random.randint(0, 255) < pCrit[self.currentPokemon[t]]:
            level = 200
        damage = self.calculateDamage(
            level,
            pAttack[self.currentPokemon[t]],
            85,
            pDefense[self.currentPokemon[o]])
        if self.currentPokemon[o] == 2:
            damage = int(damage / 2)
        if self.currentPokemon[t] == 4 or self.currentPokemon[t] == 5:
            damage = int(damage * 1.5)
        substituteBroke = False
        if self.substitute[o] <= 0:
            self.currentHP[o][self.currentPokemon[o]] -= int(damage)
        else:
            self.substitute[o] -= int(damage)
            if self.substitute[o] <= 0:
                substituteBroke = True
        if random.randint(0, 255) < 77:
            if self.currentPokemon[o] == 1 or self.currentPokemon[o] == 2 or self.currentPokemon[o] == 6:
                if self.currentHP[o][self.currentPokemon[o]] > 0:
                    if self.substitute[o] <= 0 and not substituteBroke:
                        if not self.frozen[o][self.currentPokemon[o]]:
                            if self.sleeping[o][self.currentPokemon[o]] <= 0:
                                self.paralyzed[o][self.currentPokemon[o]] = True
    
    def useIceBeam(self, t):
        
        o = (t + 1) % 2
        if random.randint(0, 255) < pCrit[self.currentPokemon[t]]:
            damage = self.calculateDamage(
                200,
                pSpecial[self.currentPokemon[t]],
                95,
                pSpecial[self.currentPokemon[o]])
        else:
            damage = self.calculateDamage(
                100,
                int(statMods[self.specialMod[t]] * pSpecial[self.currentPokemon[t]] / 100),
                95,
                int(statMods[self.specialMod[o]] * pSpecial[self.currentPokemon[o]] / 100))
        if self.currentPokemon[o] == 1 or self.currentPokemon[o] == 2 or self.currentPokemon[o] == 6:
            damage = int(damage * 2)
        substituteBroke = False
        if self.substitute[o] <= 0:
            self.currentHP[o][self.currentPokemon[o]] -= int(damage)
        else:
            self.substitute[o] -= int(damage)
            if self.substitute[o] <= 0:
                substituteBroke = True
        if random.randint(0, 255) < 26:
            if self.currentHP[o][self.currentPokemon[o]] > 0:
                if self.substitute[o] <= 0 and not substituteBroke:
                    if not self.paralyzed[o][self.currentPokemon[o]]:
                        if self.sleeping[o][self.currentPokemon[o]] <= 0:
                            freezeClause = False
                            for iP in range(1, 7):
                                if self.frozen[o][iP]:
                                    freezeClause = True
                                    break
                            if not freezeClause:
                                self.frozen[o][self.currentPokemon[o]] = True
    
    def useHyperBeam(self, t):
        
        level = 100
        o = (t + 1) % 2
        if random.randint(0, 255) < pCrit[self.currentPokemon[t]]:
            level = 200
        damage = self.calculateDamage(
            level,
            pAttack[self.currentPokemon[t]],
            150,
            pDefense[self.currentPokemon[o]])
        if self.currentPokemon[o] == 2:
            damage = int(damage / 2)
        damage = int(damage * 1.5)
        substituteBroke = False
        if self.substitute[o] <= 0:
            self.currentHP[o][self.currentPokemon[o]] -= int(damage)
        else:
            self.substitute[o] -= int(damage)
            if self.substitute[o] <= 0:
                substituteBroke = True
        if self.currentHP[o][self.currentPokemon[o]] > 0:
            if not substituteBroke:
                self.recharge[t] = True
    
    def useDrillPeck(self, t):
        
        level = 100
        o = (t + 1) % 2
        if random.randint(0, 255) < 50:
            level = 200
        damage = self.calculateDamage(
            level,
            278,
            80,
            pDefense[self.currentPokemon[o]])
        if self.currentPokemon[o] == 2 or self.currentPokemon[o] == 6:
            damage = int(damage / 2)
        if self.currentPokemon[o] == 1:
            damage = int(damage * 2)
        damage = int(damage * 1.5)
        if self.substitute[o] <= 0:
            self.currentHP[o][self.currentPokemon[o]] -= int(damage)
        else:
            self.substitute[o] -= int(damage)
    
    def useStunSpore(self, t):
        
        o = (t + 1) % 2
        if not self.frozen[o][self.currentPokemon[o]]:
            if self.sleeping[o][self.currentPokemon[o]] <= 0:
                self.paralyzed[o][self.currentPokemon[o]] = True
    
    def useSleepPowder(self, t):
        
        o = (t + 1) % 2
        if not self.frozen[o][self.currentPokemon[o]]:
            if not self.paralyzed[o][self.currentPokemon[o]]:
                sleepClause = False
                for iP in range(1, 7):
                    if self.sleeping[o][iP] > 0:
                        sleepClause = True
                        break
                if not sleepClause:
                    self.sleeping[o][self.currentPokemon[o]] = random.randint(1, 7)
                    self.recharge[o] = False
    
    def useThunderbolt(self, t):
        
        o = (t + 1) % 2
        if random.randint(0, 255) < pCrit[self.currentPokemon[t]]:
            damage = self.calculateDamage(
                200,
                pSpecial[self.currentPokemon[t]],
                95,
                pSpecial[self.currentPokemon[o]])
        else:
            damage = self.calculateDamage(
                100,
                int(statMods[self.specialMod[t]] * pSpecial[self.currentPokemon[t]] / 100),
                95,
                int(statMods[self.specialMod[o]] * pSpecial[self.currentPokemon[o]] / 100))
        if self.currentPokemon[o] == 2:
            damage = 0
        if self.currentPokemon[o] == 1:
            damage = int(damage / 2)
        if self.currentPokemon[t] == 6:
            damage = int(damage * 1.5)
        substituteBroke = False
        if self.substitute[o] <= 0:
            self.currentHP[o][self.currentPokemon[o]] -= int(damage)
        else:
            self.substitute[o] -= int(damage)
            if self.substitute[o] <= 0:
                substituteBroke = True
        if random.randint(0, 255) < 26:
            if self.currentPokemon[o] != 6:
                if self.currentHP[o][self.currentPokemon[o]] > 0:
                    if self.substitute[o] <= 0 and not substituteBroke:
                        if not self.frozen[o][self.currentPokemon[o]]:
                            if self.sleeping[o][self.currentPokemon[o]] <= 0:
                                self.paralyzed[o][self.currentPokemon[o]] = True
    
    def useThunderWave(self, t):
        
        o = (t + 1) % 2
        if self.currentPokemon[o] != 2:
            if not self.frozen[o][self.currentPokemon[o]]:
                if self.sleeping[o][self.currentPokemon[o]] <= 0:
                    self.paralyzed[o][self.currentPokemon[o]] = True
    
    def useEarthquake(self, t):
        
        level = 100
        o = (t + 1) % 2
        if random.randint(0, 255) < pCrit[self.currentPokemon[t]]:
            level = 200
        damage = self.calculateDamage(
            level,
            pAttack[self.currentPokemon[t]],
            100,
            pDefense[self.currentPokemon[o]])
        if self.currentPokemon[o] == 6:
            damage = 0
        if self.currentPokemon[o] == 1:
            damage = int(damage / 2)
        if self.currentPokemon[o] == 2:
            damage = int(damage * 2)
        if self.currentPokemon[t] == 2:
            damage = int(damage * 1.5)
        if self.substitute[o] <= 0:
            self.currentHP[o][self.currentPokemon[o]] -= int(damage)
        else:
            self.substitute[o] -= int(damage)
    
    def usePsychic(self, t):
        
        o = (t + 1) % 2
        if random.randint(0, 255) < 22:
            damage = self.calculateDamage(
                200,
                348,
                90,
                pSpecial[self.currentPokemon[o]])
        else:
            damage = self.calculateDamage(
                100,
                int(statMods[self.specialMod[t]] * 348 / 100),
                90,
                int(statMods[self.specialMod[o]] * pSpecial[self.currentPokemon[o]] / 100))
        if self.currentPokemon[o] == 1:
            damage = int(damage / 2)
        damage = int(damage * 1.5)
        substituteBroke = False
        if self.substitute[o] <= 0:
            self.currentHP[o][self.currentPokemon[o]] -= int(damage)
        else:
            self.substitute[o] -= int(damage)
            if self.substitute[o] <= 0:
                substituteBroke = True
        if random.randint(0, 255) < 85:
            if self.currentHP[o][self.currentPokemon[o]] > 0:
                if self.substitute[o] <= 0 and not substituteBroke:
                    if self.specialMod[o] > 0:
                        self.specialMod[o] -= 1
    
    def useAgility(self, t):
        
        if self.speedMod[t] < 12:
            self.speedMod[t] += 2
    
    def useSelfdestruct(self, t, hit):
        
        if hit:
            level = 100
            o = (t + 1) % 2
            if random.randint(0, 255) < 15:
                level = 200
            damage = self.calculateDamage(
                level,
                318,
                260,
                pDefense[self.currentPokemon[o]])
            if self.currentPokemon[o] == 2:
                damage = int(damage / 2)
            damage = int(damage * 1.5)
            substituteBroke = False
            if self.substitute[o] <= 0:
                self.currentHP[o][self.currentPokemon[o]] -= int(damage)
            else:
                self.substitute[o] -= int(damage)
                if self.substitute[o] <= 0:
                    substituteBroke = True
            if not substituteBroke:
                self.currentHP[t][5] = 0
        else:
            self.currentHP[t][5] = 0
    
    def useSoftboiled(self, t):
        
        self.currentHP[t][3] += 351
        if self.currentHP[t][3] > 703:
            self.currentHP[t][3] = 703
    
    def useExplosion(self, t, hit):
        
        if hit:
            level = 100
            o = (t + 1) % 2
            if random.randint(0, 255) < 22:
                level = 200
            damage = self.calculateDamage(
                level,
                288,
                340,
                pDefense[self.currentPokemon[o]])
            if self.currentPokemon[o] == 2:
                damage = int(damage / 2)
            substituteBroke = False
            if self.substitute[o] <= 0:
                self.currentHP[o][self.currentPokemon[o]] -= int(damage)
            else:
                self.substitute[o] -= int(damage)
                if self.substitute[o] <= 0:
                    substituteBroke = True
            if not substituteBroke:
                self.currentHP[t][1] = 0
        else:
            self.currentHP[t][1] = 0
    
    def useRockSlide(self, t):
        
        level = 100
        o = (t + 1) % 2
        if random.randint(0, 255) < 20:
            level = 200
        damage = self.calculateDamage(
            level,
            358,
            75,
            pDefense[self.currentPokemon[o]])
        if self.currentPokemon[o] == 2:
            damage = int(damage / 2)
        if self.currentPokemon[o] == 6:
            damage = int(damage * 2)
        damage = int(damage * 1.5)
        if self.substitute[o] <= 0:
            self.currentHP[o][self.currentPokemon[o]] -= int(damage)
        else:
            self.substitute[o] -= int(damage)
    
    def useSubstitute(self, t):
        
        if self.substitute[t] <= 0:
            if self.currentHP[t][2] > 103:
                self.currentHP[t][2] -= 103
                self.substitute[t] = 104
            elif self.currentHP[t][2] == 103:
                self.currentHP[t][2] = 0
    
    def calculateDamage(self, level, attack, power, defense):
        
        return int(random.randint(217, 255) * (2 + int((2 + int(2 * level / 5)) * power * attack / (50 * defense))) / 255)

#