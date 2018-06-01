import random


class AI:
    
    
    def getAction(self, state):
        
        if state[4][0]:
            action = self.getSwitch(state)
        else:
            moves = [[0, 1], [0, 2], [0, 3], [0, 4]]
            for iM in range(1, 5):
                if state[15][0][state[3][0] - 1][iM] <= 0:
                    moves.remove([0, iM])
            if len(moves) == 0:
                action = [0, 0]
            else:
                action = random.choice(moves)
        return action
        
    def getSwitch(self, state):
        
        switches = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0]]
        for iP in range(1, 7):
            if state[14][0][iP] <= 0:
                switches.remove([iP, 0])
            elif state[3][0] == iP:
                switches.remove([iP, 0])
        return random.choice(switches)

#