from random import randint
import time


class BoardException(Exception):
    pass


class BoardOutException(BoardException):

    def __str__(self):
        return "Вы указываете клетку за границами доски !"


class BoardUsedException(BoardException):

    def __str__(self):
        return "Вы уже стреляли в эту клетку !"


class BoardWrongShipException(Exception):
    pass


class Board:

    def __init__(self, hide = False, size = 6):

        self.size = size
        self.hide = hide

        self.quantity_ships = 0
        self.field = [[" "] * size for _ in range(size)]
        self.busy = []
        self.ships = []

    def __str__(self):

        res = ''
        res += "   |_1_|_2_|_3_|_4_|_5_|_6_|"

        for i, row in enumerate(self.field):
            res += f'\n {i + 1} | {" | ".join(row)} | '

        if self.hide:
            res = res.replace("■", " ")

        return res

    def begin(self):
        self.busy = []

    def is_out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contur(self, ship, show_ship_area = False):

        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for d in ship.dots:
            for dx, dy in near:
                cur_dot = Dot(d.x + dx, d.y + dy)

                if not self.is_out(cur_dot) and cur_dot not in self.busy:
                    if show_ship_area:
                        self.field[cur_dot.x][cur_dot.y] = '·'
                    self.busy.append(cur_dot)

    def add_ship(self, new_ship):

        for d in new_ship.dots:
            if self.is_out(d) or d in self.busy:
                raise BoardWrongShipException()

        for d in new_ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(new_ship)
        self.contur(new_ship)

    def shot(self, point):

        if self.is_out(point):
            raise BoardOutException()

        if point in self.busy:
            raise BoardUsedException()

        self.busy.append(point)

        for ship in self.ships:
            if ship.damaged(shot=point):
                ship.lives -= 1
                self.field[point.x][point.y] = "X"

                if ship.lives == 0:
                    self.quantity_ships += 1
                    self.contur(ship, True)
                    print(f'-----> Корабль убит !\n')
                    return True
                else:
                    print(f'-----> Корабль ранен !\n')
                    return True

        self.field[point.x][point.y] = '·'
        print(f'-----> Мимо !\n')
        return False


class GameField:

    def __init__(self, player_board, enemy_board):
        self.player_board = player_board
        self.enemy_board = enemy_board

    def __str__(self):
        res = ''
        res += "   ------- Ваше поле -------              ---- Поле противника ----"
        res += f'\n   |_1_|_2_|_3_|_4_|_5_|_6_|              |_1_|_2_|_3_|_4_|_5_|_6_|'
        i = 1
        for p_row, e_row in zip(self.player_board.field, self.enemy_board.field):
            res += f'\n {i} | {" | ".join(p_row)} | ' \
                   f'{"  "*5}' \
                   f' {i} | {" | ".join(list(map(lambda x: x.replace("■", " "), e_row)))} | '
            i += 1

        return res


class Dot:

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'


class Ship:

    def __init__(self, cord_, len_, orientation=0):
        self.cord_ = cord_
        self.len_ = len_
        self.orientation = orientation
        self.lives = len_

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.len_):
            cur_x = self.cord_.x
            cur_y = self.cord_.y

            if self.orientation == 0:
                cur_x += i
            elif self.orientation == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def damaged(self, shot):
        return shot in self.dots


class Player:

    def __init__(self, player_board = None, enemy_board = None, is_AI = False):
        self.player_board = player_board
        self.enemy_board = enemy_board
        self.AI_shots = []  # список успешных выстрелов ИИ
        self.is_AI = is_AI

    def request_move(self):
        raise NotImplementedError()

    def make_move(self):

        while True:
            try:
                target = self.request_move()
                repeat = self.enemy_board.shot(target)

                if repeat and self.is_AI:
                    self.AI_shots.append(target)
                elif not repeat and self.is_AI:
                    self.AI_shots = []

                return repeat
            except BoardException as e:
                print(e)


