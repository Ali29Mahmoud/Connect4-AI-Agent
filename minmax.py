import math
from screens.assets.guiAssets import *
from screens.game_screen import check_connected_4, player_scores

class Connect4AI:
    def __init__(self, user=1, comp=2, k=30):
        self.user = user
        self.comp = comp
        self.k = k

    def minimize(self, state, level):
        if self.terminalTest(state) or level == self.k:
            return None, self.eval(state)
        minChild, minUtility = None, math.inf
        for child in self.getChildren(state, self.user):
            temp, utility = self.maximize(child, level + 1)
            if utility < minUtility:
                minChild, minUtility = child, utility
        return minChild, minUtility

    def maximize(self, state, level):
        if self.terminalTest(state) or level == self.k:
            return None, self.eval(state)
        maxChild, maxUtility = None, -math.inf
        for child in self.getChildren(state, self.comp):
            temp, utility = self.minimize(child, level + 1)
            if utility > maxUtility:
                maxChild, maxUtility = child, utility
        return maxChild, maxUtility

    def minimizeWithPruning(self, state, alpha, beta, level):
        if self.terminalTest(state) or level == self.k:
            return None, self.eval(state)
        minChild, minUtility = None, math.inf
        for child in self.getChildren(state, self.user):
            temp, utility = self.maximizeWithPruning(child, alpha, beta, level + 1)
            if utility < minUtility:
                minChild, minUtility = child, utility
            if minUtility <= alpha:
                break
            if minUtility < beta:
                beta = minUtility
        return minChild, minUtility

    def maximizeWithPruning(self, state, alpha, beta, level):
        if self.terminalTest(state) or level == self.k:
            return None, self.eval(state)
        maxChild, maxUtility = None, -math.inf
        for child in self.getChildren(state, self.comp):
            temp, utility = self.minimizeWithPruning(state, alpha, beta, level + 1)
            if utility > maxUtility:
                maxChild, maxUtility = child, utility
            if maxUtility >= beta:
                break
            if maxUtility > alpha:
                alpha = maxUtility
        return maxChild, maxUtility

    def terminalTest(self, state):
        return not ("0" in state)

    def eval(self, state):
        return check_connected_4(state, self.comp) - check_connected_4(state, self.user)

    def getChildren(self, board, player):
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
