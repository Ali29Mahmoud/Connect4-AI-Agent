import math
from Node import Node
from MinMaxTree import drawTreeMinMax
from heuristic import Heuristic

rows, cols = 6, 7

board_state = "0" * (rows * cols)
player_scores = {1: 0, 2: 0}


def get_cell(row, col, board):
    return board[row * cols + col]


def set_cell(row, col, value):
    global board_state
    index = row * cols + col
    board_state = board_state[:index] + value + board_state[index + 1:]


def check_connected_4(board, player):
    def in_bounds(x, y):
        return 0 <= x < rows and 0 <= y < cols

    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    connected_count = 0

    for row in range(rows):
        for col in range(cols):
            if get_cell(row, col, board) == str(player):
                for dx, dy in directions:
                    count = 1
                    for step in range(1, 4):
                        nx, ny = row + dx * step, col + dy * step
                        if in_bounds(nx, ny) and get_cell(nx, ny, board) == str(player):
                            count += 1
                        else:
                            break
                    if count == 4:
                        connected_count += 1

    return connected_count


class Connect4AI:
    def __init__(self, user=None, comp=None, k=None):
        self.user = user
        self.comp = comp
        self.k = k
        self.myDict = {}

    def Maximize(self, state, level):
        root = Node(state=state, col=None, val=None, alpha=None, beta=None, parent=None, children=None)
        return self.maximize(root, level), root

    def MaximizeWithPruning(self, state, level):
        root = Node(state=state, col=None, val=None, alpha=-math.inf, beta=math.inf, parent=None, children=None)
        return self.maximizeWithPruning(root, level), root

    def minimize(self, root, level):
        if root.state in self.myDict:
            root.val = self.myDict[root.state].val
            root.children = self.myDict[root.state].children
            return None, root.val
        if self.terminalTest(root.state):
            root.val = self.get_score(root.state)
            return None, root.val
        if level == self.k:
            root.val = self.eval(root.state)
            return None, root.val
        minChild, minUtility = None, math.inf
        for child, col in self.getChildren(root.state, self.user):
            childN = Node(state=child, col=col, val=None, alpha=None, beta=None, parent=root.state, children=None)
            temp, utility = self.maximize(childN, level + 1)
            if utility < minUtility:
                minChild, minUtility = (child, col), utility
            root.add_child(childN)
            root.val = minUtility
            self.myDict[child] = childN
        return minChild, minUtility

    def maximize(self, root, level):
        if root.state in self.myDict:
            root.val = self.myDict[root.state].val
            root.children = self.myDict[root.state].children
            return None, root.val
        if self.terminalTest(root.state):
            root.val = self.get_score(root.state)
            return None, root.val
        if level == self.k:
            root.val = self.eval(root.state)
            return None, root.val
        maxChild, maxUtility = None, -math.inf
        for child, col in self.getChildren(root.state, self.comp):
            childN = Node(state=child, col=col, val=None, alpha=None, beta=None, parent=root.state, children=None)
            temp, utility = self.minimize(childN, level + 1)
            if utility > maxUtility:
                maxChild, maxUtility = (child, col), utility
            root.add_child(childN)
            root.val = maxUtility
            self.myDict[child] = childN
        return maxChild, maxUtility

    def minimizeWithPruning(self, root, level):
        prune = False
        if self.terminalTest(root.state):
            root.val = self.get_score(root.state)
            return None, root.val
        if level == self.k:
            root.val = self.eval(root.state)
            return None, root.val
        minChild, minUtility = None, math.inf
        for child, col in self.getChildren(root.state, self.user):
            childN = Node(state=child, col=col, val=None, alpha=root.alpha, beta=root.beta, parent=root.state,
                          children=None)
            temp, utility = self.maximizeWithPruning(childN, level + 1)
            if utility < minUtility:
                minChild, minUtility = (child, col), utility
            if minUtility <= root.alpha:
                prune = True
            if minUtility < root.beta:
                root.beta = minUtility
            root.add_child(childN)
            root.val = minUtility
            if (prune):
                break
        return minChild, minUtility

    def maximizeWithPruning(self, root, level):
        prune = False
        if self.terminalTest(root.state) :
            root.val = self.get_score(root.state)
            return None, root.val
        if level == self.k:
            root.val = self.eval(root.state)
            return None, root.val
        maxChild, maxUtility = None, -math.inf
        for child, col in self.getChildren(root.state, self.comp):
            childN = Node(state=child, col=col, val=None, alpha=root.alpha, beta=root.beta, parent=root.state,
                          children=None)
            temp, utility = self.minimizeWithPruning(childN, level + 1)
            if utility > maxUtility:
                maxChild, maxUtility = (child, col), utility
            if maxUtility >= root.beta:
                prune = True
            if maxUtility > root.alpha:
                root.alpha = maxUtility
            root.add_child(childN)
            root.val = maxUtility
            if (prune):
                break
        return maxChild, maxUtility

    def terminalTest(self, state):
        return not ("0" in state)

    def eval(self, state):
        score = Heuristic().heuristic(state, self.comp)
        real_score = self.get_score(state) * 1000
        return score + real_score
    def get_score(self, board):
        return check_connected_4(board, self.comp) - check_connected_4(board, self.user)
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


if __name__ == "__main__":
    # Initial empty board
    initial_state = '200000010000002000001200000120000012100001'

    # Initialize the AI with arbitrary player IDs and depth (k)
    ai = Connect4AI(user=1, comp=2, k=3)  # User is 1, Computer is 2, depth is 3

    # Test Minimax without pruning
    print("Testing Minimax without pruning...")
    best_move, minimax_tree = ai.Maximize(initial_state, 0)
    print(f"Best move without pruning: {best_move}")
    print(f"Minimax tree root value: {minimax_tree.val}")
    minimax_trees = drawTreeMinMax(minimax_tree)
    # Test Minimax with alpha-beta pruning
    print("\nTesting Minimax with alpha-beta pruning...")
    best_move_pruned, pruned_tree = ai.MaximizeWithPruning(initial_state, 0)
    print(f"Best move with pruning: {best_move_pruned}")
    print(f"Pruned tree root value: {pruned_tree.val}")
    # minimax_trees = drawTreeMinMax(pruned_tree)
