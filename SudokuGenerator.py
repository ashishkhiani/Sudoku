import csv

from SudokuMatrix import SudokuMatrix


class SudokuGenerator:

    @staticmethod
    def read_sudoku_csv(num_puzzles):
        sudoku_puzzles = []
        with open('datasets/sudoku.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader, None)  # skip the headers

            for i, row in enumerate(csv_reader):
                sudoku_puzzles.append(row[0])
                if len(sudoku_puzzles) == num_puzzles:
                    break

        return sudoku_puzzles

    @staticmethod
    def convert_string_to_matrix(sudoku_string):
        n = int(len(sudoku_string) ** (1 / 4))

        sudoku_matrix = SudokuMatrix(n)

        c = 0
        for i in range(n ** 2):
            for j in range(n ** 2):
                sudoku_matrix.set(i, j, int(sudoku_string[c]))
                c += 1

        return sudoku_matrix

    def generate_puzzles(self, num_puzzles):
        puzzles = self.read_sudoku_csv(num_puzzles)
        return [self.convert_string_to_matrix(puzzle) for puzzle in puzzles]
