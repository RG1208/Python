class TwoDVector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def show(self):
        print(f"2D Vector Coordinates: ({self.x}i, {self.y}j)")

class ThreeDVector(TwoDVector):
    def __init__(self, x, y, z):
        super().__init__(x, y)
        self.z = z

    def show(self):
        print(f"3D Vector Coordinates: ({self.x}i, {self.y}j, {self.z}k)")

vector2d = TwoDVector(3, 4)
vector2d.show() 
vector3d = ThreeDVector(3, 4, 5)
vector3d.show()