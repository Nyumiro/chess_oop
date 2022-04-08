from Figures import *
from Figures import King


class ChessException(Exception):
    def __init__(self, arg):
        self.arg = arg


class Desk:
    desk = {}

    def copy(self):
        new_desk = Desk()
        new_desk.desk = {k: v for k, v in self.desk.items()}
        return new_desk

    def init_desk(self):
        COLUMN_NAMES = 'ABCDEFGH'
        White_Figures = [Rook(True), Knight(True), Bishop(True), Queen(True), King(True), Bishop(True), Knight(True),
                         Rook(True)]
        Black_Figures = [Rook(False), Knight(False), Bishop(False), Queen(False), King(False), Bishop(False),
                         Knight(False), Rook(False)]

        for column in range(8):
            self.desk[COLUMN_NAMES[column] + '8'] = White_Figures[column]
            self.desk[COLUMN_NAMES[column] + '7'] = Pawn(True)
            self.desk[COLUMN_NAMES[column] + '1'] = Black_Figures[column]
            self.desk[COLUMN_NAMES[column] + '2'] = Pawn(False)

    def print_desk(self):
        print(' ---------------------')
        print('    A B C D E F G H\n')
        for row in range(1, 9):
            print(row, end='\t')
            for column in 'ABCDEFGH':
                position = column + str(row)
                print(self.desk[position].show() if position in self.desk else '.', end=' ')
            print('  ' + str(row))
        print('\n    A B C D E F G H')
        print(' ---------------------')

    def move_figure(self, step):
        figure = self.desk[step.start]
        del self.desk[step.start]
        deleted_figure = self.desk[step.end] if step.end in self.desk else None
        self.desk[step.end] = figure
        return deleted_figure

    def check_step(self, step, isWhitePlayer):
        figure = self.desk[step.start]
        if isWhitePlayer ^ figure.isWhite:
            raise ChessException('Вы не можете ходить фигурами оппонента. Повторите ввод.')

        if step.end in self.desk:
            if not isWhitePlayer ^ self.desk[step.end].isWhite:
                raise ChessException(f'Поле {step.end} занято союзной фигурой.')

        if not figure.check_step(step, step.end in self.desk):
            raise ChessException(f'Недопустимая траектория для фигуры {figure.show()}. Повторите ввод.')

    def has_figure(self, position):
        if not (position in self.desk):
            raise ChessException(f'В клетке {position} нет фигуры. Повторите ввод.')

    def has_obstacle(self, step):
        """ Функция проверяет наличие препятствий по ходу фигуры. """

        def sgn(number):
            """ Вспомогательная функция, определяющая знак переданного числа."""
            if number > 0:
                return 1
            if number < 0:
                return -1
            return 0

        if isinstance(self.desk[step.start], Knight):
            return None

        position_start_int = 'ABCDEFGH'.index(step.start[0]), int(step.start[-1])
        for i in range(1, max(abs(step.vector[0]), abs(step.vector[1]))):
            column = 'ABCDEFGH'[position_start_int[0] + i * sgn(step.vector[0])]
            row = position_start_int[1] + i * sgn(step.vector[1])
            position = column + str(row)
            if position in self.desk:
                raise ChessException(f'В поле {position} стоит {self.desk[position]}. Повторите ход.')

    def check(self):
        king_positions = [k for k, v in self.desk.items() if isinstance(self.desk[k], King)]
        step = Step()
        for king in king_positions:
            for _ in self.desk:
                if self.desk[king].isWhite ^ self.desk[_].isWhite:
                    value = _ + '-' + king
                    step.parse(value)
                    if self.desk[_].check_step(step, step.end in self.desk):
                        try:
                            self.has_obstacle(step)
                        except ChessException:
                            return None
                        return self.desk[king]
            return None

    def _is_check_position(self, isWhitePlayer, king_position):
        step = Step()
        for _ in self.desk:
            step.set(_, king_position)
            if (isWhitePlayer ^ self.desk[_].isWhite) and self.desk[_].check_step(step, step.end in self.desk):
                try:
                    self.has_obstacle(step)
                except ChessException:
                    continue
                return True
        return False

    def check_mate(self, isWhitePlayer):
        COLUMN_NAMES = 'ABCDEFGH'
        king_position = \
            [k for k, v in self.desk.items() if
             isinstance(self.desk[k], King) and isWhitePlayer == self.desk[k].isWhite][0]
        vectors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for vector in vectors:
            position_int = COLUMN_NAMES.index(king_position[0]), int(king_position[-1])
            position_end_int = vector[0] + position_int[0], vector[1] + position_int[1]
            if 0 < position_end_int[0] < len(COLUMN_NAMES) and 0 < position_end_int[-1] <= 8:
                position_end = COLUMN_NAMES[position_end_int[0]] + str(position_end_int[-1])
                # получили клетку, куда король возможно может сбежать.
                if (position_end not in self.desk) or (self.desk[position_end].isWhite ^ isWhitePlayer):
                    # если на конечной позиции нет союзной фигуры, которая блокирует перемещение короля, то проверим эти
                    # позиции
                    if not self._is_check_position(isWhitePlayer, king_position):
                        return False
        return True
