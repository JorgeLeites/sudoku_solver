import math

from src.constants import ROW_LENGTH, GROUP_WIDTH


class Sudoku:
    """Sudoku class representation"""

    def __init__(self, serialized):
        self.__parse(serialized)
        self.__set_possibilities()

    def __parse(self, serialized):
        self.__sudoku = []
        for i in range(ROW_LENGTH):
            self.__sudoku.append([])
            for j in range(ROW_LENGTH):
                self.__sudoku[i].append(int(serialized[i * ROW_LENGTH + j]))

    def __set_possibilities(self):
        self.__solved_values = 0
        self.possible_values = []
        for i, row in enumerate(self.__sudoku):
            self.possible_values.append([])
            for sudoku_value in row:
                if sudoku_value == 0:
                    possibilities = list(range(1, 10))
                else:
                    possibilities = [sudoku_value]
                    self.__solved_values += 1
                self.possible_values[i].append(possibilities)

    def __str__(self):
        serialized = ""
        for row in self.__sudoku:
            for value in row:
                serialized += str(value)
        return serialized

    def get_possible_values(self, i, j):
        return self.possible_values[i][j]

    def get_possible_row_values(self, i):
        return self.possible_values[i]

    def get_possible_column_values(self, j):
        result = []
        for row in self.possible_values:
            result.append(row[j])
        return result

    def get_possible_group_values(self, i, j):
        result = []
        offset_i = int(math.floor(i / GROUP_WIDTH) * GROUP_WIDTH)
        offset_j = int(math.floor(j / GROUP_WIDTH) * GROUP_WIDTH)
        for iter_i in range(offset_i, offset_i + GROUP_WIDTH):
            for iter_j in range(offset_j, offset_j + GROUP_WIDTH):
                result.append(
                    self.possible_values[iter_i][iter_j])
        return result

    def is_solved(self):
        return self.__solved_values == ROW_LENGTH * ROW_LENGTH

    def is_position_solved(self, i, j):
        return self.__sudoku[i][j] != 0

    def remove_possibility(self, i, j, value):
        possibilities = self.possible_values[i][j]
        possibilities.remove(value)
        if len(possibilities) == 1:
            self.__sudoku[i][j] = possibilities[0]
            self.__solved_values += 1

    def set_value(self, i, j, value):
        self.possible_values[i][j] = [value]
        self.__sudoku[i][j] = value
        self.__solved_values += 1

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
