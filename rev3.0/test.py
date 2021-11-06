
class I:
    def __init__(self, z):
        self.x = 2
        self.y = 4
        self.z = z
        self.f()
    def f(self):
        self.k = 8


i = I(6)

print(i.x, i.y, i.z, i.k)

