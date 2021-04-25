WHITE = 1
BLACK = 2


def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def print_board(board):
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(col, end='    ')
    print()


def main():
    board = Board()
    while True:
        print_board(board)
        print('Команды:')
        print('    exit                               -- выход')
        print('    move <row> <col> <row1> <row1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')
        if board.current_player_color() == WHITE:
            print('Ход белых:')
        else:
            print('Ход чёрных:')
        command = input()
        if command == 'exit':
            break
        else:
            print('НЕВЕРНАЯ КОМАНДА!!!1!!!')
            continue
        move_type, row, col, row1, col1 = command.split()
        row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
        if board.move_piece(row, col, row1, col1):
            print('Ход успешен')
        else:
            print('Координаты некорректы! Попробуйте другой ход!')


def correct_coords(row, col):
    return 0 <= row < 8 and 0 <= col < 8


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]

    def move_and_promote_pawn(self, row, col, row1, col1, char):
        if char not in ['Q', 'N', 'R', 'B']:
            return False
        if row == row1 and col == col1:
            return False
        if col != col1:
            return False

        direction = 1 if self.color == WHITE else -1
        if (row + direction == row1) and (col + 1 == col1 or col - 1 == col1):
            self.move_piece(row, col, row1, col1)
            if char == "Q":
                self.field[row1][col1] = Queen(self.color)
            if char == "N":
                self.field[row1][col1] = Knight(self.color)
            if char == "R":
                self.field[row1][col1] = Rook(self.color)
            if char == "B":
                self.field[row1][col1] = Bishop(self.color)
        elif row + direction == row1:
            self.move_piece(row, col, row1, col1)
            if char == "Q":
                self.field[row1][col1] = Queen(self.color)
            if char == "N":
                self.field[row1][col1] = Knight(self.color)
            if char == "R":
                self.field[row1][col1] = Rook(self.color)
            if char == "B":
                self.field[row1][col1] = Bishop(self.color)

        return False

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        if correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def move_piece(self, row, col, row1, col1):
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        self.field[row][col] = None
        self.field[row1][col1] = piece
        self.color = opponent(self.color)
        return True


class Rook:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        if row == row1 and col == col1:
            return False
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            if not (board.get_piece(row, c) is None):
                return False

        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Pawn:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        if row == row1 and col == col1:
            return False
        if col != col1:
            return False

        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        if row + direction == row1:
            return True

        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True

        return False

    def can_attack(self, board, row, col, row1, col1):
        direction = 1 if (self.color == WHITE) else -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))


class Knight:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'N'

    def can_move(self, board, row, col, row1, col1):
        if not (0 <= row < 8 and 0 <= col < 8):
            return False
        elif row == row1 + 2 and col == col1 + 1:
            return True
        elif row == row1 + 1 and col == col1 + 2:
            return True
        elif row == row1 - 2 and col == col1 - 1:
            return True
        elif row == row1 - 1 and col == col1 - 2:
            return True
        elif row == row1 - 1 and col == col1 + 2:
            return True
        elif row == row1 - 2 and col == col1 + 1:
            return True
        elif row == row1 + 1 and col == col1 - 2:
            return True
        elif row == row1 + 2 and col == col1 - 1:
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class King:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        if row == row1 and col == col1:
            return False
        piece1 = board.get_piece(row1, col1)
        if not piece1:
            if abs(row - row1) == 1 or abs(col - col1) == 1:
                return True
        elif piece1.get_color() == self.get_color():
            return False
        else:
            if abs(row - row1) == 1 or abs(col - col1) == 1:
                return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Queen:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        if not correct_coords(row1, col1):
            return False
        piece1 = board.get_piece(row1, col1)
        if not (piece1 is None) and piece1.get_color() == self.color:
            return False
        if row == row1 or col == col1:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                if not (board.get_piece(r, col) is None):
                    return False
            step = 1 if (col1 >= col) else -1
            for c in range(col + step, col1, step):
                if not (board.get_piece(row, c) is None):
                    return False
            return True
        if row - col == row1 - col1:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                c = col - row + r
                if not (board.get_piece(r, c) is None):
                    return False
            return True
        if row + col == row1 + col1:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                c = row + col - r
                if not (board.get_piece(r, c) is None):
                    return False
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(self, board, row, col, row1, col1)


class Bishop:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        piece1 = board.get_piece(row1, col1)
        if not (piece1 is None) and piece1.get_color() == self.color:
            return False
        if not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False
        if not (abs(row1 - row) == abs(col1 - col)):
            return False

        if row - col == row1 - col1:
            step = 1 if (row1 > row) else -1
            for r in range(row + step, row1, step):
                c = col - row + r
                if not (board.get_piece(r, c) is None):
                    return False

        elif row + col == row1 + col1:
            step = 1 if (row1 > row) else -1
            for r in range(row + step, row1, step):
                c = row + col - r
                if not (board.get_piece(r, c) is None):
                    return False

        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


if __name__ == "__main__":
    main()
