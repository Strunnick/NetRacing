import math

class Vector2:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __repr__(self):
        return 'Vector2({}, {})'.format(self.X, self.Y)

    def __str__(self):
        return '({}, {})'.format(self.X, self.Y)

    def __add__(self, other):
        return Vector2(self.X + other.X, self.Y + other.Y)

    def __iadd__(self, other):
        self.X += other.X
        self.Y += other.Y
        return self

    def __sub__(self, other):
        return Vector2(self.X - other.X, self.Y - other.Y)
    
    def __mul__(self, other):
        if(type(other) is float):
            return Vector2(self.X * other, self.Y * other)
        return Vector2(self.X * other.X, self.Y * other.Y)

    def __isub__(self, other):
        self.X -= other.X
        self.Y -= other.Y
        return self

    def __abs__(self):
        return math.hypot(self.X, self.Y)

    def __bool__(self):
        return self.X != 0 or self.Y != 0

    def __neg__(self):
        return Vector2(-self.X, -self.Y)
    #def length(self):
        #return math.sqrt(X * X + Y * Y)
    #def lengthSquare(self):
        #return X * X + Y * Y