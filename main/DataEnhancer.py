from typing import List, Callable

import pandas as pd
from pandas import Series
from pandas.io.parsers import TextFileReader
from datetime import datetime

from main.helper.GlobalFileHandler import GlobalFileHandler
from main.rowoperations.RowOperation import RowOperation
from main.rowoperations.SequencedRowOperations import SequencedRowOperations


class DataEnhancer:
  def __init__(self, files: list, out_file_name: str, folder: str = None):
    if folder is not None:
      self.folder: str = folder if folder.endswith("/") or folder.endswith("\\") else folder + "/"
    self.files: list = files if folder is None else [folder + file for file in files]
    self._col_names = None
    self.out_file_name = out_file_name
    self.error_log = GlobalFileHandler()

  def process_data(self, row_operations: Callable[['DataEnhancer', pd.DataFrame], List[RowOperation]], store_to_file: bool = True, limit=-1, single_chunk_at: int = -1, log_error_to_file: bool = False) -> pd.DataFrame:
    if row_operations is None:
      raise Exception("No row operations were provided. At least one is needed.") # everything else is senseless

    # error handler/logger
    def on_error_in_processing(lfile: str) -> Callable[[Series, Exception], Series]:
      def err(row: Series, e: Exception) -> Series:
        self.error_log.append(str(row), lfile)
        return None

      return err

    started_at = str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
    chunk_size = 1000
    df_all: pd.DataFrame = None

    for file in self.files:
      reader: TextFileReader = pd.read_csv(file, chunksize=chunk_size, sep=";", skiprows=0)

      for amount_chunks, chunk in enumerate(reader):
        if amount_chunks == limit:
          break

        if single_chunk_at != -1 and single_chunk_at > amount_chunks:
          print("Skipping chunks at " + str(amount_chunks))
          continue
        elif single_chunk_at != -1 and single_chunk_at < amount_chunks:
          break

        print("Read rows of " + file + " -> " + str((amount_chunks + 1) * chunk_size))

        processed = self.do_row_operations(
          chunk,
          row_operations(self, chunk),
          on_error=on_error_in_processing("errors_" + self.out_file_name + "_" + started_at + ".log")
        )

        if df_all is None:
          df_all = processed

        if store_to_file:
          header = True if amount_chunks == 0 else False
          df_all.to_csv(self.out_file_name + "_" + started_at + ".csv", sep=";", mode="a+", header=header)
          df_all = None
        else:
          df_all.append(processed)

    return df_all

  @staticmethod
  def classes(df: pd.DataFrame,skip_first_n: int = 6):
    return df.columns.values.tolist()[skip_first_n:]

  def col_names(self):
    return self._col_names

  @staticmethod
  def do_row_operations(df: pd.DataFrame, row_operations: List[RowOperation], on_error: Callable[[Series, Exception], Series] = None) -> pd.DataFrame:
    row_operations = SequencedRowOperations(row_operations, on_error)
    return df.apply(row_operations.apply, axis=1)
