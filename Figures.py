from Desk import *


class Step:
    def __init__(self):
        self.start = ''
        self.end = ''
        self.vector = (0, 0)

    def get_vector(self):
        start, end = ('ABCDEFGH'.index(self.start[0]), int(self.start[-1])), (
            'ABCDEFGH'.index(self.end[0]), int(self.end[-1]))
        return end[0] - start[0], end[-1] - start[-1]

    def set(self, start, end):
        self.start = start
        self.end = end
        self.vector = self.get_vector()

    def parse(self, step):
        step = step.upper().split('-')
        if len(step) != 2:
            raise ChessException('Некорректный формат хода.')
        if step[0] == step[1]:
            raise ChessException('Конечная и начальная позиции совпадают. Повторите ввод.')
        for position in step:
            if not len(position) == 2 or position[-1] not in '12345678' or position[0] not in 'ABCDEFGH':
                raise ChessException(f'Некорректная позиция {position} для шахматной доски. Повторите ввод.')

        self.set(step[0], step[1])


class Figure:
    def __init__(self, white):
        self.isWhite = white

    def check_step(self, step, hasEndFigure):
        pass

    def show(self):
        pass


class Pawn(Figure):
    def show(self):
        return 'P' if self.isWhite else 'p'

    def check_step(self, step, hasEndFigure):
        if not self.isWhite and step.start[-1] == '2' and step.vector == (0, 2):
            return True
        if self.isWhite and step.start[-1] == '7' and step.vector == (0, -2):
            return True

        if not self.isWhite and (step.vector == (-1, 1) or step.vector == (1, 1)) and hasEndFigure:
            return True
        if self.isWhite and (step.vector == (1, -1) or step.vector == (-1, -1)) and hasEndFigure:
            return True

        if not self.isWhite and step.vector == (0, 1):
            return True
        if self.isWhite and step.vector == (0, -1):
            return True
        return False


class King(Figure):
    def show(self):
        return 'K' if self.isWhite else 'k'

    def check_step(self, step, hasEndFigure):
        return abs(step.vector[0]) <= 1 and abs(step.vector[1]) <= 1


class Queen(Figure):
    def show(self):
        return 'Q' if self.isWhite else 'q'

    def check_step(self, step, hasEndFigure):
        return (abs(step.vector[0]) == abs(step.vector[1])) or step.vector[0] == 0 or step.vector[1] == 0


class Knight(Figure):
    def show(self):
        return 'N' if self.isWhite else 'n'

    def check_step(self, step, hasEndFigure):
        return (abs(step.vector[0]), abs(step.vector[-1])) == (2, 1) or (abs(step.vector[0]), abs(step.vector[-1])) == (
        1, 2)


class Rook(Figure):
    def show(self):
        return 'R' if self.isWhite else 'r'

    def check_step(self, step, hasEndFigure):
        return step.vector[0] == 0 or step.vector[1] == 0


class Bishop(Figure):
    def show(self):
        return 'B' if self.isWhite else 'b'

    def check_step(self, step, hasEndFigure):
        return abs(step.vector[0]) == abs(step.vector[1])
