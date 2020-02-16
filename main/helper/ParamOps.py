import sys
def find_param_value(param_name: str, exists = False):
  cnt = 0

  for v in sys.argv:
    if v == param_name:
      return sys.argv[cnt if exists else cnt + 1]
    cnt += 1

  return None

def find_param(param_name: str) -> bool:
  return True if find_param_value(param_name, True) is not None else False
