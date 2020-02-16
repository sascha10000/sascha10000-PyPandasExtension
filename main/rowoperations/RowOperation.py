from pandas import Series
from typing import List

# typings
StrList = List[str]

class RowOperation:
  def __init__(self, base_columns:list, new_column_postfix:StrList = ["_appended"]):
    self.base_columns = base_columns
    self.new_columns = []

    for old_column in base_columns:
      for postfix in new_column_postfix:
        self.new_columns.append((old_column + postfix, old_column))

  def apply(self, row:Series):
    pass
