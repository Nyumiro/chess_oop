
from Desk import *
from Figures import Step, King
from History import HistoryItem


class Game:
    def __init__(self):
        self.isWhitePlayer = True
        self.counter = 1
        self.desk = Desk()
        self.history = dict()

    def validate(self, inp, step):
        try:
            step.parse(inp)
            self.desk.check_step(step, self.isWhitePlayer)
            self.desk.has_figure(step.start)
            self.desk.has_obstacle(step)
            return True
        except Exception as error:
            print(error.args[0])
            return False

    def print_winner(self, player):
        print(f"Мат королю {'белых' if not player else 'черных'}. "
              f"Победа {'белых' if player else 'черных'}. "
              f"Игра окончена за количество ходов: {self.counter}.")

    def revert(self, inp):
        step = int(inp.split('-')[-1])
        if step <= 0 or step > self.counter:
            print('Нельзя откатиться к такому ходу.')
            return None

        self.desk = self.history[step].game_desk
        self.counter = step
        self.isWhitePlayer = self.history[step].player

        self.desk.print_desk()

    def game_loop(self):
        self.desk.init_desk()
        self.desk.print_desk()
        self.history[1] = HistoryItem(self.counter, self.isWhitePlayer, self.desk.copy())

        while True:
            print(f'Ход №{self.counter}.')
            print(f"Ходят {'белые' if self.isWhitePlayer else 'черные'}. ")

            inp = input('Введите ход (пример: a7-a6): ')

            if 'revert-' in inp:
                self.revert(inp)
                continue

            step = Step()

            if not self.validate(inp, step):
                continue

            deleted_figure = self.desk.move_figure(step)
            self.desk.print_desk()
            king_under_check = self.desk.check()

            if king_under_check:
                if king_under_check.isWhite == self.isWhitePlayer:
                    print(f"Недопустимый ход, т.к. король окажется под шахом.")
                    self.revert('revert-' + str(self.counter))
                    continue
                if self.desk.check_mate(not self.isWhitePlayer):
                    self.print_winner(self.isWhitePlayer)
                    break
                print(f"Король {'белых' if not self.isWhitePlayer else 'черных'} под шахом.")

            if deleted_figure:
                print(f'Съедена фигура {deleted_figure}.')

            self.counter += 1
            self.isWhitePlayer = not self.isWhitePlayer
            self.history[self.counter] = HistoryItem(self.counter, self.isWhitePlayer, self.desk.copy())




'''БЫСТРАЯ КОМБИНАЦИЯ МАТА БЕЛЫМ 
G7-G5 
E2-E4 
F7-F6 
D1-H5

G7-g5
e2-e4
a7-a5
d1-h5
f7-f6'''

Game().game_loop()
