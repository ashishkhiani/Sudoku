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
        solver(self.n, self.sudoku_matrix).solve()
        self._create_clues()

    def _create_clues(self):
        coordinates = [(x, y) for x in range(self.n ** 2) for y in range(self.n ** 2)]
        cells_to_remove = random.sample(coordinates, self.n ** 4 - self.k)

        for i, j in cells_to_remove:
            self.sudoku_matrix.make_cell_empty(i, j)
