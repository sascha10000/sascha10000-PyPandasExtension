import os
from typing import List, Dict, Tuple


class FileFinder:
  def __init__(self, folder: str):
    self.folder = folder
    self.file_list: dict = {}

  @staticmethod
  def build(folder: str, file_list: dict) -> 'FileFinder':
    new_instance = FileFinder(folder)
    new_instance.file_list = file_list
    return new_instance

  def get_files(self) -> 'FileFinder':
    if not os.path.exists(self.folder):
      raise Exception("Folder " + self.folder + " does not exist! Absolute (" + os.path.abspath(self.folder) + ")")

    file_list = {}

    for root, dirs, files in os.walk(self.folder, topdown=False):
      for name in files:
        if file_list.get(root, None) is None:
          file_list[root] = []

        file_list[root].append(name)

    return FileFinder.build(self.folder, file_list)

  def filter(self, startsWith: str = "", endsWith: str = ".csv") -> Dict[str, List[str]]:
    filtered_list = {}
    for folder in self.file_list:
      for file in self.file_list[folder]:
        if file.endswith(endsWith) and file.startswith(startsWith):
          if filtered_list.get(folder, None) is None:
            filtered_list[folder] = []
          filtered_list[folder].append(str(os.path.join(folder, file)))

    return filtered_list
