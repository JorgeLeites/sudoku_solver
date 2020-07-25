import math

ROW_LENGTH = 9
GROUP_WIDTH = 3


def parse_sudoku(serialized):
    parsed = []
    for i in range(ROW_LENGTH):
        parsed.append([])
        for j in range(ROW_LENGTH):
            parsed[i].append(int(serialized[i * ROW_LENGTH + j]))
    return parsed


def is_valid(value, i, j, possibilities):
    # Inspect rows and columns
    for inspecting_j in range(ROW_LENGTH):
        possible_values = possibilities[i][inspecting_j]
        if (
            inspecting_j != j
            and len(possible_values) == 1
            and possible_values[0] == value
        ):
            return False
    for inspecting_i in range(ROW_LENGTH):
        possible_values = possibilities[inspecting_i][j]
        if (
            inspecting_i != i
            and len(possible_values) == 1
            and possible_values[0] == value
        ):
            return False

    # Inspect groups
    i_offset = int(math.floor(i / GROUP_WIDTH) * GROUP_WIDTH)
    j_offset = int(math.floor(j / GROUP_WIDTH) * GROUP_WIDTH)
    for inspecting_i in range(i_offset, i_offset + GROUP_WIDTH):
        for inspecting_j in range(j_offset, j_offset + GROUP_WIDTH):
            possible_values = possibilities[inspecting_i][inspecting_j]
            if (
                (inspecting_i != i or inspecting_j != j)
                and len(possible_values) == 1
                and possible_values[0] == value
            ):
                return False

    return True


def is_only_option(value, i, j, possibilities):
    return (
        is_only_option_row(value, i, j, possibilities)
        or is_only_option_column(value, i, j, possibilities)
        or is_only_option_group(value, i, j, possibilities)
    )


def is_only_option_row(value, i, j, possibilities):
    for inspecting_j in range(ROW_LENGTH):
        possible_values = possibilities[i][inspecting_j]
        if inspecting_j != j and value in possible_values:
            return False

    return True


def is_only_option_column(value, i, j, possibilities):
    for inspecting_i in range(ROW_LENGTH):
        possible_values = possibilities[inspecting_i][j]
        if inspecting_i != i and value in possible_values:
            return False

    return True


def is_only_option_group(value, i, j, possibilities):
    i_offset = int(math.floor(i / GROUP_WIDTH) * GROUP_WIDTH)
    j_offset = int(math.floor(j / GROUP_WIDTH) * GROUP_WIDTH)
    for inspecting_i in range(i_offset, i_offset + GROUP_WIDTH):
        for inspecting_j in range(j_offset, j_offset + GROUP_WIDTH):
            possible_values = possibilities[inspecting_i][inspecting_j]
            if (inspecting_i != i or inspecting_j !=
                    j) and value in possible_values:
                return False

    return True


def solve_sudoku(sudoku):
    # Fill possible values with all numbers from 1 to 9
    possible_values = []
    for i in range(ROW_LENGTH):
        possible_values.append([])
        for j in range(ROW_LENGTH):
            sudoku_value = sudoku[i][j]
            possibilities = list(range(1, 10)) if sudoku_value == 0 else [
                sudoku_value]
            possible_values[i].append(possibilities)

    changed = True
    solved = False
    while changed and not solved:
        changed = False
        solved = True
        for i in range(ROW_LENGTH):
            for j in range(ROW_LENGTH):
                if len(possible_values[i][j]) > 1:
                    for value in possible_values[i][j]:
                        if is_only_option(value, i, j, possible_values):
                            changed = True
                            possible_values[i][j] = [value]
                            break
                        elif not is_valid(value, i, j, possible_values):
                            changed = True
                            possible_values[i][j].remove(value)
                    if len(possible_values[i][j]) > 1:
                        solved = False

    solution = []
    for i in range(ROW_LENGTH):
        solution.append([])
        for j in range(ROW_LENGTH):
            if len(possible_values[i][j]) > 1:
                # We don't know the solution, so we write 0
                solution[i].append(0)
            else:
                solution[i].append(possible_values[i][j][0])
    return solution


def serialize_sudoku(sudoku):
    serialized = ""
    for i in range(ROW_LENGTH):
        for j in range(ROW_LENGTH):
            serialized += str(sudoku[i][j])
    return serialized
