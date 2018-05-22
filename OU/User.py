import numpy as np

import Constants as c
import Game


class User:
    
    
    def __init__(self):
        
        self.printHelp()
        self.forceSwitchCommands = ['1', '2', '3', '4', '5', '6', 's1', 's2', 's3', 's4', 's5', 's6']
        self.moveCommands = ['m1', 'm2', 'm3', 'm4']
        self.printCommands = ['p', 'ph', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6']
        self.switchCommands = ['s1', 's2', 's3', 's4', 's5', 's6']
    
    def getAction(self, state):
        
        print()
        action = 0
        sim = Game.Game(False, state)
        if sim.forceSwitch[0]:
            while action == 0:
                i = input('Send out which Pokémon? ')
                if i in self.printCommands:
                    self.printMe(state, i)
                elif i in self.forceSwitchCommands:
                    if i not in self.switchCommands:
                        i = 's' + i
                    action = self.getSwitch(state, i)
                    if action not in c.actions:
                        print('Pokémon ' + action + ' has no HP!')
                        action = 0
        else:
            while action == 0:
                i = input('What do you want to do? ')
                if i in self.printCommands:
                    self.printMe(state, i)
                elif i in self.moveCommands:
                    action = self.getMove(state, i)
                    if action not in c.actions:
                        print('Move ' + action + ' has no PP!')
                        action = 0
                elif i in self.switchCommands:
                    action = self.getSwitch(state, i)
                    if action not in c.actions:
                        print('Pokémon ' + action + ' has no HP!')
                        action = 0
        return action
    
    def getMove(self, state, i):
        
        sim = Game.Game(False, state)
        noMoves = True
        moves = ['1', '2', '3', '4']
        for iM in range(1, 5):
            if sim.trainers[0].pokemon[sim.trainers[0].cP].moves[iM].cPP > 0:
                noMoves = False
            else:
                moves.remove(str(iM))
        if noMoves:
            action = list(c.actions[0])
        elif i[1] in moves:
            action = list(c.actions[int(i[1]) + 6])
        else:
            action = i[1]
        return action
    
    def getSwitch(self, state, i):
        
        sim = Game.Game(False, state)
        switches = ['1', '2', '3', '4', '5', '6']
        for iP in range(1, 7):
            if sim.trainers[0].pokemon[iP].cHP <= 0:
                switches.remove(str(iP))
            elif sim.trainers[0].cP == iP:
                switches.remove(str(iP))
        if i[1] in switches:
            action = list(c.actions[int(i[1])])
        else:
            action = i[1]
        return action
    
    def printMe(self, state, i):
        
        sim = Game.Game(False, state)
        if i == 'ph':
            self.printHelp()
        elif i == 'p':
            print()
            print('# AI: REMAINING POKEMON')
            self.printTrainer(state, 1)
            print()
            print('# PLAYER: REMAINING POKEMON')
            self.printTrainer(state, 0)
            print()
            if sim.trainers[0].pokemon[sim.trainers[0].cP].cHP > 0:
                print('# PLAYER: AVAILABLE MOVES')
                self.printMoves(state, 0, sim.trainers[0].cP)
                print()
        else:
            print()
            print('# POKEMON ' + i[1])
            self.printPokemon(state, 0, int(i[1]), False)
            print()
            if sim.trainers[0].pokemon[int(i[1])].cHP > 0:
                print('# AVAILABLE MOVES')
                self.printMoves(state, 0, int(i[1]))
                print()
    
    def printMoves(self, state, t, p):
        
        sim = Game.Game(False, state)
        nM = 0
        for iM in range(1, 5):
            if sim.trainers[t].pokemon[p].moves[iM].cPP > 0:
                print(
                    str(iM) + ': ' + sim.trainers[t].pokemon[p].moves[iM].name + ', '
                    + str(sim.trainers[t].pokemon[p].moves[iM].cPP) + ' / '
                    + str(sim.trainers[t].pokemon[p].moves[iM].PP) + ' PP')
                nM += 1
        if nM == 0:
            print('#: Struggle, infinite PP!')
    
    def printPokemon(self, state, t, p, includeNumber):
        
        sim = Game.Game(False, state)
        if includeNumber:
            if p == sim.trainers[t].cP:
                number = 'Current: '
            else:
                number = '      ' + str(p) + ': '
        else:
            number = ''
        if sim.trainers[t].pokemon[p].frozen:
            status = ', frozen!'
        elif sim.trainers[t].pokemon[p].paralyzed:
            status = ', paralyzed!'
        elif sim.trainers[t].pokemon[p].sleeping:
            status = ', sleeping!'
        else:
            status = ''
        if sim.trainers[t].pokemon[p].cHP > 0:
            cHP = (str(sim.trainers[t].pokemon[p].cHP) + ' / '
                + str(sim.trainers[t].pokemon[p].HP) + ' HP')
        else:
            cHP = ' fainted!'
            status = ''
        print(
            number + sim.trainers[t].pokemon[p].name + ', '
            + cHP
            + status)
    
    def printTrainer(self, state, t):
        
        sim = Game.Game(False, state)
        for iP in range(1, 7):
            if sim.trainers[t].pokemon[iP].cHP > 0:
                self.printPokemon(state, t, iP, True)
    
    def printHelp(self):
        
        print()
        print('###')
        print('### LIST OF COMMANDS')
        print('###')
        print()
        print('\'m#\' - Use move #')
        print('\'s#\' - Switch to Pokémon #')
        print()
        print('\'p\' - Print an overview of the game')
        print('\'p#\' - Print an overview of Pokémon #')
        print('\'ph\' - Print this list of all commands')
        print()
        print('###')
        print('###')
        print('###')
        print()

#