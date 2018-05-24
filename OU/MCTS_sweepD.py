import numpy as np
import os
import time

import Constants as c
import FormatTime
import Game
import Load
import MonteCarloTreeSearchAI
import RandomAI

def main():
    
    # Parameters
    nGames = 100
    depth = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    epsilon = 0.1
    limit = 100
    search = 250
    temperature = 0.2
    
    # Initialize
    progressExist = os.path.isfile('MCTS_sweepD_results/MCTS_sweepD_progress.txt')
    if progressExist:
        array = Load.loadFloatArray('MCTS_sweepD_results/MCTS_sweepD_progress', 7)
        startDepth = int(array[0])
        startGame = int(array[1])
        abort = array[2]
        loss = array[3]
        runTime = array[4]
        tie = array[5]
        win = array[6]
    else:
        startDepth = 0
        if os.path.isfile('MCTS_sweepD_results/MCTS_sweepD_info.txt'):
            exit('Info file exists but progress file doesn\'t: (Re)Move previous results before running!')
    infoFile = open('MCTS_sweepD_results/MCTS_sweepD_info.txt', 'w')
    infoFile.write(
        'Games = ' + str(nGames) + '\n'
        + 'Depth = ' + str(depth) + '\n'
        + 'Epsilon = ' + str(epsilon) + '\n'
        + 'Limit = ' + str(limit) + '\n'
        + 'Search = ' + str(search) + '\n'
        + 'Temperature = ' + str(temperature) + '\n')
    infoFile.close()
    
    # Run the parameter sweep
    for iDepth in range(startDepth, len(depth)):
        print('Completed %1.1f' % (100 * iDepth / len(depth)) + '%')
        if not progressExist:
            startGame = 0
            abort = 0
            loss = 0
            runTime = 0
            tie = 0
            win = 0
        AI = [MonteCarloTreeSearchAI.AI(depth[iDepth], epsilon, limit, search, temperature), RandomAI.AI()]
        startTime = time.time()
        for iGame in range(startGame, nGames):
            game = Game.Game(False)
            while game.running and game.round < limit:
                states = [game.getState(c.amBlack), game.getState(c.amWhite)]
                if game.forceSwitch[0] == game.forceSwitch[1]:
                    game.trainers[0].setNextAction(AI[0].getAction(states[0]))
                    game.trainers[1].setNextAction(AI[1].getAction(states[1]))
                else:
                    for iT in range(2):
                        if game.forceSwitch[iT]:
                            game.trainers[iT].setNextAction(AI[iT].getAction(states[iT]))
                game.progress()
            if game.win[0] and game.win[1]:
                tie += 1
            elif game.win[0]:
                win += 1
            elif game.win[1]:
                loss += 1
            else:
                abort += 1
            runTime += time.time() - startTime
            progressFile = open('MCTS_sweepD_results/MCTS_sweepD_progress.txt', 'w')
            progressFile.write(
                str(iDepth) + '\n'
                + str(iGame + 1) + '\n'
                + str(abort) + '\n'
                + str(loss) + '\n'
                + str(runTime) + '\n'
                + str(tie) + '\n'
                + str(win))
            progressFile.close()
        abortFile = open('MCTS_sweepD_results/MCTS_sweepD_abort.txt', 'a')
        abortFile.write(str(abort / nGames) + '\n')
        abortFile.close()
        lossFile = open('MCTS_sweepD_results/MCTS_sweepD_loss.txt', 'a')
        lossFile.write(str(loss / nGames) + '\n')
        lossFile.close()
        tieFile = open('MCTS_sweepD_results/MCTS_sweepD_tie.txt', 'a')
        tieFile.write(str(tie / nGames) + '\n')
        tieFile.close()
        timeFile = open('MCTS_sweepD_results/MCTS_sweepD_time.txt', 'a')
        timeFile.write(str(runTime / nGames) + '\n')
        timeFile.close()
        winFile = open('MCTS_sweepD_results/MCTS_sweepD_win.txt', 'a')
        winFile.write(str(win / nGames) + '\n')
        winFile.close()
        progressFile = open('MCTS_sweepD_results/MCTS_sweepD_progress.txt', 'w')
        progressFile.write(
            str(iDepth + 1) + '\n'
            + str(0) + '\n'
            + str(0) + '\n'
            + str(0) + '\n'
            + str(0) + '\n'
            + str(0) + '\n'
            + str(0))
        progressFile.close()
        progressExist = False
    print('Completed 100%')
    os.remove('MCTS_sweepD_results/MCTS_sweepD_progress.txt')

if __name__ == '__main__':
    mainTime = time.time()
    main()
    print('Runtime: ' + FormatTime.getString(time.time() - mainTime))

#