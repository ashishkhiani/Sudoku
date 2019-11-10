class SudokuMatrix:

    def __init__(self, n):
        self.n = n
        self.sudoku_matrix = [[0 for _ in range(n ** 2)] for _ in range(n ** 2)]
        self.EMPTY_CELL = 0

    def set(self, row, column, value):
        self.sudoku_matrix[row][column] = value

    def get(self, row, column):
        return self.sudoku_matrix[row][column]

    def get_rows(self):
        return self.sudoku_matrix

    def get_columns(self):
        return [*zip(*self.sudoku_matrix)]

    def get_boxes(self):
        indices = [(x % self.n, int(x / self.n)) for x in range(self.n ** 2)]
        boxes = [[self.sudoku_matrix[x * self.n + xx][y * self.n + yy] for xx, yy in indices] for x, y in indices]
        return boxes

    def get_empty_cells(self):
        empty_cells = []

        for row in range(self.n ** 2):
            for column in range(self.n ** 2):
                if self.is_empty_cell(row, column):
                    empty_cells.append((row, column))

        return empty_cells

    def is_fully_filled(self):
        return len(self.get_empty_cells()) == 0

    def is_empty_cell(self, row, column):
        return self.get(row, column) == self.EMPTY_CELL

    def make_cell_empty(self, row, column):
        self.set(row, column, self.EMPTY_CELL)
