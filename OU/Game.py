import random

# Status modifier factor
statMods = [25, 28, 33, 40, 50, 66, 100, 150, 200, 250, 300, 350, 400]

#
# Pokemon
#

# Names
pNames = ['', 'Exeggutor', 'Rhydon', 'Chansey', 'Tauros', 'Snorlax', 'Zapdos']

# Hit Points
pHP = [0, 393, 413, 703, 353, 523, 383]

# Attack
pAttack = [0, 288, 358, 108, 298, 318, 278]

# Defense
pDefense = [0, 268, 338, 108, 288, 228, 268]

# Special
pSpecial = [0, 348, 188, 308, 238, 228, 348]

# Speed
pSpeed = [0, 208, 178, 198, 318, 158, 298]

# Crit
pCrit = [0, 27, 20, 25, 55, 15, 50]

# Moves
pMoves = [
    [0, 0, 0, 0, 0],
    [0, 5, 6, 10, 14],
    [0, 1, 9, 15, 16],
    [0, 2, 7, 8, 13],
    [0, 1, 2, 3, 9],
    [0, 1, 3, 9, 12],
    [0, 4, 7, 8, 11]]

#
# Moves
#

# Names
mNames = ['Struggle',
    'Body Slam',
    'Ice Beam',
    'Hyper Beam',
    'Drill Peck',
    'Stun Spore',
    'Sleep Powder',
    'Thunderbolt', 
    'Thunder Wave',
    'Earthquake',
    'Psychic',
    'Agility',
    'Selfdestruct',
    'Softboiled',
    'Explosion',
    'Rock Slide',
    'Substitute']

# Power
mPower = [50, 85, 95, 150, 80, 0, 0, 95, 0, 100, 90, 0, 260, 0, 340, 75, 0]

# Accuracy
mAccuracy = [256, 255, 255, 230, 255, 191, 191, 255, 255, 255, 255, 256, 255, 256, 255, 230, 256]

# Power points
mPP = [10, 24, 16, 8, 32, 48, 24, 24, 32, 16, 16, 48, 8, 16, 8, 16, 16]


