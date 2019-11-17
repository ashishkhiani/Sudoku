from SudokuBackTrackingSolver import SudokuBackTrackingSolver
from SudokuExactCoverSolver import SudokuExactCoverSolver
from SudokuGenerator import SudokuGenerator
from SudokuMatrix import SudokuMatrix
from SudokuValidator import SudokuValidator


def main(n, k, solver):
    # Initialize Sudoku Matrix
    sudoku_matrix = SudokuMatrix(n)

    # Generate Sudoku Matrix
    sudoku_generator = SudokuGenerator(n, k, sudoku_matrix)
    sudoku_generator.generate_sudoku_matrix(solver)
    print(sudoku_matrix)

    # Solve Sudoku Puzzle
    solve_puzzle(s=solver(n, sudoku_matrix))
    print(sudoku_matrix)

    # Validate Sudoku Solution
    sudoku_validator = SudokuValidator(sudoku_matrix)
    sudoku_validator.validate()


def solve_puzzle(s):
    # TODO start measuring
    s.solve()
    # TODO stop measuring


main(n=3, k=17, solver=SudokuExactCoverSolver)
