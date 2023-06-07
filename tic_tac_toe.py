from random import randint

field = [[" "] * 3 for i in range(3)]
sign = None


def welcome():
    print('''                                       
                                            Добро пожаловать в игру "Крестики-нолики" !

                                                        Правила игры:
                1. Чтобы сделать ход Вам нужно указать координаты клетки в формате 'xy', например, 00; 10; 21 и т.д., 
                        где 'x' - номер строки, а 'y'- номер столбца (нумерация идет с 0)
                2. В роли второго игрока выступает компьютер
                
                                                        Желаем удачи !
    
    ''')

    print('''       Введите 1, если хотите играть "крестиком",  или 2, если "ноликом" ''')

    while True:
        input_sign = input('Ваш выбор: ')
        if input_sign == '1' or input_sign == '2':
            global sign
            sign = int(input_sign)
            print()
            break
        print('Выберите 1 или 2')


def show_game_board():

    """ Отображение игрового поля """

    print("       0 | 1 | 2 | ")
    print("     -------------")

    for row, col in enumerate(field):
        print(f'  {row}  | {" | ".join(col)} | ')
        print(" --- -------------")

    print()


def check_win():

    global sign

    win_pos = (((0, 0), (0, 1), (0, 2)),
               ((1, 0), (1, 1), (1, 2)),
               ((2, 0), (2, 1), (2, 2)),
               ((0, 2), (1, 1), (2, 0)),
               ((0, 0), (1, 1), (2, 2)),
               ((0, 0), (1, 0), (2, 0)),
               ((0, 1), (1, 1), (2, 1)),
               ((0, 2), (1, 2), (2, 2)))

    for pos in win_pos:
        symbols = []

        for c in pos:
            symbols.append(field[c[0]][c[1]])

        if symbols == ["X", "X", "X"] and sign == 1 or symbols == ["O", "O", "O"] and sign == 2:
            show_game_board()
            print("Вы победили !!!")
            return True
        elif symbols == ["X", "X", "X"] and sign != 1 or symbols == ["O", "O", "O"] and sign != 2:
            show_game_board()
            print("Вы проиграли. Выиграл компьютер !")
            return True

    return False


def request():

    global sign
    cell = input('Ваш ход: ')

    if not cell:
        print('Вы не ввели координаты')
        return request()

    if not cell.isdigit() or len(cell) != 2:
        print('Введите две координаты (принимаются только числа, без пробелов и прочих символов)')
        return request()

    x, y = int(cell[0]), int(cell[1])

    if x not in range(3) or y not in range(3):
        print('Одна из координат вне интервала (0:2). Введите корректные координаты')
        return request()

    if field[x][y] != ' ':
        print('Данная клетка занята. Введите другие координаты')
        return request()

    field[x][y] = "X" if sign == 1 else "O"


def pc_turn():

    global sign

    win_pos = (((0, 0), (0, 1), (0, 2)),
               ((1, 0), (1, 1), (1, 2)),
               ((2, 0), (2, 1), (2, 2)),
               ((0, 2), (1, 1), (2, 0)),
               ((0, 0), (1, 1), (2, 2)),
               ((0, 0), (1, 0), (2, 0)),
               ((0, 1), (1, 1), (2, 1)),
               ((0, 2), (1, 2), (2, 2)))

    turn_done = False

    while True:

        n = randint(0, 7)

        pos = win_pos[n]

        for c in pos:

            if field[c[0]][c[1]] == " ":
                field[c[0]][c[1]] = "O" if sign == 1 else "X"
                turn_done = True
                break

        if turn_done:
            break


def game_tic_tac_toe():

    """ Игра "Крестики-нолики" """

    welcome()

    turn = 1

    while turn <= 5:
        show_game_board()
        request()

        if check_win():
            break

        if turn != 5:
            pc_turn()
            if check_win():
                break

        if turn == 5:
            show_game_board()
            print('Ничья !')
            break

        turn += 1


game_tic_tac_toe()
