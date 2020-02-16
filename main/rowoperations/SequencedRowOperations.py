from typing import List

from pandas import Series

from main.rowoperations.RowOperation import RowOperation

# typings
RowOperations = List[RowOperation]

class SequencedRowOperations:
  def __init__(self, row_operations:RowOperations):
    self.operations = row_operations

  def apply(self, row:Series) -> Series:
    next_row = row
    for op in self.operations:
      next_row = op.apply(row)

    return next_row
