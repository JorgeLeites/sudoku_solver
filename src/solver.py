import math

from src.constants import ROW_LENGTH, GROUP_WIDTH


def is_valid(value, i, j, sudoku):
    # Inspect rows and columns
    possibilities = sudoku.get_possible_row_values(i)
    for inspecting_j in range(ROW_LENGTH):
        possible_values = possibilities[inspecting_j]
        if (
            inspecting_j != j
            and len(possible_values) == 1
            and possible_values[0] == value
        ):
            return False

    possibilities = sudoku.get_possible_column_values(j)
    for inspecting_i in range(ROW_LENGTH):
        possible_values = possibilities[inspecting_i]
        if (
            inspecting_i != i
            and len(possible_values) == 1
            and possible_values[0] == value
        ):
            return False

    # Inspect groups
    possibilities = sudoku.get_possible_group_values(i, j)
    for inspecting_i in range(GROUP_WIDTH):
        for inspecting_j in range(GROUP_WIDTH):
            possible_values = possibilities[inspecting_i][inspecting_j]
            if (
                (inspecting_i != i or inspecting_j != j)
                and len(possible_values) == 1
                and possible_values[0] == value
            ):
                return False

    return True


def is_only_option(value, i, j, sudoku):
    return (
        is_only_option_row(value, i, j, sudoku)
        or is_only_option_column(value, i, j, sudoku)
        or is_only_option_group(value, i, j, sudoku)
    )


def is_only_option_row(value, i, j, sudoku):
    possibilities = sudoku.get_possible_row_values(i)
    for inspecting_j in range(ROW_LENGTH):
        possible_values = possibilities[inspecting_j]
        if inspecting_j != j and value in possible_values:
            return False

    return True


def is_only_option_column(value, i, j, sudoku):
    possibilities = sudoku.get_possible_column_values(j)
    for inspecting_i in range(ROW_LENGTH):
        possible_values = possibilities[inspecting_i]
        if inspecting_i != i and value in possible_values:
            return False

    return True


def is_only_option_group(value, i, j, sudoku):
    possibilities = sudoku.get_possible_group_values(i, j)
    for inspecting_i in range(GROUP_WIDTH):
        for inspecting_j in range(GROUP_WIDTH):
            possible_values = possibilities[inspecting_i][inspecting_j]
            if (
                (inspecting_i != i or inspecting_j != j) and
                value in possible_values
            ):
                return False

    return True


def solve_sudoku(sudoku):
    changed = True
    while changed and not sudoku.is_solved():
        changed = False
        for i in range(ROW_LENGTH):
            for j in range(ROW_LENGTH):
                if not sudoku.is_position_solved(i, j):
                    for value in sudoku.get_possible_values(i, j):
                        if is_only_option(value, i, j, sudoku):
                            changed = True
                            sudoku.set_value(i, j, value)
                            break
                        elif not is_valid(value, i, j, sudoku):
                            changed = True
                            sudoku.remove_possibility(i, j, value)
