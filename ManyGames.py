import Reversi
import myPlayer
import myPlayer2
import myPlayerWithMCTS
import time
from io import StringIO
import sys

use_stability_heuristic = True


Monte_Carlo_start = 0
monte_carlo_second = 0
heuristic_start = 0
heuristic_second = 0

for iter_game in range(50):

    b = Reversi.Board(8)

    print("ITERATION NUM :",iter_game)


    players = []
    if iter_game%2 == 0:
        print("heuristic starts")
        if use_stability_heuristic:
            player1 = myPlayer2.myPlayer2()
        else:
            player1 = myPlayer.myPlayer()
    else:
        print("monte carlo starts")
        player1 = myPlayerWithMCTS.myPlayerWithMCTS()
    
    player1.newGame(b._BLACK)
    players.append(player1)

    if iter_game%2 == 0:
        player2 = myPlayerWithMCTS.myPlayerWithMCTS()
    else:
        if use_stability_heuristic:
            player2 = myPlayer2.myPlayer2()
        else:
            player2 = myPlayer.myPlayer()
    
    player2.newGame(b._WHITE)
    players.append(player2)

    totalTime = [0,0] # total real time for each player
    nextplayer = 0
    nextplayercolor = b._BLACK
    nbmoves = 1

    outputs = ["",""]
    sysstdout= sys.stdout
    stringio = StringIO()
    while not b.is_game_over():
    
        nbmoves += 1
        otherplayer = (nextplayer + 1) % 2
        othercolor = b._BLACK if nextplayercolor == b._WHITE else b._WHITE
        
        currentTime = time.time()
        sys.stdout = stringio
        move = players[nextplayer].getPlayerMove()
        sys.stdout = sysstdout
        playeroutput = "\r" + stringio.getvalue()
        stringio.truncate(0)
        outputs[nextplayer] += playeroutput
        totalTime[nextplayer] += time.time() - currentTime
        (x,y) = move
        if not b.is_valid_move(nextplayercolor,x,y):
            print(otherplayer, nextplayer, nextplayercolor)
            print("Problem: illegal move")
            break
        b.push([nextplayercolor, x, y])
        
        players[otherplayer].playOpponentMove(x,y)

        nextplayer = otherplayer
        nextplayercolor = othercolor
        #print(b)
        
        

    print("The game is over")
    (nbwhites, nbblacks) = b.get_nb_pieces()
    print("Time:", totalTime)
    print("Winner: ", end="")
    if nbwhites > nbblacks:
        print("WHITE")
        if iter_game%2 == 0:
            monte_carlo_second+=1
        else:
            heuristic_second+=1
    elif nbblacks > nbwhites:
        if iter_game%2 == 0:
            heuristic_start+=1
        else:
            Monte_Carlo_start+=1
        print("BLACK")
    else:
        print("DEUCE")


    print("Monte Carlo : Start = ",Monte_Carlo_start)
    print("Monte Carlo : Second = ",monte_carlo_second)
    print("heuristic : Start = ",heuristic_start)
    print("heuristic : Second = ",heuristic_second)
