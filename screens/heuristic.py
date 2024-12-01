class Heuristic:
    def __init__(self):
        self.row = 6
        self.col = 7

    def get_cell(self ,row, col, board_state):
        return board_state[row * self.col + col]

    def check_connected_4( self ,board, player , max_check ):
        def in_bounds(x, y):
            return 0 <= x < self.row and 0 <= y < self.col
        opponent = 1 if player == 2 else 2
        directions = [(0, 1), (-1, 0), (1, 1), (1, -1),(0,-1) ]
        connected_count = 0
        for row in range(self.row):
            for col in range(self.col):
                if self.get_cell(row, col, board) == str(player):
                    for dx, dy in directions:
                        count = 1
                        for step in range(1, 4):
                            nx, ny = row + dx * step, col + dy * step
                            if in_bounds(nx, ny) and self.get_cell(nx, ny, board) == str(opponent):
                                count = 0
                                break
                            elif in_bounds(nx, ny) and self.get_cell(nx, ny, board) == str(player):
                                count += 1
                            elif not in_bounds(nx, ny):
                                count = 0
                                break
                            else:
                                if in_bounds(nx + 1, ny) and self.get_cell(nx + 1, ny, board) == '0' :
                                    count = 0
                                    break

                        if count == max_check:
                            connected_count += 1

        return connected_count

    def heuristic(self, board, player):
        comp3 = self.check_connected_4(board, player, 3)
        comp2 = self.check_connected_4(board, player, 2)
        oppo3 = self.check_connected_4(board, 1 if player == 2 else 2, 3)
        oppo2 = self.check_connected_4(board, 1 if player == 2 else 2, 2)
        return comp3*100 + comp2*10 - oppo3*100 - oppo2*10




