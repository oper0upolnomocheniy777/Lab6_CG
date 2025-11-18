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
    print("Advanced Transformations:")
    print("F - Scale center 1.5x | G - Scale center 0.7x")
    print("H - Rotate X center   | J - Rotate Y center | K - Rotate Z center")
    print("L - Arbitrary axis    | Z - Reflect XY")
    print("X - Composite trans.  | C - Shearing")
    print("V - Line rotation     | B - Spiral transform")
    print("=" * 60)
    print("All transformations are implemented using matrices!")
    print("=" * 60)
    
    # Демонстрация работы преобразований
    demo_all_polyhedra()
    
    # Сохраняем оригинальный метод draw_ui
    original_draw_ui = visualizer.draw_ui
    
    def unified_handle_events():
        """Единая функция обработки всех событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                visualizer.running = False
            
            elif event.type == pygame.KEYDOWN:
                # Выход
                if event.key == pygame.K_ESCAPE:
                    visualizer.running = False
                
                # ОРИГИНАЛЬНЫЕ КЛАВИШИ
                # Смена многогранников
                elif event.key == pygame.K_1:
                    visualizer.set_polyhedron(Polyhedron.create_tetrahedron(), "Tetrahedron")
                    print("Switched to Tetrahedron")
                elif event.key == pygame.K_2:
                    visualizer.set_polyhedron(Polyhedron.create_hexahedron(), "Hexahedron (Cube)")
                    print("Switched to Hexahedron")
                elif event.key == pygame.K_3:
                    visualizer.set_polyhedron(Polyhedron.create_octahedron(), "Octahedron")
                    print("Switched to Octahedron")
                elif event.key == pygame.K_4:
                    visualizer.set_polyhedron(Polyhedron.create_icosahedron(), "Icosahedron")
                    print("Switched to Icosahedron")
                elif event.key == pygame.K_5:
                    visualizer.set_polyhedron(Polyhedron.create_dodecahedron(), "Dodecahedron")
                    print("Switched to Dodecahedron")
                
                # Смена проекций
                elif event.key == pygame.K_p:
                    visualizer.projection_type = "perspective"
                    print("Switched to Perspective projection")
                elif event.key == pygame.K_a:
                    visualizer.projection_type = "axonometric"
                    print("Switched to Axonometric projection")
                
                # Сброс преобразований
                elif event.key == pygame.K_r and visualizer.polyhedron:
                    visualizer.reset_polyhedron()
                
                # НАШИ КЛАВИШИ - СЛОЖНЫЕ ПРЕОБРАЗОВАНИЯ
                elif event.key == pygame.K_f and visualizer.polyhedron:
                    # Масштабирование относительно центра (увеличение)
                    matrix = scaling_around_center_matrix(visualizer.polyhedron, 1.5, 1.5, 1.5)
                    visualizer.polyhedron.apply_transform(matrix)
                    print("Applied: Scaling around center 1.5x")
                    
                elif event.key == pygame.K_g and visualizer.polyhedron:
                    # Масштабирование относительно центра (уменьшение)
                    matrix = scaling_around_center_matrix(visualizer.polyhedron, 0.7, 0.7, 0.7)
                    visualizer.polyhedron.apply_transform(matrix)
                    print("Applied: Scaling around center 0.7x")
                
                elif event.key == pygame.K_h and visualizer.polyhedron:
                    # Вращение вокруг оси X через центр
                    matrix = rotation_around_center_axis_matrix(visualizer.polyhedron, 'X', 45)
                    visualizer.polyhedron.apply_transform(matrix)
                    print("Applied: Rotation around X axis through center")
                
                elif event.key == pygame.K_j and visualizer.polyhedron:
                    # Вращение вокруг оси Y через центр
                    matrix = rotation_around_center_axis_matrix(visualizer.polyhedron, 'Y', 45)
                    visualizer.polyhedron.apply_transform(matrix)
                    print("Applied: Rotation around Y axis through center")
                
                elif event.key == pygame.K_k and visualizer.polyhedron:
                    # Вращение вокруг оси Z через центр
                    matrix = rotation_around_center_axis_matrix(visualizer.polyhedron, 'Z', 45)
                    visualizer.polyhedron.apply_transform(matrix)
                    print("Applied: Rotation around Z axis through center")
                
                elif event.key == pygame.K_l and visualizer.polyhedron:
                    # Вращение вокруг произвольной оси
                    point1 = Point(-1, -1, -1)
                    point2 = Point(1, 1, 1)
                    matrix = rotation_around_axis_matrix(point1, point2, 30)
                    visualizer.polyhedron.apply_transform(matrix)
                    print("Applied: Rotation around arbitrary axis")
                
                elif event.key == pygame.K_z and visualizer.polyhedron:
                    # Отражение относительно плоскости XY
                    matrix = reflection_matrix('XY')
                    visualizer.polyhedron.apply_transform(matrix)
                    print("Applied: Reflection across XY plane")
                
                elif event.key == pygame.K_x and visualizer.polyhedron:
                    # Композитное преобразование из advanced_transformations
                    from advanced_transformations import composite_transformation
                    matrix = composite_transformation(
                        rotation_x_matrix(25),
                        rotation_y_matrix(15),
                        scaling_matrix(1.1, 0.9, 1.1)
                    )
                    visualizer.polyhedron.apply_transform(matrix)
                    print("Applied: Composite transformation")
                
                elif event.key == pygame.K_c and visualizer.polyhedron:
                    # Сдвиг из advanced_transformations
                    from advanced_transformations import shearing_matrix
                    matrix = shearing_matrix(0.3, 0, 0, 0.2, 0, 0)
                    visualizer.polyhedron.apply_transform(matrix)
                    print("Applied: Shearing transformation")
                
                elif event.key == pygame.K_v and visualizer.polyhedron:
                    # Поворот вокруг линии из advanced_transformations
                    from advanced_transformations import rotation_around_line_matrix
                    line_point = Point(0, 0, 0)
                    direction = (1, 1, 0)
                    matrix = rotation_around_line_matrix(line_point, direction, 45)
                    visualizer.polyhedron.apply_transform(matrix)
                    print("Applied: Rotation around arbitrary line")
                
                elif event.key == pygame.K_b and visualizer.polyhedron:
                    # Спиральное преобразование из advanced_transformations
                    from advanced_transformations import create_spiral_transform
                    center = visualizer.polyhedron.center
                    matrix = create_spiral_transform(center, height=2.0, rotations=0.5, scale_factor=1.2)
                    visualizer.polyhedron.apply_transform(matrix)
                    print("Applied: Spiral transformation")
    
    def advanced_draw_ui():
        """Расширенный UI с информацией о наших преобразованиях"""
        # Вызываем оригинальный UI
        original_draw_ui()
        
        # Добавляем информацию о наших клавишах в правый нижний угол
        advanced_controls = [
            "Advanced Controls:",
            "F - Scale up     G - Scale down",
            "H - Rotate X     J - Rotate Y     K - Rotate Z",
            "L - Arbitrary    Z - Reflect",
            "X - Composite    C - Shear",
            "V - Line rot.    B - Spiral"
        ]
        
        for i, text in enumerate(advanced_controls):
            control_text = visualizer.small_font.render(text, True, (100, 255, 255))
            # Правый нижний угол: отступаем от правого края 10px, от нижнего 20px
            text_rect = control_text.get_rect()
            x_pos = visualizer.width - text_rect.width - 10
            y_pos = visualizer.height - 120 + i * 20
            visualizer.screen.blit(control_text, (x_pos, y_pos))
    
    # Заменяем методы
    visualizer.handle_events = unified_handle_events
    visualizer.draw_ui = advanced_draw_ui
    
    # Запуск основного цикла
    clock = pygame.time.Clock()
    visualizer.running = True
    
    while visualizer.running:
        visualizer.handle_events()
        
        # Отрисовка
        visualizer.screen.fill(visualizer.BG_COLOR)
        visualizer.draw_polyhedron()
        visualizer.draw_ui()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

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