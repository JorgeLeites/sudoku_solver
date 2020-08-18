import math
import copy

from src.constants import ROW_LENGTH, GROUP_WIDTH


def is_only_option(value, i, j, sudoku):
    return (
        is_only_option_row(value, i, j, sudoku)
        or is_only_option_column(value, i, j, sudoku)
        or is_only_option_group(value, i, j, sudoku)
    )


def is_only_option_row(value, i, j, sudoku):
    for inspecting_j in range(ROW_LENGTH):
        if inspecting_j != j and sudoku.is_valid(i, inspecting_j, value):
            return False

    return True


def is_only_option_column(value, i, j, sudoku):
    for inspecting_i in range(ROW_LENGTH):
        if inspecting_i != i and sudoku.is_valid(inspecting_i, j, value):
            return False

    return True


def is_only_option_group(value, i, j, sudoku):
    offset_i = int(math.floor(i / GROUP_WIDTH) * GROUP_WIDTH)
    offset_j = int(math.floor(j / GROUP_WIDTH) * GROUP_WIDTH)
    for iter_i in range(offset_i, offset_i + GROUP_WIDTH):
        for iter_j in range(offset_j, offset_j + GROUP_WIDTH):
            if (iter_i != i or iter_j != j) and sudoku.is_valid(
                    iter_i, iter_j, value):
                return False

    return True


def search_solution(sudoku, i, j):
    changed = True
    while changed and not sudoku.is_solved():
        changed = False
        for iter_i in range(ROW_LENGTH):
            for iter_j in range(ROW_LENGTH):
                if not sudoku.is_position_solved(iter_i, iter_j):
                    possibilities = sudoku.get_possible_values(iter_i, iter_j)
                    for value in possibilities:
                        if is_only_option(value, iter_i, iter_j, sudoku):
                            changed = True
                            sudoku.set_value(iter_i, iter_j, value)
                            break

    if sudoku.is_solved():
        return sudoku

    next_i = (i + 1) % ROW_LENGTH
    next_j = j + 1 if next_i == 0 else j

    if sudoku.is_position_solved(i, j):
        return search_solution(sudoku, next_i, next_j)

    possibilities = sudoku.get_possible_values(i, j)
    for value in possibilities:
        test_sudoku = copy.deepcopy(sudoku)
        try:
            test_sudoku.set_value(i, j, value)
            return search_solution(test_sudoku, next_i, next_j)
        except BaseException:
            pass
    raise Exception('None of the possible values are valid.')


def solve_sudoku(sudoku):
    return search_solution(sudoku, 0, 0)
