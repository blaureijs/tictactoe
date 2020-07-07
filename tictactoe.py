# Minimax implemented with help from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python/

import random

class InvalidCharsError(Exception):
    """Raised when invalid characters are input for Tic Tac Toe."""
    print('Please enter cell input from characters X, O, or _ for empty cells.')


class CellsLengthError(Exception):
    """Raised when the cells input is not nine characters long."""
    print('Please enter nine characters for cell input.')


def to_index(coordinates):
    lookup_coordinates = {'1 1': {'row': 2, 'col': 0},
                          '2 1': {'row': 2, 'col': 1},
                          '3 1': {'row': 2, 'col': 2},
                          '1 2': {'row': 1, 'col': 0},
                          '2 2': {'row': 1, 'col': 1},
                          '3 2': {'row': 1, 'col': 2},
                          '1 3': {'row': 0, 'col': 0},
                          '2 3': {'row': 0, 'col': 1},
                          '3 3': {'row': 0, 'col': 2}}
    return lookup_coordinates[coordinates]


def check_game_state(board):
    x_triple = False
    o_triple = False
    empty = [cell for row in board for cell in row if cell == '_']
    x_cells = [cell for row in board for cell in row if cell == 'X']
    o_cells = [cell for row in board for cell in row if cell == 'O']
    if board[0][0] == board[0][1] == board[0][2]:
        if board[0][0] == 'X':
            x_triple = True
        elif board[0][0] == 'O':
            o_triple = True
    if board[1][0] == board[1][1] == board[1][2]:
        if board[1][0] == 'X':
            x_triple = True
        elif board[1][0] == 'O':
            o_triple = True
    if board[2][0] == board[2][1] == board[2][2]:
        if board[2][0] == 'X':
            x_triple = True
        elif board[2][0] == 'O':
            o_triple = True
    if board[0][0] == board[1][0] == board[2][0]:
        if board[0][0] == 'X':
            x_triple = True
        elif board[0][0] == 'O':
            o_triple = True
    if board[0][1] == board[1][1] == board[2][1]:
        if board[0][1] == 'X':
            x_triple = True
        elif board[0][1] == 'O':
            o_triple = True
    if board[0][2] == board[1][2] == board[2][2]:
        if board[0][2] == 'X':
            x_triple = True
        elif board[0][2] == 'O':
            o_triple = True
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == 'X':
            x_triple = True
        elif board[0][0] == 'O':
            o_triple = True
    if board[2][0] == board[1][1] == board[0][2]:
        if board[2][0] == 'X':
            x_triple = True
        elif board[2][0] == 'O':
            o_triple = True
    if (x_triple and o_triple) or abs(len(x_cells) - len(o_cells)) >= 2:
        return 'Impossible'
    elif not x_triple and not o_triple and len(empty) > 0:
        return 'Game not finished'
    elif x_triple:
        return 'X wins'
    elif o_triple:
        return 'O wins'
    return 'Draw'


def is_empty(board, row, col):
    cell_value = board[row][col]
    if cell_value == '_':
        return True
    return False


