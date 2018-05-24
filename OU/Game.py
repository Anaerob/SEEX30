import numpy as np

import Constants as c
import Trainer


class Game:
    
    
    def __init__(self, printMe, state = None):
        
        self.printMe = printMe
        
        self.round = 0
        self.running = True
        self.forceSwitch = [False, False]
        self.win = [False, False]
        self.trainers = [Trainer.Trainer('Black'), Trainer.Trainer('White')]
        if state is not None:
            self.setState(state)
        elif printMe:
            print('Player sent out Exeggutor!')
            print('AI sent out Exeggutor!')
    
    def setState(self, state):
        
        self.round = state[0]
        self.running = state[1]
        self.forceSwitch = [state[2], state[3]]
        self.win = [state[4], state[5]]
        self.trainers = [
            Trainer.Trainer('Black', state[6]),
            Trainer.Trainer('White', state[7])]
    
    def getState(self, isBlack):
        
        tempState = []
        tempState.append(self.round)
        tempState.append(self.running)
        p = 1
        if isBlack:
            p = 0
        tempState.append(self.forceSwitch[p])
        tempState.append(self.forceSwitch[(p + 1) % 2])
        tempState.append(self.win[p])
        tempState.append(self.win[(p + 1) % 2])
        tempState.append(self.trainers[p].getState())
        tempState.append(self.trainers[(p + 1) % 2].getState())
        return tempState
    
    def getFeatures(self, isBlack):
        
        tempFeatures = np.array([])
        p = 1
        if isBlack:
            p = 0
        tempFeatures = np.append(tempFeatures, self.trainers[p].getFeatures())
        tempFeatures = np.append(tempFeatures, self.trainers[(p + 1) % 2].getFeatures())
        return tempFeatures
    
    def progress(self):
        
        if self.forceSwitch[0] or self.forceSwitch[1]:
            r = np.random.randint(2)
            for iT in range(2):
                t = (iT + r) % 2
                if self.forceSwitch[t]:
                    
                    if not self.trainers[t].nextActionSet:
                        exit('EXIT [Game.progress()]: Trainer ' + self.trainers[t].name + ' move not set!')
                    elif self.trainers[t].nextAction[0] < 1 or self.trainers[t].nextAction[0] > 6:
                        exit('EXIT [Game.progress()]: Trainer ' + self.trainers[t].name + '\'s chosen switch is illegal!')
                    elif self.trainers[t].pokemon[self.trainers[t].nextAction[0]].cHP <= 0:
                        exit('EXIT [Game.progress()]: Trainer ' + self.trainers[t].name + ' tried switching in fainted ' + self.trainers[t].pokemon[self.trainers[t].nextAction[0]].name)
                    
                    self.doSwitch(t)
                
                else:
                    self.trainers[t].resetNextAction()
        else:
            
            if self.printMe:
                print('\n' + 'Round ' + str(self.round + 1) + '!\n')
            
            for iT in range(2):
                if not self.trainers[iT].nextActionSet:
                    exit('EXIT [Game.progress()]: Trainer ' + self.trainers[iT].name + ' move not set!')
                elif self.trainers[iT].nextAction[0] < 0 or self.trainers[iT].nextAction[0] > 6:
                    exit('EXIT [Game.progress()]: Trainer ' + self.trainers[iT].name + '\'s chosen switch is illegal!')
                elif self.trainers[iT].nextAction[1] < 0 or self.trainers[iT].nextAction[1] > 4:
                    exit('EXIT [Game.progress()]: Trainer ' + self.trainers[iT].name + '\'s chosen move is illegal!')
                elif self.trainers[iT].nextAction[0] != 0:
                    if self.trainers[iT].pokemon[self.trainers[iT].nextAction[0]].cHP <= 0:
                        exit('EXIT [Game.progress()]: Trainer ' + self.trainers[iT].name + ' tried switching in fainted Pokémon!')
            
            bSwitch = self.trainers[0].nextAction[0] > 0 and not self.trainers[0].recharge
            wSwitch = self.trainers[1].nextAction[0] > 0 and not self.trainers[1].recharge
            if bSwitch and wSwitch:
                t = np.random.randint(2)
                self.doSwitch(t)
                self.doSwitch((t + 1) % 2)
            elif bSwitch:
                self.doSwitch(0)
                self.useMove(1)
            elif wSwitch:
                self.doSwitch(1)
                self.useMove(0)
            else:
                
                # Flooring and division by 100 * 100 omitted because not neccessary for comparison
                bSpeed = (self.trainers[0].pokemon[self.trainers[0].cP].speed
                    * c.statMods[self.trainers[0].speedMod]
                    * (100 - 75 * self.trainers[0].pokemon[self.trainers[0].cP].paralyzed))
                wSpeed = (self.trainers[1].pokemon[self.trainers[1].cP].speed
                    * c.statMods[self.trainers[1].speedMod]
                    * (100 - 75 * self.trainers[1].pokemon[self.trainers[1].cP].paralyzed))
                
                t = int(bSpeed < wSpeed)
                if bSpeed == wSpeed:
                    t = np.random.randint(2)
                
                # Use moves in order, only use second move if Pokemon still active
                self.useMove(t)
                if (self.trainers[t].pokemon[self.trainers[t].cP].cHP > 0
                        and self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP].cHP > 0):
                    self.useMove((t + 1) % 2)
                else:
                    self.trainers[(t + 1) % 2].resetNextAction()
            
            for iT in range(2):
                if self.trainers[iT].pokemon[self.trainers[iT].cP].cHP <= 0:
                    if self.printMe:
                        print(self.trainers[iT].name + '\'s ' + self.trainers[iT].pokemon[self.trainers[iT].cP].name + ' fainted!')
                    self.forceSwitch[iT] = True
                    self.trainers[iT].rP -= 1
                    self.trainers[iT].pokemon[self.trainers[iT].cP].frozen = False
                    self.trainers[iT].pokemon[self.trainers[iT].cP].paralyzed = False
                    self.trainers[iT].pokemon[self.trainers[iT].cP].sleeping = 0
            
            for iT in range(2):
                if self.trainers[iT].rP <= 0:
                    self.running = False
                    self.win[(iT + 1) % 2] = True
                    if self.printMe:
                        print('\n' + self.trainers[(iT + 1) % 2].name + ' wins!\n')
            
            self.round += 1
    
    def doSwitch(self, t):
        
        self.trainers[t].cP = self.trainers[t].nextAction[0]
        self.forceSwitch[t] = False
        self.trainers[t].resetNextAction()
        self.trainers[t].recharge = False
        self.trainers[t].substitute = 0
        self.trainers[t].specialMod = 6
        self.trainers[t].speedMod = 6
        
        if self.printMe:
            print(self.trainers[t].name + ' switched to ' + str(self.trainers[t].pokemon[self.trainers[t].cP].name) + '!')
    
    def useMove(self, t):
        
        # Recharge if needed
        if self.trainers[t].recharge:
            self.trainers[t].recharge = False
            if self.printMe:
                print(self.trainers[t].name + '\'s ' + str(self.trainers[t].pokemon[self.trainers[t].cP].name) + ' recharged!')
        
        # Check and determine if paralyzed
        elif self.trainers[t].pokemon[self.trainers[t].cP].paralyzed and np.random.randint(256) < 64:
            if self.printMe:
                print(self.trainers[t].name + '\'s ' + str(self.trainers[t].pokemon[self.trainers[t].cP].name) + ' is paralyzed and can\'t move!')
        
        # Check if frozen
        elif self.trainers[t].pokemon[self.trainers[t].cP].frozen:
            if self.printMe:
                print(self.trainers[t].name + '\'s ' + str(self.trainers[t].pokemon[self.trainers[t].cP].name) + ' is frozen and can\'t move!')
        
        # Check if sleeping and try to wake up
        elif self.trainers[t].pokemon[self.trainers[t].cP].sleeping > 0:
            self.trainers[t].pokemon[self.trainers[t].cP].sleeping -= 1
            if self.printMe:
                if self.trainers[t].pokemon[self.trainers[t].cP].sleeping <= 0:
                    print(self.trainers[t].name + '\'s ' + str(self.trainers[t].pokemon[self.trainers[t].cP].name) + ' woke up from sleep!')
                else:
                    print(self.trainers[t].name + '\'s ' + str(self.trainers[t].pokemon[self.trainers[t].cP].name) + ' is sleeping and can\'t move!')
        
        else:
            if self.printMe:
                print(self.trainers[t].name + '\'s ' + str(self.trainers[t].pokemon[self.trainers[t].cP].name) + ' used ' + str(self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextAction[1]].name) + '!')
            
            # Deduct PP, unless the move is Struggle
            if self.trainers[t].nextAction[1] != 0:
                self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextAction[1]].cPP -= 1
            
            # Check if move misses (1/256 miss bugg included)
            if np.random.randint(256) < self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextAction[1]].accuracy:
                
                if self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextAction[1]].index == 34:
                    self.useBodySlam(t)
                elif self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextAction[1]].index == 58:
                    self.useIceBeam(t)
                elif self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextAction[1]].index == 63:
                    self.useHyperBeam(t)
                elif self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextAction[1]].index == 65:
                    self.useDrillPeck(t)
                elif self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextAction[1]].index == 78:
                    self.useStunSpore(t)
                elif self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextAction[1]].index == 79:
                    self.useSleepPowder(t)
                elif self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextAction[1]].index == 85:
                    self.useThunderbolt(t)
                elif self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextAction[1]].index == 86:
                    self.useThunderWave(t)
                elif self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextAction[1]].index == 89:
                    self.useEarthquake(t)
                elif self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextAction[1]].index == 94:
                    self.usePsychic(t)
                elif self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextAction[1]].index == 97:
                    self.useAgility(t)
                elif self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextAction[1]].index == 120:
                    self.useSelfdestruct(t, True)
                elif self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextAction[1]].index == 135:
                    self.useSoftboiled(t)
                elif self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextAction[1]].index == 153:
                    self.useExplosion(t, True)
                elif self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextAction[1]].index == 157:
                    self.useRockSlide(t)
                elif self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextAction[1]].index == 164:
                    self.useSubstitute(t)
                elif self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextAction[1]].index == 165:
                    self.useStruggle(t)
            else:
                if self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextAction[1]].index == 120:
                    self.useSelfdestruct(t, False)
                elif self.trainers[t].pokemon[self.trainers[t].cP].moves[self.trainers[t].nextAction[1]].index == 153:
                    self.useExplosion(t, False)
                if self.printMe:
                    print(self.trainers[t].name + '\'s ' + str(self.trainers[t].pokemon[self.trainers[t].cP].name) + ' missed!')
        self.trainers[t].resetNextAction()
    
    def useBodySlam(self, t): # Rhydon, Tauros, Snorlax
        
        critical = ' damage'
        level = 100
        o = (t + 1) % 2
        
        # Critical hit?
        if np.random.randint(256) < np.floor(self.trainers[t].pokemon[self.trainers[t].cP].baseSpeed / 2):
            level = 200
            critical = ' critical damage'
        
        damage = self.calculateDamage(
            level,
            self.trainers[t].pokemon[self.trainers[t].cP].attack,
            85,
            self.trainers[o].pokemon[self.trainers[o].cP].defense)
        
        # x0.5 against Rhydon
        if self.trainers[o].pokemon[self.trainers[o].cP].index == 112:
            damage = int(damage / 2)
        
        # STAB using Tauros, Snorlax
        if (self.trainers[t].pokemon[self.trainers[t].cP].index == 128
                or self.trainers[t].pokemon[self.trainers[t].cP].index == 143):
            damage = int(damage * 1.5)
        
        [overkill, subBroke] = self.trainers[o].inflictDamage(damage, False)
        if self.printMe:
            self.damagePrint(o, critical, damage, overkill, subBroke)
        
        # Paralyze except against Chansey, Tauros, Snorlax
        if (self.trainers[o].pokemon[self.trainers[o].cP].index != 113
                and self.trainers[o].pokemon[self.trainers[o].cP].index != 128
                and self.trainers[o].pokemon[self.trainers[o].cP].index != 143):
            
            if self.trainers[o].pokemon[self.trainers[o].cP].cHP > 0:
                
                # Can not paralyze substitute, even if broken
                if self.trainers[o].substitute <= 0 and not subBroke:
                    
                    # 30%: paralyze
                    if np.random.randint(256) < 77:
                        if not self.trainers[o].pokemon[self.trainers[o].cP].frozen:
                            if not self.trainers[o].pokemon[self.trainers[o].cP].paralyzed:
                                if self.trainers[o].pokemon[self.trainers[o].cP].sleeping <= 0:
                                    self.trainers[o].pokemon[self.trainers[o].cP].paralyzed = True
                                    if self.printMe:
                                        print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + ' was paralyzed!')
                                else:
                                    if self.printMe:
                                        print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + ' is already sleeping!')
                            else:
                                if self.printMe:
                                    print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + ' is already paralyzed!')
                        else:
                            if self.printMe:
                                print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + ' is already frozen!')
    
    def useIceBeam(self, t): # Chansey, Tauros
        
        critical = ' damage'
        o = (t + 1) % 2
        
        # Critical hit?
        if np.random.randint(256) < np.floor(self.trainers[t].pokemon[self.trainers[t].cP].baseSpeed / 2):
            damage = self.calculateDamage(
                200,
                self.trainers[t].pokemon[self.trainers[t].cP].special,
                95,
                self.trainers[o].pokemon[self.trainers[o].cP].special)
            critical = ' critical damage'
        else:
            damage = self.calculateDamage(
                100,
                np.floor(
                    c.statMods[self.trainers[t].specialMod]
                    * self.trainers[t].pokemon[self.trainers[t].cP].special / 100),
                95,
                np.floor(
                    c.statMods[self.trainers[o].specialMod]
                    * self.trainers[o].pokemon[self.trainers[o].cP].special / 100))
        
        # x2 against Exeggutor, Rhydon, Zapdos
        if (self.trainers[o].pokemon[self.trainers[o].cP].index == 103
                or self.trainers[o].pokemon[self.trainers[o].cP].index == 112
                or self.trainers[o].pokemon[self.trainers[o].cP].index == 145):
            damage = int(damage * 2)
        
        [overkill, subBroke] = self.trainers[o].inflictDamage(damage, False)
        if self.printMe:
            self.damagePrint(o, critical, damage, overkill, subBroke)
        
        if self.trainers[o].pokemon[self.trainers[o].cP].cHP > 0:
            
            # Can not freeze substitute, even if broken
            if self.trainers[o].substitute <= 0 and not subBroke:
            
                # 10%: freeze
                if np.random.randint(256) < 26:
                    freezeClause = False
                    for iP in range(1, 7):
                        if self.trainers[o].pokemon[iP].frozen:
                            freezeClause = True
                    if not freezeClause:
                        if not self.trainers[o].pokemon[self.trainers[o].cP].paralyzed:
                            if self.trainers[o].pokemon[self.trainers[o].cP].sleeping <= 0:
                                self.trainers[o].pokemon[self.trainers[o].cP].frozen = True
                                if self.printMe:
                                    print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + ' was frozen!')
                            else:
                                if self.printMe:
                                    print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + ' is already sleeping!')
                        else:
                            if self.printMe:
                                print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + ' is already paralyzed!')
                    else:
                        if self.printMe:
                            print('Only one Pokémon on each team may be frozen at one time!')
    
    def useHyperBeam(self, t): # Tauros, Snorlax
        
        critical = ' damage'
        level = 100
        o = (t + 1) % 2
        
        # Critical hit?
        if np.random.randint(256) < np.floor(self.trainers[t].pokemon[self.trainers[t].cP].baseSpeed / 2):
            level = 200
            critical = ' critical damage'
        
        damage = self.calculateDamage(
            level,
            self.trainers[t].pokemon[self.trainers[t].cP].attack,
            150,
            self.trainers[o].pokemon[self.trainers[o].cP].defense)
        
        # x0.5 against Rhydon
        if self.trainers[o].pokemon[self.trainers[o].cP].index == 112:
            damage = int(damage / 2)
        
        # STAB using Tauros, Snorlax
        damage = int(damage * 1.5)
        
        [overkill, subBroke] = self.trainers[o].inflictDamage(damage, False)
        if self.printMe:
            self.damagePrint(o, critical, damage, overkill, subBroke)
        
        # Force recharge
        if self.trainers[o].pokemon[self.trainers[o].cP].cHP > 0:
            if not subBroke:
                self.trainers[t].recharge = True
    
    def useDrillPeck(self, t): # Zapdos
        
        critical = ' damage'
        level = 100
        o = (t + 1) % 2
        
        # Critical hit?
        if np.random.randint(256) < 50:
            level = 200
            critical = ' critical damage'
        
        damage = self.calculateDamage(
            level,
            278,
            80,
            self.trainers[o].pokemon[self.trainers[o].cP].defense)
        
        # x0.5 against Rhydon, Zapdos
        if (self.trainers[o].pokemon[self.trainers[o].cP].index == 112
                or self.trainers[o].pokemon[self.trainers[o].cP].index == 145):
            damage = int(damage / 2)
        
        # x2 against Exeggutor
        if self.trainers[o].pokemon[self.trainers[o].cP].index == 103:
            damage = int(damage * 2)
        
        # STAB using Zapdos
        damage = int(damage * 1.5)
        
        [overkill, subBroke] = self.trainers[o].inflictDamage(damage, False)
        if self.printMe:
            self.damagePrint(o, critical, damage, overkill, subBroke)
    
    def useStunSpore(self, t): # Exeggutor
        
        # Can paralyze even with substitute
        
        o = (t + 1) % 2
        if not self.trainers[o].pokemon[self.trainers[o].cP].frozen:
            if not self.trainers[o].pokemon[self.trainers[o].cP].paralyzed:
                if self.trainers[o].pokemon[self.trainers[o].cP].sleeping <= 0:
                    self.trainers[o].pokemon[self.trainers[o].cP].paralyzed = True
                    if self.printMe:
                        print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + ' was paralyzed!')
                else:
                    if self.printMe:
                        print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + ' is already sleeping!')
            else:
                if self.printMe:
                    print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + ' is already paralyzed!')
        else:
            if self.printMe:
                print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + ' is already frozen!')
    
    def useSleepPowder(self, t): # Exeggutor
        
        # Can sleep even with substitute
        
        o = (t + 1) % 2
        sleepClause = False
        for iP in range(1, 7):
            if self.trainers[o].pokemon[iP].sleeping > 0:
                sleepClause = True
        if not sleepClause:
            if not self.trainers[o].pokemon[self.trainers[o].cP].frozen:
                if not self.trainers[o].pokemon[self.trainers[o].cP].paralyzed:
                    self.trainers[o].pokemon[self.trainers[o].cP].sleeping = 1 + np.random.randint(7)
                    self.trainers[o].recharge = False
                    if self.printMe:
                        print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + ' fell asleep!')
                else:
                    if self.printMe:
                        print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + ' is already paralyzed!')
            else:
                if self.printMe:
                    print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + ' is already frozen!')
        else:
            if self.printMe:
                print('Only one Pokémon on each team may be sleeping at one time!')
    
    def useThunderbolt(self, t): # Chansey, Zapdos
        
        critical = ' damage'
        o = (t + 1) % 2
        
        # Critical hit?
        if np.random.randint(256) < np.floor(self.trainers[t].pokemon[self.trainers[t].cP].baseSpeed / 2):
            damage = self.calculateDamage(
                200,
                self.trainers[t].pokemon[self.trainers[t].cP].special,
                95,
                self.trainers[o].pokemon[self.trainers[o].cP].special)
            critical = ' critical damage'
        else:
            damage = self.calculateDamage(
                100,
                np.floor(
                    c.statMods[self.trainers[t].specialMod]
                    * self.trainers[t].pokemon[self.trainers[t].cP].special / 100),
                95,
                np.floor(
                    c.statMods[self.trainers[o].specialMod]
                    * self.trainers[o].pokemon[self.trainers[o].cP].special / 100))
        
        # x0 against Rhydon
        if self.trainers[o].pokemon[self.trainers[o].cP].index == 112:
            damage = 0
            critical = ' damage'
        
        # x0.5 against Exeggutor
        if self.trainers[o].pokemon[self.trainers[o].cP].index == 103:
            damage = int(damage / 2)
        
        # STAB using Zapdos
        if self.trainers[t].pokemon[self.trainers[t].cP].index == 145:
            damage = int(damage * 1.5)
        
        [overkill, subBroke] = self.trainers[o].inflictDamage(damage, False)
        if self.printMe:
            self.damagePrint(o, critical, damage, overkill, subBroke)
        
        # Paralyze except against Zapdos
        if self.trainers[o].pokemon[self.trainers[o].cP].index != 145:
            
            if self.trainers[o].pokemon[self.trainers[o].cP].cHP > 0:
                
                # Can not paralyze substitute, even if broken
                if self.trainers[o].substitute <= 0 and not subBroke:
                    
                    # 10%: paralyze
                    if np.random.randint(256) < 26:
                        if not self.trainers[o].pokemon[self.trainers[o].cP].frozen:
                            if not self.trainers[o].pokemon[self.trainers[o].cP].paralyzed:
                                if self.trainers[o].pokemon[self.trainers[o].cP].sleeping <= 0:
                                    self.trainers[o].pokemon[self.trainers[o].cP].paralyzed = True
                                    if self.printMe:
                                        print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + ' was paralyzed!')
                                else:
                                    if self.printMe:
                                        print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + ' is already sleeping!')
                            else:
                                if self.printMe:
                                    print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + ' is already paralyzed!')
                        else:
                            if self.printMe:
                                print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + ' is already frozen!')
    
    def useThunderWave(self, t): # Chansey, Zapdos
        
        # Can paralyze even with substitute
        
        o = (t + 1) % 2
        
        # Paralyze except against Rhydon
        if self.trainers[o].pokemon[self.trainers[o].cP].index != 112:
            
            if not self.trainers[o].pokemon[self.trainers[o].cP].frozen:
                if not self.trainers[o].pokemon[self.trainers[o].cP].paralyzed:
                    if self.trainers[o].pokemon[self.trainers[o].cP].sleeping <= 0:
                        self.trainers[o].pokemon[self.trainers[o].cP].paralyzed = True
                        if self.printMe:
                            print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + ' was paralyzed!')
                    else:
                        if self.printMe:
                            print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + ' is already sleeping!')
                else:
                    if self.printMe:
                        print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + ' is already paralyzed!')
            else:
                if self.printMe:
                    print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + ' is already frozen!')
        else:
            if self.printMe:
                print('It has no effect against ' + self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + '!')
    
    def useEarthquake(self, t): # Rhydon, Tauros, Snorlax
        
        critical = ' damage'
        level = 100
        o = (t + 1) % 2
        
        # Critical hit?
        if np.random.randint(256) < np.floor(self.trainers[t].pokemon[self.trainers[t].cP].baseSpeed / 2):
            level = 200
            critical = ' critical damage'
        
        damage = self.calculateDamage(
            level,
            self.trainers[t].pokemon[self.trainers[t].cP].attack,
            100,
            self.trainers[o].pokemon[self.trainers[o].cP].defense)
        
        # x0 against Zapdos
        if self.trainers[o].pokemon[self.trainers[o].cP].index == 145:
            damage = 0
            critical = ' damage'
        
        # x0.5 against Exeggutor
        if self.trainers[o].pokemon[self.trainers[o].cP].index == 103:
            damage = int(damage / 2)
        
        # x2 against Rhydon
        if self.trainers[o].pokemon[self.trainers[o].cP].index == 112:
            damage = int(damage * 2)
        
        # STAB using Rhydon
        if self.trainers[t].pokemon[self.trainers[t].cP].index == 112:
            damage = int(damage * 1.5)
        
        [overkill, subBroke] = self.trainers[o].inflictDamage(damage, False)
        if self.printMe:
            self.damagePrint(o, critical, damage, overkill, subBroke)
    
    def usePsychic(self, t): # Exeggutor
        
        critical = ' damage'
        o = (t + 1) % 2
        
        # Critical hit?
        if np.random.randint(256) < 22:
            damage = self.calculateDamage(
                200,
                348,
                90,
                self.trainers[o].pokemon[self.trainers[o].cP].special)
            critical = ' critical damage'
        else:
            damage = self.calculateDamage(
                100,
                np.floor(c.statMods[self.trainers[t].specialMod] * 348 / 100),
                90,
                np.floor(
                    c.statMods[self.trainers[o].specialMod]
                    * self.trainers[o].pokemon[self.trainers[o].cP].special / 100))
        
        # x0.5 against Exeggutor
        if self.trainers[o].pokemon[self.trainers[o].cP].index == 103:
            damage = int(damage / 2)
        
        # STAB using Exeggutor
        damage = int(damage * 1.5)
        
        [overkill, subBroke] = self.trainers[o].inflictDamage(damage, False)
        if self.printMe:
            self.damagePrint(o, critical, damage, overkill, subBroke)
        
        if self.trainers[o].pokemon[self.trainers[o].cP].cHP > 0:
            
            # Can not decrease special if there's a substitute, even if broken
            if self.trainers[o].substitute <= 0 and not subBroke:
                
                # 33.2%: decrease special
                if np.random.randint(256) < 85:
                    if self.trainers[o].specialMod > 0:
                        self.trainers[o].specialMod -= 1
                        if self.printMe:
                            print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + '\'s special fell!')
                    else:
                        if self.printMe:
                            print(self.trainers[o].name + '\'s ' + self.trainers[o].pokemon[self.trainers[o].cP].name + '\'s special can not be decreased more!')
    
    def useAgility(self, t): # Zapdos
        
        if self.trainers[t].speedMod < 12:
            self.trainers[t].speedMod += 2
            if self.printMe:
                print(self.trainers[t].name + '\'s ' + self.trainers[t].pokemon[self.trainers[t].cP].name + '\'s speed greatly rose!')
        else:
            if self.printMe:
                print(self.trainers[t].name + '\'s ' + self.trainers[t].pokemon[self.trainers[t].cP].name + '\'s speed can not rise more!')
    
    def useSelfdestruct(self, t, hit): # Snorlax
        
        if hit:
            critical = ' damage'
            level = 100
            o = (t + 1) % 2
            
            # Critical hit?
            if np.random.randint(256) < 15:
                level = 200
                critical = ' critical damage'
            
            damage = self.calculateDamage(
                level,
                318,
                130,
                np.floor(self.trainers[o].pokemon[self.trainers[o].cP].defense / 2))
            
            # x0.5 against Rhydon
            if self.trainers[o].pokemon[self.trainers[o].cP].index == 112:
                damage = int(damage / 2)
            
            # STAB using Snorlax
            damage = int(damage * 1.5)
            
            [overkill, subBroke] = self.trainers[o].inflictDamage(damage, False)
            if self.printMe:
                self.damagePrint(o, critical, damage, overkill, subBroke)
            if not subBroke:
                self.trainers[t].inflictDamage(self.trainers[t].pokemon[self.trainers[t].cP].cHP, True)
        else:
            self.trainers[t].inflictDamage(self.trainers[t].pokemon[self.trainers[t].cP].cHP, True)
    
    def useSoftboiled(self, t): # Chansey
        
        healed = self.trainers[t].healDamage(351)
        if self.printMe:
            print('Softboiled healed for ' + str(healed) + ' damage!')
    
    def useExplosion(self, t, hit): # Exeggutor
        
        if hit:
            critical = ' damage'
            level = 100
            o = (t + 1) % 2
            
            # Critical hit?
            if np.random.randint(256) < 22:
                level = 200
                critical = ' critical damage'
            
            damage = self.calculateDamage(
                level,
                288,
                170,
                np.floor(self.trainers[o].pokemon[self.trainers[o].cP].defense / 2))
            
            # x0.5 against Rhydon
            if self.trainers[o].pokemon[self.trainers[o].cP].index == 112:
                damage = int(damage / 2)
            
            [overkill, subBroke] = self.trainers[o].inflictDamage(damage, False)
            if self.printMe:
                self.damagePrint(o, critical, damage, overkill, subBroke)
            if not subBroke:
                self.trainers[t].inflictDamage(self.trainers[t].pokemon[self.trainers[t].cP].cHP, True)
        else:
            self.trainers[t].inflictDamage(self.trainers[t].pokemon[self.trainers[t].cP].cHP, True)
    
    def useRockSlide(self, t): # Rhydon
        
        critical = ' damage'
        level = 100
        o = (t + 1) % 2
        
        # Critical hit?
        if np.random.randint(256) < np.floor(self.trainers[t].pokemon[self.trainers[t].cP].baseSpeed / 2):
            level = 200
            critical = ' critical damage'
        
        damage = self.calculateDamage(
            level,
            358,
            75,
            self.trainers[o].pokemon[self.trainers[o].cP].defense)
        
        # x0.5 against Rhydon
        if self.trainers[o].pokemon[self.trainers[o].cP].index == 112:
            damage = int(damage / 2)
        
        # x2 against Zapdos
        if self.trainers[o].pokemon[self.trainers[o].cP].index == 145:
            damage = int(damage * 2)
        
        # STAB using Rhydon
        damage = int(damage * 1.5)
        
        [overkill, subBroke] = self.trainers[o].inflictDamage(damage, False)
        if self.printMe:
            self.damagePrint(o, critical, damage, overkill, subBroke)
    
    def useSubstitute(self, t): # Rhydon
        
        if self.trainers[t].substitute <= 0:
            if self.trainers[t].pokemon[self.trainers[t].cP].cHP > 103:
                self.trainers[t].inflictDamage(103, False)
                self.trainers[t].substitute = 104
                if self.printMe:
                    print(self.trainers[t].name + '\'s Rhydon did 103 damage to itself and created a substitute with 104 hit points!')
            elif self.trainers[t].pokemon[self.trainers[t].cP].cHP < 103:
                if self.printMe:
                    print(self.trainers[t].name + '\'s Rhydon\'s health is too low to create a substitute!')
            else:
                self.trainers[t].inflictDamage(103, False)
                if self.printMe:
                    print(self.trainers[t].name + '\'s Rhydon did 103 damage to itself!')
        else:
            if self.printMe:
                print(self.trainers[t].name + '\'s Rhydon already has a substitute!')
    
    def useStruggle(self, t): # All Pokémon
        
        critical = ' damage'
        level = 100
        o = (t + 1) % 2
        
        # Critical hit?
        if np.random.randint(256) < np.floor(self.trainers[t].pokemon[self.trainers[t].cP].baseSpeed / 2):
            level = 200
            critical = ' critical damage'
        
        damage = self.calculateDamage(
            level,
            self.trainers[t].pokemon[self.trainers[t].cP].attack,
            50,
            self.trainers[o].pokemon[self.trainers[o].cP].defense)
        
        # x0.5 against Rhydon
        if self.trainers[o].pokemon[self.trainers[o].cP].index == 112:
            damage = int(damage / 2)
        
        # STAB using Chansey, Tauros, Snorlax
        if (self.trainers[t].pokemon[self.trainers[t].cP].index == 113
                or self.trainers[t].pokemon[self.trainers[t].cP].index == 128
                or self.trainers[t].pokemon[self.trainers[t].cP].index == 143):
            damage = int(damage * 1.5)
        
        [overkill, subBroke] = self.trainers[o].inflictDamage(damage, False)
        if self.printMe:
            self.damagePrint(o, critical, damage, overkill, subBroke)
        if not subBroke:
            [overkill, subBroke] = self.trainers[t].inflictDamage(int(damage / 2), True)
            if self.printMe:
                if overkill == 0:
                    print('Struggle did ' + str(int(damage / 2)) + ' recoil damage!')
                else:
                    print('Struggle did ' + str(int(damage / 2)) + ' recoil damage! ' + str(overkill) + ' overkill!')
    
    def calculateDamage(self, level, attack, power, defense):
        
        # Calculate raw damage
        factor1 = 2 + np.floor(2 * level / 5)
        factor2 = power * attack
        denominator = 50 * defense
        unmodified = 2 + np.floor(factor1 * factor2 / denominator)
        
        # Apply random modifier
        rand = np.random.randint(217, 256)
        damage = np.floor(unmodified * rand / 255)
        
        return int(damage)
    
    def damagePrint(self, t, critical, damage, overkill, subBroke):
        
        move = self.trainers[(t + 1) % 2].pokemon[self.trainers[(t + 1) % 2].cP].moves[self.trainers[(t + 1) % 2].nextAction[1]].name
        if self.trainers[t].substitute <= 0 and not subBroke:
            if overkill == 0:
                print(move + ' did ' + str(damage) + critical + '!')
            else:
                print(move + ' did ' + str(damage) + critical + '! ' + str(overkill) + ' overkill!')
        elif self.trainers[t].substitute > 0:
            print(move + ' did ' + str(damage) + critical + ' to the substitute!')
        elif subBroke:
            print(move + ' did ' + str(damage) + critical + ' and broke the substitute! ' + str(overkill) + ' overkill!')

#