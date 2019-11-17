import sys

from Node import Node, DancingNode, ColumnNode
from SudokuMatrix import SudokuMatrix


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

        while not isinstance(self.matrix[row][j], Node):
            j = (j - 1) % len(self.matrix[row])

        return self.matrix[row][j]

    def _get_right(self, row, column):
        """
        Returns the node to the right of the node at (row, column)
        """
        j = (column + 1) % len(self.matrix[row])

        while not isinstance(self.matrix[row][j], Node):
            j = (j + 1) % len(self.matrix[row])

        return self.matrix[row][j]

    def _get_up(self, row, column):
        """
        Returns the node above the node at (row, column)
        """
        i = (row - 1) % len(self.matrix)

        while not isinstance(self.matrix[i][column], Node):
            i = (i - 1) % len(self.matrix)

        return self.matrix[i][column]

    def _get_down(self, row, column):
        """
        Returns the node below the node at (row, column)
        """
        i = (row + 1) % len(self.matrix)

        while not isinstance(self.matrix[i][column], Node):
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

    def search(self, k, o):

        if self.header.right == self.header:
            return o

        c = self._choose_column()
        self._cover(c)

        r = c.down
        while r != c:
            o[k] = r

            j = r.right
            while j != r:
                # cover column header of j
                self._cover(j.column_header)

                # iterate to next right element
                j = j.right

            return self.search(k + 1, o)

        #     r = o[k]
        #     c = r.column_header
        #
        #     j = r.left
        #     while j != r:
        #         # uncover column header of j
        #         self._uncover(j.column_header)
        #
        #         # iterate to next left element
        #         j = j.left
        #
        #     # iterate to next down element
        #     r = r.down
        #
        # self._uncover(c)
        # return o

    def _choose_column(self):
        """
        Returns the column with the smallest number of 1s.
        """
        current_node = self.header.right
        min_size = sys.maxsize
        column_selected = None

        while current_node != self.header:
            if current_node.size < min_size:
                min_size = current_node.size
                column_selected = current_node
            current_node = current_node.right

        return column_selected

    @staticmethod
    def _cover(c):
        # remove column c from header list
        c.right.left = c.left
        c.left.right = c.right

        i = c.down
        while i != c:

            j = i.right
            while j != i:
                # remove j from current row i
                j.down.up = j.up
                j.up.down = j.down

                # decrement size of column that j refers to
                j.column_header.size -= 1

                # iterate to next right element
                j = j.right

            # iterate to next down element
            i = i.down

    @staticmethod
    def _uncover(c):
        i = c.up
        while i != c:

            j = i.left
            while j != i:
                # increment size of column that j refers to
                j.column_header.size += 1

                # add j back to current row i
                j.down.up = j
                j.up.down = j

                # iterate to next left element
                j = j.left

            # iterate to next up element
            i = i.up

        # add column c to header list
        c.right.left = c
        c.left.right = c


class SudokuExactCoverSolver:

    def __init__(self, n, sudoku_matrix):
        """
        :type sudoku_matrix: SudokuMatrix
        """
        self.n = n
        self.sudoku_matrix = sudoku_matrix
        self.exact_cover_matrix, self.possibilities = self._create_exact_cover_matrix()

    def solve(self):
        exact_cover_solver = ExactCoverSolver(self.exact_cover_matrix)
        rows_to_select = []

        solutions = exact_cover_solver.search(k=0, o=dict())

        for solution in solutions.values():
            rows_to_select.append(solution.row_id - 1)

        for row_id in rows_to_select:
            row, column, value = self.possibilities[row_id]
            self.sudoku_matrix.set(row, column, value)

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
