
import os
import glob
import sys

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

_all = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__)+"/*.py")]

for m in _all:
  if m == "__init__":
    continue
  try:
    mod = __import__(m, locals(), globals())
    d = mod.__dict__
    for k in d.keys():
      globals()[k] = d[k]
  except Exception as e:
    print(" Error loading Smil submodule : ", m, e)

del _all, m, d, mod, k

__version__ = "0.3.3"

