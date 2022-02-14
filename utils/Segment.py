from . import Vector2

class Segment:
    def __init__(self, ffrom,  to):
        self.From = Vector2.Vector2D(ffrom.X, ffrom.Y)
        self.To = Vector2.Vector2D(to.X, to.Y)
