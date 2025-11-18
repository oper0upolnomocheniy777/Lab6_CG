import pygame
import sys
from polyhedron import Polyhedron
from transformations import *
from visualizer import Visualizer

def main():
    """Основная функция приложения"""
    # Инициализация Pygame
    pygame.init()
    
    # Создание расширенного визуализатора
    visualizer = Visualizer()
    
    # Создание начального многогранника
    tetrahedron = Polyhedron.create_tetrahedron()
    visualizer.set_polyhedron(tetrahedron, "Tetrahedron")
    
    print("=" * 70)
    print("🎮 3D Polyhedron Visualizer - Enhanced GUI Version")
    print("=" * 70)
    print("🌟 Features:")
    print("• Interactive GUI with buttons and sliders")
    print("• Mouse controls: drag to rotate, wheel to zoom")
    print("• All 5 Platonic solids")
    print("• Multiple projection types")
    print("• Real-time transformations")
    print("• Auto-rotation mode")
    print("=" * 70)
    print("🖱️  Mouse Controls:")
    print("Left Drag: Rotate | Wheel: Zoom | Right Click: Reset View")
    print("=" * 70)
    print("⌨️  Keyboard Shortcuts:")
    print("1-5: Switch polyhedra | P/A: Projections | R: Reset")
    print("Space: Auto-rotate | H: Help | ESC: Exit")
    print("=" * 70)
    print("🚀 Advanced Features:")
    print("• Scale/rotate with UI buttons")
    print("• Perspective distance control")
    print("• Animation speed adjustment")
    print("• Real-time transformation preview")
    print("=" * 70)
    
    # Запуск основного цикла
    try:
        visualizer.run()
    except Exception as e:
        print(f"Error during execution: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install numpy pygame")
        input("Press Enter to exit...")

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
    # Демонстрация работы всех многогранников
    demo_all_polyhedra()
    
    # Запуск приложения
    try:
        main()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")