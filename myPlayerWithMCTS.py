# -*- coding: utf-8 -*-

import time
import Reversi_2
from random import randint
from playerInterface import *
from fonctionsMinMax import *
from MCTS import *

class myPlayerWithMCTS(PlayerInterface):

    def __init__(self,board_size=8,resources=80):
        self._board = Reversi_2.Board(board_size)
        self.resources = resources
        self._mycolor = None

    def getPlayerName(self):
        return "With MCTS"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        move = MCTS(self._board,self._mycolor,resources_left=self.resources)
        (c,x,y) = move
        print(move)
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



