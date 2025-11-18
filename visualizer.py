import pygame
import numpy as np
from transformations import *

class Button:
    """Класс для создания кнопок"""
    def __init__(self, x, y, width, height, text, color=(100, 100, 200), hover_color=(150, 150, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 24)
    
    def draw(self, screen):
        """Отрисовка кнопки"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=8)
        
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def check_hover(self, pos):
        """Проверка наведения курсора"""
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
    
    def is_clicked(self, pos, event):
        """Проверка клика по кнопке"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class Slider:
    """Класс для создания слайдеров"""
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.knob_radius = 10
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.dragging = False
        self.font = pygame.font.Font(None, 20)
    
    def draw(self, screen):
        """Отрисовка слайдера"""
        # Фон слайдера
        pygame.draw.rect(screen, (80, 80, 100), self.rect, border_radius=5)
        
        # Заполненная часть
        fill_width = int((self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(screen, (100, 200, 100), fill_rect, border_radius=5)
        
        # Ползунок
        knob_x = self.rect.x + fill_width
        knob_y = self.rect.y + self.rect.height // 2
        pygame.draw.circle(screen, (255, 255, 255), (knob_x, knob_y), self.knob_radius)
        
        # Текст
        label_text = self.font.render(f"{self.label}: {self.value:.1f}", True, (255, 255, 255))
        screen.blit(label_text, (self.rect.x, self.rect.y - 25))
    
    def handle_event(self, event):
        """Обработка событий слайдера"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            knob_x = self.rect.x + int((self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width)
            knob_rect = pygame.Rect(knob_x - self.knob_radius, self.rect.y - self.knob_radius, 
                                  self.knob_radius * 2, self.knob_radius * 2)
            if knob_rect.collidepoint(mouse_pos):
                self.dragging = True
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x = pygame.mouse.get_pos()[0]
            relative_x = max(0, min(self.rect.width, mouse_x - self.rect.x))
            self.value = self.min_val + (relative_x / self.rect.width) * (self.max_val - self.min_val)
            return True
        
        return False

class Visualizer:
    def __init__(self, width=1200, height=800):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("3D Polyhedron Visualizer - Enhanced GUI")
        self.clock = pygame.time.Clock()
        self.running = True
        self.polyhedron = None
        self.projection_type = "axonometric"
        self.perspective_d = 5
        
        # Colors
        self.BG_COLOR = (20, 20, 40)
        self.UI_BG_COLOR = (30, 30, 60, 200)
        self.FACE_COLORS = [
            (255, 100, 100, 150), (100, 255, 100, 150), (100, 100, 255, 150),
            (255, 255, 100, 150), (255, 100, 255, 150), (100, 255, 255, 150),
            (200, 150, 100, 150), (150, 200, 100, 150), (100, 150, 200, 150),
            (200, 100, 150, 150), (150, 100, 200, 150), (100, 200, 150, 150)
        ]
        self.EDGE_COLOR = (255, 255, 255)
        self.VERTEX_COLOR = (255, 255, 0)
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 48)
        
        # Current polyhedron
        self.current_polyhedron_type = "Tetrahedron"
        
        # Mouse control
        self.dragging = False
        self.last_mouse_pos = (0, 0)
        self.rotation_x = 0
        self.rotation_y = 0
        self.scale = 1.0
        
        # Create UI elements
        self.create_ui_elements()
        
        # Animation
        self.auto_rotate = False
        self.animation_speed = 1.0
    
    def create_ui_elements(self):
        """Create UI elements"""
        # Polyhedron selection buttons
        self.poly_buttons = [
            Button(20, 100, 120, 40, "Tetrahedron"),
            Button(150, 100, 120, 40, "Cube"),
            Button(280, 100, 120, 40, "Octahedron"),
            Button(410, 100, 120, 40, "Icosahedron"),
            Button(540, 100, 140, 40, "Dodecahedron")
        ]
        
        # Projection buttons
        self.proj_buttons = [
            Button(700, 100, 120, 40, "Perspective"),
            Button(830, 100, 140, 40, "Axonometric")
        ]
        
        # Control buttons
        self.control_buttons = [
            Button(980, 100, 100, 40, "Reset"),
            Button(1090, 100, 90, 40, "Auto Rotate")
        ]
        
        # Sliders
        self.sliders = [
            Slider(20, 200, 200, 20, 0.1, 3.0, 1.0, "Scale"),
            Slider(20, 250, 200, 20, 0.0, 5.0, 1.0, "Rotation Speed"),
            Slider(20, 300, 200, 20, 1.0, 10.0, 5.0, "Perspective")
        ]
        
        # Transformation buttons
        self.transform_buttons = [
            Button(250, 200, 120, 30, "Scale Up"),
            Button(380, 200, 120, 30, "Scale Down"),
            Button(250, 240, 120, 30, "Rotate X"),
            Button(380, 240, 120, 30, "Rotate Y"),
            Button(250, 280, 120, 30, "Rotate Z"),
            Button(380, 280, 120, 30, "Reflect XY"),
            Button(250, 320, 120, 30, "Shear"),
            Button(380, 320, 120, 30, "Spiral")
        ]
    
    def set_polyhedron(self, polyhedron, poly_type="Unknown"):
        """Set polyhedron for display"""
        self.polyhedron = polyhedron
        self.current_polyhedron_type = poly_type
        self.reset_view()
    
    def reset_view(self):
        """Reset view to initial state"""
        self.rotation_x = 0
        self.rotation_y = 0
        self.scale = 1.0
    
    def axonometric_project(self, point):
        """Axonometric projection"""
        # Apply current rotations
        rotated = self.apply_current_rotation(point)
        
        # Isometric projection
        x = rotated.x - rotated.z
        y = rotated.y + (rotated.x + rotated.z) * 0.5
        
        # Scaling and centering
        scale = 100 * self.scale
        x = x * scale + self.width // 2
        y = -y * scale + self.height // 2
        return (x, y)
    
    def perspective_project(self, point):
        """Perspective projection"""
        # Apply current rotations
        rotated = self.apply_current_rotation(point)
        
        d = self.perspective_d
        if rotated.z + d == 0:
            return (self.width // 2, self.height // 2)
        
        x = (rotated.x * d) / (rotated.z + d)
        y = (rotated.y * d) / (rotated.z + d)
        
        # Scaling and centering
        scale = 200 * self.scale
        x = x * scale + self.width // 2
        y = -y * scale + self.height // 2
        return (x, y)
    
    def apply_current_rotation(self, point):
        """Apply current rotations to point"""
        from point import Point
        # Create temporary point copy
        temp_point = Point(point.x, point.y, point.z)
        
        # Apply rotations
        if self.rotation_x != 0:
            matrix = rotation_x_matrix(self.rotation_x)
            temp_point.transform(matrix)
        
        if self.rotation_y != 0:
            matrix = rotation_y_matrix(self.rotation_y)
            temp_point.transform(matrix)
        
        return temp_point
    
    def project_point(self, point):
        """Choose projection for point"""
        if self.projection_type == "perspective":
            return self.perspective_project(point)
        else:
            return self.axonometric_project(point)
    
    def draw_polyhedron(self):
        """Draw polyhedron"""
        if not self.polyhedron:
            return
        
        # Auto rotation
        if self.auto_rotate:
            self.rotation_y += 0.5 * self.animation_speed
        
        # Create surface for semi-transparent faces
        face_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # First draw faces on separate surface
        for i, face in enumerate(self.polyhedron.faces):
            if len(face.points) < 3:
                continue
                
            color = self.FACE_COLORS[i % len(self.FACE_COLORS)]
            points_2d = [self.project_point(p) for p in face.points]
            
            # Draw filled face on separate surface
            if len(points_2d) >= 3:
                pygame.draw.polygon(face_surface, color, points_2d)
        
        # Display face surface
        self.screen.blit(face_surface, (0, 0))
        
        # Then draw edges over faces
        for face in self.polyhedron.faces:
            points_2d = [self.project_point(p) for p in face.points]
            if len(points_2d) >= 2:
                # Draw face outline
                for j in range(len(points_2d)):
                    start = points_2d[j]
                    end = points_2d[(j + 1) % len(points_2d)]
                    pygame.draw.line(self.screen, self.EDGE_COLOR, start, end, 2)
        
        # Finally draw vertices over everything
        for vertex in self.polyhedron.vertices:
            x, y = self.project_point(vertex)
            pygame.draw.circle(self.screen, self.VERTEX_COLOR, (int(x), int(y)), 4)
    
    def draw_ui_panel(self):
        """Draw UI panel"""
        # Semi-transparent panel
        panel_surface = pygame.Surface((self.width, 160), pygame.SRCALPHA)
        panel_surface.fill((30, 30, 60, 200))
        self.screen.blit(panel_surface, (0, 0))
        
        # Title
        title_text = self.title_font.render("3D Polyhedron Visualizer", True, (255, 255, 255))
        self.screen.blit(title_text, (20, 20))
        
        # Polyhedron info
        if self.polyhedron:
            poly_info = f"{self.current_polyhedron_type} - Vertices: {len(self.polyhedron.vertices)} - Faces: {len(self.polyhedron.faces)}"
            info_text = self.small_font.render(poly_info, True, (255, 255, 255))
            self.screen.blit(info_text, (20, 65))
        
        # Projection info
        proj_text = self.small_font.render(f"Projection: {self.projection_type.upper()}", True, (255, 255, 255))
        self.screen.blit(proj_text, (700, 65))
        
        # Auto rotation status
        auto_text = "ON" if self.auto_rotate else "OFF"
        auto_color = (100, 255, 100) if self.auto_rotate else (255, 100, 100)
        rotate_text = self.small_font.render(f"Auto Rotate: {auto_text}", True, auto_color)
        self.screen.blit(rotate_text, (1000, 65))
    
    def draw_control_panel(self):
        """Draw control panel"""
        # Control panel on the right
        panel_width = 300
        panel_surface = pygame.Surface((panel_width, self.height - 160), pygame.SRCALPHA)
        panel_surface.fill((40, 40, 80, 180))
        self.screen.blit(panel_surface, (self.width - panel_width, 160))
        
        # Control panel title
        controls_title = self.font.render("Controls", True, (255, 255, 255))
        self.screen.blit(controls_title, (self.width - panel_width + 20, 180))
        
        # Instructions
        instructions = [
            "Mouse Controls:",
            "- Drag: Rotate",
            "- Wheel: Zoom",
            "- Right Click: Reset",
            "",
            "Transformations:",
            "- Use buttons below",
            "- Or keyboard shortcuts"
        ]
        
        for i, text in enumerate(instructions):
            inst_text = self.small_font.render(text, True, (200, 200, 100))
            self.screen.blit(inst_text, (self.width - panel_width + 20, 230 + i * 25))
    
    def draw_ui(self):
        """Draw entire user interface"""
        # Main panel
        self.draw_ui_panel()
        
        # Control panel
        self.draw_control_panel()
        
        # Draw all buttons
        all_buttons = self.poly_buttons + self.proj_buttons + self.control_buttons + self.transform_buttons
        for button in all_buttons:
            button.draw(self.screen)
        
        # Draw all sliders
        for slider in self.sliders:
            slider.draw(self.screen)
        
        # Additional info
        info_text = self.small_font.render("Press H for Help", True, (255, 255, 255))
        self.screen.blit(info_text, (self.width - 150, self.height - 30))
    
    def handle_ui_events(self, event):
        """Handle UI events"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Update hover state for all buttons
        all_buttons = self.poly_buttons + self.proj_buttons + self.control_buttons + self.transform_buttons
        for button in all_buttons:
            button.check_hover(mouse_pos)
        
        # Handle sliders
        for slider in self.sliders:
            if slider.handle_event(event):
                if slider.label == "Scale":
                    self.scale = slider.value
                elif slider.label == "Rotation Speed":
                    self.animation_speed = slider.value
                elif slider.label == "Perspective":
                    self.perspective_d = slider.value
        
        # Handle button clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_button_clicks(mouse_pos, event)
    
    def handle_button_clicks(self, mouse_pos, event):
        """Handle button clicks"""
        # Polyhedron buttons
        if self.poly_buttons[0].is_clicked(mouse_pos, event):
            from polyhedron import Polyhedron
            self.set_polyhedron(Polyhedron.create_tetrahedron(), "Tetrahedron")
        elif self.poly_buttons[1].is_clicked(mouse_pos, event):
            from polyhedron import Polyhedron
            self.set_polyhedron(Polyhedron.create_hexahedron(), "Hexahedron (Cube)")
        elif self.poly_buttons[2].is_clicked(mouse_pos, event):
            from polyhedron import Polyhedron
            self.set_polyhedron(Polyhedron.create_octahedron(), "Octahedron")
        elif self.poly_buttons[3].is_clicked(mouse_pos, event):
            from polyhedron import Polyhedron
            self.set_polyhedron(Polyhedron.create_icosahedron(), "Icosahedron")
        elif self.poly_buttons[4].is_clicked(mouse_pos, event):
            from polyhedron import Polyhedron
            self.set_polyhedron(Polyhedron.create_dodecahedron(), "Dodecahedron")
        
        # Projection buttons
        elif self.proj_buttons[0].is_clicked(mouse_pos, event):
            self.projection_type = "perspective"
        elif self.proj_buttons[1].is_clicked(mouse_pos, event):
            self.projection_type = "axonometric"
        
        # Control buttons
        elif self.control_buttons[0].is_clicked(mouse_pos, event) and self.polyhedron:
            self.reset_polyhedron()
        elif self.control_buttons[1].is_clicked(mouse_pos, event):
            self.auto_rotate = not self.auto_rotate
        
        # Transformation buttons
        elif self.transform_buttons[0].is_clicked(mouse_pos, event) and self.polyhedron:
            matrix = scaling_around_center_matrix(self.polyhedron, 1.2, 1.2, 1.2)
            self.polyhedron.apply_transform(matrix)
        elif self.transform_buttons[1].is_clicked(mouse_pos, event) and self.polyhedron:
            matrix = scaling_around_center_matrix(self.polyhedron, 0.8, 0.8, 0.8)
            self.polyhedron.apply_transform(matrix)
        elif self.transform_buttons[2].is_clicked(mouse_pos, event) and self.polyhedron:
            matrix = rotation_around_center_axis_matrix(self.polyhedron, 'X', 30)
            self.polyhedron.apply_transform(matrix)
        elif self.transform_buttons[3].is_clicked(mouse_pos, event) and self.polyhedron:
            matrix = rotation_around_center_axis_matrix(self.polyhedron, 'Y', 30)
            self.polyhedron.apply_transform(matrix)
        elif self.transform_buttons[4].is_clicked(mouse_pos, event) and self.polyhedron:
            matrix = rotation_around_center_axis_matrix(self.polyhedron, 'Z', 30)
            self.polyhedron.apply_transform(matrix)
        elif self.transform_buttons[5].is_clicked(mouse_pos, event) and self.polyhedron:
            matrix = reflection_matrix('XY')
            self.polyhedron.apply_transform(matrix)
        elif self.transform_buttons[6].is_clicked(mouse_pos, event) and self.polyhedron:
            from advanced_transformations import shearing_matrix
            matrix = shearing_matrix(0.2, 0, 0, 0.1, 0, 0)
            self.polyhedron.apply_transform(matrix)
        elif self.transform_buttons[7].is_clicked(mouse_pos, event) and self.polyhedron:
            from advanced_transformations import create_spiral_transform
            center = self.polyhedron.center
            matrix = create_spiral_transform(center, height=1.5, rotations=0.3, scale_factor=1.1)
            self.polyhedron.apply_transform(matrix)
    
    def handle_mouse_events(self, event):
        """Handle mouse events"""
        mouse_pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left button - rotation
                self.dragging = True
                self.last_mouse_pos = mouse_pos
            elif event.button == 3:  # Right button - reset
                self.reset_view()
            elif event.button == 4:  # Wheel up - zoom in
                self.scale = min(3.0, self.scale * 1.1)
                self.sliders[0].value = self.scale
            elif event.button == 5:  # Wheel down - zoom out
                self.scale = max(0.1, self.scale * 0.9)
                self.sliders[0].value = self.scale
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            dx = mouse_pos[0] - self.last_mouse_pos[0]
            dy = mouse_pos[1] - self.last_mouse_pos[1]
            
            self.rotation_y += dx * 0.5
            self.rotation_x += dy * 0.5
            
            self.last_mouse_pos = mouse_pos
    
    def handle_keyboard_events(self, event):
        """Handle keyboard events"""
        # Polyhedron selection
        if event.key == pygame.K_1:
            from polyhedron import Polyhedron
            self.set_polyhedron(Polyhedron.create_tetrahedron(), "Tetrahedron")
        elif event.key == pygame.K_2:
            from polyhedron import Polyhedron
            self.set_polyhedron(Polyhedron.create_hexahedron(), "Hexahedron (Cube)")
        elif event.key == pygame.K_3:
            from polyhedron import Polyhedron
            self.set_polyhedron(Polyhedron.create_octahedron(), "Octahedron")
        elif event.key == pygame.K_4:
            from polyhedron import Polyhedron
            self.set_polyhedron(Polyhedron.create_icosahedron(), "Icosahedron")
        elif event.key == pygame.K_5:
            from polyhedron import Polyhedron
            self.set_polyhedron(Polyhedron.create_dodecahedron(), "Dodecahedron")
        
        # Projection selection
        elif event.key == pygame.K_p:
            self.projection_type = "perspective"
        elif event.key == pygame.K_a:
            self.projection_type = "axonometric"
        
        # Controls
        elif event.key == pygame.K_r and self.polyhedron:
            self.reset_polyhedron()
        elif event.key == pygame.K_SPACE:
            self.auto_rotate = not self.auto_rotate
        elif event.key == pygame.K_h:
            self.show_help_message()
        elif event.key == pygame.K_ESCAPE:
            self.running = False
        
        # Transformations
        elif event.key == pygame.K_f and self.polyhedron:
            matrix = scaling_around_center_matrix(self.polyhedron, 1.5, 1.5, 1.5)
            self.polyhedron.apply_transform(matrix)
        elif event.key == pygame.K_g and self.polyhedron:
            matrix = scaling_around_center_matrix(self.polyhedron, 0.7, 0.7, 0.7)
            self.polyhedron.apply_transform(matrix)
    
    def handle_events(self):
        """Handle all events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Handle UI events
            self.handle_ui_events(event)
            
            # Handle mouse events
            self.handle_mouse_events(event)
            
            # Handle keyboard events
            if event.type == pygame.KEYDOWN:
                self.handle_keyboard_events(event)
    
    def show_help_message(self):
        """Show help message"""
        help_lines = [
            "=== 3D Polyhedron Visualizer - Help ===",
            "",
            "Mouse Controls:",
            "- Left Drag: Rotate object",
            "- Mouse Wheel: Zoom in/out", 
            "- Right Click: Reset view",
            "",
            "Keyboard Shortcuts:",
            "1-5: Switch polyhedra",
            "P: Perspective projection",
            "A: Axonometric projection",
            "R: Reset transformations",
            "Space: Toggle auto-rotation",
            "F/G: Scale up/down",
            "ESC: Exit",
            "",
            "UI Controls:",
            "- Use buttons for transformations",
            "- Sliders for fine control",
            "- Click polyhedron names to switch"
        ]
        
        print("\n" + "\n".join(help_lines))
    
    def reset_polyhedron(self):
        """Reset polyhedron to original state"""
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
        
        self.reset_view()
    
    def run(self):
        """Main application loop"""
        while self.running:
            self.handle_events()
            
            # Clear screen
            self.screen.fill(self.BG_COLOR)
            
            # Draw
            self.draw_polyhedron()
            self.draw_ui()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()