import random


class SudokuGenerator:

    def __init__(self, n, k, sudoku_matrix):
        """
        Initializes the Sudoku Board
        :param n: Rank of Sudoku puzzle
        :param k: Number of Clues to initialize puzzle with
        """
        self.n = n
        self.k = k
        self.sudoku_matrix = sudoku_matrix

    def generate_sudoku_matrix(self, solver):
        self._fill_diagonal()
        solver.solve()
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

    def _create_clues(self):
        coordinates = [(x, y) for x in range(self.n ** 2) for y in range(self.n ** 2)]
        cells_to_remove = random.sample(coordinates, self.n ** 4 - self.k)

        for i, j in cells_to_remove:
            self.sudoku_matrix.make_cell_empty(i, j)
