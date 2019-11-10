import random

from sudoku_matrix import SudokuMatrix


class SudokuGenerator:

    def __init__(self, n, k):
        """
        Initializes the Sudoku Board
        :param n: Rank of Sudoku puzzle
        :param k: Number of Clues to initialize puzzle with
        """
        self.n = n
        self.k = k
        self.sudoku_matrix = SudokuMatrix(n)

    def generate_sudoku_matrix(self):
        """
        Generates a Sudoku puzzle of rank n with k clues.
        :return: An n^2 by n^2 board with k clues
        """
        self._fill_diagonal()
        self._fill_remaining(0, self.n)
        self._create_clues()
        return self.sudoku_matrix

    def _fill_diagonal(self):
        for x in range(0, self.n ** 2, self.n):
            self._fill_box(x, x)

    def _fill_box(self, row, column):
        for i in range(self.n):
            for j in range(self.n):
                while True:
                    rand = random.randint(1, self.n ** 2)

                    if self._unused_in_box(row, column, rand):
                        break

                self.sudoku_matrix.set(row + i, column + j, rand)

    def _unused_in_box(self, row, column, num):
        for i in range(self.n):
            for j in range(self.n):
                if self.sudoku_matrix.get(row + i, column + j) == num:
                    return False

        return True

    def _fill_remaining(self, i, j):

        N = self.n ** 2
        SRN = self.n

        if j >= N and i < N - 1:
            i = i + 1
            j = 0

        if i >= N and j >= N:
            return True

        if i < SRN:
            if j < SRN:
                j = SRN
        elif i < N - SRN:
            if j == (int(i / SRN) * SRN):
                j = j + SRN
        else:
            if j == N - SRN:
                i = i + 1
                j = 0
                if i >= N:
                    return True

        for num in range(1, N + 1):
            if self._check_if_safe(i, j, num):
                self.sudoku_matrix.set(i, j, num)

                if self._fill_remaining(i, j + 1):
                    return True

                self.sudoku_matrix.make_cell_empty(i, j)

        return False

    def _check_if_safe(self, i, j, num):
        return self._unused_in_row(i, num) and \
               self._unused_in_column(j, num) and \
               self._unused_in_box(i - i % self.n, j - j % self.n, num)

    def _unused_in_row(self, i, num):
        for j in range(self.n ** 2):
            if self.sudoku_matrix.get(i, j) == num:
                return False

        return True

    def _unused_in_column(self, j, num):
        for i in range(self.n ** 2):
            if self.sudoku_matrix.get(i, j) == num:
                return False

        return True

    def _create_clues(self):
        coordinates = [(x, y) for x in range(self.n ** 2) for y in range(self.n ** 2)]
        cells_to_remove = random.sample(coordinates, self.n ** 4 - self.k)

        for i, j in cells_to_remove:
            self.sudoku_matrix.make_cell_empty(i, j)


