from SudokuBackTrackingSolver import SudokuBackTrackingSolver
from SudokuExactCoverSolver import SudokuExactCoverSolver
from SudokuGenerator import SudokuGenerator
from SudokuMatrix import SudokuMatrix
from SudokuValidator import SudokuValidator


def main(n, k):
    # Initialize Sudoku Matrix
    sudoku_matrix = SudokuMatrix(n)
    sudoku_generator = SudokuGenerator(n, k, sudoku_matrix)
    sudoku_backtracking_solver = SudokuBackTrackingSolver(n, sudoku_matrix)
    sudoku_exact_cover_solver = SudokuExactCoverSolver(n, sudoku_matrix)
    sudoku_validator = SudokuValidator(sudoku_matrix)

    # Generate Sudoku Puzzle
    sudoku_generator.generate_sudoku_matrix(sudoku_backtracking_solver)
    print(sudoku_matrix)

    # Solve Sudoku Puzzle
    # sudoku_backtracking_solver.solve()
    sudoku_exact_cover_solver.solve()
    print(sudoku_matrix)

    # Validate Sudoku Solution
    sudoku_validator.validate()


main(n=2, k=16)
