import math
import sys

# Coordinate manipulations
class Vector2D:
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        
        self.PI = math.pi
        self.PIby2 = self.PI / 2
        self.PIby3 = self.PI / 3
        self.PIby4 = self.PI / 4
        self.PIby6 = self.PI / 6

        self.ToRadians = self.PI / 180.0
        self.ToDegrees = 180.0 / self.PI

    def __repr__(self):
        return 'Vector2D({}, {})'.format(self.X, self.Y)

    def __str__(self):
        return '({}, {})'.format(self.X, self.Y)

    def __add__(self, other):
        return Vector2D(self.X + other.X, self.Y + other.Y)

    def __iadd__(self, other):
        self.X += other.X
        self.Y += other.Y
        return self

    def __sub__(self, other):
        return Vector2D(self.X - other.X, self.Y - other.Y)
    
    def __mul__(self, other):
        if(type(other) is float):
            return Vector2D(self.X * other, self.Y * other)
        return Vector2D(self.X * other.X, self.Y * other.Y)

    def __isub__(self, other):
        self.X -= other.X
        self.Y -= other.Y
        return self

    def __abs__(self):
        return math.hypot(self.X, self.Y)

    def __bool__(self):
        return self.X != 0 or self.Y != 0

    def __neg__(self):
        return Vector2D(-self.X, -self.Y)
    
    def InitFromAngle(self, r, angle):
        res = Vector2D(r * math.cos(angle),r * math.sin(angle))
        return res

    def Inverse(self):
        res = Vector2D(-self.X, -self.Y)
        return res

    # Complex conjugate (комплексно-сопряженный вектор)
    def Conjugate(self):
        res = Vector2D(self.X, -self.Y)
        return res

    # Determine which side of the line the 2D point is at
    # 1 if on the right hand side
    # 0 if on the line;
    # -1 if on the left hand side
    def Side(self, point):
        res = self.X * point.Y - point.X * self.Y
        if(res > sys.float_info.epsilon): 
            res = 1
            return res
        if(res < -sys.float_info.epsilon):
            res = -1
            return res
        else: 
            res = 0
            return res

    # Normal from the line to the point (the line is defined by normalized direction)
    def Normal2(normalizedDirection, point):
        cosAngle = point.X * normalizedDirection.X + point.Y * normalizedDirection.Y
        x = normalizedDirection.X * cosAngle
        y = normalizedDirection.Y * cosAngle
        return Vector2D(point.X - x, point.Y - y)

    # Normal from the line to the point
    def Normal(direction, point):
        cosAngle = (point.X * direction.X + point.Y * direction.Y) / direction.lengthSquare()
        x = direction.X * cosAngle
        y = direction.Y * cosAngle
        return Vector2D(point.X - x, point.Y - y)

    # Distance to the point
    def DistanceTo(point1, point2):
        dx = point2.X - point1.X
        dy = point2.Y - point1.Y
        return math.sqrt(dx * dx + dy * dy)

    # Angle from (-PI ; PI]
    def Angle(self):
        return math.atan2(self.Y, self.X)

    # Angle from [0 ; PI)
    def AngleBy2(self):
        a = math.atan2(self.Y, self.X)
        if(a < 0 ):
            return a + self.PI
        else:
            if(a >= self.PI ):
                return self.PI - sys.float_info.epsilon
            else:
                return a

    # Minimal degree between vectors
    def Angle2( c1, c2):
        a = c1.Angle() - c2.Angle()
        if(a > self.PI):
            a += -2 * self.PI
        else:
            if(a < -self.PI):
                a += 2 * self.PI
            else:
                a += 0
        return a

    def Length(self):
        x = self.X
        y = self.Y
        return math.sqrt(x * x + y * y)

    def LengthSquare(self):
        x = self.X
        y = self.Y
        return x * x + y * y

    def LengthManhattan(self):
        return abs(self.X) + abs(self.Y)

    def Normalized(self):
        l = self.Length()
        return Vector2D(self.X / l, self.Y / l)

    def Add(c1, c2):
        return Vector2D(c1.X + c2.X, c1.Y + c2.Y)

    def Sub(c1, c2):
        return Vector2D(c1.X - c2.X, c1.Y - c2.Y)

    def Mul(self, k):
        return Vector2D(self.X * k, self.Y * k)

    # Dot product (скалярное произведение)
    def DotScalar(x1, x2):
        return x1.X * x2.X + x1.Y * x2.Y

    # Dot product for complex numbers (скалярное произведение комплексных чисел)
    def DotComplex(x1, x2):
        return Vector2D(x1.X * x2.X - x1.Y * x2.Y, x1.Y * x2.X + x1.X * x2.Y);

    # Norma of cross product (норма векторного произведения, площадь натянутого паралелограмма)
    def DotVectorLength(x1, x2):
        return abs(x1.X * x2.Y - x1.Y * x2.X)

    # Projection on direction
    def Projection(x, normalizedDirection):
        cosAngle = x.X * normalizedDirection.X + x.Y * normalizedDirection.Y
        return Vector2D(normalizedDirection.X * cosAngle, normalizedDirection.Y * cosAngle)

    # Linear interpolation
    def Lerp(x1, x2, k):
        m = 1.0 - k
        return Vector2D(x1.X * m + x2.X * k, x1.Y * m + x2.Y * k)

    # Linear interpolation
    def LerpTrim(x1, x2, k):
        if(k < 0): k = 0.0
        if(k > 1): k = 1.0
        return Lerp(x1, x2, k)

    def CosAngle(self):
        return self.X / self.length()

    # Cos of angle betwwen this and other vector
    def CosAngle(x1, x2):
        return (x1.X * x2.X + x1.Y * x2.Y) / x1.length() / x2.length()

    def Rotate(self, cosAngle, sinAngle):
        return Vector2D(cosAngle * self.X - sinAngle * self.Y, sinAngle * self.X + cosAngle * self.Y)

    def Rotate90(self):
        return Vector2D(-self.Y, self.X)

    def RotateAngle(self, angle):
        cosAngle = math.cos(angle)
        sinAngle = math.sin(angle)
        return Vector2D(cosAngle * self.X - sinAngle * self.Y, sinAngle * self.X + cosAngle * self.Y)

    def RotateCenter(self, angle, center):
        cosAngle = math.cos(angle)
        sinAngle = math.sin(angle)

        xx = self.X - center.X
        yy = self.Y - center.Y

        return Vector2D(cosAngle * xx - sinAngle * yy + center.X, sinAngle * xx + cosAngle * yy + center.Y)
    
    def toVector2(p):
        return Vector2D(p.X, p.Y)

    # Find the point of intersection between
    # the lines p1 --> p2 and p3 --> p4.
    # Находит пересечение отрезков, если точно известно, что они пересекаются
    def segmentIntersection(p1, p2, p3, p4):
    # Get the segments' parameters.
        dx12 = p2.X - p1.X
        dy12 = p2.Y - p1.Y
        dx34 = p4.X - p3.X
        dy34 = p4.Y - p3.Y

        # Solve for t1 and t2
        denominator = (dy12 * dx34 - dx12 * dy34)

        t1 = ((p1.X - p3.X) * dy34 + (p3.Y - p1.Y) * dx34) / denominator
        t2 = ((p3.X - p1.X) * dy12 + (p1.Y - p3.Y) * dx12) / -denominator

        # Find the point of intersection.
        return Vector2D(p1.X + dx12 * t1, p1.Y + dy12 * t1)

    # Точка пересечения между двумя прямыми, заднными направляющей и точкой
    def intersection(dir1, point1, dir2, point2):
        x2 = point1.X
        y2 = point1.Y
        x1 = point1.X + dir1.X
        y1 = point1.Y + dir1.Y

        a2 = point2.X
        b2 = point2.Y
        a1 = point2.X + dir2.X
        b1 = point2.Y + dir2.Y

        c = (b2 - b1) / (a2 - a1 + 0.00001)
        z = (y2 - y1) / (x2 - x1 + 0.00001)

        x = (c * x2 - y2 - z * a2 + b2) / (c - z)
        y = c * x - c * x2 + y2

        return Vector2D(x, y)

    def intersection2(dir1, point1, dir2, point2):
        x0 = point1.X
        p = dir1.X
        y0 = point1.Y
        q = dir1.Y

        x1 = point2.X
        p1 = dir2.X
        y1 = point2.Y
        q1 = dir2.Y

        x = (x0 * q * p1 - x1 * q1 * p - y0 * p * p1 + y1 * p * p1) / (q * p1 - q1 * p)
        y = (y0 * p * q1 - y1 * p1 * q - x0 * q * q1 + x1 * q * q1) / (p * q1 - p1 * q)

        return Vector2D(x, y)

# his is essentially the same as Lerp but instead the function will ensure that the speed never exceeds maxDistanceDelta. 
# Negative values of maxDistanceDelta pushes the vector away from target.
    def moveTowards(current, target, maxDistanceDelta):
        _dir = target - current
        magnitude = _dir.Length()
        if (magnitude <= maxDistanceDelta or magnitude <= sys.float_info.epsilon):
            return target
        return current + (_dir * (maxDistanceDelta / magnitude))

  # Distance square to the point
    def distanceSquareTo(point1, point2):
        dx = point2.X - point1.X
        dy = point2.Y - point1.Y
        return dx * dx + dy * dy