class AI(Player):

    def request_move(self):

        target = None
        attempts = None

        # "Приблизительный" механизм добивания кораблей пользователя
        if self.AI_shots:
            last_shot = self.AI_shots[-1]
            cur_x, cur_y = last_shot.x, last_shot.y

            attempts = 1
            while True:
                target = Dot(cur_x+1, cur_y)
                if attempts == 2:
                    target = Dot(cur_x - 1, cur_y)
                if attempts == 3:
                    target = Dot(cur_x, cur_y + 1)
                if attempts == 4:
                    target = Dot(cur_x, cur_y - 1)

                if attempts > 4:
                    break

                if self.enemy_board.is_out(d=target) or target in self.enemy_board.busy:
                    attempts += 1
                    continue
                else:
                    break

        if attempts == 5 or not self.AI_shots:
            while True:
                target = Dot(randint(0, 5), randint(0, 5))
                if self.enemy_board.is_out(d=target) or target in self.enemy_board.busy:
                    continue
                else:
                    break

        print(f'\n-----> Ход противника: {target.x + 1}-{target.y + 1}')
        return target


class Us(Player):

    def request_move(self):

        while True:

            print()
            target = input('-----> Ваш ход: ').split()

            if len(target) == 1:
                if len(target[0]) != 2:
                    print(f'Введите две координаты. Принимаются только цифры (через пробел, или слитно)!')
                    continue

                x, y = target[0][0], target[0][1]

            elif len(target) == 2:
                x, y = target

            else:
                print(f'Введите две координаты. Принимаются только цифры (через пробел, или слитно)!')
                continue

            if not(x.isdigit()) or not(y.isdigit()):
                print(f'Одна из координат не является числом. Введите корректные координаты. '
                      f'Принимаются только цифры  (через пробел, или слитно)!')
                continue

            x, y = int(x), int(y)

            return Dot(x-1, y-1)


class Game:

    def __init__(self, size = 6):
        self.size = size
        player_board = self.random_board()
        enemy_board = self.random_board()
        enemy_board.hide = True

        self.AI = AI(enemy_board, player_board, True)
        self.User = Us(player_board, enemy_board)

    def try_make_board(self):

        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0

        for l in lens:
            while True:
                attempts += 1

                if attempts > 2000:
                    return None

                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))

                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass

        board.begin()
        return board

    def random_board(self):

        board = None
        while board is None:
            board = self.try_make_board()
        return board

    def show_game_field(self):

        return print(GameField(self.User.player_board, self.AI.player_board))

    def welcome(self):

        print('''                                       
                                                Добро пожаловать в игру "Морской бой" !

                                                            Правила игры:
                            1. Чтобы сделать ход Вам нужно указать координаты клетки в формате:
                                    а) 'x y' (через пробел), например, 1 1; 1 2; 2 1 и т.д.,
                                    б) 'xy' (слитно), например, 11; 12; 21 и т.д.
                                    где 'x' - номер строки, 'y'- номер столбца (нумерация идет с 1).
                            2. В роли второго игрока выступает компьютер, он делает ходы автоматически.

                                                            Желаем удачи !

        ''')

    def game_process(self):

        num_move = 0

        while True:
            self.show_game_field()

            if num_move % 2 == 0 or num_move == 0:
                repeat_move = self.User.make_move()
            else:
                time.sleep(3)
                repeat_move = self.AI.make_move()

            if self.AI.enemy_board.quantity_ships == 7:
                print(f'\n----------------- Противник победил ! Вы проиграли.-----------------\n')
                self.show_game_field()
                break

            if self.User.enemy_board.quantity_ships == 7:
                print('\n----------------- Вы победили ! -----------------\n')
                print()
                self.show_game_field()
                break

            if not repeat_move:
                num_move += 1

    def start(self):
        self.welcome()
        self.game_process()


g = Game()
g.start()