def find_terminal_move(board, active_player=None, only_player=False):
    x_o = ['X', 'O']
    if only_player:  # Use case with minmax hard AI, only looking for own final moves
        # Horizontal rows
        for i, row in enumerate(board):
            if (board[i][0] == board[i][1] == active_player) and board[i][2] not in x_o:
                return i, 2
            elif (board[i][0] == board[i][2] == active_player) and board[i][1] not in x_o:
                return i, 1
            elif (board[i][1] == board[i][2] == active_player) and board[i][0] not in x_o:
                return i, 0
        # Vertical cols
        for i in range(3):
            if (board[0][i] == board[1][i] == active_player) and board[2][i] not in x_o:
                return 2, i
            elif (board[1][i] == board[2][i] == active_player) and board[0][i] not in x_o:
                return 0, i
            elif (board[0][i] == board[2][i] == active_player) and board[1][i] not in x_o:
                return 1, i
        # Diagonals
        if (board[0][0] == board[1][1] == active_player) and board[2][2] not in x_o:
            return 2, 2
        elif (board[0][0] == board[2][2] == active_player) and board[1][1] not in x_o:
            return 1, 1
        elif (board[2][2] == board[1][1] == active_player) and board[0][0] not in x_o:
            return 0, 0
        elif (board[0][2] == board[1][1] == active_player) and board[2][0] not in x_o:
            return 2, 0
        elif (board[0][2] == board[2][0] == active_player) and board[1][1] not in x_o:
            return 1, 1
        elif (board[2][0] == board[1][1] == active_player) and board[0][2] not in x_o:
            return 0, 2
        return 'none', 'none'
    else:  # Use case with medium AI, looking for own moves but also blocking opponent
        # Horizontal rows
        for i, row in enumerate(board):
            if (board[i][0] == board[i][1]) and board[i][0] in x_o and board[i][2] not in x_o:
                return i, 2
            elif (board[i][0] == board[i][2]) and board[i][0] in x_o and board[i][1] not in x_o:
                return i, 1
            elif (board[i][1] == board[i][2]) and board[i][1] in x_o and board[i][0] not in x_o:
                return i, 0
        # Vertical cols
        for i in range(3):
            if (board[0][i] == board[1][i]) and board[0][i] in x_o and board[2][i] not in x_o:
                return 2, i
            elif (board[1][i] == board[2][i]) and board[1][i] in x_o and board[0][i] not in x_o:
                return 0, i
            elif (board[0][i] == board[2][i]) and board[0][i] in x_o and board[1][i] not in x_o:
                return 1, i
        # Diagonals
        if (board[0][0] == board[1][1]) and board[0][0] in x_o and board[2][2] not in x_o:
            return 2, 2
        elif (board[0][0] == board[2][2]) and board[0][0] in x_o and board[1][1] not in x_o:
            return 1, 1
        elif (board[2][2] == board[1][1]) and board[2][2] in x_o and board[0][0] not in x_o:
            return 0, 0
        elif (board[0][2] == board[1][1]) and board[0][0] in x_o and board[2][0] not in x_o:
            return 2, 0
        elif (board[0][2] == board[2][0]) and board[0][2] in x_o and board[1][1] not in x_o:
            return 1, 1
        elif (board[2][0] == board[1][1]) and board[2][0] in x_o and board[0][2] not in x_o:
            return 0, 2
        return 'none', 'none'


def evaluate(board, active_player):
    if check_game_state(board) == 'Draw':
        return int()  # 0
    elif check_game_state(board) == 'X wins':
        if active_player == 'X':
            return 1
        return -1
    elif check_game_state(board) == 'O wins':
        if active_player == 'O':
            return 1
        return -1