class Game:
    
    
    def __init__(self, state = None):
        
        self.summary = ''
        self.names = ['Player', 'AI']
        
        if state is None:
            
            # Game
            self.round = 0
            self.running = True
            self.win = [False, False]
            
            # Trainer
            self.currentPokemon = [1, 1]
            self.forceSwitch = [False, False]
            self.nextAction = [0, 0]
            self.recharge = [False, False]
            self.remainingPokemon = [6, 6]
            self.substitute = [0, 0]
            self.specialMod = [6, 6]
            self.speedMod = [6, 6]
            
            # Pokemon
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
            
            # Move
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
        
        # Game
        self.round = state[0]
        self.running = state[1]
        self.win = list(state[2])
        
        # Trainer
        self.currentPokemon = list(state[3])
        self.forceSwitch = list(state[4])
        self.nextAction = list(state[5])
        self.recharge = list(state[6])
        self.remainingPokemon = list(state[7])
        self.substitute = list(state[8])
        self.specialMod = list(state[9])
        self.speedMod = list(state[10])
        
        # Pokemon
        self.frozen = [list(state[11][0]), list(state[11][1])]
        self.paralyzed = [list(state[12][0]), list(state[12][1])]
        self.sleeping = [list(state[13][0]), list(state[13][1])]
        self.currentHP = [list(state[14][0]), list(state[14][1])]
        
        # Move
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
        
        # Set perspective
        t = 1
        o = 0
        if isPlayer:
            t = 0
            o = 1
        
        tempState = []
        
        # Game
        tempState.append(self.round)
        tempState.append(self.running)
        tempState.append([self.win[t], self.win[o]])
        
        # Trainer
        tempState.append([self.currentPokemon[t], self.currentPokemon[o]])
        tempState.append([self.forceSwitch[t], self.forceSwitch[o]])
        tempState.append([self.nextAction[t], self.nextAction[o]])
        tempState.append([self.recharge[t], self.recharge[o]])
        tempState.append([self.remainingPokemon[t], self.remainingPokemon[o]])
        tempState.append([self.substitute[t], self.substitute[o]])
        tempState.append([self.specialMod[t], self.specialMod[o]])
        tempState.append([self.speedMod[t], self.speedMod[o]])
        
        # Pokemon
        tempState.append([list(self.frozen[t]), list(self.frozen[o])])
        tempState.append([list(self.paralyzed[t]), list(self.paralyzed[o])])
        tempState.append([list(self.sleeping[t]), list(self.sleeping[o])])
        tempState.append([list(self.currentHP[t]), list(self.currentHP[o])])
        
        # Move
        tempState.append([
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
                list(self.currentPP[o][6])]])
        
        return tempState
    
    def getSummary(self):
        
        temp = self.summary
        if not (self.forceSwitch[0] or self.forceSwitch[1]):
            self.summary = ''
        return temp
    
    def progress(self):
        
        if self.forceSwitch[0] or self.forceSwitch[1]:
            r = random.randint(0, 1)
            for iT in range(2):
                t = (iT + r) % 2
                if self.forceSwitch[t]:
                    
                    # Check for illegal switches
                    if self.nextAction[t] == 0:
                        exit('EXIT [Game.progress()]: Trainer ' + self.names[t] + ' move not set!')
                    if self.nextAction[t][0] < 1 or self.nextAction[t][0] > 6:
                        exit('EXIT [Game.progress()]: Trainer ' + self.names[t] + '\'s chosen switch is illegal!')
                    if self.currentHP[t][self.nextAction[t][0]] <= 0:
                        exit('EXIT [Game.progress()]: Trainer ' + self.names[t] + ' tried switching in fainted ' + pNames[self.nextAction[t][0]] + '!')
                    
                    self.doSwitch(t)
                
                else:
                    self.nextAction[t] = 0
        else:
            
            self.summary += ('Round ' + str(self.round + 1) + '!\n\n')
            
            # Check for illegal actions
            for iT in range(2):
                if self.nextAction[iT] == 0:
                    exit('EXIT [Game.progress()]: Trainer ' + self.names[iT] + ' move not set!')
                if self.nextAction[iT][0] < 0 or self.nextAction[iT][0] > 6:
                    exit('EXIT [Game.progress()]: Trainer ' + self.names[iT] + '\'s chosen switch is illegal!')
                if self.nextAction[iT][1] < 0 or self.nextAction[iT][1] > 4:
                    exit('EXIT [Game.progress()]: Trainer ' + self.names[iT] + '\'s chosen move is illegal!')
                if self.nextAction[iT][0] != 0 and self.currentHP[iT][self.nextAction[iT][0]] <= 0:
                    exit('EXIT [Game.progress()]: Trainer ' + self.names[iT] + ' tried switching in fainted ' + pNames[self.nextAction[iT][0]] + '!')
                if self.nextAction[iT][1] != 0 and self.currentPP[iT][self.currentPokemon[iT]][self.nextAction[iT][1]] <= 0:
                    exit('EXIT [Game.progress()]: Trainer ' + self.names[iT] + ' tried using zero PP move ' + mNames[pMoves[self.currentPokemon[iT]][self.nextAction[iT][1]]] + '!')
            
            # Check if any trainer wants to switch
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
                
                # Compare speed
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
                
                # Use moves in order, only use second move if Pokemon still active
                self.useMove(t)
                if (self.currentHP[t][self.currentPokemon[t]] > 0
                        and self.currentHP[(t + 1) % 2][self.currentPokemon[(t + 1) % 2]] > 0):
                    self.useMove((t + 1) % 2)
                else:
                    self.nextAction[(t + 1) % 2] = 0
            
            # Check if any Pokemon fainted
            for iT in range(2):
                if self.currentHP[iT][self.currentPokemon[iT]] <= 0:
                    self.forceSwitch[iT] = True
                    self.remainingPokemon[iT] -= 1
                    self.frozen[iT][self.currentPokemon[iT]] = False
                    self.paralyzed[iT][self.currentPokemon[iT]] = False
                    self.sleeping[iT][self.currentPokemon[iT]] = 0
                    self.summary += (self.names[iT] + '\'s ' + pNames[self.currentPokemon[iT]] + ' fainted!\n')
            
            # Check if any trainer ran out of Pokemon
            for iT in range(2):
                if self.remainingPokemon[iT] <= 0:
                    self.running = False
                    self.win[(iT + 1) % 2] = True
                    self.summary += ('\n' + self.names[(iT + 1) % 2] + ' wins!\n')
            
            self.round += 1
    
    def doSwitch(self, t):
        
        self.currentPokemon[t] = self.nextAction[t][0]
        self.recharge[t] = False
        self.substitute[t] = 0
        self.specialMod[t] = 6
        self.speedMod[t] = 6
        
        self.forceSwitch[t] = False
        self.nextAction[t] = 0
        
        self.summary += (self.names[t] + ' switched to ' + pNames[self.currentPokemon[t]] + '!\n')
    
    def useMove(self, t):
        
        # Recharge if needed
        if self.recharge[t]:
            self.recharge[t] = False
            self.summary += (self.names[t] + '\'s ' + pNames[self.currentPokemon[t]] + ' recharged!\n')
        
        # Check and determine if paralyzed
        elif self.paralyzed[t][self.currentPokemon[t]] and random.randint(0, 255) < 64:
            self.summary += (self.names[t] + '\'s ' + pNames[self.currentPokemon[t]] + ' is fully paralyzed and can\'t move!\n')
        
        # Check if sleeping and try to wake up
        elif self.sleeping[t][self.currentPokemon[t]] > 0:
            self.sleeping[t][self.currentPokemon[t]] -= 1
            if self.sleeping[t][self.currentPokemon[t]] <= 0:
                self.summary += (self.names[t] + '\'s ' + pNames[self.currentPokemon[t]] + ' woke up from sleep!\n')
            else:
                self.summary += (self.names[t] + '\'s ' + pNames[self.currentPokemon[t]] + ' is sleeping and can\'t move!\n')
        
        # Check if frozen
        elif self.frozen[t][self.currentPokemon[t]]:
            self.summary += (self.names[t] + '\'s ' + pNames[self.currentPokemon[t]] + ' is frozen solid and can\'t move!\n')
        
        else:
            self.summary += (self.names[t] + '\'s ' + pNames[self.currentPokemon[t]] + ' used ' + mNames[pMoves[self.currentPokemon[t]][self.nextAction[t][1]]] + '!\n')
            
            # Deduct PP, unless the move is Struggle
            if self.nextAction[t][1] != 0:
                self.currentPP[t][self.currentPokemon[t]][self.nextAction[t][1]] -= 1
            
            # Check if move misses (1/256 miss bugg included)
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
                self.summary += (self.names[t] + '\'s ' + pNames[self.currentPokemon[t]] + ' missed!\n')
        self.nextAction[t] = 0
    
    def useStruggle(self, t): # All Pokémon
        
        critical = ''
        level = 100
        o = (t + 1) % 2
        
        # Critical hit?
        if random.randint(0, 255) < pCrit[self.currentPokemon[t]]:
            level = 200
            critical = ' critical'
        
        damage = self.calculateDamage(
            level,
            pAttack[self.currentPokemon[t]],
            50,
            pDefense[self.currentPokemon[o]])
        
        # x0.5 against Rhydon
        if self.currentPokemon[o] == 2:
            damage = int(damage / 2)
        
        # STAB using Chansey, Tauros, Snorlax
        if self.currentPokemon[t] == 3 or self.currentPokemon[t] == 4 or self.currentPokemon[t] == 5:
            damage = int(damage * 1.5)
        
        substituteBroke = False
        if self.substitute[o] <= 0:
            self.currentHP[o][self.currentPokemon[o]] -= int(damage)
            self.summary += ('Struggle did ' + str(damage) + critical + ' damage!\n')
        else:
            self.substitute[o] -= int(damage)
            self.summary += ('Struggle did ' + str(damage) + critical + ' damage')
            if self.substitute[o] <= 0:
                substituteBroke = True
                self.summary += (' and broke the substitute!\n')
            else:
                self.summary += (' to the substitute!\n')
        
        if not substituteBroke:
            self.currentHP[t][self.currentPokemon[t]] -= int(damage / 2)
            self.summary += (self.names[t] + '\'s ' + pNames[self.currentPokemon[t]] + ' took ' + str(int(damage / 2)) + ' recoil damage!\n')
    
    def useBodySlam(self, t): # Rhydon, Tauros, Snorlax
        
        critical = ''
        level = 100
        o = (t + 1) % 2
        
        # Critical hit?
        if random.randint(0, 255) < pCrit[self.currentPokemon[t]]:
            level = 200
            critical = ' critical'
        
        damage = self.calculateDamage(
            level,
            pAttack[self.currentPokemon[t]],
            85,
            pDefense[self.currentPokemon[o]])
        
        # x0.5 against Rhydon
        if self.currentPokemon[o] == 2:
            damage = int(damage / 2)
        
        # STAB using Tauros, Snorlax
        if self.currentPokemon[t] == 4 or self.currentPokemon[t] == 5:
            damage = int(damage * 1.5)
        
        substituteBroke = False
        if self.substitute[o] <= 0:
            self.currentHP[o][self.currentPokemon[o]] -= int(damage)
            self.summary += ('Body Slam did ' + str(damage) + critical + ' damage!\n')
        else:
            self.substitute[o] -= int(damage)
            self.summary += ('Body Slam did ' + str(damage) + critical + ' damage')
            if self.substitute[o] <= 0:
                substituteBroke = True
                self.summary += (' and broke the substitute!\n')
            else:
                self.summary += (' to the substitute!\n')
        
        # 30%: Paralyze
        if random.randint(0, 255) < 77:
            
            # Can only paralyze Exeggutor, Rhydon, Zapdos
            if self.currentPokemon[o] == 1 or self.currentPokemon[o] == 2 or self.currentPokemon[o] == 6:
                
                # Don't if fainted from attack
                if self.currentHP[o][self.currentPokemon[o]] > 0:
                    
                    # Don't if substitute exist or existed
                    if self.substitute[o] <= 0 and not substituteBroke:
                        
                        # Unless already frozen
                        if not self.frozen[o][self.currentPokemon[o]]:
                            
                            # Unless already paralyzed
                            if not self.paralyzed[o][self.currentPokemon[o]]:
                                
                                # Unless already sleeping
                                if self.sleeping[o][self.currentPokemon[o]] <= 0:
                                    
                                    self.paralyzed[o][self.currentPokemon[o]] = True
                                    self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + ' was paralyzed!\n')
                                else:
                                    self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + ' is already sleeping!\n')
                            else:
                                self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + ' is already paralyzed!\n')
                        else:
                            self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + ' is already frozen!\n')
    
    def useIceBeam(self, t): # Chansey, Tauros
        
        critical = ''
        o = (t + 1) % 2
        
        # Critical hit?
        if random.randint(0, 255) < pCrit[self.currentPokemon[t]]:
            damage = self.calculateDamage(
                200,
                pSpecial[self.currentPokemon[t]],
                95,
                pSpecial[self.currentPokemon[o]])
            critical = ' critical'
        else:
            damage = self.calculateDamage(
                100,
                int(statMods[self.specialMod[t]] * pSpecial[self.currentPokemon[t]] / 100),
                95,
                int(statMods[self.specialMod[o]] * pSpecial[self.currentPokemon[o]] / 100))
        
        # x2 against Exeggutor, Rhydon, Zapdos
        if self.currentPokemon[o] == 1 or self.currentPokemon[o] == 2 or self.currentPokemon[o] == 6:
            damage = int(damage * 2)
        
        substituteBroke = False
        if self.substitute[o] <= 0:
            self.currentHP[o][self.currentPokemon[o]] -= int(damage)
            self.summary += ('Ice Beam did ' + str(damage) + critical + ' damage!\n')
        else:
            self.substitute[o] -= int(damage)
            self.summary += ('Ice Beam did ' + str(damage) + critical + ' damage')
            if self.substitute[o] <= 0:
                substituteBroke = True
                self.summary += (' and broke the substitute!\n')
            else:
                self.summary += (' to the substitute!\n')
        
        # 10%: Freeze
        if random.randint(0, 255) < 26:
        
            # Don't if fainted from attack
            if self.currentHP[o][self.currentPokemon[o]] > 0:
                
                # Don't if substitute exist or existed
                if self.substitute[o] <= 0 and not substituteBroke:
                    
                    # Only if no other freeze currently exists
                    freezeClause = False
                    for iP in range(1, 7):
                        if self.frozen[o][iP]:
                            freezeClause = True
                            break
                    if not freezeClause:
                        
                        # Unless already paralyzed
                        if not self.paralyzed[o][self.currentPokemon[o]]:
                            
                            # Unless already sleeping
                            if self.sleeping[o][self.currentPokemon[o]] <= 0:
                            
                                self.frozen[o][self.currentPokemon[o]] = True
                                self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + ' was frozen!\n')
                            else:
                                self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + ' is already sleeping!\n')
                        else:
                            self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + ' is already paralyzed!\n')
                    else:
                        self.summary += ('Only one Pokémon on each team may be frozen at one time!\n')
    
    def useHyperBeam(self, t): # Tauros, Snorlax
        
        critical = ''
        level = 100
        o = (t + 1) % 2
        
        # Critical hit?
        if random.randint(0, 255) < pCrit[self.currentPokemon[t]]:
            level = 200
            critical = ' critical'
        
        damage = self.calculateDamage(
            level,
            pAttack[self.currentPokemon[t]],
            150,
            pDefense[self.currentPokemon[o]])
        
        # x0.5 against Rhydon
        if self.currentPokemon[o] == 2:
            damage = int(damage / 2)
        
        # STAB using Tauros, Snorlax
        damage = int(damage * 1.5)
        
        substituteBroke = False
        if self.substitute[o] <= 0:
            self.currentHP[o][self.currentPokemon[o]] -= int(damage)
            self.summary += ('Hyper Beam did ' + str(damage) + critical + ' damage!\n')
        else:
            self.substitute[o] -= int(damage)
            self.summary += ('Hyper Beam did ' + str(damage) + critical + ' damage')
            if self.substitute[o] <= 0:
                substituteBroke = True
                self.summary += (' and broke the substitute!\n')
            else:
                self.summary += (' to the substitute!\n')
        
        # Force recharge, unless opponent fainted or substitute broke
        if self.currentHP[o][self.currentPokemon[o]] > 0:
            if not substituteBroke:
                self.recharge[t] = True
    
    def useDrillPeck(self, t): # Zapdos
        
        critical = ''
        level = 100
        o = (t + 1) % 2
        
        # Critical hit?
        if random.randint(0, 255) < 50:
            level = 200
            critical = ' critical'
        
        damage = self.calculateDamage(
            level,
            278,
            80,
            pDefense[self.currentPokemon[o]])
        
        # x0.5 against Rhydon, Zapdos
        if self.currentPokemon[o] == 2 or self.currentPokemon[o] == 6:
            damage = int(damage / 2)
        
        # x2 against Exeggutor
        if self.currentPokemon[o] == 1:
            damage = int(damage * 2)
        
        # STAB using Zapdos
        damage = int(damage * 1.5)
        
        if self.substitute[o] <= 0:
            self.currentHP[o][self.currentPokemon[o]] -= int(damage)
            self.summary += ('Drill Peck did ' + str(damage) + critical + ' damage!\n')
        else:
            self.substitute[o] -= int(damage)
            self.summary += ('Drill Peck did ' + str(damage) + critical + ' damage')
            if self.substitute[o] <= 0:
                self.summary += (' and broke the substitute!\n')
            else:
                self.summary += (' to the substitute!\n')
    
    def useStunSpore(self, t): # Exeggutor
        
        # Can paralyze even with substitute
        
        o = (t + 1) % 2
        
        # Unless already frozen
        if not self.frozen[o][self.currentPokemon[o]]:
            
            # Unless already paralyzed
            if not self.paralyzed[o][self.currentPokemon[o]]:
                
                # Unless already sleeping
                if self.sleeping[o][self.currentPokemon[o]] <= 0:
                    
                    self.paralyzed[o][self.currentPokemon[o]] = True
                    self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + ' was paralyzed!\n')
                else:
                    self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + ' is already sleeping!\n')
            else:
                self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + ' is already paralyzed!\n')
        else:
            self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + ' is already frozen!\n')
    
    def useSleepPowder(self, t): # Exeggutor
        
        # Can sleep even with substitute
        
        o = (t + 1) % 2
        
        # Only if no other sleep currently exists
        sleepClause = False
        for iP in range(1, 7):
            if self.sleeping[o][iP] > 0:
                sleepClause = True
                break
        if not sleepClause:
            
            # Unless already frozen
            if not self.frozen[o][self.currentPokemon[o]]:
                
                # Unless already paralyzed
                if not self.paralyzed[o][self.currentPokemon[o]]:
                    
                    self.sleeping[o][self.currentPokemon[o]] = random.randint(1, 7)
                    self.recharge[o] = False
                    self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + ' fell asleep!\n')
                else:
                    self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + ' is already paralyzed!\n')
            else:
                self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + ' is already frozen!\n')
        else:
            self.summary += ('Only one Pokémon on each team may be sleeping at one time!\n')
    
    def useThunderbolt(self, t): # Chansey, Zapdos
        
        critical = ''
        o = (t + 1) % 2
        
        # Critical hit?
        if random.randint(0, 255) < pCrit[self.currentPokemon[t]]:
            damage = self.calculateDamage(
                200,
                pSpecial[self.currentPokemon[t]],
                95,
                pSpecial[self.currentPokemon[o]])
            critical = ' critical'
        else:
            damage = self.calculateDamage(
                100,
                int(statMods[self.specialMod[t]] * pSpecial[self.currentPokemon[t]] / 100),
                95,
                int(statMods[self.specialMod[o]] * pSpecial[self.currentPokemon[o]] / 100))
        
        # x0 against Rhydon
        if self.currentPokemon[o] == 2:
            damage = 0
            critical = ''
        
        # x0.5 against Exeggutor
        if self.currentPokemon[o] == 1:
            damage = int(damage / 2)
        
        # STAB using Zapdos
        if self.currentPokemon[t] == 6:
            damage = int(damage * 1.5)
        
        substituteBroke = False
        if self.substitute[o] <= 0:
            self.currentHP[o][self.currentPokemon[o]] -= int(damage)
            self.summary += ('Thunderbolt did ' + str(damage) + critical + ' damage!\n')
        else:
            self.substitute[o] -= int(damage)
            self.summary += ('Thunderbolt did ' + str(damage) + critical + ' damage')
            if self.substitute[o] <= 0:
                substituteBroke = True
                self.summary += (' and broke the substitute!\n')
            else:
                self.summary += (' to the substitute!\n')
        
        # 10%: Paralyze
        if random.randint(0, 255) < 26:
            
            # Can not paralyze Zapdos
            if self.currentPokemon[o] != 6:
                
                # Don't if fainted from attack
                if self.currentHP[o][self.currentPokemon[o]] > 0:
                    
                    # Don't if substitute exist or existed
                    if self.substitute[o] <= 0 and not substituteBroke:
                        
                        # Unless already frozen
                        if not self.frozen[o][self.currentPokemon[o]]:
                            
                            # Unless already paralyzed
                            if not self.paralyzed[o][self.currentPokemon[o]]:
                                
                                # Unless already sleeping
                                if self.sleeping[o][self.currentPokemon[o]] <= 0:
                                    
                                    self.paralyzed[o][self.currentPokemon[o]] = True
                                    self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + ' was paralyzed!\n')
                                else:
                                    self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + ' is already sleeping!\n')
                            else:
                                self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + ' is already paralyzed!\n')
                        else:
                            self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + ' is already frozen!\n')
    
    def useThunderWave(self, t): # Chansey, Zapdos
        
        # Can paralyze even with substitute
        
        o = (t + 1) % 2
        
        # Can not paralyze Rhydon
        if self.currentPokemon[o] != 2:
            
            # Unless already frozen
            if not self.frozen[o][self.currentPokemon[o]]:
                
                # Unless already paralyzed
                if not self.paralyzed[o][self.currentPokemon[o]]:
                    
                    # Unless already sleeping
                    if self.sleeping[o][self.currentPokemon[o]] <= 0:
                        self.paralyzed[o][self.currentPokemon[o]] = True
                        self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + ' was paralyzed!\n')
                    else:
                        self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + ' is already sleeping!\n')
                else:
                    self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + ' is already paralyzed!\n')
            else:
                self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + ' is already frozen!\n')
        else:
            self.summary += ('It has no effect against ' + self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + '!\n')
    
    def useEarthquake(self, t): # Rhydon, Tauros, Snorlax
        
        critical = ''
        level = 100
        o = (t + 1) % 2
        
        # Critical hit?
        if random.randint(0, 255) < pCrit[self.currentPokemon[t]]:
            level = 200
            critical = ' critical'
        
        damage = self.calculateDamage(
            level,
            pAttack[self.currentPokemon[t]],
            100,
            pDefense[self.currentPokemon[o]])
        
        # x0 against Zapdos
        if self.currentPokemon[o] == 6:
            damage = 0
            critical = ''
        
        # x0.5 against Exeggutor
        if self.currentPokemon[o] == 1:
            damage = int(damage / 2)
        
        # x2 against Rhydon
        if self.currentPokemon[o] == 2:
            damage = int(damage * 2)
        
        # STAB using Rhydon
        if self.currentPokemon[t] == 2:
            damage = int(damage * 1.5)
        
        if self.substitute[o] <= 0:
            self.currentHP[o][self.currentPokemon[o]] -= int(damage)
            self.summary += ('Earthquake did ' + str(damage) + critical + ' damage!\n')
        else:
            self.substitute[o] -= int(damage)
            self.summary += ('Earthquake did ' + str(damage) + critical + ' damage')
            if self.substitute[o] <= 0:
                self.summary += (' and broke the substitute!\n')
            else:
                self.summary += (' to the substitute!\n')
    
    def usePsychic(self, t): # Exeggutor
        
        critical = ''
        o = (t + 1) % 2
        
        # Critical hit?
        if random.randint(0, 255) < 27:
            damage = self.calculateDamage(
                200,
                348,
                90,
                pSpecial[self.currentPokemon[o]])
            critical = ' critical'
        else:
            damage = self.calculateDamage(
                100,
                int(statMods[self.specialMod[t]] * 348 / 100),
                90,
                int(statMods[self.specialMod[o]] * pSpecial[self.currentPokemon[o]] / 100))
        
        # x0.5 against Exeggutor
        if self.currentPokemon[o] == 1:
            damage = int(damage / 2)
        
        # STAB using Exeggutor
        damage = int(damage * 1.5)
        
        substituteBroke = False
        if self.substitute[o] <= 0:
            self.currentHP[o][self.currentPokemon[o]] -= int(damage)
            self.summary += ('Psychic did ' + str(damage) + critical + ' damage!\n')
        else:
            self.substitute[o] -= int(damage)
            self.summary += ('Psychic did ' + str(damage) + critical + ' damage')
            if self.substitute[o] <= 0:
                substituteBroke = True
                self.summary += (' and broke the substitute!\n')
            else:
                self.summary += (' to the substitute!\n')
        
        # 33.2%: Decrease special
        if random.randint(0, 255) < 85:
            
            # Unless fainted from the attack
            if self.currentHP[o][self.currentPokemon[o]] > 0:
                
                # Don't if substitute exist or existed
                if self.substitute[o] <= 0 and not substituteBroke:
                    
                    # Don't if at minimum
                    if self.specialMod[o] > 0:
                        self.specialMod[o] -= 1
                        self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + '\'s special fell!\n')
                    else:
                        self.summary += (self.names[o] + '\'s ' + pNames[self.currentPokemon[o]] + '\'s special can not be decreased more!\n')
    
    def useAgility(self, t): # Zapdos
        
        if self.speedMod[t] < 12:
            self.speedMod[t] += 2
            self.summary += (self.names[t] + '\'s Zapdos\'s speed greatly rose!\n')
        else:
            self.summary += (self.names[t] + '\'s Zapdos\'s speed can not rise more!\n')
    
    def useSelfdestruct(self, t, hit): # Snorlax
        
        if hit:
            critical = ''
            level = 100
            o = (t + 1) % 2
            
            # Critical hit?
            if random.randint(0, 255) < 15:
                level = 200
                critical = ' critical'
            
            damage = self.calculateDamage(
                level,
                318,
                260,
                pDefense[self.currentPokemon[o]])
            
            # x0.5 against Rhydon
            if self.currentPokemon[o] == 2:
                damage = int(damage / 2)
            
            # STAB using Snorlax
            damage = int(damage * 1.5)
            
            substituteBroke = False
            if self.substitute[o] <= 0:
                self.currentHP[o][self.currentPokemon[o]] -= int(damage)
                self.summary += ('Selfdestruct did ' + str(damage) + critical + ' damage!\n')
            else:
                self.substitute[o] -= int(damage)
                self.summary += ('Selfdestruct did ' + str(damage) + critical + ' damage')
                if self.substitute[o] <= 0:
                    substituteBroke = True
                    self.summary += (' and broke the substitute!\n')
                else:
                    self.summary += (' to the substitute!\n')
            
            if not substituteBroke:
                self.currentHP[t][5] = 0
        else:
            self.currentHP[t][5] = 0
    
    def useSoftboiled(self, t): # Chansey
        
        self.currentHP[t][3] += 351
        if self.currentHP[t][3] > 703:
            overheal = self.currentHP[t][3] - 703
            self.currentHP[t][3] = 703
            self.summary += ('Softboiled healed for ' + str(351 - overheal) + ' damage!\n')
        else:
            self.summary += ('Softboiled healed for ' + str(351) + ' damage!\n')
    
    def useExplosion(self, t, hit): # Exeggutor
        
        if hit:
            critical = ''
            level = 100
            o = (t + 1) % 2
            
            # Critical hit?
            if random.randint(0, 255) < 27:
                level = 200
                critical = ' critical'
            
            damage = self.calculateDamage(
                level,
                288,
                340,
                pDefense[self.currentPokemon[o]])
            
            # x0.5 against Rhydon
            if self.currentPokemon[o] == 2:
                damage = int(damage / 2)
            
            substituteBroke = False
            if self.substitute[o] <= 0:
                self.currentHP[o][self.currentPokemon[o]] -= int(damage)
                self.summary += ('Explosion did ' + str(damage) + critical + ' damage!\n')
            else:
                self.substitute[o] -= int(damage)
                self.summary += ('Explosion did ' + str(damage) + critical + ' damage')
                if self.substitute[o] <= 0:
                    substituteBroke = True
                    self.summary += (' and broke the substitute!\n')
                else:
                    self.summary += (' to the substitute!\n')
            
            if not substituteBroke:
                self.currentHP[t][1] = 0
        else:
            self.currentHP[t][1] = 0
    
    def useRockSlide(self, t): # Rhydon
        
        critical = ''
        level = 100
        o = (t + 1) % 2
        
        # Critical hit?
        if random.randint(0, 255) < 20:
            level = 200
            critical = ' critical'
        
        damage = self.calculateDamage(
            level,
            358,
            75,
            pDefense[self.currentPokemon[o]])
        
        # x0.5 against Rhydon
        if self.currentPokemon[o] == 2:
            damage = int(damage / 2)
        
        # x2 against Zapdos
        if self.currentPokemon[o] == 6:
            damage = int(damage * 2)
        
        # STAB using Rhydon
        damage = int(damage * 1.5)
        
        if self.substitute[o] <= 0:
            self.currentHP[o][self.currentPokemon[o]] -= int(damage)
            self.summary += ('Rock Slide did ' + str(damage) + critical + ' damage!\n')
        else:
            self.substitute[o] -= int(damage)
            self.summary += ('Rock Slide did ' + str(damage) + critical + ' damage')
            if self.substitute[o] <= 0:
                self.summary += (' and broke the substitute!\n')
            else:
                self.summary += (' to the substitute!\n')
    
    def useSubstitute(self, t): # Rhydon
        
        if self.substitute[t] <= 0:
            if self.currentHP[t][2] > 103:
                self.currentHP[t][2] -= 103
                self.substitute[t] = 104
                self.summary += (self.names[t] + '\'s Rhydon did 103 damage to itself and created a substitute with 104 hit points!\n')
            elif self.currentHP[t][2] < 103:
                self.summary += (self.names[t] + '\'s Rhydon\'s health is too low to create a substitute!\n')
            else:
                self.currentHP[t][2] = 0
                self.summary += (self.names[t] + '\'s Rhydon did 103 damage to itself!\n')
        else:
            self.summary += (self.names[t] + '\'s Rhydon already has a substitute!\n')
    
    def calculateDamage(self, level, attack, power, defense):
        
        return int(random.randint(217, 255) * (2 + int((2 + int(2 * level / 5)) * power * attack / (50 * defense))) / 255)

#