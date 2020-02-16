from pandas import DataFrame

from main.helper.FileFinder import FileFinder
from main.DataEnhancer import DataEnhancer

# defines some operations to execute
from main.rowoperations.AddConfusionColumns import AddConfusionColumns
from main.rowoperations.AddPredictionColumn import AddPredictionColumn


def row_ops(de: DataEnhancer, df:DataFrame):
  classes = DataEnhancer.classes(df)
  return [
    AddPredictionColumn(base_columns=classes, new_column_name="prediction"),
    AddConfusionColumns(base_columns=classes, label_column_name="Label", prediction_column_name="prediction")
  ]


# the file finder will create a dictionary of all directories containing files {parent folder -> [files]} fitting the filter
files = FileFinder("example_data").get_files().filter(startsWith="training_")
for folder in files:
  DataEnhancer(files=files[folder], out_file_name="modified_data").process_data(row_ops, limit=2)



