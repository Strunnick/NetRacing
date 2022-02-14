from utils.Vector2 import Vector2D
from utils.SegmentIntersection import SegmentIntersection
from utils.Segment import Segment

# Provides methods to calculate intersections of sensor rays with segments of wall
class Sensors:
    def __init__(self):
        self.Rays = [i for i in range(0,5)]
        v = Vector2D(100, 0)
        self.Rays[0] = v.RotateAngle(-70 * v.ToRadians)
        self.Rays[1] = v.RotateAngle(-30 * v.ToRadians)
        self.Rays[2] = v.RotateAngle(+ 0 * v.ToRadians).Mul(1.2)
        self.Rays[3] = v.RotateAngle(+30 * v.ToRadians)
        self.Rays[4] = v.RotateAngle(+70 * v.ToRadians)

        self.segments = []

    def GetDistances(self, car, track, sensors, startIndex=0):
        # get segments of walls
        self.segments.clear()
        p = car.CapturedPoint
        self.segments.append(p.LeftWall)
        self.segments.append(p.RightWall)
        while (track.DistanceBetweenPoints(car.CapturedPoint, p) <= 130):
            p = p.Next
            self.segments.append(p.LeftWall)
            self.segments.append(p.RightWall)
        # enumarate sensors of car
        angle = car.LookAt.Angle()
        for i in range( len(self.Rays)):
            p = self.Rays[i]
            p = p.RotateAngle(angle) # rotate sensor by car orientation
            ray = Segment(car.Pos, car.Pos + p)
            sensors[startIndex + i] = self.GetDistance(ray, self.segments) # calc distance to nearest wall segment
        return sensors

    def GetDistance(self, seg, segments):
        minDist = seg.From.DistanceTo(seg.To)

        for i in range(len(self.segments)):
            s = self.segments[i]
            p = SegmentIntersection.findIntersection(seg.From, seg.To, s.From, s.To)
            if (p != None):
                dist = p.DistanceTo(seg.From)
                if (dist < minDist):
                    minDist = dist
                return minDist
        return minDist