class TicTacToe:

    def display_ttt_board(self):
        start_end = '---------'
        row1 = f'| {self.board[0][0]} {self.board[0][1]} {self.board[0][2]} |'
        row2 = f'| {self.board[1][0]} {self.board[1][1]} {self.board[1][2]} |'
        row3 = f'| {self.board[2][0]} {self.board[2][1]} {self.board[2][2]} |'
        return f'{start_end}\n{row1}\n{row2}\n{row3}\n{start_end}'

    def check_next_move(self):
        x_cells = [cell for row in self.board for cell in row if cell == 'X']
        o_cells = [cell for row in self.board for cell in row if cell == 'O']
        if len(x_cells) > len(o_cells):
            return 'O'
        return 'X'

    def is_valid(self, row, col):
        if row < 0 or row > 2 or col < 0 or col > 2:
            return False
        elif self.board[row][col] != '_':
            return False
        return True

    def find_terminal_move(self):
        x_o = ['X', 'O']
        # Horizontal rows
        for i, row in enumerate(self.board):
            if (self.board[i][0] == self.board[i][1]) and self.board[i][0] in x_o and self.board[i][2] not in x_o:
                return i, 2
            elif (self.board[i][0] == self.board[i][2]) and self.board[i][0] in x_o and self.board[i][1] not in x_o:
                return i, 1
            elif (self.board[i][1] == self.board[i][2]) and self.board[i][1] in x_o and self.board[i][0] not in x_o:
                return i, 0
        # Vertical cols
        for i in range(3):
            if (self.board[0][i] == self.board[1][i]) and self.board[0][i] in x_o and self.board[2][i] not in x_o:
                return 2, i
            elif (self.board[1][i] == self.board[2][i]) and self.board[1][i] in x_o and self.board[0][i] not in x_o:
                return 0, i
            elif (self.board[0][i] == self.board[2][i]) and self.board[0][i] in x_o and self.board[1][i] not in x_o:
                return 1, i
        # Diagonals
        if (self.board[0][0] == self.board[1][1]) and self.board[0][0] in x_o and self.board[2][2] not in x_o:
            return 2, 2
        elif (self.board[0][0] == self.board[2][2]) and self.board[0][0] in x_o and self.board[1][1] not in x_o:
            return 1, 1
        elif (self.board[2][2] == self.board[1][1]) and self.board[2][2] in x_o and self.board[0][0] not in x_o:
            return 0, 0
        elif (self.board[0][2] == self.board[1][1]) and self.board[0][0] in x_o and self.board[2][0] not in x_o:
            return 2, 0
        elif (self.board[0][2] == self.board[2][0]) and self.board[0][2] in x_o and self.board[1][1] not in x_o:
            return 1, 1
        elif (self.board[2][0] == self.board[1][1]) and self.board[2][0] in x_o and self.board[0][2] not in x_o:
            return 0, 2
        return None, None

    def check_winner(self):
        # Columns
        for i, _ in enumerate(self.board):
            if (self.board[0][i] != '_' and
                    self.board[0][i] == self.board[1][i] and
                    self.board[1][i] == self.board[2][i]):
                return self.board[0][i]
        # Rows
        for i, _ in enumerate(self.board):
            if (self.board[i][0] != '_' and
                    self.board[i][0] == self.board[i][1] and
                    self.board[i][1] == self.board[i][2]):
                return self.board[i][0]
        # Second diagonal
        if (self.board[0][2] != '_' and
                self.board[0][2] == self.board[1][1] and
                self.board[0][2] == self.board[2][0]):
            return self.board[0][2]
        # Main diagonal
        if (self.board[0][0] != '_' and
                self.board[0][0] == self.board[1][1] and
                self.board[0][0] == self.board[2][2]):
            return self.board[0][0]
        # Full board?
        for i, _ in enumerate(self.board):
            for j, _ in enumerate(self.board[i]):
                if self.board[i][j] == '_':
                    return None
        # Tie
        return '_'

    def min(self, player):
        # Set opponent variable
        if player == 'X':
            opponent = 'O'
        else:
            opponent = 'X'

        # Set initial comparison (high minimum)
        min_val = 2

        # 1) Check if there is a winner first
        result = self.check_winner()
        if result == player:
            return -1, None, None
        elif result == opponent:
            return 1, None, None
        elif result == '_':
            return 0, None, None

        # 2) Check if there is a game ending move
        row_play, col_play = self.find_terminal_move()
        if row_play is not None:
            self.board[row_play][col_play] = player
            result = self.check_winner()
            self.board[row_play][col_play] = '_'
            if result == player:
                return -1, row_play, col_play
            elif result == opponent:
                return 1, row_play, col_play

        # 3) No winner, no terminal moves, so iterate through empty spaces and find optimal move
        for i, _ in enumerate(self.board):
            for j, _ in enumerate(self.board):
                if self.board[i][j] == '_':
                    # Test each empty field. Player makes a move and calls max method (one branch of game tree)
                    self.board[i][j] = player
                    (m, max_i, max_j) = self.max(opponent)
                    # Set max_val
                    if m < min_val:
                        min_val = m
                        row_play = i
                        col_play = j
                    # Reset current field to empty
                    self.board[i][j] = '_'

        return min_val, row_play, col_play

    def max(self, player):
        # Set opponent variable
        if player == 'X':
            opponent = 'O'
        else:
            opponent = 'X'

        # Set initial comparison value (low maximum)
        max_val = -2

        # 1) Check if there is a winner
        result = self.check_winner()
        if result == player:
            return -1, 0, 0
        elif result == opponent:
            return 1, 0, 0
        elif result == '_':
            return 0, 0, 0

        # 2) Check if there is a game ending move
        row_play, col_play = self.find_terminal_move()
        if row_play is not None:
            self.board[row_play][col_play] = player
            result = self.check_winner()
            self.board[row_play][col_play] = '_'
            if result == player:
                return -1, row_play, col_play
            elif result == opponent:
                return 1, row_play, col_play

        # 3) No winner, no terminal moves, so iterate through empty spaces and find optimal move
        for i, _ in enumerate(self.board):
            for j, _ in enumerate(self.board):
                if self.board[i][j] == '_':
                    # Test each empty field. Player makes a move and calls max method (one branch of game tree)
                    self.board[i][j] = player
                    (m, max_i, max_j) = self.max(opponent)
                    # Set max_val
                    if m > max_val:
                        max_val = m
                        row_play = i
                        col_play = j
                    # Reset current field to empty
                    self.board[i][j] = '_'

        return max_val, row_play, col_play

    def player_input(self, player):
        got_input = False
        while not got_input:
            try:
                coordinates = input('Enter the coordinates: ')
                number_strings = coordinates.split()
                number_integers = [int(x) for x in number_strings]
                index = to_index(coordinates)
                empty = is_empty(self.board, index['row'], index['col'])
                if not empty:
                    print('This cell is occupied! Choose another one!')
                else:
                    got_input = True
                    self.board[index['row']][index['col']] = player
            except KeyError:
                print('Coordinates should be from 1 to 3!')
            except ValueError:
                print('You should enter numbers!')

    def ai_input(self, player, level):
        if player == 'X':
            other = 'O'
        else:
            other = 'X'

        if level == 'easy':
            print('Making move level "easy"')
            selecting = True
            while selecting:
                random_row = random.randint(0, 2)
                random_col = random.randint(0, 2)
                empty = is_empty(self.board, random_row, random_col)
                if empty:
                    selecting = False
                    self.board[random_row][random_col] = player

        elif level == 'medium':
            print('Making move level "medium"')
            selecting = True
            while selecting:
                med_row, med_col = find_terminal_move(self.board)
                if med_row == 'none':
                    random_row = random.randint(0, 2)
                    random_col = random.randint(0, 2)
                    empty = is_empty(self.board, random_row, random_col)
                    if empty:
                        selecting = False
                        self.board[random_row][random_col] = player
                else:
                    empty = is_empty(self.board, med_row, med_col)
                    if empty:
                        selecting = False
                        self.board[med_row][med_col] = player

        elif level == 'hard':
            print('Making move level "hard"')
            selecting = True
            while selecting:
                term_row, term_col = self.find_terminal_move()
                if term_row is not None:
                    row_sel = term_row
                    col_sel = term_col
                else:
                    m, row_sel, col_sel = self.max(player)
                selecting = False
                self.board[row_sel][col_sel] = player

    def play_game(self):
        while self.game_state not in self.end_states:
            if self.player_one in self.ai_levels and self.player_two in self.ai_levels:
                if self.check_next_move() == 'X':
                    self.ai_input('X', self.player_one)
                else:
                    self.ai_input('O', self.player_two)
                print(self.display_ttt_board())
                self.game_state = check_game_state(self.board)
                if self.game_state in self.end_states:
                    print(self.game_state)

            elif self.player_one in self.ai_levels and self.player_two == 'user':
                if self.check_next_move() == 'X':
                    self.ai_input('X', self.player_one)
                else:
                    self.player_input('O')
                print(self.display_ttt_board())
                self.game_state = check_game_state(self.board)
                if self.game_state in self.end_states:
                    print(self.game_state)

            elif self.player_one == 'user' and self.player_two in self.ai_levels:
                if self.check_next_move() == 'X':
                    self.player_input('X')
                else:
                    self.ai_input('O', self.player_two)
                print(self.display_ttt_board())
                self.game_state = check_game_state(self.board)
                if self.game_state in self.end_states:
                    print(self.game_state)

            elif self.player_one == 'user' and self.player_two == 'user':
                if self.check_next_move() == 'X':
                    self.player_input('X')
                else:
                    self.player_input('O')
                print(self.display_ttt_board())
                self.game_state = check_game_state(self.board)
                if self.game_state in self.end_states:
                    print(self.game_state)

    def __init__(self, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two
        self.board = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
        print(self.display_ttt_board())
        self.end_states = ['X wins', 'O wins', 'Draw']
        self.ai_levels = ['easy', 'medium', 'hard']
        self.game_state = check_game_state(self.board)
        self.play_game()


def menu():
    running = True
    while running:
        command = input('Input command: ').split()
        if command[0] == 'exit':
            running = False
        elif len(command) != 3:
            print('Bad parameters!')
        else:
            tic_tac_toe = TicTacToe(command[1], command[2])


menu()
