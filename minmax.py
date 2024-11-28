import math
from screens.assets.guiAssets import *
from screens.game_screen import check_connected_4, player_scores
import time 
import threading

class Connect4AI:
    def __init__(self, user=None, comp=None, k=None):
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
    @staticmethod
    def check_connected_thread(state, player, result, index):
        result[index] = check_connected_4(state, player)
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

my = Connect4AI()
my.k=6
my.comp=2
my.user=1
# Define an intermediate board state (after a few moves)
# The state represents a board with some moves made by both the user (1) and the computer (2)
intermediate_state = "000000000000000000000000000000000000000000"

# Call the maximizeWithPruning function to get the best move for the computer (level 0)
start_time = time.time()
max_move, max_utility = my.maximizeWithPruning(intermediate_state, -math.inf, math.inf, 0)
end_time = time.time()
print("Best Move (Computer's Turn):", max_move)
print("Utility Value of Best Move:", max_utility)
print(-1000*(start_time-end_time))# Call the maximizeWithPruning function to get the best move for the computer (level 0)
start_time = time.time()
max_move, max_utility = my.maximize(intermediate_state,  0)
end_time = time.time()
print(-1000*(start_time-end_time))
# Print the result of the best move and the corresponding utility value
print("Best Move (Computer's Turn):", max_move)
print("Utility Value of Best Move:", max_utility)
print(check_connected_4("211121212121212121212121212121212121212121212121",2))
print(check_connected_4("211121212121212121212121212121212121212121212121",1))
