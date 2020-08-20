import sys


def print_progress(solved, total):
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
        '\rSolving... {} {}/{} sudokus'.format(progress_bar, solved, total)
    )
    if solved == total:
        print('')
