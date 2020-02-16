from pandas import Series

from main.rowoperations.RowOperation import RowOperation


class AddTrueFalseColumns(RowOperation):
  def __init__(self,base_columns:list, label_column_name:str, prediction_column_name:str):
    super().__init__(base_columns, ["_true", "_false"])
    self.label_column_name = label_column_name
    self.prediction_column_name = prediction_column_name

  def apply(self, row:Series) -> Series:
    row = row.append(Series(0, index=[new_column_name[0] for new_column_name in self.new_columns]))

    clazz = row[self.label_column_name]
    prediction = row[self.prediction_column_name]

    if clazz != prediction:
      row[clazz + "_false"] = 1
    else:
      row[clazz + "_true"] = 1

    return row
