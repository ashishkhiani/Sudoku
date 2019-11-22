import csv

from app.SudokuMatrix import SudokuMatrix


class SudokuGenerator:

    def __init__(self, n):
        self.n = n
        self.csv_file = f'datasets/sudoku_rank_{self.n}.csv'

    def generate_puzzles(self, num_puzzles=None):
        puzzles = self._read_sudoku_csv(num_puzzles)
        return [self._convert_string_to_matrix(puzzle) for puzzle in puzzles]

    def _read_sudoku_csv(self, num_puzzles=None):
        sudoku_puzzles = []
        with open(self.csv_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader, None)  # skip the headers

            for i, row in enumerate(csv_reader):
                if num_puzzles and len(sudoku_puzzles) == num_puzzles:
                    break

                sudoku_puzzles.append(row[0])

        return sudoku_puzzles

    @staticmethod
    def _convert_string_to_matrix(sudoku_string):
        m = int(len(sudoku_string) / 2)
        n = int(m ** (1 / 4))

        sudoku_matrix = SudokuMatrix(n)

        c = 0
        for i in range(n ** 2):
            for j in range(n ** 2):
                if sudoku_string[c] == '.':
                    sudoku_matrix.set(i, j, 0)
                else:
                    sudoku_matrix.set(i, j, int(sudoku_string[c:c + 2]))
                c += 2

        return sudoku_matrix
