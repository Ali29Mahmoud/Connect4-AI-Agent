import random

from Node import *

class ExpectiMinMax :
    def __init__(self, state, max_depth , computer_player):
        self.board = state
        self.depth = max_depth
        self.computer_player = computer_player ## 1 or 2
        self.opponent = 1 if computer_player == 2 else 2 ## 1 or 2
        self.best_move = None
        self.visited = set()
        self.row = 6
        self.col = 7

    def solve_expectiminmax(self, dummy1, dummy2):

        root = Node(state=self.board , type="MAX" , val=0 )
        self.expectiminmax(root , self.depth , False, True , None)
        self.best_move = self.col // 2
        best_cols =[]
        for child in root.children:
            if root.val == child.val:
                best_cols.append(child.col)
        if len(best_cols) >= 1:
            random_index = random.randrange(len(best_cols))
            self.best_move = best_cols[random_index]
        return self.best_move ,  root

    def expectiminmax(self , root : Node , depth  , is_chance , is_max , col_played = None):
        if self.is_full(root.state) or depth == 0:
            root.val = self.get_score(root.state)
            self.visited.add(root)
            return root.val
        if is_chance:
            return self.chance_node(root , depth,  is_max , col_played)
        if is_max:
            return self.max_node(root, depth)
        return self.min_node(root, depth)

    def chance_node(self, root, depth , is_max , col_played):
        player = self.computer_player if is_max else self.opponent
        total_score = 0
        props = [0.2 , 0.6 , 0.2]
        for col in range(col_played-1 , col_played+2):
            if self.is_valid_column(root.state, col):
                new_board = self.make_move(root.state, col, player)
                new_type = "MAX" if is_max else "MIN"
                child = Node(state=new_board, type=new_type, val=0)
                root.add_child(child)
                total_score += self.expectiminmax(child, depth - 1,False, not is_max, None) * props[col - col_played + 1]
        root.val = total_score
        return total_score

    def max_node(self, root, depth ):
        best_score = float('-inf')
        for col in range(self.col):
            child = Node(state=root.state, type="CHANCE", val=0 , col=col)
            root.add_child(child)
            best_score = max( best_score , self.expectiminmax(child, depth - 1 , True, True , col) )
        root.val = best_score
        return best_score
    def min_node(self, root, depth):
        best_score = float('inf')
        children = []
        for col in range(self.col):
            child = Node(state=root.state, type="CHANCE", val=0 , col=col)
            root.add_child(child)
            best_score = min(best_score , self.expectiminmax(child, depth - 1 , True, False , col) )
        root.val = best_score
        return best_score
    def get_best_col(self , board , child):
        for col in range(len(board)):
            if board[col] != child[col]:
                return col % self.col

    def make_move(self, board, col, player):
        new_board = list(board)
        for row in range(self.row - 1, -1, -1):
            if new_board[row * self.col + col] == '0':
                new_board[row * self.col + col] = str(player)
                return "".join(new_board)

        return board  # Return the original board if no move is possible

    def is_valid_column(self, board, col):
        if col < 0 or col >= self.col:
            return False
        return board[col] == '0'
    def get_best_move(self):
        return self.best_move
    def get_score(self, board):
        return self.check_connected_4(board, self.computer_player) - self.check_connected_4(board, self.opponent)
    def evaluate(self, board, player):
        return self.check_connected_4(board, self.computer_player) - self.check_connected_4(board, self.opponent)
    def is_full(self, board):
        return not any([cell == '0' for cell in board])
    def get_cell(self,row, col, board_state):
        return board_state[row * self.col + col]

    def check_connected_4( self ,board, player):
        def in_bounds(x, y):
            return 0 <= x < self.row and 0 <= y < self.col
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        connected_count = 0
        for row in range(self.row):
            for col in range(self.col):
                if self.get_cell(row, col, board) == str(player):
                    for dx, dy in directions:
                        count = 1
                        for step in range(1, 4):
                            nx, ny = row + dx * step, col + dy * step
                            if in_bounds(nx, ny) and self.get_cell(nx, ny, board) == str(player):
                                count += 1
                            else:
                                break
                        if count == 4:
                            connected_count += 1

        return connected_count
    def print_board(self, board):
        for row in range(self.row):
            print(board[row * self.col: row * self.col + self.col])



if __name__ == "__main__":
    trial = "000000200000012000012100112120011222011122"
    expecti = ExpectiMinMax(trial, 5, 2)
    best_move, node = expecti.solve_expectiminmax(1, 2)
    print("Best move:")
    print(best_move)
    print("Node:")
    print(node)
    print(len(node.children))
    print(len(node.children[1].children[0].children[0].children))
    print(node.val)

