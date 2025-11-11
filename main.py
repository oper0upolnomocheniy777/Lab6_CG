import pygame
import sys
from polyhedron import Polyhedron
from transformations import *
from visualizer import Visualizer

def main():
    """Основная функция приложения"""
    # Инициализация Pygame
    pygame.init()
    
    # Создание визуализатора
    visualizer = Visualizer()
    
    # Создание начального многогранника (тетраэдр)
    tetrahedron = Polyhedron.create_tetrahedron()
    visualizer.set_polyhedron(tetrahedron, "Tetrahedron")
    
    print("=" * 60)
    print("3D Polyhedron Visualizer - All Platonic Solids")
    print("=" * 60)
    print("Controls:")
    print("1 - Tetrahedron (4 faces)  | 2 - Cube (6 faces)")
    print("3 - Octahedron (8 faces)   | 4 - Icosahedron (20 faces)")
    print("5 - Dodecahedron (12 faces)")
    print("P - Perspective | A - Axonometric")
    print("R - Reset Transformations | ESC - Exit")
    print("=" * 60)
    print("All transformations are implemented using matrices!")
    print("=" * 60)
    
    # Демонстрация работы преобразований
    demo_all_polyhedra()
    
    # Запуск основного цикла
    visualizer.run()

def demo_all_polyhedra():
    """Демонстрация всех многогранников и преобразований"""
    print("\n🧪 Testing all polyhedra creation...")
    
    polyhedra = [
        ("Tetrahedron", Polyhedron.create_tetrahedron),
        ("Hexahedron", Polyhedron.create_hexahedron),
        ("Octahedron", Polyhedron.create_octahedron),
        ("Icosahedron", Polyhedron.create_icosahedron),
        ("Dodecahedron", Polyhedron.create_dodecahedron)
    ]
    
    for name, creator in polyhedra:
        try:
            poly = creator()
            print(f"✓ {name}: {len(poly.vertices)} vertices, {len(poly.faces)} faces")
            
            # Тестирование преобразований
            poly.apply_transform(rotation_x_matrix(45))
            poly.apply_transform(translation_matrix(0.5, 0, 0))
            print(f"  Transformations applied successfully")
            
        except Exception as e:
            print(f"✗ {name}: Error - {e}")

if __name__ == "__main__":
    # Запуск приложения
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install numpy pygame matplotlib")
        input("Press Enter to exit...")