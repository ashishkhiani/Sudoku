from tabulate import tabulate

from SudokuBackTrackingSolver import SudokuBackTrackingSolver
from SudokuGenerator import SudokuGenerator
from SudokuValidator import SudokuValidator


def print_sudoku_matrix(matrix):
    print(tabulate(matrix.get_rows(), tablefmt="fancy_grid"))


def main(n, k):
    # Generate Sudoku Puzzle
    sudoku_generator = SudokuGenerator(n, k)
    sudoku_matrix = sudoku_generator.generate_sudoku_matrix()

    print_sudoku_matrix(sudoku_matrix)

    # Solve Sudoku Puzzle
    sudoku_backtracking_solver = SudokuBackTrackingSolver(n, sudoku_matrix)
    sudoku_backtracking_solver.solve()

    print_sudoku_matrix(sudoku_matrix)

    # Validate Sudoku Solution
    sudoku_validator = SudokuValidator(sudoku_matrix)
    sudoku_validator.validate()


main(n=3, k=0)
