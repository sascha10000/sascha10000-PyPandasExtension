from typing import List

from pandas import Series

from main.rowoperations.RowOperation import RowOperation


class AddPredictionColumn(RowOperation):
  def __init__(self, base_columns: List[str], new_column_name: str = "predicted_class"):
    super().__init__(base_columns, [])

    self.new_column_name = new_column_name

  def apply(self, row: Series) -> Series:
    max_val = None

    for i, ncol in enumerate(self.base_columns):
      if max_val is None:
        max_val = row[ncol]
        row[self.new_column_name] = ncol

      if row[ncol] > max_val:
        max_val = row[ncol]
        row[self.new_column_name] = ncol

    return row
