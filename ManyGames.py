import Reversi_2
import myPlayerHeuristic
import myPlayerWithMCTS
import time
from io import StringIO
import sys
import numpy as np
import pandas as pd
from tqdm import tqdm

ressources = np.arange(start=30,stop=110,step=10)
df_stats = pd.DataFrame(columns=['MCTS_First_Win','MCTS_Second_Win','MCTS_First_Lose','MCTS_Second_Lose','Resources','MCTS_TIME','Other_Player_Timer'])
for r in tqdm(ressources):
    #print("Resources = ",r)
    
    Monte_Carlo_start = 0
    monte_carlo_second = 0
    heuristic_start = 0
    heuristic_second = 0

    epochs = 10
    mcts_times = []
    other_times = []
    
    
    for iter_game in tqdm(range(epochs)):

        

        board_size = 8
        b = Reversi_2.Board(board_size)

        monte_carlo_plays_first = False
        
        players = []
        if iter_game%2 == 0:
            #print("heuristic starts")
            player1 = myPlayerHeuristic.myPlayerHeuristic()
        else:
            #print("monte carlo starts")
            monte_carlo_plays_first = True
            player1 = myPlayerWithMCTS.myPlayerWithMCTS(board_size=board_size,resources=r)
        
        player1.newGame(b._BLACK)
        players.append(player1)

        if iter_game%2 == 0:
            player2 = myPlayerWithMCTS.myPlayerWithMCTS(board_size=board_size,resources=r)
        else:
            player2 = myPlayerHeuristic.myPlayerHeuristic()
        
        player2.newGame(b._WHITE)
        players.append(player2)

        totalTime = [0,0] # total real time for each player
        nextplayer = 0
        nextplayercolor = b._BLACK
        nbmoves = 1

        outputs = ["",""]
        sysstdout= sys.stdout
        stringio = StringIO()
        #print('Playing ...')
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
            
        #print("The game is over")
        (nbwhites, nbblacks) = b.get_nb_pieces()
        #print("Time:", totalTime)

        if monte_carlo_plays_first:
            mcts_times.append(totalTime[0])
            other_times.append(totalTime[1])
        else:
            mcts_times.append(totalTime[1])
            other_times.append(totalTime[0])

        #print("Winner: ", end="")
        if nbwhites > nbblacks:
            #print("WHITE")
            if iter_game%2 == 0:
                monte_carlo_second+=1
            else:
                heuristic_second+=1
        elif nbblacks > nbwhites:
            if iter_game%2 == 0:
                heuristic_start+=1
            else:
                Monte_Carlo_start+=1
            #print("BLACK")
        else:
            pass#print("DEUCE")
    df_stats = df_stats.append({'MCTS_First_Win':Monte_Carlo_start,'MCTS_Second_Win':monte_carlo_second,\
        'MCTS_First_Lose':heuristic_second,'MCTS_Second_Lose':heuristic_start,\
            'Resources':r,'MCTS_TIME':sum(mcts_times)/len(mcts_times),\
                'Other_Player_Timer':sum(other_times)/len(other_times)}\
                    ,ignore_index=True)
    print(df_stats)
    #print("Monte Carlo : Second = ",monte_carlo_second)
    #print("Monte Carlo : Start = ",Monte_Carlo_start)
    #print("heuristic : Start = ",heuristic_start)
    #print("heuristic : Second = ",heuristic_second)
df_stats.to_csv("results.csv",index=False)