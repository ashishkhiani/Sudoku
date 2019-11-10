from sudoku_matrix import SudokuMatrix


def contains_duplicates(arr):
    if len(set(arr)) != len(arr):
        return True

    return False


class SudokuValidator:

    def __init__(self, matrix):
        """

        :type matrix: SudokuMatrix
        """
        self.matrix = matrix

    def validate(self):

        fully_filled = self.matrix.is_fully_filled()
        validated_rows = self._validate_rows()
        validated_columns = self._validate_columns()
        validated_boxes = self._validate_box()

        print(f'fully_filled={fully_filled}, validated_rows={validated_rows}, validated_columns={validated_columns}, '
              f'validated_boxes={validated_boxes}')

        return fully_filled and validated_rows and validated_columns and validated_boxes

    def validate_completed(self):
        return self.matrix.is_fully_filled()

    def _validate_rows(self):
        for row in self.matrix.get_rows():
            if contains_duplicates(row):
                return False

        return True

    def _validate_columns(self):
        for column in self.matrix.get_columns():
            if contains_duplicates(column):
                return False

        return True

    def _validate_box(self):
        for box in self.matrix.get_boxes():
            if contains_duplicates(box):
                return False

        return True
