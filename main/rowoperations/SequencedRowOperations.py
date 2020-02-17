from typing import List, Callable

from pandas import Series

from main.rowoperations.RowOperation import RowOperation

# typings
RowOperations = List[RowOperation]


class SequencedRowOperations:
  def __init__(self, row_operations: RowOperations, on_error: Callable[[Series, Exception], Series] = None):
    def default_err_handler(row, exception):
      raise exception

    self.operations = row_operations
    self.on_error = default_err_handler if on_error is None else on_error

  def apply(self, row: Series) -> Series:
    next_row = row
    for op in self.operations:
      try:
        next_row = op.apply(row)
      except Exception as e:
        return self.on_error(row, e)

    return next_row
