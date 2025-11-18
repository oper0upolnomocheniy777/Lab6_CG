import numpy as np
from point import Point

def translation_matrix(dx, dy, dz):
    """Матрица смещения"""
    return np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ], dtype=float)

def scaling_matrix(sx, sy, sz):
    """Матрица масштабирования"""
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ], dtype=float)

def rotation_x_matrix(angle_degrees):
    """Матрица поворота вокруг оси X (угол в градусах)"""
    angle = np.radians(angle_degrees)
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)
    
    return np.array([
        [1, 0, 0, 0],
        [0, cos_a, -sin_a, 0],
        [0, sin_a, cos_a, 0],
        [0, 0, 0, 1]
    ], dtype=float)

def rotation_y_matrix(angle_degrees):
    """Матрица поворота вокруг оси Y (угол в градусах)"""
    angle = np.radians(angle_degrees)
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)
    
    return np.array([
        [cos_a, 0, sin_a, 0],
        [0, 1, 0, 0],
        [-sin_a, 0, cos_a, 0],
        [0, 0, 0, 1]
    ], dtype=float)

def rotation_z_matrix(angle_degrees):
    """Матрица поворота вокруг оси Z (угол в градусах)"""
    angle = np.radians(angle_degrees)
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)
    
    return np.array([
        [cos_a, -sin_a, 0, 0],
        [sin_a, cos_a, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=float)

def reflection_matrix(plane):
    """Матрица отражения относительно координатной плоскости"""
    if plane == 'XY':
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, -1, 0],
            [0, 0, 0, 1]
        ], dtype=float)
    elif plane == 'XZ':
        return np.array([
            [1, 0, 0, 0],
            [0, -1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=float)
    elif plane == 'YZ':
        return np.array([
            [-1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=float)
    else:
        raise ValueError("Plane must be 'XY', 'XZ', or 'YZ'")
    

    
    # === Новые преобразования (участник 2) ===

def scaling_around_point_matrix(point, sx, sy, sz):
    """Матрица масштабирования относительно произвольной точки"""
    # 1. Смещаем точку в начало координат
    # 2. Масштабируем
    # 3. Возвращаем обратно
    translate_to_origin = translation_matrix(-point.x, -point.y, -point.z)
    scale = scaling_matrix(sx, sy, sz)
    translate_back = translation_matrix(point.x, point.y, point.z)
    
    return translate_back @ scale @ translate_to_origin

def scaling_around_center_matrix(polyhedron, sx, sy, sz):
    """Матрица масштабирования относительно центра многогранника"""
    return scaling_around_point_matrix(polyhedron.center, sx, sy, sz)

def rotation_around_axis_matrix(axis_point1, axis_point2, angle_degrees):
    """
    Матрица поворота вокруг произвольной прямой (по двум точкам)
    
    Args:
        axis_point1: Point - первая точка на оси
        axis_point2: Point - вторая точка на оси  
        angle_degrees: float - угол поворота в градусах
    """
    # Вектор направления оси
    u = axis_point2.x - axis_point1.x
    v = axis_point2.y - axis_point1.y
    w = axis_point2.z - axis_point1.z
    
    # Нормализуем вектор направления
    length = np.sqrt(u*u + v*v + w*w)
    if length == 0:
        raise ValueError("Axis points must be different")
    
    u /= length
    v /= length
    w /= length
    
    # Угол поворота в радианах
    angle = np.radians(angle_degrees)
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)
    
    # Матрица поворота вокруг произвольной оси (формула Родригеса)
    rotation = np.array([
        [cos_a + u*u*(1-cos_a),     u*v*(1-cos_a) - w*sin_a, u*w*(1-cos_a) + v*sin_a, 0],
        [u*v*(1-cos_a) + w*sin_a,   cos_a + v*v*(1-cos_a),   v*w*(1-cos_a) - u*sin_a, 0],
        [u*w*(1-cos_a) - v*sin_a,   v*w*(1-cos_a) + u*sin_a, cos_a + w*w*(1-cos_a),   0],
        [0, 0, 0, 1]
    ], dtype=float)
    
    # Комбинируем с переносами
    translate_to_origin = translation_matrix(-axis_point1.x, -axis_point1.y, -axis_point1.z)
    translate_back = translation_matrix(axis_point1.x, axis_point1.y, axis_point1.z)
    
    return translate_back @ rotation @ translate_to_origin

def rotation_around_center_axis_matrix(polyhedron, axis, angle_degrees):
    """
    Вращение вокруг прямой через центр многогранника, параллельной координатной оси
    
    Args:
        polyhedron: Polyhedron - многогранник
        axis: str - ось ('X', 'Y', или 'Z')
        angle_degrees: float - угол поворота в градусах
    """
    center = polyhedron.center
    
    # Создаем две точки на оси, проходящей через центр и параллельной выбранной оси
    if axis == 'X':
        axis_point1 = Point(center.x, center.y, center.z)
        axis_point2 = Point(center.x + 1, center.y, center.z)
    elif axis == 'Y':
        axis_point1 = Point(center.x, center.y, center.z)
        axis_point2 = Point(center.x, center.y + 1, center.z)
    elif axis == 'Z':
        axis_point1 = Point(center.x, center.y, center.z)
        axis_point2 = Point(center.x, center.y, center.z + 1)
    else:
        raise ValueError("Axis must be 'X', 'Y', or 'Z'")
    
    return rotation_around_axis_matrix(axis_point1, axis_point2, angle_degrees)

def identity_matrix():
    """Единичная матрица (без преобразования)"""
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=float)

def composite_transform(*matrices):
    """Композиция нескольких матричных преобразований"""
    if not matrices:
        return identity_matrix()
    
    result = matrices[0]
    for matrix in matrices[1:]:
        result = result @ matrix  # Умножение матриц
    
    return result

def get_center(points):
    """Вычисление центра точек"""
    if not points:
        return Point(0, 0, 0)
    
    sum_x = sum(p.x for p in points)
    sum_y = sum(p.y for p in points)
    sum_z = sum(p.z for p in points)
    
    n = len(points)
    return Point(sum_x / n, sum_y / n, sum_z / n)

def create_coordinate_system():
    """Создание координатной системы для отладки"""
    vertices = [
        Point(0, 0, 0),  # Начало
        Point(2, 0, 0),  # Ось X
        Point(0, 2, 0),  # Ось Y
        Point(0, 0, 2)   # Ось Z
    ]
    
    faces_indices = [
        [0, 1],  # Ось X
        [0, 2],  # Ось Y
        [0, 3]   # Ось Z
    ]
    
    from polyhedron import Polyhedron
    return Polyhedron(vertices, faces_indices)