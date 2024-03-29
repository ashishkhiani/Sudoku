import sys

from app.Iterator import DownIterable, RightIterable, LeftIterable, UpIterable
from app.Node import DancingNode, ColumnNode
from app.SudokuMatrix import SudokuMatrix


class DancingLinks:

    def __init__(self, matrix):
        self.matrix = matrix
        self._pad_matrix()

    def _pad_matrix(self):
        """
        Updates the input matrix by adding column headers and padding matrix with 0s to keep it a perfect square
        """
        for row in self.matrix:
            row.insert(0, 0)

        column_headers = []
        for j in range(len(self.matrix[0])):

            if j == 0:
                # insert header node
                column_headers.append('H')
            else:
                # insert column headers
                column_headers.append(f'C{j}')

        self.matrix.insert(0, column_headers)

    def create_dancing_links(self):
        """
        Method used to connect all nodes using doubly linked lists
        """
        nodes = self._create_nodes()
        self._create_links_between_nodes(nodes)

    def _create_nodes(self):
        """
        Converts all column headers and cells with 1s to Nodes
        """
        nodes = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                value = self.matrix[i][j]

                # Nothing to do
                if value == 0:
                    continue

                node = None

                # convert all 1's to DancingNode
                if value == 1:
                    node = DancingNode(value)

                # convert all column headers to ColumnNode
                if value != 1 and value != 0:
                    node = ColumnNode(value)

                node.row_id = i
                node.column_id = j
                nodes.append(node)
                self.matrix[i][j] = node

        return nodes

    def _create_links_between_nodes(self, nodes):
        """
        Creates a link between nodes that are connected to the left, right, up and down.
        Additionally, each DancingNode is referenced to a ColumnNode
        """
        for node in nodes:
            node.left = self._get_left(node.row_id, node.column_id)
            node.right = self._get_right(node.row_id, node.column_id)

            # header node does not need up or down links
            if node.value != 'H':
                node.up = self._get_up(node.row_id, node.column_id)
                node.down = self._get_down(node.row_id, node.column_id)

            # create reference to column header
            if node.value == 1:
                node.column_header = self._get_column_header(node.column_id)
                node.column_header.size += 1

    def _get_left(self, row, column):
        """
        Returns the node to the left of the node at (row, column)
        """
        j = (column - 1) % len(self.matrix[row])

        while self.matrix[row][j] == 0:
            j = (j - 1) % len(self.matrix[row])

        return self.matrix[row][j]

    def _get_right(self, row, column):
        """
        Returns the node to the right of the node at (row, column)
        """
        j = (column + 1) % len(self.matrix[row])

        while self.matrix[row][j] == 0:
            j = (j + 1) % len(self.matrix[row])

        return self.matrix[row][j]

    def _get_up(self, row, column):
        """
        Returns the node above the node at (row, column)
        """
        i = (row - 1) % len(self.matrix)

        while self.matrix[i][column] == 0:
            i = (i - 1) % len(self.matrix)

        return self.matrix[i][column]

    def _get_down(self, row, column):
        """
        Returns the node below the node at (row, column)
        """
        i = (row + 1) % len(self.matrix)

        while self.matrix[i][column] == 0:
            i = (i + 1) % len(self.matrix)

        return self.matrix[i][column]

    def _get_column_header(self, column):
        """
        Returns the column header of the node at column
        """
        return self.matrix[0][column]


