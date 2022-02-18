from Carbase import CarBase
from Track import Track, CControlPoint
from PathPoint import PathP

# Car intended to moving on Track
class Car(CarBase):

    def __init__(self, index):
        CarBase.__init__(self)
        self.Index = index
        self.Penalty = 0.0
        self.maxDistFromStart = 0.0
        self.Index = 0
        self.CapturedPoint = PathP()
        self.TotalCapturedLength = 0.0
        self.PosOnSegment = 0.0 # пройденный путь внутри текущего сегмента
        self.TotalPassedLength = self.GetPassLength() # общее пройденное расстояние
        self.IsAlive = True
        self.IsOutOfTrack = False
        self.IsOnGround = True
        
        self.steeringdump = 0
        
    def GetPassLength(self): 
        return self.TotalCapturedLength + self.PosOnSegment

    def Update(self, track, throttle, steering, breaks, dt):
        if (not self.IsAlive): return
        if (self.IsOutOfTrack):
            self.Pos = self.CapturedPoint.Point
            self.Velocity *= 0.1
            self.LookAt = self.CapturedPoint.Dir.Normalized()
            self.IsOutOfTrack = False

        self.FindNextCapturedPoint(track)
        # update passed length
        self.TotalPassedLength = self.TotalCapturedLength + self.PosOnSegment
        
        super().Update(throttle, steering, breaks, dt)

    def Reset(self, track, placeByIndex):
        if (placeByIndex):
            pp = PathP()
            p = track.PathPosToPoint(-self.Index * 5, pp)
            self.LookAt = pp.Dir.Normalized()
            if(self.Index % 2 == 0 ):
                self.Pos = p + self.LookAt.Rotate90() * 2 * 1
            else: 
                self.Pos = p + self.LookAt.Rotate90() * 2 * -1
            self.CapturedPoint = pp
        else:
            self.Pos = track.Points[0].Point
            self.LookAt = track.Points[0].Dir.Normalized()
            self.CapturedPoint = track.Points[0]

        self.TotalCapturedLength = 0
        self.Adhesion = track.Adhesion

        self.IsAlive = True
        self.IsOutOfTrack = False
        self.IsOnGround = True
        self.Penalty = 0

    def FindNextCapturedPoint(self, track):
        # check side
        if (self.CapturedPoint.Next.ContainsPoint(self.Pos)):
            if (self.CapturedPoint.Next.Point.distanceSquareTo(self.Pos) <= self.CapturedPoint.Next.r2):
                dist = track.DistanceBetweenPoints(self.CapturedPoint, self.CapturedPoint.Next)
                # we captured next checkpoint
                self.CapturedPoint = self.CapturedPoint.Next
                self.TotalCapturedLength += dist
                self.PosOnSegment = 0

        # check out of track
        d = self.CapturedPoint.Dir * (1 / self.CapturedPoint.Length)
        p = self.Pos - self.CapturedPoint.Point
        proj = p.Projection(d)
        onSegment = False
        if(proj.DotScalar(d) >= 0): 
            onSegment = True
        if (onSegment):
            l = proj.Length()
            self.PosOnSegment = l
            if (l > self.CapturedPoint.Length):
                    onSegment = False
            l = proj.distanceSquareTo(p)
            if (l > self.CapturedPoint.r2):
                onSegment = False

        if (not onSegment):
            if (self.CapturedPoint.Point.distanceSquareTo(self.Pos) <= self.CapturedPoint.r2 or
                self.CapturedPoint.Next.Point.distanceSquareTo(self.Pos) <= self.CapturedPoint.Next.r2):
                onSegment = True

        self.IsOutOfTrack = not onSegment