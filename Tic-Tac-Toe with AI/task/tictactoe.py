import numpy as np
from itertools import product
from random import randint


def set_cell(x, y, value, board):
    board_copy = board.copy()
    board_copy[x - 1, y - 1] = value
    return board_copy


def print_winner(score):
    if score == 1:
        print('X wins')
    elif score == -1:
        print('O wins')
    elif score == 0:
        print('Draw')


def main_diagonal(board):
    return np.array([board[0][0], board[1][1], board[2][2]])


def sec_diagonal(board):
    return np.array([board[0][2], board[1][1], board[2][0]])


def get_board():
    temp = []
    board_str = input('Enter the cells:')
    for s in board_str:
        if s == 'X':
            temp.append(1)
        elif s == '_':
            temp.append(0)
        elif s == 'O':
            temp.append(-1)
    board = np.array(temp).reshape(3, 3)
    return board


def end_game(board):
    if np.any(np.all(board == 1, axis=1)) or np.any(np.all(board == 1, axis=0)) \
            or np.all(sec_diagonal(board) == 1) or np.all(main_diagonal(board) == 1):
        # print('X')
        return True, 1
    elif np.any(np.all(board == -1, axis=1)) or np.any(np.all(board == -1, axis=0)) \
            or np.all(sec_diagonal(board) == -1) or np.all(main_diagonal(board) == -1):
        # print('O')
        return True, -1
    elif np.all(board):
        # print('Y')
        return True, 0
    else:
        # print('M')
        return False, 99
        # print('Game not finished')


