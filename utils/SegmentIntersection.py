import math
from . import Vector2

class SegmentIntersection:
    # Find the point of intersection between
    # the lines p1 --> p2 and p3 --> p4
    def findIntersection(p1, p2, p3, p4):  # segments parameters.
        dx12 = p2.X - p1.X
        dy12 = p2.Y - p1.Y
        dx34 = p4.X - p3.X
        dy34 = p4.Y - p3.Y

        denominator = (dy12 * dx34 - dx12 * dy34)  # Solve for t1 and t2
        if(denominator!=0):
            t1 = ((p1.X - p3.X) * dy34 + (p3.Y - p1.Y) * dx34) / denominator
            t2 = ((p3.X - p1.X) * dy12 + (p1.Y - p3.Y) * dx12) / -denominator
        else:
            return None # The lines are parallel (or close enough to it)
        
        # The segments intersect if t1 and t2 are between 0 and 1
        segments_intersect = ((t1 >= 0) and (t1 <= 1) and (t2 >= 0) and (t2 <= 1))

        # Find the point of intersection.
        if(segments_intersect):
            return Vector2.Vector2D(p1.X + dx12 * t1, p1.Y + dy12 * t1)

        return None

    # Find the point of intersection between
    # the lines p1 --> p2 and p3 --> p4.
    def _findIntersection( p1, p2, p3, p4 ):
    # out bool lines_intersect
    # out bool segments_intersect
    # out Vector2D intersection
    # out Vector2D close_p1
    # out Vector2D close_p2
    # Get the segments' parameters
        dx12 = p2.X - p1.X
        dy12 = p2.Y - p1.Y
        dx34 = p4.X - p3.X
        dy34 = p4.Y - p3.Y

        # Solve for t1 and t2
        denominator = (dy12 * dx34 - dx12 * dy34)
        if(denominator!=0):
            t1 = ((p1.X - p3.X) * dy34 + (p3.Y - p1.Y) * dx34) / denominator
        else:    # The lines are parallel (or close enough to it)
            lines_intersect = False
            segments_intersect = False
            intersection = Vector2.Vector2D(float('nan'), float('nan'))
            close_p1 = Vector2.Vector2D(float('nan'), float('nan'))
            close_p2 = Vector2.Vector2D(float('nan'), float('nan'))
            return lines_intersect, segments_intersect, intersection, close_p1, close_p2
        
        lines_intersect = True

        t2 = ((p3.X - p1.X) * dy12 + (p1.Y - p3.Y) * dx12) / -denominator

        # Find the point of intersection
        intersection = Vector2.Vector2D(p1.X + dx12 * t1, p1.Y + dy12 * t1)
        # The segments intersect if t1 and t2 are between 0 and 1
        segments_intersect = ((t1 >= 0) and (t1 <= 1) and (t2 >= 0) and (t2 <= 1))

        # Find the closest points on the segments
        if (t1 < 0):  t1 = 0
        else:
            if (t1 > 1): t1 = 1

        if (t2 < 0): t2 = 0
        else:
            if (t2 > 1): t2 = 1

        close_p1 = Vector2.Vector2D(p1.X + dx12 * t1, p1.Y + dy12 * t1)
        close_p2 = Vector2.Vector2D(p3.X + dx34 * t2, p3.Y + dy34 * t2)
        return lines_intersect, segments_intersect, intersection, close_p1, close_p2

    # Find the point of intersection between
    # the lines p1 --> p2 and p3 --> p4.
    # Находит пересечение отрезков, если точно известно, что они пересекаются
    def intersection(p1, p2, p3, p4):
        # Get the segments' parameters
        dx12 = p2.X - p1.X
        dy12 = p2.Y - p1.Y
        dx34 = p4.X - p3.X
        dy34 = p4.Y - p3.Y

        # Solve for t1 and t2
        denominator = (dy12 * dx34 - dx12 * dy34)

        t1 = ((p1.X - p3.X) * dy34 + (p3.Y - p1.Y) * dx34) / denominator

        # Find the point of intersection.
        return Vector2.Vector2D(p1.X + dx12 * t1, p1.Y + dy12 * t1)
