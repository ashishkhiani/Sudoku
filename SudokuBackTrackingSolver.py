from SudokuMatrix import SudokuMatrix


class SudokuBackTrackingSolver:

    def __init__(self, sudoku_matrix):
        """
        :type sudoku_matrix: SudokuMatrix
        """
        self.sudoku_matrix = sudoku_matrix
        self.n = sudoku_matrix.get_rank()

    def solve(self):

        if not self.sudoku_matrix.has_empty_cells():
            return True

        current_row, current_column = self.sudoku_matrix.get_empty_cells()[0]

        for i in range(1, self.n ** 2 + 1):

            if self.sudoku_matrix.set_if_valid(current_row, current_column, i):
                if self.solve():
                    return True

                self.sudoku_matrix.make_cell_empty(current_row, current_column)

        return False