class TicTac:
    def __init__(self):
        self.board = np.zeros((3, 3))


        # self.board[0, 0] = 1
        # self.board[0, 1] = 1
        # # self.board[2, 0] = 1
        #
        # self.board[0, 2] = -1
        # self.board[1, 1] = -1
        # # self.board[1, 0] = -1
        #
        self.empty_cells = list(product(range(1, 4), repeat=2))
        #
        # self.empty_cells.pop(self.empty_cells.index((1, 1)))
        # self.empty_cells.pop(self.empty_cells.index((2, 2)))
        # self.empty_cells.pop(self.empty_cells.index((1, 2)))
        # self.empty_cells.pop(self.empty_cells.index((1, 3)))
        # # self.empty_cells.pop(self.empty_cells.index((3, 1)))
        # self.empty_cells.pop(self.empty_cells.index((2, 1)))

        self.main_diag_indices = [(1, 1), (2, 2), (3, 3)]
        self.sec_diag_indices = [(3, 1), (2, 2), (1, 3)]
        self.n_cols = 3
        self.col_width = 2
        self.n_rows = 3
        self.filled_cells = []
        self.player1 = ''
        self.player2 = ''
        self.level = 'easy'

    def minmax(self, s, AIplayer, cell, board, empty_cells, level=0):
        # print('player:', s)
        # print(board, empty_cells)
        empty_cells_copy = empty_cells.copy()
        # print('c:', cell, 'p:', s)

        empty_cells_copy.pop(empty_cells_copy.index(cell))
        next_board = set_cell(*cell, s, board)
        end, score = end_game(next_board)
        # print(f"board, level={level}\n{next_board}")
        if end:
            if score == 0:
                # print(f'cell {cell}, score: {score}, empties: {empty_cells_copy}, player: {s}, level={level}')
                return score
            else:
                # print(f'cell {cell}, score: {score}, empties: {empty_cells_copy}, player: {s}, level={level}')
                return 1 if AIplayer == score else -1
        else:
            scores = []
            # print('empty cells', empty_cells, '\nboard:\n', board)
            for c in empty_cells_copy:
                scores.append(self.minmax(-s, AIplayer, c, next_board, empty_cells_copy, level=level + 1))
            # if level == 0:
            #     print(f'cell: {cell}, scores: {scores}, player {s},  AI {AIplayer}, level={level}')
            return max(scores) if s != AIplayer else min(scores)

    def best_cell(self, s, AIPlayer, board, empty_cells):
        if len(empty_cells) == 9:
            best_cell = (1, 1)
        # if s == 1:
        else:
            best_score = -99
            for cell in empty_cells:
                # print('-' * 80)
                # print(f' Cell {cell}, empties {empty_cells}')
                # print('-' * 80)
                score = self.minmax(s,  AIPlayer, cell, board, empty_cells)
                # print('-' * 80)
                # print(f'S: {score}')
                # print('-' * 80)
                if best_score < score:
                    best_score = score
                    best_cell = cell
        # else:
        #     best_score = 99
        #     for cell in empty_cells:
        #         score = self.minmax(-s, AIPlayer, cell, board, empty_cells)
        #         if best_score > score:
        #             best_score = score
        #             best_cell = cell
        return best_cell


    def menu(self):
        while True:
            command = input('Input command:').split()
            if command[0] == 'exit':
                break
            elif len(command) != 3:
                print('Bad parameters!')
            elif len(command) == 3 and command[0] == 'start':
                level1 = command[1]
                level2 = command[2]
                self.play(level1, level2)

    def user_move(self, marker, level):
        if marker == 'X':
            s = 1
        else:
            s = -1
        while True:
            try:
                x, y = input('Enter the coordinates:').split()
                x, y = int(x), int(y)
                if x > 3 or x < 1 or y > 3 or y < 1:
                    print('Coordinates should be from 1 to 3!')
                elif self.is_occupied(x, y):
                    print('This cell is occupied! Choose another one!')
                    continue
                else:
                    self.board = set_cell(x, y, s, self.board)
                    self.empty_cells.pop(self.empty_cells.index((x, y)))
                    # if self.board.sum() == 1:
                    #     self.set_cell(x, y, -1)
                    # elif self.board.sum() == 0:
                    #     self.set_cell(x, y, 1)
                    #     self.empty_cells.pop(self.empty_cells.index((x, y)))
                    break
            except ValueError:
                print('You should enter numbers!')

    def computer_move(self, marker='O', level='easy'):
        print(f'Making move level "{level}"')
        if marker == 'X':
            s = 1
        else:
            s = -1
        if level == 'easy':
            i = randint(0, len(self.empty_cells) - 1)
            cell = self.empty_cells.pop(i)
        elif level == 'medium':
            x_empty, o_empty = self.two_in_row_empty()
            # print(x_empty, o_empty)
            if marker == 'X':
                if x_empty:
                    cell = x_empty[0]
                    self.empty_cells.pop(self.empty_cells.index(cell))
                elif o_empty:
                    cell = o_empty[0]
                    self.empty_cells.pop(self.empty_cells.index(cell))
                else:
                    i = randint(0, len(self.empty_cells) - 1)
                    cell = self.empty_cells.pop(i)
            elif marker == 'O':
                if o_empty:
                    cell = o_empty[0]
                    self.empty_cells.pop(self.empty_cells.index(cell))
                elif x_empty:
                    cell = x_empty[0]
                    self.empty_cells.pop(self.empty_cells.index(cell))
                else:
                    i = randint(0, len(self.empty_cells) - 1)
                    cell = self.empty_cells.pop(i)
        elif level == 'hard':
            if marker == 'O':
                cell = self.best_cell(-1, -1, self.board, self.empty_cells)
            else:
                cell = self.best_cell(1, 1, self.board, self.empty_cells)
            self.empty_cells.pop(self.empty_cells.index(cell))

        self.board = set_cell(*cell, s, self.board)

    def is_occupied(self, x, y):
        return self.board[x - 1, y - 1] != 0

    def two_in_row_empty(self):
        two_X_empties = []
        two_O_empties = []
        row_X = np.where(self.board.sum(axis=1) == 2)[0] + 1
        col_X = np.where(self.board.sum(axis=0) == 2)[0] + 1
        row_O = np.where(self.board.sum(axis=1) == -2)[0] + 1
        col_O = np.where(self.board.sum(axis=0) == -2)[0] + 1
        for cell in self.empty_cells:
            if cell[1] in col_X or cell[0] in row_X:
                two_X_empties.append(cell)
            if cell[1] in col_O or cell[0] in row_O:
                two_O_empties.append(cell)
            if main_diagonal(self.board).sum() == 2 and cell in self.main_diag_indices and cell not in two_X_empties:
                two_X_empties.append(cell)
            if sec_diagonal(self.board).sum() == 2 and cell in self.sec_diag_indices and cell not in two_X_empties:
                two_X_empties.append(cell)
            if main_diagonal(self.board).sum() == -2 and cell in self.main_diag_indices and cell not in two_O_empties:
                two_O_empties.append(cell)
            if sec_diagonal(self.board).sum() == -2 and cell in self.sec_diag_indices and cell not in two_O_empties:
                two_O_empties.append(cell)
        return two_X_empties, two_O_empties

    def draw_board(self):
        top = '-' * (self.n_cols * self.col_width + 3)
        bottom = top
        print(top)
        for i in range(self.n_rows):
            self.draw_row(i)
        print(bottom)

    def draw_row(self, i):
        row = self.board[i]
        left = '| '
        right = '|'
        row_string = ''
        for s in row:
            if s == 1:
                row_string += 'X '
            elif s == -1:
                row_string += 'O '
            else:
                row_string += '  '
        row_string = left + row_string + right
        print(row_string)

    def play(self, player1, player2):
        computer = ['easy', 'medium', 'hard']
        self.draw_board()
        marker1 = 'X'
        marker2 = 'O'
        level1 = player1
        level2 = player2
        if player1 in computer and player2 in computer:
            f_player1 = self.computer_move
            f_player2 = self.computer_move

        elif player1 == 'user' and player2 == 'user':
            f_player1 = self.user_move
            f_player2 = self.user_move

        elif player1 == 'user' and player2 in computer:
            f_player1 = self.user_move
            f_player2 = self.computer_move

        elif player1 in computer and player2 == 'user':
            f_player1 = self.computer_move
            f_player2 = self.user_move

        while True:
            f_player1(marker1, level1)
            self.draw_board()
            end, score = end_game(self.board)
            if end:
                print_winner(score)
                break
            f_player2(marker2, level2)
            self.draw_board()
            end, score = end_game(self.board)
            if end:
                print_winner(score)
                break


if __name__ == '__main__':
    game = TicTac()
    game.menu()
