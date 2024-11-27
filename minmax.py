import math
def minimize(state):
    if terminalTest(state):
        return eval(state)
    minChild , minUtility = None , math.inf
    for child in getChildren(state):
        temp , utility= maximize(child)
        if utility < minUtility:
            minChild , minUtility = child , utility
    return minChild , minUtility

def maximize(state):
    if terminalTest(state):
        return  eval(state)
    maxChild , maxUtility = None , -math.inf
    for child in getChildren(state):
        temp , utility = minimize(state)
        if utility > maxUtility:
            maxChild , maxUtility = child , utility
    return maxChild , maxUtility

def minimizeWithPruning(state , alpha , beta):
    if terminalTest(state):
        return eval(state)
    minChild , minUtility = None , math.inf
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
    maxChild , maxUtility = None , -math.inf
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
    return 0
def eval(state):
    return 0
def getChildren():
    return None