import math

from src.constants import ROW_LENGTH, GROUP_WIDTH


def is_valid(value, i, j, sudoku):
    # Inspect rows and columns
    possibilities = sudoku.get_possible_row_values(i)
    for inspecting_j, possible_values in enumerate(possibilities):
        if (
            inspecting_j != j
            and len(possible_values) == 1
            and possible_values[0] == value
        ):
            return False

    possibilities = sudoku.get_possible_column_values(j)
    for inspecting_i, possible_values in enumerate(possibilities):
        if (
            inspecting_i != i
            and len(possible_values) == 1
            and possible_values[0] == value
        ):
            return False

    # Inspect groups
    possibilities = sudoku.get_possible_group_values(i, j)
    inspected_index = (i%GROUP_WIDTH) * GROUP_WIDTH + (j%GROUP_WIDTH)
    for index, possible_values in enumerate(possibilities):
        if (
            (index != inspected_index)
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
    for inspecting_j, possible_values in enumerate(possibilities):
        if inspecting_j != j and value in possible_values:
            return False

    return True


def is_only_option_column(value, i, j, sudoku):
    possibilities = sudoku.get_possible_column_values(j)
    for inspecting_i, possible_values in enumerate(possibilities):
        if inspecting_i != i and value in possible_values:
            return False

    return True


def is_only_option_group(value, i, j, sudoku):
    possibilities = sudoku.get_possible_group_values(i, j)
    inspected_index = (i%GROUP_WIDTH) * GROUP_WIDTH + (j%GROUP_WIDTH)
    for index, possible_values in enumerate(possibilities):
        if (
            (index != inspected_index) and
            value in possible_values
        ):
            return False

    return True



def solve_sudoku(sudoku):
    changed = True
    while changed and not sudoku.is_solved():
        changed = False
        for i, row in enumerate(sudoku.possible_values):
            for j, possibilities in enumerate(row):
                if not sudoku.is_position_solved(i, j):
                    for value in possibilities:
                        if is_only_option(value, i, j, sudoku):
                            changed = True
                            sudoku.set_value(i, j, value)
                            break
                        elif not is_valid(value, i, j, sudoku):
                            changed = True
                            sudoku.remove_possibility(i, j, value)
