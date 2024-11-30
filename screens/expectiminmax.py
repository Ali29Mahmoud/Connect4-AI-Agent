class ExpectiMinMax :
    def __init__(self, board, max_depth , computer_player):
        self.board = board
        self.depth = max_depth
        self.computer_player = computer_player ## 1 or 2
        self.opponent = 1 if computer_player == 2 else 2 ## 1 or 2
        self.best_move = None
        self.node = {}
        self.row = 6
        self.col = 7

    def solve_expectiminmax(self, board, levels):
        self.expectiminmax(board, self.depth, 2, False, True , None)
        self.best_move = self.col // 2
        for child in self.node[board][1]:
            if self.node[child][0] == self.node[board][0]:
                self.best_move = self.get_best_col(board, child)
                break
        return self.best_move , self.node , self.node[board]

    def expectiminmax(self, board, depth, player , is_chance , is_max , col_played = None):
        if self.is_full(board):
            score = self.get_score(board)
            self.node[board] = (score,[])
            return score
        if depth == 0:
            score = self.evaluate(board, player)
            self.node[board] = (score, [])
            return score

        if is_chance:
            return self.chance_node(board, depth, player , is_max , col_played)
        if is_max:
            return self.max_node(board, depth, player)
        return self.min_node(board, depth, player)

    def chance_node(self, board, depth, player , is_max , col_played):
        total_score = 0
        props = [0.2 , 0.6 , 0.2]
        children = []
        for col in range(col_played-1 , col_played+2):
            if self.is_valid_column(board, col):
                new_board = self.make_move(board, col, player)
                children.append(new_board)
                if new_board in self.node:
                    total_score += self.node[new_board][0] * props[col - col_played + 1]
                else:
                    total_score += self.expectiminmax(new_board, depth - 1, player, False, is_max, None) * props[col - col_played + 1]
        self.node[board] = (total_score, children)
        return total_score

    def max_node(self, board, depth, player):
        best_score = float('-inf')
        children = []
        for col in range(self.col):
            if not self.is_valid_column(board, col):
                continue

            new_board = self.make_move(board, col, player)
            children.append(new_board)
            best_score = max( best_score , self.expectiminmax(board, depth, player, True, False , col) )

        self.node[board] = (best_score, children)
        return best_score
    def min_node(self, board, depth, player):
        best_score = float('inf')
        children = []
        for col in range(self.col):
            if not self.is_valid_column(board, col):
                continue
            new_board = self.make_move(board, col, player)
            children.append(new_board)
            best_score = min(best_score , self.expectiminmax(new_board, depth , player, True, True , col) )
        self.node[board] = (best_score, children)
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
    board = "000000000000000000000000000000000000000000"
    expecti = ExpectiMinMax(board, 2, 1)
    best_move, node, score = expecti.solve_expectiminmax(board, 1)
    print("Best move:")
    print(best_move)
    print("Node:")
    print(node)
    print("Score:")
    print(score)
    print(len(node))
