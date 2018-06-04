import io
import os
import sys
import threading
import time

import Game
import Load
import MonteCarloTreeSearchAI
import RandomAI
import User

def setAction(game, t, AI, state):
    
    game.nextAction[t] = AI.getAction(state)

def main(id):
    
    # Parameters
    depth = 1
    epsilon = 0.1
    limit = 100
    search = 10
    temperature = 0.2
    
    # Initialize
    AI = [RandomAI.AI(), MonteCarloTreeSearchAI.AI(depth, epsilon, limit, search, temperature)]
    idExists = os.path.isfile('run_results/gamePrint_' + str(id) + '.txt')
    while idExists:
        id += 1
        idExists = os.path.isfile('run_results/gamePrint_' + str(id) + '.txt')
    gamePrintFile = open('run_results/gamePrint_' + str(id) + '.txt', 'w')
    if os.path.isfile('run_results/results.txt'):
        array = Load.loadFloatArray('run_results/results', 5)
        initializedGames = array[0]
        initializedGames += 1
        completedGames = array[1]
        losses = array[2]
        ties = array[3]
        wins = array[4]
    else:
        initializedGames = 1
        completedGames = 0
        losses = 0
        ties = 0
        wins = 0
    resultsFile = open('run_results/results.txt', 'w')
    resultsFile.write(
            str(int(initializedGames)) + '\n'
            + str(int(completedGames)) + '\n'
            + str(int(losses)) + '\n'
            + str(int(ties)) + '\n'
            + str(int(wins)) + '\n')
    resultsFile.close()
    
    # Run the battle
    game = Game.Game()
    while game.running:
        states = [game.getState(True), game.getState(False)]
        if game.forceSwitch[0] == game.forceSwitch[1]:
            thread0 = threading.Thread(target=setAction, args=(game, 0, AI[0], states[0]))
            thread0.daemon = True
            thread0.start()
            thread1 = threading.Thread(target=setAction, args=(game, 1, AI[1], states[1]))
            thread1.daemon = True
            AI[1].extendSearch = True
            thread1.start()
            while thread1.isAlive():
                if not thread0.isAlive():
                    AI[1].extendSearch = False
                    if AI[1].searchNotFinished:
                        print('\nPlease wait for the AI to make a decision!')
                    break
            thread0.join()
            thread1.join()
        else:
            for iT in range(2):
                if game.forceSwitch[iT]:
                    game.nextAction[iT] = AI[iT].getAction(states[iT])
        #stdout = sys.stdout
        #sys.stdout = io.StringIO()
        game.progress()
        summary = game.getSummary()
        print(summary[0:(len(summary) - 1)])
        gamePrintFile.write(summary)
        #gamePrint = sys.stdout.getvalue()
        #gamePrintFile.write(gamePrint)
        #sys.stdout = stdout
        #print(gamePrint[0:(len(gamePrint) - 1)])
    gamePrintFile.close()
    
    # Save the results
    completedGames += 1
    if game.win[0] and game.win[1]:
        ties += 1
        print('Tie after ' + str(game.round) + ' rounds!')
    elif game.win[0]:
        wins += 1
        print('Win after ' + str(game.round) + ' rounds!')
    elif game.win[1]:
        losses += 1
        print('Loss after ' + str(game.round) + ' rounds!')
    resultsFile = open('run_results/results.txt', 'w')
    resultsFile.write(
            str(int(initializedGames)) + '\n'
            + str(int(completedGames)) + '\n'
            + str(int(losses)) + '\n'
            + str(int(ties)) + '\n'
            + str(int(wins)) + '\n')
    resultsFile.close()

if __name__ == '__main__':
    main(int(int(time.time()) % (10 ** 8)))

#