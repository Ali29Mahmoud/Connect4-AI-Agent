import math
from screens.assets.guiAssets import *
from screens.game_screen import check_connected_4, player_scores
import time 
import threading
from Node import Node
class Connect4AI:
    def __init__(self, user=None, comp=None, k=None):
        self.user = user
        self.comp = comp
        self.k = k

    def Maximize(self, state, level):
       root=Node(state=state ,col=None, val=None, alpha=None, beta=None, parent=None, children=None)
       return self.maximize(root, level),root
    
    def MaximizeWithPruning(self, state, level):
       root=Node(state=state ,col=None, val=None, alpha=-math.inf, beta=math.inf, parent=None, children=None)
       return self.maximizeWithPruning(root, level),root
    
    def minimize(self, root, level):
        if self.terminalTest(root.state) or level == self.k:
            return None, self.eval(root.state)
        minChild, minUtility = None, math.inf
        for child ,col in self.getChildren(root.state, self.user):
            childN =Node(state=child ,col=col, val=None, alpha=None, beta=None, parent=root.state, children=None)
            temp, utility = self.maximize(childN, level + 1)
            if utility < minUtility:
                minChild, minUtility = (child, col),utility
            root.add_child(childN)
            root.val = minUtility
        return minChild, minUtility

    def maximize(self,root, level):
        if self.terminalTest(root.state) or level == self.k:
            return None, self.eval(root.state)
        maxChild, maxUtility = None, -math.inf
        for child ,col in self.getChildren(root.state, self.comp):
            childN =Node(state=child ,col=col, val=None, alpha=None, beta=None, parent=root.state, children=None)
            temp, utility = self.minimize(childN, level + 1)
            if utility > maxUtility:
                maxChild, maxUtility = (child, col), utility
            root.add_child(childN)
            root.val = maxUtility
        return maxChild, maxUtility

    def minimizeWithPruning(self, root, level):
        if self.terminalTest(root.state) or level == self.k:
            return None, self.eval(root.state)
        minChild, minUtility = None, math.inf
        for child,col in self.getChildren(root.state, self.user):
            childN =Node(state=child ,col=col, val=None, alpha=root.alpha, beta=root.beta, parent=root.state, children=None)
            temp, utility = self.maximizeWithPruning(childN,  level + 1)
            if utility < minUtility:
                minChild, minUtility = (child, col),utility
            if minUtility <= root.alpha:
                print("pruning")
                break
            if minUtility < root.beta:
                root.beta = minUtility
            root.add_child(childN)
            root.val = minUtility
        return minChild, minUtility

    def maximizeWithPruning(self,root, level):
        if self.terminalTest(root.state) or level == self.k:
            return None, self.eval(root.state)
        maxChild, maxUtility = None, -math.inf
        for child,col in self.getChildren(root.state, self.comp):
            childN =Node(state=child ,col=col, val=None, alpha=root.alpha, beta=root.beta, parent=root.state, children=None)
            temp, utility = self.minimizeWithPruning(childN, level + 1)
            if utility > maxUtility:
                maxChild, maxUtility = (child, col),utility
            if maxUtility >= root.beta:
                print("pruning")
                break
            if maxUtility > root.alpha:
                root.alpha = maxUtility
            root.add_child(childN)
            root.val = maxUtility
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
                    child_state = ''.join(new_board)
                    children.append((child_state, col))  
                    break 
        return children


