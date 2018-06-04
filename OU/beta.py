import Game
import RandomAI
import User

def main():
    
    AI = [User.User(), RandomAI.AI()]
    game = Game.Game()
    while game.running:
        states = [game.getState(True), game.getState(False)]
        if game.forceSwitch[0] == game.forceSwitch[1]:
            game.nextAction[0] = AI[0].getAction(states[0])
            game.nextAction[1] = AI[1].getAction(states[1])
        else:
            for iT in range(2):
                if game.forceSwitch[iT]:
                    game.nextAction[iT] = AI[iT].getAction(states[iT])
        game.progress()
    if game.win[0] and game.win[1]:
        print('Tie after ' + str(game.round) + ' rounds!')
    elif game.win[0]:
        print('Win after ' + str(game.round) + ' rounds!')
    elif game.win[1]:
        print('Loss after ' + str(game.round) + ' rounds!')

if __name__ == '__main__':
    main()

#