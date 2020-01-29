import copy
from random import randint
import numpy as np
import sys
import math


Black_color = 1 
White_color = 2

class Node_MCTS:
    def __init__(self,parent,board):
        self.parent = parent
        self.nb_win_black = 0
        self.nb_win_white = 0
        self.nb_visits = 0
        self.children = []
        self.board = board

    def get_next_board_randomly(self):
        legal_moves = self.board.legal_moves()
        move =  legal_moves[randint(0,len(legal_moves)-1)]
        new_board = copy.deepcopy(self.board)  
        new_board.push(move)
        return new_board

def selection(root,color):
    
    aux = root
    while len(aux.children)>0:
        best_score = sys.maxsize*-1
        best_node = None
        for node in aux.children:
            score = node.nb_win_black - node.nb_win_white
            score = -score if color == White_color else score
            if score>best_score:
                best_score = score
                best_node = node
        rand = np.random.rand(1)[0]
        if rand>0.5:
            aux = expansion(aux)
        else:
            aux = best_node
    
    return aux

def expansion(root):
    board = root.get_next_board_randomly()
    new_node = Node_MCTS(root,board)
    root.children.append(new_node)
    return new_node

def simulation(node):
    while not node.board.is_game_over():
        legal_moves = node.board.legal_moves()
        move =  legal_moves[randint(0,len(legal_moves)-1)]
        node.board.push(move)
    result = node.board._nbBLACK - node.board._nbWHITE

    if result > 0:
        return (1,0)
    else:
        if result<0:
            return (0,1)
        else:
            return (0,0)

def backpropagation(node,result):
    
    while node != None:
        node.nb_visits+=1
        node.nb_win_black += result[0]
        node.nb_win_white += result[1]
        node = node.parent
def best_child(root,color):
    best_score = sys.maxsize*-1
    best_node = None
    
    for node in root.children:
        
        score = node.nb_win_black - node.nb_win_white
        score = -score if color == White_color else score
        if score>best_score:
            best_score = score
            best_node = node
        

    print("Best Score = ","Black win ",str(best_node.nb_win_black)+" vs ","White win ",str(best_node.nb_win_white))

    move = best_node.board.pop()

    return move if move != None else (color,-1,-1)

def MCTS(board,color,resources_left=80):
    root = Node_MCTS(None,board)
    while(resources_left>0):
        node = selection(root,color)
        new_node = expansion(node)
        result = simulation(copy.deepcopy(new_node))
        backpropagation(new_node,result)
        resources_left-=1
    
    move = best_child(root,color)
    return move
