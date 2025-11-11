import numpy as np
from point import Point
from polygon import Polygon

class Polyhedron:
    def __init__(self, vertices, faces_indices):
        """
        vertices: список объектов Point
        faces_indices: список списков индексов вершин, образующих грани
        """
        self.vertices = vertices
        self.faces = []
        self.center = Point(0, 0, 0)
        
        # Создание граней на основе индексов
        for face_indices in faces_indices:
            face_points = [self.vertices[i].copy() for i in face_indices]
            self.faces.append(Polygon(face_points))
        
        self.calculate_center()
    
    def calculate_center(self):
        """Вычисление геометрического центра многогранника"""
        if not self.vertices:
            return
        
        sum_x = sum(p.x for p in self.vertices)
        sum_y = sum(p.y for p in self.vertices)
        sum_z = sum(p.z for p in self.vertices)
        
        n = len(self.vertices)
        self.center = Point(sum_x / n, sum_y / n, sum_z / n)
    
    def apply_transform(self, matrix):
        """Применение матрицы преобразования ко всем вершинам"""
        for vertex in self.vertices:
            vertex.transform(matrix)
        
        # Обновляем грани (каждая грань содержит копии вершин)
        for face in self.faces:
            for point in face.points:
                point.transform(matrix)
        
        # Пересчитываем центр
        self.calculate_center()
    
    @classmethod
    def create_tetrahedron(cls):
        """Создание тетраэдра (4 вершины, 4 треугольные грани)"""
        vertices = [
            Point(1, 1, 1),
            Point(1, -1, -1),
            Point(-1, 1, -1),
            Point(-1, -1, 1)
        ]
        
        # Грани тетраэдра
        faces_indices = [
            [0, 1, 2],
            [0, 2, 3],
            [0, 3, 1],
            [1, 3, 2]
        ]
        
        return cls(vertices, faces_indices)
    
    @classmethod
    def create_hexahedron(cls):
        """Создание гексаэдра (куба) - 8 вершин, 6 квадратных граней"""
        vertices = []
        for x in [-1, 1]:
            for y in [-1, 1]:
                for z in [-1, 1]:
                    vertices.append(Point(x, y, z))
        
        # Грани куба
        faces_indices = [
            [0, 1, 3, 2],  # нижняя
            [4, 5, 7, 6],  # верхняя
            [0, 1, 5, 4],  # передняя
            [2, 3, 7, 6],  # задняя
            [0, 2, 6, 4],  # левая
            [1, 3, 7, 5]   # правая
        ]
        
        return cls(vertices, faces_indices)
    
    @classmethod
    def create_octahedron(cls):
        """Создание октаэдра (6 вершин, 8 треугольных граней)"""
        vertices = [
            Point(1, 0, 0),
            Point(-1, 0, 0),
            Point(0, 1, 0),
            Point(0, -1, 0),
            Point(0, 0, 1),
            Point(0, 0, -1)
        ]
        
        # Грани октаэдра
        faces_indices = [
            [0, 2, 4], [0, 4, 3], [0, 3, 5], [0, 5, 2],
            [1, 2, 5], [1, 5, 3], [1, 3, 4], [1, 4, 2]
        ]
        
        return cls(vertices, faces_indices)
    
    @classmethod
    def create_icosahedron(cls):
        """Создание икосаэдра (12 вершин, 20 треугольных граней)"""
        # Более простой и надежный метод
        t = (1.0 + np.sqrt(5.0)) / 2.0
        
        # Вершины икосаэдра
        vertices = [
            Point(-1,  t,  0),
            Point( 1,  t,  0),
            Point(-1, -t,  0),
            Point( 1, -t,  0),
            Point( 0, -1,  t),
            Point( 0,  1,  t),
            Point( 0, -1, -t),
            Point( 0,  1, -t),
            Point( t,  0, -1),
            Point( t,  0,  1),
            Point(-t,  0, -1),
            Point(-t,  0,  1)
        ]
        
        # Нормализация
        for v in vertices:
            length = np.sqrt(v.x**2 + v.y**2 + v.z**2)
            v.x /= length
            v.y /= length
            v.z /= length
        
        # Грани икосаэдра
        faces_indices = [
            [0, 11, 5],
            [0, 5, 1],
            [0, 1, 7],
            [0, 7, 10],
            [0, 10, 11],
            [1, 5, 9],
            [5, 11, 4],
            [11, 10, 2],
            [10, 7, 6],
            [7, 1, 8],
            [3, 9, 4],
            [3, 4, 2],
            [3, 2, 6],
            [3, 6, 8],
            [3, 8, 9],
            [4, 9, 5],
            [2, 4, 11],
            [6, 2, 10],
            [8, 6, 7],
            [9, 8, 1]
        ]
        
        return cls(vertices, faces_indices)
    
    @classmethod
    def create_dodecahedron(cls):
        """Создание додекаэдра (20 вершин, 12 пятиугольных граней)"""
        # Явное задание координат вершин додекаэдра
        phi = (1 + np.sqrt(5)) / 2  # золотое сечение
        
        # Вершины додекаэдра
        vertices = [
            # (±1, ±1, ±1)
            Point(1, 1, 1), Point(1, 1, -1), Point(1, -1, 1), Point(1, -1, -1),
            Point(-1, 1, 1), Point(-1, 1, -1), Point(-1, -1, 1), Point(-1, -1, -1),
            
            # (0, ±1/φ, ±φ)
            Point(0, 1/phi, phi), Point(0, 1/phi, -phi),
            Point(0, -1/phi, phi), Point(0, -1/phi, -phi),
            
            # (±1/φ, ±φ, 0)
            Point(1/phi, phi, 0), Point(1/phi, -phi, 0),
            Point(-1/phi, phi, 0), Point(-1/phi, -phi, 0),
            
            # (±φ, 0, ±1/φ)
            Point(phi, 0, 1/phi), Point(phi, 0, -1/phi),
            Point(-phi, 0, 1/phi), Point(-phi, 0, -1/phi)
        ]
        
        # Нормализация вершин к единичной сфере
        for v in vertices:
            length = np.sqrt(v.x**2 + v.y**2 + v.z**2)
            v.x /= length
            v.y /= length
            v.z /= length
        
        # Грани додекаэдра - 12 пятиугольников
        faces_indices = [
            # Верхний пятиугольник
            [8, 16, 0, 12, 4],
            # Нижний пятиугольник  
            [11, 19, 7, 15, 3],
            # Передние пятиугольники
            [0, 16, 2, 13, 1],
            [4, 12, 6, 14, 5],
            # Задние пятиугольники
            [8, 10, 2, 17, 9],
            [18, 6, 14, 7, 19],
            # Боковые пятиугольники
            [0, 1, 9, 5, 4],
            [2, 10, 11, 3, 13],
            [16, 8, 18, 19, 17],
            [12, 0, 4, 5, 14],
            [1, 13, 3, 15, 7],
            [10, 8, 4, 6, 18]
        ]
        
        return cls(vertices, faces_indices)
    
    def get_vertex_list(self):
        """Возвращает список вершин в удобном формате"""
        return [(v.x, v.y, v.z) for v in self.vertices]
    
    def get_face_vertex_indices(self):
        """Возвращает индексы вершин для каждой грани"""
        return [list(range(len(face.points))) for face in self.faces]
    
    def __repr__(self):
        return f"Polyhedron({len(self.vertices)} vertices, {len(self.faces)} faces)"