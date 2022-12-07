
import os
import glob
import sys

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__)+"/*.py")]

smOld  = []
smGood = []
smBad  = []
smMods = {}

for m in all__:
  if m in smOld:
    continue
  if m != "__init__":
    try:
      mod = __import__(m, locals(), globals())
      d = mod.__dict__
      for k in d.keys():
        globals()[k] = d[k]
      smGood.append(m)
      smMods[m] = True
    except:
      print(" Error loading Smil submodule : ", m)
      smBad.append(m)
      smMods[m] = False
      pass
