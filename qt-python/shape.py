from PySide6.QtCore import QPoint, QRect

class Shape:
    def __init__(self, shape_type, points=None, params=None):
        self.shape_type = shape_type  # "line", "rectangle", "circle"
        self.points = points or []
        self.params = params or {}
        self.selected = False
        self.moving = False
        self.resizing = False
        self.resize_handle = None

    def to_dict(self):
        return {
            'shape_type': self.shape_type,
            'points': [(p.x(), p.y()) for p in self.points],
            'params': self.params
        }

    @classmethod
    def from_dict(cls, data):
        shape = cls(data['shape_type'])
        shape.points = [QPoint(x, y) for x, y in data['points']]
        shape.params = data['params']
        return shape

    def contains_point(self, point):
        if self.shape_type == "line":
            # Sprawdzanie czy punkt jest blisko linii
            if len(self.points) >= 2:
                p1, p2 = self.points[0], self.points[1]
                return self.point_line_distance(point, p1, p2) < 5
        elif self.shape_type == "rectangle":
            if len(self.points) >= 2:
                rect = self.get_rect()
                return rect.contains(point)
        elif self.shape_type == "circle":
            if len(self.points) >= 2:
                center = self.points[0]
                radius = self.calculate_radius()
                distance = ((point.x() - center.x()) ** 2 + (point.y() - center.y()) ** 2) ** 0.5
                return abs(distance - radius) < 5
        return False

    def point_line_distance(self, point, line_start, line_end):
        # Obliczanie odległości punktu od linii
        numerator = abs((line_end.y() - line_start.y()) * point.x() - 
                       (line_end.x() - line_start.x()) * point.y() + 
                       line_end.x() * line_start.y() - 
                       line_end.y() * line_start.x())
        denominator = ((line_end.y() - line_start.y()) ** 2 + 
                      (line_end.x() - line_start.x()) ** 2) ** 0.5
        return numerator / denominator if denominator != 0 else 0

    def get_rect(self):
        if len(self.points) >= 2:
            x1, y1 = self.points[0].x(), self.points[0].y()
            x2, y2 = self.points[1].x(), self.points[1].y()
            return QRect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        return QRect()

    def calculate_radius(self):
        if len(self.points) >= 2:
            dx = self.points[1].x() - self.points[0].x()
            dy = self.points[1].y() - self.points[0].y()
            return (dx * dx + dy * dy) ** 0.5
        return 0

    def get_resize_handles(self):
        handles = []
        if self.shape_type == "rectangle":
            rect = self.get_rect()
            handles = [
                QPoint(rect.left(), rect.top()),
                QPoint(rect.right(), rect.top()),
                QPoint(rect.left(), rect.bottom()),
                QPoint(rect.right(), rect.bottom())
            ]
        elif self.shape_type == "circle":
            if len(self.points) >= 2:
                handles = [self.points[1]]
        return handles