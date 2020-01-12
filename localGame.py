import Reversi_2
import myPlayerHeuristic
import myPlayerWithMCTS
import time
from io import StringIO
import sys

b = Reversi_2.Board(10)

players = []
player1 = myPlayerHeuristic.myPlayerHeuristic()
player1.newGame(b._BLACK)
players.append(player1)
player2 = myPlayerWithMCTS.myPlayerWithMCTS()
player2.newGame(b._WHITE)
players.append(player2)

totalTime = [0,0] # total real time for each player
nextplayer = 0
nextplayercolor = b._BLACK
nbmoves = 1

outputs = ["",""]
sysstdout= sys.stdout
stringio = StringIO()
# ProblÃ¨me : quand on est en fin de partie, le ID est relancÃ© des millieurs de fois avec une profondeur max trÃ¨s grande
#print(b.legal_moves())
while not b.is_game_over():
    #print("Referee Board:")
    #print(b)
    #print("Before move", nbmoves)
    #print("Legal Moves: ", b.legal_moves())
    nbmoves += 1
    otherplayer = (nextplayer + 1) % 2
    othercolor = b._BLACK if nextplayercolor == b._WHITE else b._WHITE
    
    currentTime = time.time()
    sys.stdout = stringio
    move = players[nextplayer].getPlayerMove()
    sys.stdout = sysstdout
    playeroutput = "\r" + stringio.getvalue()
    stringio.truncate(0)
    print(("[Player "+str(nextplayer) + "] ").join(playeroutput.splitlines(True)))
    outputs[nextplayer] += playeroutput
    totalTime[nextplayer] += time.time() - currentTime
    print("Player ", nextplayercolor, players[nextplayer].getPlayerName(), "plays" + str(move))
    (x,y) = move
    #x=x+1
    #y=y+1
    #print(move)
    if not b.is_valid_move(nextplayercolor,x,y):
        print(otherplayer, nextplayer, nextplayercolor)
        print("Problem: illegal move")
        break
    b.push([nextplayercolor, x, y])
    
    players[otherplayer].playOpponentMove(x,y)

    nextplayer = otherplayer
    nextplayercolor = othercolor
    print(b)
    
    

print("The game is over")
print(b)
(nbwhites, nbblacks) = b.get_nb_pieces()
print("Time:", totalTime)
print("Winner: ", end="")
if nbwhites > nbblacks:
    print("WHITE")
elif nbblacks > nbwhites:
    print("BLACK")
else:
    print("DEUCE")

print(totalTime)