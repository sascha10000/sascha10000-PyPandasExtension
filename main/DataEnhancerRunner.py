import os

from pandas import DataFrame

from main.DataEnhancer import DataEnhancer
from main.helper.FileFinder import FileFinder
from main.helper.ParamOps import find_param_value
from main.rowoperations.AddConfusionColumns import AddConfusionColumns
from main.rowoperations.AddPredictionColumn import AddPredictionColumn


# defines some operations to execute
def row_ops(de: DataEnhancer, df: DataFrame):
  classes = DataEnhancer.classes(df)
  return [
    AddPredictionColumn(base_columns=classes, new_column_name="prediction"),
    AddConfusionColumns(base_columns=classes, label_column_name="Label", prediction_column_name="prediction")
  ]


folder = find_param_value("--folder") if find_param_value("--folder") is not None else "example_data"

# the file finder will create a dictionary of all directories containing files {parent folder -> [files]} fitting the filter
files = FileFinder(folder).get_files().filter(startsWith="training_")
for folder in files:
  f_name = os.path.basename(os.path.normpath(folder))
  DataEnhancer(files=files[folder], out_file_name="modified_data_" + f_name).process_data(row_ops, log_error_to_file=True, limit=1)

