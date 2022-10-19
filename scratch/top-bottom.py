

class top:
  def __init__(self):
    print("I'm the boss")
    top.x = "Je suis au top"


class bottom(top):
  def __init__(self):
    super().__init__()
    print("I'm the slave")
    print(self.x)

  def __str__(self):
    return "Top value is : " + str(self.x)



x = bottom()
print(x)
