from utils.Vector2 import Vector2D
from utils.Segment import Segment

# Point of Track
class PathP:
    def __init__(self):
        self.Point = Vector2D(0.0,0.0) # position in 2D space
        self.Width = 0.0 # width of road (m)
        self.Prev = None # previous Point
        self.Next = None # next Point
        self.DistanceFromStart = 0.0 # distance from start to this point along track (m)
        self.LeftWall = Segment(Vector2D(0.0,0.0), Vector2D(0.0,0.0)) # segment of left wall
        self.RightWall = Segment(Vector2D(0.0,0.0), Vector2D(0.0,0.0)) # segment of right wall
        self.Normal = Vector2D(0.0,0.0) # normal to direction of road
        self.Dir = Vector2D(0.0,0.0) # direction of road
        self.Length = 0.0 # length of this part of track (m)
        self.ControlPoint = CControlPoint(0.0,0.0)
        self.r2 = 0.0
        
    def ContainsPoint(self, p):
        if(self.Normal.Side(p.Sub(self.Point)) <= 0):
            return True
        else:
            return False

# Контрольная точка
class CControlPoint:
    def __init__(self, point = Vector2D(0,0), width = 0.0):
        self.Point = point
        self.Width = width
        self.Temp = True
