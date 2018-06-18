import numpy as np
import os
import time

import FormatTime
import Game
import LinearNeuralNetworkAI
import RandomAI
import Sim

def main():
    
    # Parameters
    nGames = 100
    limit = 100
    
    AI = [LinearNeuralNetworkAI.AI(0, 0, True), RandomAI.AI()]
    if not os.path.isdir('LNN_benchmark'):
        os.makedirs('LNN_benchmark')
    progressExist = os.path.isfile('LNN_benchmark/progress.txt')
    if progressExist:
        array = Load.loadFloatArray('LNN_benchmark/progress', 5)
        startGame = int(array[0])
        abort = array[1]
        loss = array[2]
        tie = array[3]
        win = array[4]
    else:
        if os.path.isfile('LNN_benchmark/results.txt'):
            exit('Results file exists but progress file doesn\'t: (Re)Move previous results before running!')
        startGame = 0
        abort = 0
        loss = 0
        tie = 0
        win = 0
    infoFile = open('LNN_benchmark/info.txt', 'w')
    infoFile.write(
        'Games = ' + str(nGames) + '\n'
        + 'Limit = ' + str(limit) + '\n')
    infoFile.close()
    
    for iGame in range(nGames):
        if iGame % int(nGames / 10) == 0:
            print('Completed ' + str(int(100 * iGame / nGames)) + '%')
        
        game = Game.Game()
        while game.running and game.round < limit:
            if game.forceSwitch[0] == game.forceSwitch[1]:
                game.nextAction[0] = AI[0].getAction(game.getState(True))
                game.nextAction[1] = AI[1].getAction(game.getState(False))
            elif game.forceSwitch[0]:
                game.nextAction[0] = AI[0].getAction(game.getState(True))
            elif game.forceSwitch[1]:
                game.nextAction[1] = AI[1].getAction(game.getState(False))
            game.progress()
        if game.win[0] and game.win[1]:
            tie += 1
        elif game.win[0]:
            win += 1
        elif game.win[1]:
            loss += 1
        else:
            abort += 1
        progressFile = open('LNN_benchmark/progress.txt', 'w')
        progressFile.write(
            str(iGame + 1) + '\n'
            + str(abort) + '\n'
            + str(loss) + '\n'
            + str(tie) + '\n'
            + str(win))
        progressFile.close()
    resultsFile = open('LNN_benchmark/results.txt', 'w')
    resultsFile.write(
        'Abort: ' + str(abort / nGames) + '\n'
        + 'Loss:  ' + str(loss / nGames) + '\n'
        + 'Tie:   ' + str(tie / nGames) + '\n'
        + 'Win:   ' + str(win / nGames) + '\n')
    resultsFile.close()
    print('Completed 100%')
    os.remove('LNN_benchmark/progress.txt')

if __name__ == '__main__':
    mainTime = time.time()
    main()
    print('Runtime: ' + FormatTime.getString(time.time() - mainTime))

#