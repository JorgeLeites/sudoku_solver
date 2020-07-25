# Sudoku solver

A silly little project to amuse myself.

## Install

```
pip install -r requirements.txt
```

## Encoding the sudoku

The sudokus must be encoded from left to right, from top to bottom,
using 0s to encode the empty spaces.

For example the following sudoku:

```
6 X X | X X X | X X 5
X 4 X | X X 3 | X X X
2 3 X | X X X | X X X
---------------------
3 X X | 1 X X | 5 4 X
X X X | 3 2 X | 8 7 X
X X X | X X 8 | X 1 X
---------------------
X X 1 | X X 6 | 2 X X
X X 3 | X X X | X X 7
9 X X | 4 5 X | 6 X 1
```

Must be encoded like this:
`600000005040003000230000000300100540000320870000008010001006200003000007900450601`

## Run

```
python sudoku_solver.py solve <sudoku>
```

## Test

```
python sudoku_solver.py test <dataset path>
```

Each row of the dataset must contain two columns: the first with the unsolved sudoku
and the second with the solution.
