import csv
import click

from src.printer import print_progress
from src.solver import solve_sudoku
from src.sudoku import Sudoku


@click.group()
def cli():
    pass


@click.command()
@click.argument('sudoku')
def solve(sudoku):
    """Solve a sudoku"""
    parsed_sudoku = Sudoku(sudoku)
    print('\nSudoku:\n')
    parsed_sudoku.print()
    solve_sudoku(parsed_sudoku)
    print('\n=============================\n')
    print('Solution:\n')
    parsed_sudoku.print()
    print('\nSerialized: {}\n'.format(parsed_sudoku))


@click.command()
@click.argument('dataset', type=click.File('r'))
def test(dataset):
    """Test the solving algorithm against a dataset"""
    reader = csv.reader(dataset)
    total_problems = sum(1 for row in reader)
    solved_problems = 0
    dataset.seek(0)
    print_progress(solved_problems, total_problems)
    for row in reader:
        problem = row[0]
        solution = row[1]
        sudoku = Sudoku(problem)
        solve_sudoku(sudoku)
        if str(sudoku) != solution:
            raise Exception(
                "Incorrect solution: {} != {}".format(
                    sudoku, solution))
        solved_problems += 1
        print_progress(solved_problems, total_problems)

    print("Done!")


cli.add_command(solve)
cli.add_command(test)

if __name__ == '__main__':
    cli()
