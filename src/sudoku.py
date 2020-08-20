import math

from src.constants import ROW_LENGTH, GROUP_WIDTH
from src.exceptions import SudokuSolvingError, InvalidInputError


class Sudoku:
    """Sudoku class representation"""

    def __init__(self, serialized):
        self.__parse(serialized)
        self.__set_possibilities()

    def __parse(self, serialized):
        if len(serialized) != ROW_LENGTH * ROW_LENGTH:
            raise InvalidInputError('The length of the sudoku is incorrect.')

        self.__sudoku = []
        for i in range(ROW_LENGTH):
            new_row = []
            for j in range(ROW_LENGTH):
                new_row.append(int(serialized[i * ROW_LENGTH + j]))
            self.__sudoku.append(new_row)

    def __set_possibilities(self):
        self.__possible_values = []
        self.__solved_values = [
            [False for _ in range(ROW_LENGTH)] for _ in range(ROW_LENGTH)]
        for row in self.__sudoku:
            new_row = []
            for sudoku_value in row:
                new_row.append([True for _ in range(ROW_LENGTH)])
            self.__possible_values.append(new_row)

        for i, row in enumerate(self.__sudoku):
            for j, value in enumerate(row):
                if value != 0:
                    self.set_value(i, j, value)

    def __traverse_row(self, i, j, function):
        for iter_j in range(ROW_LENGTH):
            if iter_j != j:
                function(i, iter_j)

    def __traverse_column(self, i, j, function):
        for iter_i in range(ROW_LENGTH):
            if iter_i != i:
                function(iter_i, j)

    def __traverse_group(self, i, j, function):
        offset_i = int(math.floor(i / GROUP_WIDTH) * GROUP_WIDTH)
        offset_j = int(math.floor(j / GROUP_WIDTH) * GROUP_WIDTH)
        for iter_i in range(offset_i, offset_i + GROUP_WIDTH):
            for iter_j in range(offset_j, offset_j + GROUP_WIDTH):
                if iter_i != i or iter_j != j:
                    function(iter_i, iter_j)

    def get_possibilities_number(self, i, j):
        amount = 0
        for possible in self.__possible_values[i][j]:
            if possible:
                amount += 1
        return amount

    def remove_possibility(self, i, j, value):
        if self.__possible_values[i][j][value - 1]:
            self.__possible_values[i][j][value - 1] = False
            number_of_possibilities = self.get_possibilities_number(i, j)
            if number_of_possibilities == 0:
                raise SudokuSolvingError(
                    'There are no more possibilities for position {}, {}.'.format(i, j))
            if number_of_possibilities == 1:
                for index, possible in enumerate(self.__possible_values[i][j]):
                    if possible:
                        self.set_value(i, j, index + 1)

    def set_value(self, i, j, value):
        if not self.__solved_values[i][j]:
            self.__possible_values[i][j] = [
                index + 1 == value for index in range(ROW_LENGTH)]
            self.__sudoku[i][j] = value
            self.__solved_values[i][j] = True
            self.__traverse_row(
                i,
                j,
                lambda iter_i, iter_j: self.remove_possibility(
                    iter_i, iter_j, value)
            )
            self.__traverse_column(
                i,
                j,
                lambda iter_i, iter_j: self.remove_possibility(
                    iter_i, iter_j, value)
            )
            self.__traverse_group(
                i,
                j,
                lambda iter_i, iter_j: self.remove_possibility(
                    iter_i, iter_j, value)
            )

    def print(self):
        for i, row in enumerate(self.__sudoku):
            if i != 0 and i % GROUP_WIDTH == 0:
                print('---------------------')
            formatted_row = []
            for j, value in enumerate(row):
                if j != 0 and j % GROUP_WIDTH == 0:
                    formatted_row.append('|')
                formatted_row.append(str(value))
            print(' '.join(formatted_row))

    def __str__(self):
        serialized = ''
        for row in self.__sudoku:
            for value in row:
                serialized += str(value)
        return serialized

    def get_value(self, i, j):
        return self.__sudoku[i][j]

    def is_solved(self):
        for row in self.__solved_values:
            for solved in row:
                if not solved:
                    return False
        return True

    def is_valid(self, i, j, value):
        return self.__possible_values[i][j][value - 1]

    def is_position_solved(self, i, j):
        return self.__solved_values[i][j]

    def get_possible_values(self, i, j):
        values = []
        for index, valid in enumerate(self.__possible_values[i][j]):
            if valid:
                values.append(index + 1)
        return values
