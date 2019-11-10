from sudoku_generator import SudokuGenerator
from tabulate import tabulate

from sudoku_validator import SudokuValidator


def print_sudoku_matrix(matrix):
    print(tabulate(matrix.get_rows(), tablefmt="fancy_grid"))


def main(n, k):
    sudoku_generator = SudokuGenerator(n, k)
    sudoku_matrix = sudoku_generator.generate_sudoku_matrix()

    print_sudoku_matrix(sudoku_matrix)

    sudoku_validator = SudokuValidator(matrix=sudoku_matrix)
    sudoku_validator.validate()


main(n=3, k=17)
