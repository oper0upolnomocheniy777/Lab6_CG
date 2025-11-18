import numpy as np
from transformations import *
from point import Point

def perspective_projection_matrix(d):
    """
    Матрица перспективной проекции
    """
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 1/d, 0]
    ], dtype=float)

def orthographic_projection_matrix():
    """Матрица ортографической проекции"""
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 1]
    ], dtype=float)

def shearing_matrix(sh_xy, sh_xz, sh_yx, sh_yz, sh_zx, sh_zy):
    """Матрица сдвига"""
    return np.array([
        [1,   sh_xy, sh_xz, 0],
        [sh_yx, 1,   sh_yz, 0],
        [sh_zx, sh_zy, 1,   0],
        [0,   0,    0,   1]
    ], dtype=float)

def transform_point(point, matrix):
    """Применение матрицы преобразования к точке"""
    homogeneous = np.array([point.x, point.y, point.z, 1.0])
    transformed = matrix @ homogeneous
    return Point(transformed[0]/transformed[3], 
                transformed[1]/transformed[3], 
                transformed[2]/transformed[3])


def rotation_around_line_matrix(line_point, direction_vector, angle_degrees):
    """
    Поворот вокруг произвольной прямой, заданной точкой и вектором направления
    """
    # Нормализуем вектор направления
    dx, dy, dz = direction_vector
    length = np.sqrt(dx*dx + dy*dy + dz*dz)
    if length == 0:
        raise ValueError("Direction vector cannot be zero")
    
    u = dx / length
    v = dy / length
    w = dz / length
    
    # Угол поворота в радианах
    angle = np.radians(angle_degrees)
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)
    one_minus_cos = 1 - cos_a
    
    # Матрица поворота вокруг произвольной оси
    rotation = np.array([
        [
            cos_a + u*u*one_minus_cos,
            u*v*one_minus_cos - w*sin_a,
            u*w*one_minus_cos + v*sin_a,
            0
        ],
        [
            u*v*one_minus_cos + w*sin_a,
            cos_a + v*v*one_minus_cos,
            v*w*one_minus_cos - u*sin_a,
            0
        ],
        [
            u*w*one_minus_cos - v*sin_a,
            v*w*one_minus_cos + u*sin_a,
            cos_a + w*w*one_minus_cos,
            0
        ],
        [0, 0, 0, 1]
    ], dtype=float)
    
    # Комбинируем с переносами
    translate_to_origin = translation_matrix(-line_point.x, -line_point.y, -line_point.z)
    translate_back = translation_matrix(line_point.x, line_point.y, line_point.z)
    
    return translate_back @ rotation @ translate_to_origin

def composite_transformation(*matrices):
    """
    Композиция нескольких матричных преобразований
    Порядок применения: первая матрица применяется последней
    """
    if not matrices:
        return identity_matrix()
    
    result = matrices[0]
    for matrix in matrices[1:]:
        result = matrix @ result
    
    return result

def create_spiral_transform(center, height, rotations, scale_factor=1.0):
    """
    Создание спирального преобразования
    """
    matrices = []
    
    # Перенос в начало координат
    matrices.append(translation_matrix(-center.x, -center.y, -center.z))
    
    # Постепенный поворот и подъем
    angle_per_step = rotations * 360 / 10
    height_per_step = height / 10
    
    for i in range(1, 11):
        matrices.append(rotation_y_matrix(angle_per_step * i))
        matrices.append(translation_matrix(0, 0, height_per_step * i))
    
    # Масштабирование
    matrices.append(scaling_matrix(scale_factor, scale_factor, scale_factor))
    
    # Возврат обратно
    matrices.append(translation_matrix(center.x, center.y, center.z))
    
    return composite_transformation(*matrices)

def transform_multiple_points(points, matrix):
    """
    Применение матрицы преобразования к нескольким точкам
    """
    transformed_points = []
    for point in points:
        new_point = point.copy()
        new_point.transform(matrix)
        transformed_points.append(new_point)
    return transformed_points

def print_matrix_info(matrix, name="Matrix"):
    """
    Красивый вывод информации о матрице
    """
    print(f"\n{name}:")
    for i, row in enumerate(matrix):
        row_str = ", ".join([f"{val:8.3f}" for val in row])
        if i == len(matrix) - 1:
            print(f"[{row_str}]")
        else:
            print(f"[{row_str}],")