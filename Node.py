class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        self.row_id = None
        self.column_id = None


class DancingNode(Node):
    def __init__(self, value):
        super().__init__(value)
        self.column_header = None

    def __repr__(self):
        node = (self.row_id, self.column_id)
        left = None if self.left is None else (self.left.row_id, self.left.column_id)
        right = None if self.right is None else (self.right.row_id, self.right.column_id)
        up = None if self.up is None else (self.up.row_id, self.up.column_id)
        down = None if self.down is None else (self.down.row_id, self.down.column_id)
        column_header = None if self.column_header is None else self.column_header.value
        return f'({node}, Left: {left}, Right: {right}, Up: {up}, Down: {down}, Column Header: {column_header})'


class ColumnNode(Node):
    def __init__(self, value):
        super().__init__(value)
        self.size = 0

    def __repr__(self):
        left = None if self.left is None else (self.left.row_id, self.left.column_id)
        right = None if self.right is None else (self.right.row_id, self.right.column_id)
        up = None if self.up is None else (self.up.row_id, self.up.column_id)
        down = None if self.down is None else (self.down.row_id, self.down.column_id)
        return f'({self.value, self.size}, Left: {left}, Right: {right}, Up: {up}, Down: {down})'
