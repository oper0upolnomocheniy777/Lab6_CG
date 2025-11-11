import numpy as np

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