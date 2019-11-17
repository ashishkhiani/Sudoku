import time

from SudokuBackTrackingSolver import SudokuBackTrackingSolver
from SudokuExactCoverSolver import SudokuExactCoverSolver
from SudokuGenerator import SudokuGenerator
from SudokuValidator import SudokuValidator


def main(solver):
    # Generate Sudoku Matrices
    sudoku_generator = SudokuGenerator()
    sudoku_matrices = sudoku_generator.generate_puzzles(num_puzzles=10)

    # Solve Sudoku Puzzle
    for sudoku_matrix in sudoku_matrices:
        s = solver(sudoku_matrix)
        solve_puzzle(s)

        # Validate Sudoku Solution
        sudoku_validator = SudokuValidator(sudoku_matrix)
        is_valid = sudoku_validator.validate()
        assert is_valid


def solve_puzzle(s):
    start = time.time()
    s.solve()
    end = time.time()
    print(end - start)


print('Backtracking Solver')
main(solver=SudokuBackTrackingSolver)
print('------------------')

print('Exact Cover Solver')
main(solver=SudokuExactCoverSolver)
print('------------------')
