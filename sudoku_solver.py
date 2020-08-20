import csv
import click

from src.printer import print_progress
from src.solver import solve_sudoku
from src.sudoku import Sudoku
from src.exceptions import SudokuSolvingError, InvalidInputError


@click.group()
def cli():
    pass


@click.command()
@click.argument('sudoku')
def solve(sudoku):
    """Solve a sudoku"""
    try:
        parsed_sudoku = Sudoku(sudoku)
        print('\nSudoku:\n')
        parsed_sudoku.print()
        solved_sudoku = solve_sudoku(parsed_sudoku)
        print('\n=============================\n')
        if (solved_sudoku.is_solved()):
            print('Solution:\n')
            solved_sudoku.print()
            print('\nSerialized: {}\n'.format(solved_sudoku))
        else:
            print("Couldn't find the solution :(\n")
    except InvalidInputError as error:
        print('\n' + str(error))
    except SudokuSolvingError as error:
        print('\n' + 'Invalid sudoku.')


@click.command()
@click.argument('dataset', type=click.File('r'))
def test(dataset):
    """Test the solving algorithm against a dataset"""
    reader = csv.reader(dataset)
    total_problems = sum(1 for row in reader)
    solved_problems = 0
    dataset.seek(0)
    print_progress(solved_problems, total_problems)
    try:
        for row in reader:
            problem = row[0]
            solution = row[1]
            sudoku = Sudoku(problem)
            sudoku = solve_sudoku(sudoku)
            if str(sudoku) != solution:
                raise SudokuSolvingError(
                    'Incorrect solution: {} != {}.'.format(
                        sudoku, solution))
            solved_problems += 1
            print_progress(solved_problems, total_problems)

        print('\nDone!')
    except SudokuSolvingError as error:
        # We need two line breaks because of the progress bar
        print('\n\n' + str(error))


cli.add_command(solve)
cli.add_command(test)

if __name__ == '__main__':
    cli()
