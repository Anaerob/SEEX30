import os

actions = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [0, 1], [0, 2], [0, 3], [0, 4]]
pNames = ['', 'Exeggutor', 'Rhydon', 'Chansey', 'Tauros', 'Snorlax', 'Zapdos']
pNamesSpaced = ['           ', 'Exeggutor  ', 'Rhydon     ', 'Chansey    ', 'Tauros     ', 'Snorlax    ', 'Zapdos     ']
pHP = [0, 393, 413, 703, 353, 523, 383]
pAttack = ['0', '288', '358', '108', '298', '318', '278']
pDefense = ['0', '268', '338', '108', '288', '228', '268']
pSpecial = ['0', '348', '188', '308', '238', '228', '348']
pSpeed = ['0', '208', '178', '198', '318', '158', '298']
pCrit = ['0', '27', '20', '25', '55', '15', '50']
pMoves = [
    [0, 0, 0, 0, 0],
    [0, 5, 6, 10, 14],
    [0, 1, 9, 15, 16],
    [0, 2, 7, 8, 13],
    [0, 1, 2, 3, 9],
    [0, 1, 3, 9, 12],
    [0, 4, 7, 8, 11]]
pType = ['', 'Grass / Psychic', 'Ground / Rock', 'Normal', 'Normal', 'Normal', 'Electric / Flying']
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
mPower = ['50', '85', '95', '150', '80', '0', '0', '95', '0', '100', '90', '0', '130', '0', '170', '75', '0']
mAccuracy = ['-%', '100%', '100%', '90%', '100%', '75%', '75%', '100%', '100%', '100%', '100%', '-%', '100%', '-%', '100%', '90%', '-%']
mPP = ['10', '24', '16', '8', '32', '48', '24', '24', '32', '16', '16', '48', '8', '16', '8', '16', '16']
mEffectiveness = [
    ['S', 'B', 'I', 'H', 'D', 'S', 'S', 'T', 'T', 'E', 'P', 'A', 'S', 'S', 'E', 'R', 'S'],
    ['1', '1', '2', '1', '2', '-', '-', '0.5', '-', '0.5', '0.5', '-', '1', '-', '1', '1', '-'],
    ['0.5', '0.5', '2', '0.5', '0.5', '-', '-', '0', '0', '2', '1', '-', '0.5', '-', '0.5', '0.5', '-'],
    ['1', '1', '1', '1', '1', '-', '-', '1', '-', '1', '1', '-', '1', '-', '1', '1', '-'],
    ['1', '1', '1', '1', '1', '-', '-', '1', '-', '1', '1', '-', '1', '-', '1', '1', '-'],
    ['1', '1', '1', '1', '1', '-', '-', '1', '-', '1', '1', '-', '1', '-', '1', '1', '-'],
    ['1', '1', '2', '1', '0.5', '-', '-', '1', '-', '0', '1', '-', '1', '-', '1', '2', '-']]
mSTAB = [
    [False],
    [False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True, False],
    [True, True, False, True, False, False, False, False, False, False, False, False, True, False, True, False, False],
    [True, True, False, True, False, False, False, False, False, False, False, False, True, False, True, False, False],
    [True, True, False, True, False, False, False, False, False, False, False, False, True, False, True, False, False],
    [False, False, False, False, True, False, False, True, False, False, False, False, False, False, False, False, False]]
mDescription = [
    'Inflicts damage and casues 50% recoil damage to the user.',
    'Inflicts damage and has a 30% chance of paralyzing the opponent. \n   It cannot paralyze Normal-type Pokémon.',
    'Inflicts damage and has a 10% chance of freezing the opponent.',
    'Inflicts damage and requires recharging on the following turn.',
    'Inflicts damage.',
    'Paralyzes the opponent.',
    'Puts the opponent to sleep.',
    'Inflicts damage and has a 10% chance of paralyzing the opponent.',
    'Paralyzes the target.',
    'Inflicts damage.',
    'Inflicts damage and has a 33.2% chance of \n   decreasing the special of the opponent by one stage.',
    'Increases the speed of the user by two stages.',
    'Inflicts damage and causes the user to faint. \n   The defense of the opponent is halved during the attack.',
    'Restores up to 50% of the users hit points.',
    'Inflicts damage and causes the user to faint. \n   The defense of the opponent is halved during the attack.',
    'Inflicts damage.',
    'Removes 25% of the users hit points and creates a substitute.']


