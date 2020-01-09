# -*- coding: utf-8 -*-

import time
import Reversi
from random import randint
from playerInterface import *
from fonctionsMinMax import *

class myPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(8)
        self._mycolor = None

    def getPlayerName(self):
        return "Amin"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        somme  = self._board._nbBLACK + self._board._nbWHITE
        total = self._board._boardsize*self._board._boardsize
        avancement = somme/total
        profondeur = 2
        
        #if randint(0,100)>90:
        #    profondeur = 4

        if avancement>0.85:
            profondeur = 4

        if avancement>0.90:
            profondeur = (total-somme)+(total-somme)%2
        
        print('Profondeur = ',profondeur)
        move = MTDF(self._board, profondeur)
        """
        legal_moves = self._board.legal_moves()
        
        move =  legal_moves[randint(0,len(legal_moves)-1)]
        print('nb legal moves = ',len(legal_moves))
        """

        #move[1]+=1
        #move[2]+=1
        
        
        (c,x,y) = move

        self._board.push(move)
        print("I am playing", move)
        assert(c==self._mycolor)
        #print("My current board :")
        #print(self._board)
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



