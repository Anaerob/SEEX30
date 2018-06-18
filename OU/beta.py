import os
import time

import Game
import RandomAI
import User

def main(id):
    
    user = User.User()
    AI = RandomAI.AI()
    
    if not os.path.isdir('Logs'):
        os.makedirs('Logs')
    idExists = os.path.isfile('Logs/' + str(id) + '.txt')
    while idExists:
        id += 1
        idExists = os.path.isfile('Logs/' + str(id) + '.txt')
    logFile = open('Logs/' + str(id) + '.txt', 'w')
    
    game = Game.Game()
    user.printMe(game.getState(True))
    
    while game.running and not user.exit:
        if not (game.forceSwitch[0] or game.forceSwitch[1]):
            game.nextAction[0] = user.getAction(game.getState(True))
            game.nextAction[1] = AI.getAction(game.getState(False))
        else:
            if game.forceSwitch[0] and game.forceSwitch[1]:
                game.nextAction[0] = user.getAction(game.getState(True))
                game.nextAction[1] = AI.getAction(game.getState(False))
            elif game.forceSwitch[0]:
                game.nextAction[0] = user.getAction(game.getState(True))
            elif game.forceSwitch[1]:
                game.nextAction[1] = AI.getAction(game.getState(False))
        
        if not user.exit:
            game.progress()
            summary = game.getSummary()
            user.printMe(game.getState(True), summary)
            if not (game.forceSwitch[0] or game.forceSwitch[1]):
                logFile.write(summary + '\n\n')
    
    if game.forceSwitch[0] or game.forceSwitch[1]:
        logFile.write(summary)
    logFile.close()
    
    if game.win[0] and game.win[1]:
        print('Tie after ' + str(game.round) + ' rounds!\n')
    elif game.win[0]:
        print('Win after ' + str(game.round) + ' rounds!\n')
    elif game.win[1]:
        print('Loss after ' + str(game.round) + ' rounds!\n')
    else:
        print('Aborted after ' + str(game.round) + ' rounds!\n')

if __name__ == '__main__':
    main(int(int(time.time()) % (10 ** 8)))

#