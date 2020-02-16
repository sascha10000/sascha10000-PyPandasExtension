from pandas import Series

from main.rowoperations.RowOperation import RowOperation


class AddConfusionColumns(RowOperation):
  def __init__(self, base_columns: list, label_column_name: str, prediction_column_name: str, prefix: str = "confuse_"):
    super().__init__(base_columns, [""])
    self.prefix = prefix
    # reset new_columns according to internal logic
    self.new_columns = []
    for clazz in base_columns:
      for prediction in base_columns:
        self.new_columns.append((self.prefix + clazz + "_" + prediction, clazz))

    self.label_column_name = label_column_name
    self.prediction_column_name = prediction_column_name

  def apply(self, row: Series) -> Series:
    row = row.append(Series(0, index=[new_column_name[0] for new_column_name in self.new_columns]))

    clazz = row[self.label_column_name]
    prediction = row[self.prediction_column_name]

    if str(clazz) == 'nan':
      return None

    row[self.prefix + clazz + "_" + prediction] = 1

    return row
