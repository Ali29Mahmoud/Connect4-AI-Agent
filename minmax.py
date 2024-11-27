# from screens.assets.guiAssets import *
# from screens.game_screen import check_connected_4, player_scores

user =1
comp =2
def minimize(state):
    if terminalTest(state):
        return eval(state)
    minChild , minUtility = None , 111111111
    for child in getChildren(state):
        temp , utility= maximize(child)
        if utility < minUtility:
            minChild , minUtility = child , utility
    return minChild , minUtility

def maximize(state):
    if terminalTest(state):
        return  eval(state)
    maxChild , maxUtility = None , -11111111
    for child in getChildren(state):
        temp , utility = minimize(state)
        if utility > maxUtility:
            maxChild , maxUtility = child , utility
    return maxChild , maxUtility

def minimizeWithPruning(state , alpha , beta):
    if terminalTest(state):
        return eval(state)
    minChild , minUtility = None ,  1111111111
    for child in getChildren(state):
        temp , utility= maximizeWithPruning(child)
        if utility < minUtility:
            minChild , minUtility = child , utility
        if minUtility <= alpha:
            break
        if minUtility< beta:
            beta = minUtility
    return minChild , minUtility

def maximizeWithPruning(state , alpha , beta):
    if terminalTest(state):
        return  eval(state)
    maxChild , maxUtility = None , -11111111
    for child in getChildren(state):
        temp , utility = minimizeWithPruning(state)
        if utility > maxUtility:
            maxChild , maxUtility = child , utility
        if maxUtility >= beta:
            break
        if maxUtility > alpha:
            alpha = maxUtility
    return maxChild , maxUtility

def terminalTest(state):
    return 0 #check_connected_4(state,comp)-check_connected_4(state,user)
def eval(state):
    return 0
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
    return children
