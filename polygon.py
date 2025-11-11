class Polygon:
    def __init__(self, points):
        self.points = points  # Список объектов Point
    
    def __repr__(self):
        return f"Polygon with {len(self.points)} points"
    
    def copy(self):
        """Создание копии многоугольника"""
        return Polygon([p.copy() for p in self.points])