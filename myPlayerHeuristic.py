# -*- coding: utf-8 -*-

import time
import Reversi_2
from random import randint
from playerInterface import *
from fonctionsMinMax import *

class myPlayerHeuristic(PlayerInterface):

    def __init__(self):
        self._board = Reversi_2.Board(10)
        self._mycolor = None

    def getPlayerName(self):
        return "Heuristic"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        
        
        somme  = self._board._nbBLACK + self._board._nbWHITE
        total = self._board._boardsize*self._board._boardsize
        avancement = somme/total
        profondeur = 2
        
        if avancement>0.85:
            profondeur = 4

        if avancement>0.95:
            profondeur = (total-somme)+(total-somme)%2
        
        move = MTDF(self._board, profondeur)
        (c,x,y) = move
        
        self._board.push(move)
        assert(c==self._mycolor)
        return (x,y) 

    def playOpponentMove(self, x,y):
        #print('move ',x,y)
        #print(self._board)
        assert(self._board.is_valid_move(self._opponent, x, y))
        #print("Opponent played ", (x,y))
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")



