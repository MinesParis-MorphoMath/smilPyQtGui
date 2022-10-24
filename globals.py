

images = {}

def register(uuid=None, view = None):
  if uuid is None:
    return
  images[uuid] = view

def unregister(uuid = None):
  if uuid is None:
    return
  if uuid in images:
    del images[uuid]
  else:
    print("uuid not in list")

def list():
  for k in images:
    print(k, images[k].imName)
