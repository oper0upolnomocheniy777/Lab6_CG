import numpy as np

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def to_homogeneous(self):
        """Преобразование в однородные координаты"""
        return np.array([self.x, self.y, self.z, 1.0])
    
    def from_homogeneous(self, homogeneous):
        """Преобразование из однородных координаты"""
        self.x = homogeneous[0] / homogeneous[3]
        self.y = homogeneous[1] / homogeneous[3]
        self.z = homogeneous[2] / homogeneous[3]
    
    def transform(self, matrix):
        """Применение матрицы преобразования 4x4 к точке"""
        homogeneous = self.to_homogeneous()
        transformed = matrix @ homogeneous  # Умножение матрицы на вектор
        self.from_homogeneous(transformed)
    
    def __repr__(self):
        return f"Point({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"
    
    def copy(self):
        """Создание копии точки"""
        return Point(self.x, self.y, self.z)