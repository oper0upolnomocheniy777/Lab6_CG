import pygame
import numpy as np
from transformations import *

class Visualizer:
    def __init__(self, width=1000, height=700):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("3D Polyhedron Visualizer - All Platonic Solids")
        self.clock = pygame.time.Clock()
        self.running = True
        self.polyhedron = None
        self.projection_type = "axonometric"  # "axonometric" or "perspective"
        self.perspective_d = 5  # Distance for perspective projection
        
        # Colors
        self.BG_COLOR = (20, 20, 40)
        self.FACE_COLORS = [
            (255, 100, 100, 120), (100, 255, 100, 120), (100, 100, 255, 120),
            (255, 255, 100, 120), (255, 100, 255, 120), (100, 255, 255, 120),
            (200, 150, 100, 120), (150, 200, 100, 120), (100, 150, 200, 120),
            (200, 100, 150, 120), (150, 100, 200, 120), (100, 200, 150, 120)
        ]
        self.EDGE_COLOR = (255, 255, 255)
        self.VERTEX_COLOR = (255, 255, 0)
        
        # Font for UI
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Current polyhedron type
        self.current_polyhedron_type = "Tetrahedron"
    
    def set_polyhedron(self, polyhedron, poly_type="Unknown"):
        """Установка многогранника для отображения"""
        self.polyhedron = polyhedron
        self.current_polyhedron_type = poly_type
    
    def axonometric_project(self, point):
        """Аксонометрическая проекция (изометрическая)"""
        # Изометрическая проекция
        x = point.x - point.z
        y = point.y + (point.x + point.z) * 0.5
        # Масштабирование и центрирование
        scale = 100
        x = x * scale + self.width // 2
        y = -y * scale + self.height // 2
        return (x, y)
    
    def perspective_project(self, point):
        """Перспективная проекция"""
        d = self.perspective_d
        if point.z + d == 0:  # Избегаем деления на ноль
            return (self.width // 2, self.height // 2)
        
        x = (point.x * d) / (point.z + d)
        y = (point.y * d) / (point.z + d)
        # Масштабирование и центрирование
        scale = 200
        x = x * scale + self.width // 2
        y = -y * scale + self.height // 2
        return (x, y)
    
    def project_point(self, point):
        """Выбор проекции для точки"""
        if self.projection_type == "perspective":
            return self.perspective_project(point)
        else:
            return self.axonometric_project(point)
    
    def draw_polyhedron(self):
        """Отрисовка многогранника"""
        if not self.polyhedron:
            return
        
        # Создаем поверхность для полупрозрачных граней
        face_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Сначала рисуем грани на отдельной поверхности
        for i, face in enumerate(self.polyhedron.faces):
            if len(face.points) < 3:
                continue
                
            color = self.FACE_COLORS[i % len(self.FACE_COLORS)]
            points_2d = [self.project_point(p) for p in face.points]
            
            # Рисуем заполненную грань на отдельной поверхности
            if len(points_2d) >= 3:
                pygame.draw.polygon(face_surface, color, points_2d)
        
        # Отображаем поверхность с гранями
        self.screen.blit(face_surface, (0, 0))
        
        # Затем рисуем рёбра поверх граней
        for face in self.polyhedron.faces:
            points_2d = [self.project_point(p) for p in face.points]
            if len(points_2d) >= 2:
                # Рисуем контур грани
                for j in range(len(points_2d)):
                    start = points_2d[j]
                    end = points_2d[(j + 1) % len(points_2d)]
                    pygame.draw.line(self.screen, self.EDGE_COLOR, start, end, 2)
        
        # И наконец рисуем вершины поверх всего
        for vertex in self.polyhedron.vertices:
            x, y = self.project_point(vertex)
            pygame.draw.circle(self.screen, self.VERTEX_COLOR, (int(x), int(y)), 3)
    
    def draw_ui(self):
        """Отрисовка пользовательского интерфейса"""
        # Информация о многограннике
        if self.polyhedron:
            poly_info = f"{self.current_polyhedron_type} - V: {len(self.polyhedron.vertices)} F: {len(self.polyhedron.faces)}"
            info_text = self.small_font.render(poly_info, True, (255, 255, 255))
            self.screen.blit(info_text, (10, 10))
        
        # Информация о проекции
        proj_text = self.small_font.render(f"Projection: {self.projection_type.upper()}", True, (255, 255, 255))
        self.screen.blit(proj_text, (10, 35))
        
        # Управление
        controls = [
            "Controls:",
            "1-Tetrahedron 2-Cube 3-Octahedron 4-Icosahedron 5-Dodecahedron",
            "P-Perspective A-Axonometric",
            "R-Reset Transformations ESC-Exit"
        ]
        
        for i, text in enumerate(controls):
            control_text = self.small_font.render(text, True, (200, 200, 100))
            self.screen.blit(control_text, (10, self.height - 120 + i * 20))
    
    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                # Смена многогранников
                if event.key == pygame.K_1:
                    from polyhedron import Polyhedron
                    self.set_polyhedron(Polyhedron.create_tetrahedron(), "Tetrahedron")
                    print("Switched to Tetrahedron")
                elif event.key == pygame.K_2:
                    from polyhedron import Polyhedron
                    self.set_polyhedron(Polyhedron.create_hexahedron(), "Hexahedron (Cube)")
                    print("Switched to Hexahedron")
                elif event.key == pygame.K_3:
                    from polyhedron import Polyhedron
                    self.set_polyhedron(Polyhedron.create_octahedron(), "Octahedron")
                    print("Switched to Octahedron")
                elif event.key == pygame.K_4:
                    from polyhedron import Polyhedron
                    self.set_polyhedron(Polyhedron.create_icosahedron(), "Icosahedron")
                    print("Switched to Icosahedron")
                elif event.key == pygame.K_5:
                    from polyhedron import Polyhedron
                    self.set_polyhedron(Polyhedron.create_dodecahedron(), "Dodecahedron")
                    print("Switched to Dodecahedron")
                
                # Смена проекций
                elif event.key == pygame.K_p:
                    self.projection_type = "perspective"
                    print("Switched to Perspective projection")
                elif event.key == pygame.K_a:
                    self.projection_type = "axonometric"
                    print("Switched to Axonometric projection")
                
                # Сброс преобразований
                elif event.key == pygame.K_r and self.polyhedron:
                    self.reset_polyhedron()
                
                # Выход
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def reset_polyhedron(self):
        """Сброс многогранника к исходному состоянию"""
        from polyhedron import Polyhedron
        
        poly_type = self.current_polyhedron_type
        if "Tetrahedron" in poly_type:
            self.set_polyhedron(Polyhedron.create_tetrahedron(), "Tetrahedron")
        elif "Hexahedron" in poly_type:
            self.set_polyhedron(Polyhedron.create_hexahedron(), "Hexahedron (Cube)")
        elif "Octahedron" in poly_type:
            self.set_polyhedron(Polyhedron.create_octahedron(), "Octahedron")
        elif "Icosahedron" in poly_type:
            self.set_polyhedron(Polyhedron.create_icosahedron(), "Icosahedron")
        elif "Dodecahedron" in poly_type:
            self.set_polyhedron(Polyhedron.create_dodecahedron(), "Dodecahedron")
        
        print(f"Reset {poly_type}")
    
    def run(self):
        """Основной цикл приложения"""
        while self.running:
            self.handle_events()
            
            # Очистка экрана
            self.screen.fill(self.BG_COLOR)
            
            # Отрисовка
            self.draw_polyhedron()
            self.draw_ui()
            
            # Обновление экрана
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()