class ExactCoverSolver:

    def __init__(self, exact_cover_matrix):
        self.exact_cover_matrix = exact_cover_matrix
        DancingLinks(exact_cover_matrix).create_dancing_links()
        self.header = self.exact_cover_matrix[0][0]
        self.num_updates = 0
        self.answer = []

    def search(self, k, o):

        if self.header.right == self.header:
            self.answer.append(o.copy())
            return

        c = self._choose_column()
        self._cover(c)

        for r in DownIterable(c):
            o[k] = r

            for j in RightIterable(r):
                self._cover(j.column_header)

            self.search(k + 1, o)

            r = o.pop(k, None)
            c = r.column_header

            for j in LeftIterable(r):
                self._uncover(j.column_header)

        self._uncover(c)
        return

    def get_num_updates(self):
        return self.num_updates

    def get_answer(self):
        return self.answer

    def _choose_column(self):
        """
        Returns the column with the smallest number of 1s.
        """
        min_size = sys.maxsize
        column_selected = None

        for c in RightIterable(self.header):
            if c.size < min_size:
                min_size = c.size
                column_selected = c

        return column_selected

    def _cover(self, c):
        self._unlinkLR(c)

        for i in DownIterable(c):
            for j in RightIterable(i):
                self._unlinkUD(j)
                j.column_header.size -= 1

    def _uncover(self, c):
        for i in UpIterable(c):
            for j in LeftIterable(i):
                j.column_header.size += 1
                self._relinkUD(j)

        self._relinkLR(c)

    def _unlinkUD(self, x):
        x.down.up = x.up
        x.up.down = x.down
        self.num_updates += 1

    def _relinkUD(self, x):
        x.down.up = x
        x.up.down = x
        self.num_updates += 1

    def _unlinkLR(self, x):
        x.right.left = x.left
        x.left.right = x.right
        self.num_updates += 1

    def _relinkLR(self, x):
        x.right.left = x
        x.left.right = x
        self.num_updates += 1


class SudokuExactCoverSolver:

    def __init__(self, sudoku_matrix):
        """
        :type sudoku_matrix: SudokuMatrix
        """
        self.sudoku_matrix = sudoku_matrix
        self.n = sudoku_matrix.get_rank()
        self.exact_cover_matrix, self.possibilities = self._create_exact_cover_matrix()
        self.exact_cover_solver = ExactCoverSolver(self.exact_cover_matrix)

    def solve(self):
        self.exact_cover_solver.search(k=0, o=dict())
        solutions = self.exact_cover_solver.get_answer()

        for solution in solutions[0].values():
            row, column, value = self.possibilities[solution.row_id - 1]
            if self.sudoku_matrix.is_empty_cell(row, column):
                self.sudoku_matrix.set(row, column, value)

    def get_num_updates(self):
        return self.exact_cover_solver.get_num_updates()

    def _create_exact_cover_matrix(self):
        possibilities = self._create_possibilities()
        constraints = self._create_constraints()
        exact_cover_matrix = []

        for possibility in possibilities:
            m = []
            for constraint in constraints:
                m.append(self._handle_possibility_constraint_combination(possibility, constraint))
            exact_cover_matrix.append(m)

        return exact_cover_matrix, possibilities

    def _create_possibilities(self):
        possibilities = []

        for row in range(self.n ** 2):
            for column in range(self.n ** 2):
                if self.sudoku_matrix.is_empty_cell(row, column):
                    for i in range(1, self.n ** 2 + 1):
                        if self.sudoku_matrix.is_valid(row, column, i):
                            possibilities.append((row, column, i))
                else:
                    possibilities.append((row, column, self.sudoku_matrix.get(row, column)))

        return possibilities

    def _create_constraints(self):
        constraints = []

        # row-column constraint
        for row in range(self.n ** 2):
            for column in range(self.n ** 2):
                constraints.append(('rc', row, column))

        # row-number constraint
        for row in range(self.n ** 2):
            for number in range(1, self.n ** 2 + 1):
                constraints.append(('rn', row, number))

        # column-number constraint
        for column in range(self.n ** 2):
            for number in range(1, self.n ** 2 + 1):
                constraints.append(('cn', column, number))

        # box-number constraint
        for box in range(self.n ** 2):
            for number in range(1, self.n ** 2 + 1):
                constraints.append(('bn', box, number))

        return constraints

    def _handle_possibility_constraint_combination(self, possibility, constraint):
        row, column, value = possibility
        constraint_type, x, y = constraint

        if constraint_type == 'rc':
            return 1 if row == x and column == y else 0

        if constraint_type == 'rn':
            return 1 if row == x and value == y else 0

        if constraint_type == 'cn':
            return 1 if column == x and value == y else 0

        if constraint_type == 'bn':
            box_index = self.sudoku_matrix.get_box_index(row, column)
            return 1 if box_index == x and value == y else 0
