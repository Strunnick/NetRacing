from PathPoint import PathP
from utils.Vector2 import Vector2D
from utils.Segment import Segment
import math, sys

# Track 
class Track:
    def __init__(self):
        self.ControlPoints = []
        self.Points = []
        self.Length = 0.0
        self.Adhesion = 1.0

    def DistanceBetweenPoints(self, p1, p2):
        d = abs(p2.DistanceFromStart - p1.DistanceFromStart)
        return min(d, abs(d - self.Length))

    def Prepare(self):
        p_count = len(self.Points)
        #calc prev/next
        for i in range(p_count):
            self.Points[i].Next = self.Points[(i + 1) % p_count]
            self.Points[i].Prev = self.Points[(i - 1 + p_count) % p_count]

        cpIndex = 0
        prevI = 0
        for i in range(p_count):
            if (cpIndex < len(self.ControlPoints) - 1):
                if (self.ControlPoints[cpIndex + 1].Point.distanceSquareTo(self.Points[i].Point) < 0.001):
                    cpIndex += 1
            self.Points[i].ControlPoint = self.ControlPoints[cpIndex]

        #calc
        self.Length = 0.0
        for i in range(p_count):
            p = self.Points[i]
            p.Dir = p.Next.Point.Sub(p.Point)
            p.Length = p.Dir.Length()
            p.Normal = p.Dir.Normalized().Rotate90()
            p.DistanceFromStart = self.Length
            self.Length += p.Length

        # calc width
        for i in range(p_count):
            self.CalcWidth(self.Points[i])

        # calc walls
        for i in range(p_count):
            p = self.Points[i]
            _next = p.Next

            # right
            p1 = p.Point.Add(p.Normal.Mul(p.Width / 2))
            p2 = _next.Point.Add(_next.Normal.Mul(_next.Width / 2))
            p.RightWall = Segment(p1, p2)

            # left
            p1 = p.Point.Add(p.Normal.Mul(-p.Width / 2))
            p2 = _next.Point.Add(_next.Normal.Mul(-_next.Width / 2))
            p.LeftWall = Segment(p1, p2)


    def CalcWidth(self, p):
        if (len(self.ControlPoints) < 3):
            p.Width = p.ControlPoint.Width
        else:
            myCP = p.ControlPoint
            _next = p
            while (_next.ControlPoint == myCP):
                _next = _next.Next
            prev = p
            while (prev.ControlPoint == myCP):
                prev = prev.Prev
            first = prev.Next
            firstDist = first.DistanceFromStart
            if (firstDist > p.DistanceFromStart):
                firstDist -= self.Length
            nextDist = _next.DistanceFromStart
            if (nextDist < p.DistanceFromStart):
                nextDist += self.Length
            k = (p.DistanceFromStart - firstDist) / (nextDist - firstDist)
            p.Width = p.ControlPoint.Width * (1 - k) + _next.ControlPoint.Width * k

            p.r2 = (p.Width / 2) * (p.Width / 2)

    def FindPathPointForPoint(self, p):
        bestDist = sys.float_info.max
        res = None
        for pp in self.Points:
            if (pp.ContainsPoint(p)):
                d = pp.Point.DistanceTo(p)
                if (d < bestDist):
                    bestDist = d
                    res = pp
        return res

    def PathPosToPoint(self, trackPos, pp):
        while (trackPos < 0):
                trackPos += Length;

        for p in self.Points:
            if (trackPos <= p.DistanceFromStart + p.Length):
                pp = p
                d = (trackPos - p.DistanceFromStart) / p.Length
                return p.Point + p.Dir * d
        pp = self.Points[0]
        return pp.Point
    
    def Load(self, file):
        f = open(file, 'r')
        l = [line.strip() for line in f]
        # первая строка - Длина трека
        self.Length = float(l[0])
        # Далее - размер массива контрольных точек
        lengt = int(l[1])
        i = 0
        for i in range(1, lengt+1):
        
            x, y, width, temp = l[ 1 + i ].split()  # отсчёт с третьей строки
            CP = CControlPoint( Vector2D(float(x), float(y)), int(width) )
            CP.Temp = bool(temp)
            self.ControlPoints.append(CP)
            
        # Далее - до конца файла - точки сегментов стен
        for n in range( i+2 , len(l) ):

            x, y, width = l[ n ].split()  # отсчёт с третьей строки
            p = PathP()
            p.Point.X = float(x)
            p.Point.Y = float(y)
            p.Width = int(width) # float - может быть округлён!
            self.Points.append(p)
        
        f.close()
        
    def Save(self, file):
        with open(file, "w") as f:
            print(self.Length, file = f)
            print(len(self.ControlPoints), file = f)
            for p in self.ControlPoints:
                print(str(p), file = f)
            for n in self.Points:
                print(str(n), file = f)
            f.close()
            
# Контрольная точка
class CControlPoint:
    def __init__(self, point = Vector2D(0.0,0.0), width = 0.0):
        self.Point = point
        self.Width = width
        self.Temp = True
    
    def __str__(self):
        return "{} {} {} {}".format(self.Point.X, self.Point.Y, self.Width, self.Temp)