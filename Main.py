import time

games = [
            [[5, 3, None, None, 7, None, None, None, None],
            [6, None, None, 1, 9, 5, None, None, None],
            [None, 9, 8, None, None, None, None, 6, None],
            [8, None, None, None, 6, None, None, None, 3],
            [4, None, None, 8, None, 3, None, None, 1],
            [7, None, None, None, 2, None, None, None, 6],
            [None, 6, None, None, None, None, 2, 8, None],
            [None, None, None, 4, 1, 9, None, None, 5],
            [None, None, None, None, 8, None, None, 7, 9]],

            [[None, None, None, None, 3, 7, 6, None, None],
            [None, None, None, 6, None, None, None, 9, None],
            [None, None, 8, None, None, None, None, None, 4],
            [None, 9, None, None, None, None, None, None, 1],
            [6, None, None, None, None, None, None, None, 9],
            [3, None, None, None, None, None, None, 4, None],
            [7, None, None, None, None, None, 8, None, None],
            [None, 1, None, None, None, 9, None, None, None],
            [None, None, 2, 5, 4, None, None, None, None]],

            [[None, None, 4, None, None, None, None, 7, None],
            [5, None, None, None, None, 6, None, None, None],
            [None, None, None, 5, None, None, None, None, 3],
            [None, 3, None, None, None, None, 7, None, None],
            [None, None, None, None, 6, None, None, None, None],
            [None, None, 1, None, None, None, None, 2, None],
            [2, None, None, None, None, 7, None, None, None],
            [None, None, None, 2, None, None, None, None, 5],
            [None, 6, None, None, None, None, 2, None, None]]
        ]


def run():
    game_picked = False
    while not game_picked:
        try:
            game_number = int(input("Enter game number from 1 to %d: " % len(games)))
            start_time = time.time()
            solved_game = solve(0, 0, game_number - 1)
            end_time = time.time()
            time_solved = end_time - start_time
            print(game_output(solved_game))
            print("Time took to solve: %4.3f" % time_solved)
        except IndexError:
            print("Number entered was out of range")
            continue
        except TypeError:
            print("Game given is not solvable")
            continue
        game_picked = True


def solve(row_position, column_position, game_number_position):
    game = games[game_number_position]
    safety_checks(game)  # This safety check tests the game to see if it is even solvable in first place
    print("Please wait...\n")
    if recursion(row_position, column_position, game, game_number_position):
        return game


def safety_checks(game):
    total_rows_counter = 0
    total_columns_counter = 0
    starting_numbers_counter = 0
    for row in game:
        for number in row:
            if number is not None:
                starting_numbers_counter += 1
            total_columns_counter += 1
        total_rows_counter += 1
        if total_columns_counter != 9:
            raise TypeError
        total_columns_counter = 0
    if total_rows_counter != 9:
        raise TypeError
    if starting_numbers_counter < 17:  # Any game that has fewer than 17 starting numbers cannot have a unique answer
        raise TypeError


def recursion(row_position, column_position, game, game_number_position):
    if column_position >= 9:
        column_position = 0
        row_position += 1
        if row_position >= 9:
            return True
    if games[game_number_position][row_position][column_position] is None:
        for i in range(9):
            i += 1
            if not is_in_row(i, game[row_position]) and\
                not is_in_column(i, column_position, game) and\
                not is_in_box(i, row_position, column_position, game):

                game[row_position][column_position] = i
                if not recursion(row_position, column_position + 1, game, game_number_position):
                    continue
                else:
                    return True
        game[row_position][column_position] = None
        return False
    return recursion(row_position, column_position + 1, game, game_number_position)


def is_in_row(number, row):
    return number in row


def is_in_column(number, column_position, game):
    column = []
    for i in game:
        column.append(i[column_position])
    return number in column


def is_in_box(number, row_position, column_position, game):
    box_coordinates = [[0, 2], [3, 5], [6, 8]]
    for box_row_coordinate in box_coordinates:
        if box_row_coordinate[0] <= row_position <= box_row_coordinate[1]:
            for box_column_coordinate in box_coordinates:
                if box_column_coordinate[0] <= column_position <= box_column_coordinate[1]:
                    return loop_box(box_row_coordinate[0], box_column_coordinate[0], number, game)


def loop_box(row_position, column_position, number, game):
    for box_row_position in range(3):
        box_row_position += row_position
        for box_column_position in range(3):
            box_column_position += column_position
            if game[box_row_position][box_column_position] == number:
                return True
    return False


def game_output(game):
    output = ""
    for row_position in range(9):
        for column_position in range(9):
            output += str(game[row_position][column_position]) + " "
            if (column_position + 1) % 3 == 0 and column_position != 8:
                output += "| "
        output += "\n"
        if (row_position + 1) % 3 == 0:
            for i in range(21):
                output += "-"
            output += "\n"
    return output


run()
