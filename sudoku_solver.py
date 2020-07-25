import csv
import math
import sys

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
            inspecting_j != j and
            len(possible_values) == 1 and
            possible_values[0] == value
        ):
            return False
    for inspecting_i in range(ROW_LENGTH):
        possible_values = possibilities[inspecting_i][j]
        if (
            inspecting_i != i and
            len(possible_values) == 1 and
            possible_values[0] == value
        ):
            return False

    # Inspect groups
    i_offset = int(math.floor(i / GROUP_WIDTH) * GROUP_WIDTH)
    j_offset = int(math.floor(j / GROUP_WIDTH) * GROUP_WIDTH)
    for inspecting_i in range(i_offset, i_offset + GROUP_WIDTH):
        for inspecting_j in range(j_offset, j_offset + GROUP_WIDTH):
            possible_values = possibilities[inspecting_i][inspecting_j]
            if (
                (inspecting_i != i or inspecting_j != j) and
                len(possible_values) == 1 and
                possible_values[0] == value
            ):
                return False

    return True

def solve_sudoku(sudoku):
    # Fill possible values with all numbers from 1 to 9
    possible_values = []
    for i in range(ROW_LENGTH):
        possible_values.append([])
        for j in range(ROW_LENGTH):
            sudoku_value = sudoku[i][j]
            possibilities = list(range(1, 10)) if sudoku_value == 0 else [sudoku_value]
            possible_values[i].append(possibilities)

    changed = True
    solved = False
    while changed and not solved:
        changed = False
        solved = True
        for i in range(ROW_LENGTH):
            for j in range(ROW_LENGTH):
                for value in possible_values[i][j]:
                    if not is_valid(value, i, j, possible_values):
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
    serialized = ''
    for i in range(ROW_LENGTH):
        for j in range(ROW_LENGTH):
            serialized += str(sudoku[i][j])
    return(serialized)

def printProgress(solved, total):
    """Print a progress bar on the console"""
    total_squares = 50
    completed = solved * total_squares / total
    progress_bar = ''
    for index in range(total_squares):
        if index <= completed:
            progress_bar += '■'
        else:
            progress_bar += '□'
    sys.stdout.write(
        '\rSolving... {} {}/{} sudokus'.format(progress_bar, solved, total))
    if solved == total:
        print('')

with open('datasets/sudoku.csv') as dataset:
    reader = csv.reader(dataset)
    total_problems = sum(1 for row in reader)
    solved_problems = 0
    dataset.seek(0)
    for row in reader:
        printProgress(solved_problems, total_problems)
        problem = row[0]
        real_solution = row[1]
        sudoku = parse_sudoku(problem)
        solution = solve_sudoku(sudoku)
        if serialize_sudoku(solution) != real_solution:
            raise Exception('Incorrect solution: {} != {}'.format(serialize_sudoku(solution), real_solution))
        solved_problems += 1

print('Done!')
