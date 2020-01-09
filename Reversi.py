# -*- coding: utf-8 -*-

''' Fichier de règles du Reversi pour le tournoi Inge2 Enseirb en IA.
    Certaines parties de ce code sont fortement inspirée de 
    https://inventwithpython.com/chapter15.html

    '''
import numpy as np
from random import randint

bonusPos = []
bonusBlack = 0
bonusWhite = 0

class Board:
    _BLACK = 1
    _WHITE = 2
    _EMPTY = 0

    # Attention, la taille du plateau est donnée en paramètre
    def __init__(self, boardsize = 10):
        global bonusPos

        self._nbWHITE = 2
        self._nbBLACK = 2
        self._nextPlayer = self._BLACK
        self._boardsize = boardsize
        self._board = []
        for x in range(self._boardsize):
            self._board.append([self._EMPTY]* self._boardsize)
            bonusPos.append([self._EMPTY]* self._boardsize)
        _middle = int(self._boardsize / 2)
        self._board[_middle-1][_middle-1] = self._WHITE 
        self._board[_middle-1][_middle] = self._BLACK
        self._board[_middle][_middle-1] = self._BLACK
        self._board[_middle][_middle] = self._WHITE 
        
        self._stack= []
        self._successivePass = 0
        #-------------- our code -----------------
        
        for i in range(boardsize):
            for j in range(boardsize):
                if(i==0 and j==0) or (i==0 and j == boardsize-1) or (i==boardsize-1 and j==0) or (i==boardsize-1 and j== boardsize-1):
                    bonusPos[i][j] = 250
                
                if(i>1 and i<boardsize-2 and j==0) or (i>1 and i<boardsize-2 and j==boardsize-1):
                    bonusPos[i][j] = 10
                
                if(j>1 and j<boardsize-2 and i==0) or (j>1 and j<boardsize-2 and i==boardsize-1):
                    bonusPos[i][j] = 10
                
                if(i>1 and i<boardsize-2 and j==1) or (i>1 and i<boardsize-2 and j==boardsize-2):
                    bonusPos[i][j] = -15
                if(j>1 and j<boardsize-2 and i==1) or (j>1 and j<boardsize-2 and i==boardsize-2):
                    bonusPos[i][j] = -15
                
                if(i == 0 and (j==1 or j==boardsize-2)):
                    bonusPos[i][j] = -200
                if(i == 1 and (j==0 or j==1 or j==boardsize-2 or j==boardsize-1)):
                    bonusPos[i][j] = -200
                
                if(i == boardsize-1 and (j==1 or j==boardsize-2)):
                    bonusPos[i][j] = -200
                if(i == boardsize-2 and (j==0 or j==1 or j==boardsize-2 or j==boardsize-1)):
                    bonusPos[i][j] = -200
        #-------------------------------------------
        #for i in range(boardsize):
        #    print(bonusPos[i])

    def reset(self):
        self.__init__()

    # Donne la taille du plateau 
    def get_board_size(self):
        return self._boardsize

    # Donne le nombre de pieces de blanc et noir sur le plateau
    # sous forme de tuple (blancs, noirs) 
    # Peut être utilisé si le jeu est terminé pour déterminer le vainqueur
    def get_nb_pieces(self):
      return (self._nbWHITE, self._nbBLACK)

    # Vérifie si player a le droit de jouer en (x,y)
    def is_valid_move(self, player, x, y):
        if x == -1 and y == -1:
            return not self.at_least_one_legal_move(player)
        return self.lazyTest_ValidMove(player,x,y)

    def _isOnBoard(self,x,y):
        return x >= 0 and x < self._boardsize and y >= 0 and y < self._boardsize 

    # Renvoie la liste des pieces a retourner si le coup est valide
    # Sinon renvoie False
    # Ce code est très fortement inspiré de https://inventwithpython.com/chapter15.html
    # y faire référence dans tous les cas
    def testAndBuild_ValidMove(self, player, xstart, ystart):
        if self._board[xstart][ystart] != self._EMPTY or not self._isOnBoard(xstart, ystart):
            return False
    
        self._board[xstart][ystart] = player # On pourra remettre _EMPTY ensuite 
    
        otherPlayer = self._flip(player)
    
        tilesToFlip = [] # Si au moins un coup est valide, on collecte ici toutes les pieces a retourner
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection 
            y += ydirection
            if self._isOnBoard(x, y) and self._board[x][y] == otherPlayer:
                # There is a piece belonging to the other player next to our piece.
                x += xdirection
                y += ydirection
                if not self._isOnBoard(x, y):
                    continue
                while self._board[x][y] == otherPlayer:
                    x += xdirection
                    y += ydirection
                    if not self._isOnBoard(x, y): # break out of while loop, then continue in for loop
                        break
                if not self._isOnBoard(x, y):
                    continue
                if self._board[x][y] == player: # We are sure we can at least build this move. Let's collect
                    while True:
                        x -= xdirection
                        y -= ydirection
                        if x == xstart and y == ystart:
                            break
                        tilesToFlip.append([x, y])
    
        self._board[xstart][ystart] = self._EMPTY # restore the empty space
        if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
            return False
        return tilesToFlip

    # Pareil que ci-dessus mais ne revoie que vrai / faux (permet de tester plus rapidement)
    def lazyTest_ValidMove(self, player, xstart, ystart):
        if self._board[xstart][ystart] != self._EMPTY or not self._isOnBoard(xstart, ystart):
            return False
    
        self._board[xstart][ystart] = player # On pourra remettre _EMPTY ensuite 
    
        otherPlayer = self._flip(player)
    
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection 
            y += ydirection
            if self._isOnBoard(x, y) and self._board[x][y] == otherPlayer:
                # There is a piece belonging to the other player next to our piece.
                x += xdirection
                y += ydirection
                if not self._isOnBoard(x, y):
                    continue
                while self._board[x][y] == otherPlayer:
                    x += xdirection
                    y += ydirection
                    if not self._isOnBoard(x, y): # break out of while loop, then continue in for loop
                        break
                if not self._isOnBoard(x, y): # On a au moins 
                    continue
                if self._board[x][y] == player: # We are sure we can at least build this move. 
                    self._board[xstart][ystart] = self._EMPTY
                    return True
                 
        self._board[xstart][ystart] = self._EMPTY # restore the empty space
        return False

    def _flip(self, player):
        if player == self._BLACK:
            return self._WHITE 
        return self._BLACK

    def is_game_over(self):
        if self.at_least_one_legal_move(self._nextPlayer):
            return False
        if self.at_least_one_legal_move(self._flip(self._nextPlayer)):
            return False
        return True 

    def push(self, move):
        [player, x, y] = move

        assert player == self._nextPlayer
        if x==-1 and y==-1: # pass
            self._nextPlayer = self._flip(player)
            self._stack.append([move, []])
            self._successivePass += 1
            return
        self._successivePass = 0
        toflip = self.testAndBuild_ValidMove(player,x,y)
        self._stack.append([move,toflip])
        self._board[x][y] = player
        if type(toflip) != bool:
            for xf,yf in toflip:
                self._board[xf][yf] = self._flip(self._board[xf][yf])
            if player == self._BLACK:
                self._nbBLACK += 1 + len(toflip)
                self._nbWHITE -= len(toflip)
                self._nextPlayer = self._WHITE
            else:
                self._nbWHITE += 1 + len(toflip)
                self._nbBLACK -= len(toflip)
                self._nextPlayer = self._BLACK
        #-----------our code---------
        global bonusBlack
        global bonusWhite
        global bonusPos
        if player == self._WHITE:
            bonusWhite+=bonusPos[x][y]
        else:
            bonusBlack+=bonusPos[x][y]
        #----------------------------

    def pop(self):
        [move, toflip] = self._stack.pop()
        [player,x,y] = move



        self._nextPlayer = player 
        if len(toflip) == 0: # pass
            assert x == -1 and y == -1
            #assert self._successivePass > 0
            self._successivePass -= 1
            return
        self._board[x][y] = self._EMPTY
        for xf,yf in toflip:
            self._board[xf][yf] = self._flip(self._board[xf][yf])
        if player == self._BLACK:
            self._nbBLACK -= 1 + len(toflip)
            self._nbWHITE += len(toflip)
        else:
            self._nbWHITE -= 1 + len(toflip)
            self._nbBLACK += len(toflip)
        #-----------our code---------
        global bonusBlack
        global bonusWhite
        global bonusPos
        if player == self._WHITE:
            bonusWhite-=bonusPos[x][y]
        else:
            bonusBlack-=bonusPos[x][y]
        #----------------------------

    # Est-ce que on peut au moins jouer un coup ?
    # Note: cette info pourrait être codée plus efficacement
    def at_least_one_legal_move(self, player):
        for x in range(0,self._boardsize):
            for y in range(0,self._boardsize):
                if self.lazyTest_ValidMove(player, x, y):
                   return True
        return False

    # Renvoi la liste des coups possibles
    # Note: cette méthode pourrait être codée plus efficacement
    def legal_moves(self):
        moves = []
        for x in range(0,self._boardsize):
            for y in range(0,self._boardsize):
                if self.lazyTest_ValidMove(self._nextPlayer, x, y):
                    moves.append([self._nextPlayer,x,y])
        if len(moves) is 0:
            moves = [[self._nextPlayer, -1, -1]] # We shall pass
        return moves

    # Exemple d'heuristique tres simple : compte simplement les pieces
    def heuristique(self, player=None):
        
        global bonusBlack
        global bonusWhite

        if player is None:
            player = self._nextPlayer
        
        gameOver = (self._nbBLACK+self._nbWHITE)==(self._boardsize*self._boardsize)#self.is_game_over()
        
        isWhite = player is self._WHITE
        difference = self._nbWHITE - self._nbBLACK
        avancement = (self._nbBLACK+self._nbWHITE)/self._boardsize*self._boardsize
        """
        whiteStability = 0
        blackStability = 0
        
        for i in range(self._boardsize):
            for j in range(self._boardsize):
                
                if self._board[i][j]!=0:
                    neighbors = np.zeros((3,3))
                    neighbors[1][1] = self._board[i][j]    
                    # down
                    r_i = i+1
                    while( r_i<self._boardsize and self._board[r_i][j] == self._board[i][j]):
                        r_i+=1
                    r_i = r_i - 1 if r_i == self._boardsize else r_i
                    neighbors[2][1] = self._board[r_i][j]

                    # up
                    r_i = i-1
                    while( r_i > -1 and self._board[r_i][j] == self._board[i][j]):
                        r_i-=1
                    r_i = r_i + 1 if r_i == -1 else r_i

                    neighbors[0][1] = self._board[r_i][j]

                    # right
                    r_j = j+1
                    while( r_j < self._boardsize and self._board[i][r_j] == self._board[i][j]):
                        r_j+=1
                    r_j = r_j - 1 if r_j == self._boardsize else r_j

                    neighbors[1][2] = self._board[i][r_j]

                    # left
                    r_j = j-1
                    while( r_j > -1 and self._board[i][r_j] == self._board[i][j]):
                        r_j-=1
                    r_j = r_j + 1 if r_j == -1 else r_j

                    neighbors[1][0] = self._board[i][r_j]

                    #TOP_RIGHT
                    r_i = i-1
                    r_j = j+1
                    while(r_i > -1 and r_j < self._boardsize and self._board[r_i][r_j] == self._board[i][j]):
                        r_i-=1
                        r_j+=1
                    r_i = r_i + 1 if r_i == -1 else r_i
                    r_j = r_j - 1 if r_j == self._boardsize else r_j
                    #print("TOP_RIGHT = ",r_i,r_j)
                    neighbors[0][2] = self._board[r_i][r_j]

                    #DOWN_LEFT
                    r_j = j-1
                    r_i = i+1
                    while(r_i<self._boardsize and r_j > -1 and self._board[r_i][r_j] == self._board[i][j]):
                        r_i+=1
                        r_j-=1
                    r_j = r_j + 1 if r_j == -1 else r_j
                    r_i = r_i - 1 if r_i == self._boardsize else r_i

                    neighbors[2][0] = self._board[r_i][r_j]

                    #TOP_LEFT
                    r_i = i-1
                    r_j = j-1
                    while(r_i > -1 and r_j > -1 and self._board[r_i][r_j] == self._board[i][j]):
                        r_i-=1
                        r_j-=1
                    r_i = r_i + 1 if r_i == -1 else r_i
                    r_j = r_j + 1 if r_j == -1 else r_j

                    neighbors[0][0] = self._board[r_i][r_j]

                    #DOWN_RIGHT
                    r_i = i+1
                    r_j = j+1
                    while(r_i<self._boardsize and r_j < self._boardsize and self._board[r_i][r_j] == self._board[i][j]):
                        r_i+=1
                        r_j+=1
                    r_i = r_i - 1 if r_i == self._boardsize else r_i
                    r_j = r_j - 1 if r_j == self._boardsize else r_j

                    neighbors[2][2] = self._board[r_i][r_j]
                    
                    isStable = False

                    if  (neighbors[0][1] == neighbors[1][1] or neighbors[2][1] == neighbors[1][1]) and \
                        (neighbors[1][0] == neighbors[1][1] or neighbors[1][2] == neighbors[1][1]) and \
                        (neighbors[0][0] == neighbors[1][1] or neighbors[2][2] == neighbors[1][1]) and \
                        (neighbors[0][2] == neighbors[1][1] or neighbors[2][0] == neighbors[1][1]):
                        
                        isStable = True
                    
                    if isStable:
                        whiteStability+= 1 if isWhite else 0
                        blackStability+= 1 if not isWhite else 0
                    else:
                        if  (neighbors[0][1] != neighbors[1][1] and neighbors[2][1] == 0) or \
                            (neighbors[0][1] == 0 and neighbors[2][1] != neighbors[1][1]) or \
                            (neighbors[1][0] != neighbors[1][1] and neighbors[1][2] == 0) or \
                            (neighbors[1][0] == 0 and neighbors[1][2] != neighbors[1][1]) or \
                            (neighbors[0][0] != neighbors[1][1] and neighbors[2][2] == 0) or \
                            (neighbors[0][0] == 0 and neighbors[2][2] != neighbors[1][1]) or\
                            (neighbors[0][2] != neighbors[1][1] and neighbors[2][0] == 0) or \
                            (neighbors[0][2] == 0 and neighbors[2][0] != neighbors[1][1]):
                            
                            whiteStability-= 1 if isWhite else 0
                            blackStability-= 1 if not isWhite else 0

                    #print("i=",i,"j=",j)
                    #print(neighbors)


        stability = 0

        if whiteStability + blackStability>0:
            diff = whiteStability - blackStability
            stability = 100*(diff if isWhite else -diff)/(whiteStability + blackStability)
        
        """

        cornersWhite = (1 if self._board[0][0] == 2 else 0)
        cornersWhite += (1 if self._board[0][self._boardsize-1] == 2 else 0)
        cornersWhite += (1 if self._board[self._boardsize-1][0] == 2 else 0)
        cornersWhite += (1 if self._board[self._boardsize-1][self._boardsize-1] == 2 else 0)

        cornersBlack = (1 if self._board[0][0] == 1 else 0)
        cornersBlack += (1 if self._board[0][self._boardsize-1] == 1 else 0)
        cornersBlack += (1 if self._board[self._boardsize-1][0] == 1 else 0)
        cornersBlack += (1 if self._board[self._boardsize-1][self._boardsize-1] == 1 else 0)
        
        if cornersWhite+cornersBlack >0:
            corners = 100*((cornersWhite - cornersBlack) / (cornersWhite+cornersBlack))
            corners = int(corners)
        else:
            corners = 0
        
        coin_parity =100*((self._nbWHITE-self._nbBLACK)/(self._nbBLACK+self._nbWHITE))
        coin_parity = int(coin_parity)

        legal_moves = self.legal_moves()
        mobility_adv = len(legal_moves)
        random_move =  legal_moves[randint(0,len(legal_moves)-1)]
        self.push(random_move)
        mobility_player = len(self.legal_moves())
        self.pop()
        mobility = 100*((mobility_player - mobility_adv)/(mobility_player + mobility_adv))
        mobility = int (mobility)

        if gameOver:
            win = self._nbWHITE>self._nbBLACK
            result = (10000 if win else -10000) if isWhite else (-10000 if win else 10000)
            return result
        else:
            result = mobility + 0 + (coin_parity+corners if isWhite else coin_parity*-1 + corners*-1)#+ int((difference*100 if isWhite else difference*-100)*1/avancement) - 50*len(self.legal_moves()) 
            return result
    def _piece2str(self, c):
        if c==self._WHITE:
            return 'O'
        elif c==self._BLACK:
            return 'X'
        else:
            return '.'

    def __str__(self):
        toreturn=""
        for l in self._board:
            for c in l:
                toreturn += self._piece2str(c)
            toreturn += "\n"
        toreturn += "Next player: " + ("BLACK" if self._nextPlayer == self._BLACK else "WHITE") + "\n"
        toreturn += str(self._nbBLACK) + " blacks and " + str(self._nbWHITE) + " whites on board\n"
        toreturn += "(successive pass: " + str(self._successivePass) + " )"
        return toreturn

    __repr__ = __str__