class User:
    
    
    def __init__(self):
        
        self.exit = False
        self.key = ''
        self.keys = ['-', 'e', 'h', 'm', 'o', 's']
        self.keyWords = ['-', 'exit', 'help', 'move', 'option', 'switch']
        self.moveDictionary = [
            {'struggle': '0'},
            {'stunspore': '1', 'sleeppowder': '2', 'psychic': '3', 'explosion': '4'},
            {'bodyslam': '1', 'earthquake': '2', 'rockslide': '3', 'substitute': '4'},
            {'icebeam': '1', 'thunderbolt': '2', 'thunderwave': '3', 'softboiled': '4'},
            {'bodyslam': '1', 'icebeam': '2', 'hyperbeam': '3', 'earthquake': '4'},
            {'bodyslam': '1', 'hyperbeam': '2', 'earthquake': '3', 'selfdestruct': '4'},
            {'drillpeck': '1', 'thunderbolt': '2', 'thunderwave': '3', 'agility': '4'}]
        self.moves = ['0', '1', '2', '3', '4']
        self.moveWords = [
            'struggle', 'bodyslam', 'icebeam', 'hyperbeam', 'drillpeck',
            'stunspore', 'sleeppowder', 'thunderbolt', 'thunderwave', 'earthquake',
            'psychic', 'agility', 'selfdestruct', 'softboiled', 'explosion',
            'rockslide', 'substitute']
        self.optionDictionary = {'longkeys': '1', 'staticinfo': '2'}
        self.options = ['1', '2']
        self.optionWords = ['longkeys', 'staticinfo']
        self.state = 0
        self.summary = ''
        self.switchDictionary = {
            'exeggutor': '1', 'rhydon': '2', 'chansey': '3',
            'tauros': '4', 'snorlax': '5', 'zapdos': '6'}
        self.switches = ['1', '2', '3', '4', '5', '6']
        self.switchWords = ['exeggutor', 'rhydon', 'chansey', 'tauros', 'snorlax', 'zapdos']
        
        if not os.path.isdir('User'):
            os.makedirs('User')
        if os.path.isfile('User/options.txt'):
            optionsFile = open('User/options.txt', 'r')
            options = optionsFile.read()
            optionsFile.close()
            if len(options) >= 2:
                if options[0].isdigit():
                    self.optionLongKeys = bool(int(options[0]))
                else:
                    self.optionLongKeys = True
                if options[1].isdigit():
                    self.optionStaticInfo = bool(int(options[1]))
                else:
                    self.optionStaticInfo = False
            else:
                self.optionLongKeys = True
                self.optionStaticInfo = False
        else:
            self.optionLongKeys = True
            self.optionStaticInfo = False
            optionsFile = open('User/options.txt', 'w')
            optionsFile.write(str(int(self.optionLongKeys)) + str(int(self.optionStaticInfo)))
            optionsFile.close()
    
    def getAction(self, state):
        
        self.state = state
        remain = True
        
        if state[4][0]:
            while remain:
                
                previousKey = self.key
                self.key = 's'
                self.printMe()
                
                string = input('Send out which Pokémon? ')
                [key, choice] = self.processInput(string)
                
                if key == 'e':
                    action = [0, 0]
                    self.exit = True
                    remain = False
                
                elif key == 's' and choice in self.getAllowedSwitches():
                    action = [int(choice), 0]
                    remain = False
                
                if not self.exit:
                    self.key = previousKey
                self.printMe()
        
        else:
            while remain:
                
                self.printMe()
                
                string = input('What do you want to do? ')
                [key, choice] = self.processInput(string)
                
                if key == 'e':
                    action = [0, 0]
                    self.exit = True
                    remain = False
                
                elif key != '' and choice == '':
                    self.key = key
                
                elif key == 'm' and choice in self.getAllowedMoves():
                    action = [0, int(choice)]
                    remain = False
                
                elif key == 's' and choice in self.getAllowedSwitches():
                    action = [int(choice), 0]
                    remain = False
                
                elif key == 'o':
                    if choice == '1':
                        self.optionLongKeys = not self.optionLongKeys
                        if not os.path.isdir('User'):
                            os.makedirs('User')
                        optionsFile = open('User/options.txt', 'w')
                        optionsFile.write(str(int(self.optionLongKeys)) + str(int(self.optionStaticInfo)))
                        optionsFile.close()
                    elif choice == '2':
                        self.optionStaticInfo = not self.optionStaticInfo
                        if not os.path.isdir('User'):
                            os.makedirs('User')
                        optionsFile = open('User/options.txt', 'w')
                        optionsFile.write(str(int(self.optionLongKeys)) + str(int(self.optionStaticInfo)))
                        optionsFile.close()
                
                self.printMe()
        
        return action
    
    def getAllowedMoves(self):
        
        moves = ['1', '2', '3', '4']
        for iM in range(1, 5):
            if self.state[15][0][self.state[3][0] - 1][iM] <= 0:
                moves.remove(str(iM))
        if len(moves) == 0:
            moves = ['0']
        return moves
    
    def getAllowedSwitches(self):
        
        switches = ['1', '2', '3', '4', '5', '6']
        for iP in range(1, 7):
            if self.state[14][0][iP] <= 0:
                switches.remove(str(iP))
            elif self.state[3][0] == iP:
                switches.remove(str(iP))
        return switches
    
    def printInterface(self):
        
        
        steps = 28
        HP = ['|', '|']
        for i in range(steps):
            for t in range(2):
                if steps * self.state[14][t][self.state[3][t]] > i * pHP[self.state[3][t]]:
                    HP[t] += 'x'
                else:
                    HP[t] += ' '
        for t in range(2):
            HP[t] += '|'
        
        substitute = ['', '']
        if self.state[8][0] <= 0:
            substitute[0] += '|                                           |'
        else:
            substitute[0] += '| Substitute |'
            for i in range(steps):
                if steps * self.state[8][0] > i * 104:
                    substitute[0] += 'x'
                else:
                    substitute[0] += ' '
            substitute[0] += '| |'
        if self.state[8][1] <= 0:
            substitute[1] += '|                                           |'
        else:
            substitute[1] += '| Substitute |'
            for i in range(steps):
                if steps * self.state[8][1] > i * 104:
                    substitute[1] += 'x'
                else:
                    substitute[1] += ' '
            substitute[1] += '| |'
        
        status = ['| ', '| ']
        bStatus = [[False, False, False], [False, False, False]]
        for t in range(2):
            if self.state[6][t] and self.state[14][t][self.state[3][t]] > 0:
                status[t] += 'Recharge!  | '
            else:
                status[t] += '           | '
            
            if self.state[11][t][self.state[3][t]]:
                status[t] += 'FRZ | '
                bStatus[t][0] = True
            elif self.state[12][t][self.state[3][t]]:
                status[t] += 'PAR | '
                bStatus[t][0] = True
            elif self.state[13][t][self.state[3][t]] > 0:
                status[t] += 'SLP | '
                bStatus[t][0] = True
            
            if self.state[9][t] == 5:
                status[t] += 'SPC x 0.66 | '
                bStatus[t][1] = True
            elif self.state[9][t] == 4:
                status[t] += 'SPC x 0.50 | '
                bStatus[t][1] = True
            elif self.state[9][t] == 3:
                status[t] += 'SPC x 0.40 | '
                bStatus[t][1] = True
            elif self.state[9][t] == 2:
                status[t] += 'SPC x 0.33 | '
                bStatus[t][1] = True
            elif self.state[9][t] == 1:
                status[t] += 'SPC x 0.28 | '
                bStatus[t][1] = True
            elif self.state[9][t] == 0:
                status[t] += 'SPC x 0.25 | '
                bStatus[t][1] = True
            
            if self.state[10][t] == 8:
                status[t] += 'SPE x 2 | '
                bStatus[t][2] = True
            elif self.state[10][t] == 10:
                status[t] += 'SPE x 3 | '
                bStatus[t][2] = True
            elif self.state[10][t] == 12:
                status[t] += 'SPE x 4 | '
                bStatus[t][2] = True
            
            if not bStatus[t][0]:
                status[t] += '      '
            if not bStatus[t][1]:
                status[t] += '             '
            if not bStatus[t][2]:
                status[t] += '          '
            
            status[t] += '|'
            if not ((self.state[6][t] and self.state[14][t][self.state[3][t]] > 0) or bStatus[t][0] or bStatus[t][1] or bStatus[t][2]):
                status[t] = '|                                           |'
        
        if os.name == 'nt':
            os.system('cls')
        elif os.name == 'posix':
            os.system('clear')
        
        print('|-------------------------------------------|')
        print('|                                           |')
        print('| AI         |    Remaining Pokémon: ' + str(self.state[7][1]) + '    | |')
        if self.state[7][1] == 0:
            print('|                                           |')
        else:
            print('| ' + pNamesSpaced[self.state[3][1]] + HP[1] + ' |')
        if self.state[8][1] <= 0:
            print(status[1])
            print(substitute[1])
        else:
            print(substitute[1])
            print(status[1])
        print('|                                           |')
        print('|                                           |')
        print('| Player     |    Remaining Pokémon: ' + str(self.state[7][0]) + '    | |')
        if self.state[7][0] == 0:
            print('|                                           |')
        else:
            print('| ' + pNamesSpaced[self.state[3][0]] + HP[0] + ' |')
        if self.state[8][0] <= 0:
            print(status[0])
            print(substitute[0])
        else:
            print(substitute[0])
            print(status[0])
        print('|                                           |')
        print('|-------------------------------------------|')
        print()
    
    def printMe(self, state=None, summary=None):
        
        if state is not None:
            self.state = state
        if summary is not None:
            self.summary = summary
        
        self.printInterface()
        print()
        
        if self.summary != '':
            print(self.summary)
            print()
        elif self.key == '':
            if self.optionLongKeys:
                print('Input \'help\' for help!\n')
            else:
                print('Input \'h\' for help!\n')
            print()
        
        if self.state[1]:
            if self.key == 'h':
               self.printHelp()
               print()
            elif self.key == 'm':
                print('Available moves:')
                print()
                self.printMoves(0, self.state[3][0])
                print()
            elif self.key == 'o':
                print('Available options:')
                print()
                self.printOptions()
                print()
            elif self.key == 's':
                print('Available switches:')
                print()
                self.printSwitches(0)
                print()
    
    def printMoves(self, t, p):
        
        nM = 0
        for iM in range(1, 5):
            if self.state[15][t][p - 1][iM] > 0:
                if self.optionStaticInfo:
                    print(str(iM) + ': ' + mNames[pMoves[p][iM]])
                    print('   PP: ' + str(self.state[15][t][p - 1][iM]) + ' / ' + mPP[pMoves[p][iM]])
                    if int(mPower[pMoves[p][iM]]) != 0:
                        print('   Power: ' + mPower[pMoves[p][iM]])
                    if mAccuracy[pMoves[p][iM]] != '-%':
                        print('   Accuracy: ' + mAccuracy[pMoves[p][iM]])
                    if mEffectiveness[self.state[3][1]][pMoves[p][iM]] != '-':
                        print('   Effectiveness: ' + mEffectiveness[self.state[3][1]][pMoves[p][iM]])
                    if mSTAB[p][pMoves[p][iM]]:
                        print('   Same type attack bonus')
                    print('   ' + mDescription[pMoves[p][iM]])
                    print()
                else:
                    print(
                        str(iM) + ': ' + mNames[pMoves[p][iM]] + ', '
                        + str(self.state[15][t][p - 1][iM]) + ' PP')
                nM += 1
        if nM == 0:
            if self.optionStaticInfo:
                print('0: Struggle')
                print('   PP: Infinite')
                print('   Shit move')
                print()
            else:
                print('0: Struggle, infinite PP')
        if not self.optionStaticInfo:
            print()
    
    def printOptions(self):
        
        print()
        if self.optionLongKeys:
            print('1: Long Keys, [On]')
        else:
            print('1: Long Keys, [Off]')
        print()
        print('On   | Intuitive usage')
        print('     | Game only recognizes long key and choice names')
        print('-----|-------------------------------------------------')
        print('Off  | Faster usage')
        print('     | Game only recognizes short key and choice names')
        print()
        print()
        if self.optionStaticInfo:
            print('2: Static Info, [On]')
        else:
            print('2: Static Info, [Off]')
        print()
        print('On   | More details')
        print('     | List of available moves and switches also includes static information')
        print('-----|-------------------------------------------------------------------------')
        print('Off  | Only important info')
        print('     | List of available moves and switches only includes variable information')
        print()
    
    def printPokemon(self, t, p):
        
        if p == self.state[3][t]:
            number = 'C: '
        else:
            number = str(p) + ': '
        
        if self.state[11][t][p]:
            status = ', frozen!'
        elif self.state[12][t][p]:
            status = ', paralyzed!'
        elif self.state[13][t][p] > 0:
            status = ', sleeping!'
        else:
            status = ''
        
        if self.state[14][t][p] > 0:
            cHP = (str(self.state[14][t][p]) + ' / '
                + str(pHP[p]) + ' HP')
            percent = str(int(100 * self.state[14][t][p] / pHP[p])) + '%'
        else:
            cHP = ' fainted!'
            percent = str(int(100 * self.state[14][t][p] / pHP[p])) + '%'
            status = ''
        
        if self.optionStaticInfo:
            print(number + pNames[p] + ' [' + pType[p] + ']')
            print('   ' + cHP) # + ' (' + percent + ')')
            print('   Attack: ' + pAttack[p] + ', Defense: ' + pDefense[p])
            print('   Special: ' + pSpecial[p] + ', Speed: ' + pSpeed[p])
            crit = str(int(100 * int(pCrit[p]) / 256)) + '%'
            print('   Crit: ' + crit)
            print()
        else:
            print(
                number + pNames[p] + ', '
                + percent + ' HP'
                + status)
    
    def printSwitches(self, t):
        
        for iP in range(1, 7):
            if self.state[14][t][iP] > 0 and (iP != self.state[3][t] or self.optionStaticInfo):
                self.printPokemon(t, iP)
        if not self.optionStaticInfo:
            print()
    
    def printHelp(self):
        
        print('Enter: a \'key\'')
        print('       a \'choice\' if a \'key\' was previously entered')
        print('       a \'key\' and a \'choice\' simultaneously')
        print()
        print('Inputs are not case sensitive and non keywords are ignored')
        print()
        print()
        if self.optionLongKeys:
            print('Key     | Example usage      | Description       ')
            print('--------|--------------------|-------------------')
            print('-       | -                  | Clear key         ')
            print('exit    | exit               | Exits the game    ')
            print('help    | help               | Print this        ')
            print('move    | move sleep powder  | Use a move        ')
            print('option  | option long keys   | Change an option  ')
            print('switch  | switch snorlax     | Switch to Pokémon ')
        else:
            print('Key  | Example usage  | Description       ')
            print('-----|----------------|-------------------')
            print('-    | -              | Clear key         ')
            print('e    | e              | Exits the game    ')
            print('h    | h              | Print this        ')
            print('m    | m2             | Use a move        ')
            print('o    | o1             | Change an option  ')
            print('s    | s5             | Switch to Pokémon ')
        print()
    
    def processInput(self, inp):
        
        inp = inp.lower()
        inp = inp.replace(' ', '')
        
        choices = []
        keys = []
        
        iChoice = ''
        iKey = ''
        
        if self.optionLongKeys:
            
            if inp == 'e':
                return ['e', '']
            elif inp == 'h':
                return ['h', '']
            
            for key in self.keyWords:
                if key in inp:
                    keys.append(key[0])
            
            if len(keys) == 1:
                iKey = keys[0][0]
            elif len(keys) == 0 and self.key != '':
                iKey = self.key
            
            if iKey == 'm':
                for choice in self.moveWords:
                    if choice in inp and choice in self.moveDictionary[self.state[3][0]]:
                        choices.append(self.moveDictionary[self.state[3][0]][choice])
            
            if iKey == 'o':
                for choice in self.optionWords:
                    if choice in inp and choice in self.optionDictionary:
                        choices.append(self.optionDictionary[choice])
            
            if iKey == 's':
                for choice in self.switchWords:
                    if choice in inp and choice in self.switchDictionary:
                        choices.append(self.switchDictionary[choice])
            
            if len(choices) == 1:
                iChoice = choices[0]
        
        else:
            
            if 'exit' in inp:
                return ['e', '']
            elif 'help' in inp:
                return ['h', '']
            
            for key in self.keys:
                if key in inp:
                    keys.append(key)
            
            if len(keys) == 1:
                iKey = keys[0]
            elif len(keys) == 0 and self.key != '':
                iKey = self.key
            
            if iKey == 'm':
                for choice in self.moves:
                    if choice in inp:
                        choices.append(choice)
            
            if iKey == 'o':
                for choice in self.options:
                    if choice in inp:
                        choices.append(choice)
            
            if iKey == 's':
                for choice in self.switches:
                    if choice in inp:
                        choices.append(choice)
            
            if len(choices) == 1:
                iChoice = choices[0]
        
        return [iKey, iChoice]

#