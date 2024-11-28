from screens.assets.guiAssets import *
from screens.game_screen import check_connected_4, player_scores
import math
user =1
comp =2
k=30
def minimize(state,level):
    if terminalTest(state) or level== k:
        return None ,eval(state)
    minChild , minUtility = None , math.inf
    for child in getChildren(state,user):
        temp , utility= maximize(child,level+1)
        if utility < minUtility:
            minChild , minUtility = child , utility
    return minChild , minUtility

def maximize(state,level):
    if terminalTest(state) or level== k:
        return  None ,eval(state)
    maxChild , maxUtility = None , -math.inf
    for child in getChildren(state,comp):
        temp , utility = minimize(state,level+1)
        if utility > maxUtility:
            maxChild , maxUtility = child , utility
    return maxChild , maxUtility

def minimizeWithPruning(state , alpha , beta,level):
    if terminalTest(state) or level== k:
        return None, eval(state)
    minChild , minUtility = None ,  math.inf
    for child in getChildren(state,user):
        temp , utility= maximizeWithPruning(child ,alpha , beta, level+1)
        if utility < minUtility:
            minChild , minUtility = child , utility
        if minUtility <= alpha:
            break
        if minUtility< beta:
            beta = minUtility
    return minChild , minUtility

def maximizeWithPruning(state , alpha , beta ,level):
    if terminalTest(state) or level== k:
        return None , eval(state)
    maxChild , maxUtility = None , -math.inf
    for child in getChildren(state,comp):
        temp , utility = minimizeWithPruning(state ,alpha , beta, level+1)
        if utility > maxUtility:
            maxChild , maxUtility = child , utility
        if maxUtility >= beta:
            break
        if maxUtility > alpha:
            alpha = maxUtility
    return maxChild , maxUtility

def terminalTest(state):
    return not ("0" in state) 
def eval(state):
    return check_connected_4(state,comp)-check_connected_4(state,user)
def getChildren(board,player):
    children = []
    for col in range(7):
        for row in range(5, -1, -1):
            index = row * 7 + col
            if board[index] == '0':
                new_board = list(board)
                new_board[index] = str(player)
                children.append(''.join(new_board))
                break
    print(children)
    return children

