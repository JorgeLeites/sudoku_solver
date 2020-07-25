import csv
import click

from src.printer import print_progress
from src.solver import parse_sudoku, solve_sudoku, serialize_sudoku


@click.group()
def cli():
    pass


@click.command()
@click.argument('sudoku')
def solve(sudoku):
    """Solve a sudoku"""
    parsed_sudoku = parse_sudoku(sudoku)
    solution = solve_sudoku(parsed_sudoku)
    print('Solved: {}'.format(serialize_sudoku(solution)))


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
        real_solution = row[1]
        sudoku = parse_sudoku(problem)
        solution = solve_sudoku(sudoku)
        if serialize_sudoku(solution) != real_solution:
            raise Exception(
                "Incorrect solution: {} != {}".format(
                    serialize_sudoku(solution), real_solution
                )
            )
        solved_problems += 1
        print_progress(solved_problems, total_problems)

    print("Done!")


cli.add_command(solve)
cli.add_command(test)

if __name__ == '__main__':
    cli()
