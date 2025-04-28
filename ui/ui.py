import pygame

class UIManager:
    def __init__(self, gui: dict):
        self.gui = gui
        self.hovering_any = False

    def change_cursor(self):
        if self.hovering_any:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def update(self):
        self.hovering_any = False
        for element in self.gui:
            self.gui[element].update()
            if self.gui[element].hovering:
                self.hovering_any = True
        self.change_cursor()


class Button:
    def __init__(self, screen_pos, width, height, fill_colour, border_colour, hover_colour, text = "", action = None, border_width = 5, border_radius = 10, font_size = 30):
        self.image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect(topleft = screen_pos)
        self.font = pygame.font.SysFont('segoeuiblack', font_size)
        self.display = pygame.display.get_surface()
        self.screen_pos = screen_pos
        self.action = action

        self.hovering = False
        self.text = str(text)
        self.fill_colour = fill_colour
        
        self.border_colour = border_colour
        self.hover_colour = hover_colour

        self.size = (width, height)
        self.border_width = border_width
        self.border_radius = border_radius

    def on_click(self):
        if self.hovering and pygame.mouse.get_just_released()[0]:
            self.hovering = False
            self.action()

    def on_hover(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.hovering:
            self.rect_colour = self.hover_colour
        else:
            self.rect_colour = self.fill_colour

        if self.rect.collidepoint(mouse_pos):
            self.hovering = True
        else:
            self.hovering = False

        if self.hovering and pygame.mouse.get_pressed()[0]:
            self.rect.y = self.screen_pos[1] + 2 # Moves the button down 2 pixels when hovering
        else:
            self.rect.y = self.screen_pos[1]

    def draw(self):
        text_surf = self.font.render(self.text, True, '#202020')
        text_rect = text_surf.get_rect(center = (self.rect.center))
        
        # RECTANGLE
        pygame.draw.rect(self.image, self.rect_colour, ((0, 0), self.size), border_radius = self.border_radius)

        # BORDER
        pygame.draw.rect(self.image, self.border_colour, ((0, 0), self.size), self.border_width, self.border_radius)

        self.display.blit(self.image, self.rect)
        self.display.blit(text_surf, text_rect)

    def update(self):
        self.on_hover()
        self.on_click()
        self.draw()

class Slider:
    def __init__(self, screen_pos, min_val, max_val, default, unfilled_colour, border_colour, hover_colour, fill_colour, desc = "", width = 500, height = 10, font_size = 20):
        self.image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        self.circle_surface = pygame.Surface((height * 3, height * 3), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect(topleft = screen_pos)
        self.circle_rect = self.circle_surface.get_rect()
        self.font = pygame.font.SysFont("segoeuiblack", font_size)
        self.display = pygame.display.get_surface()
        self.screen_pos = screen_pos

        self.min, self.max, self.default = min_val, max_val, default
        self.current_value = self.default
        self.size = (width, height)
        self.desc = desc
        self.sliding = False

        self.unfilled_colour = unfilled_colour
        self.original_border_colour = border_colour
        self.hover_colour = hover_colour
        self.fill_colour = fill_colour
        
        self.text_pos = (self.screen_pos[0], self.screen_pos[1] + height)
        self.hovering = False
        self.dist_percentage = max_val / width

    def change_value(self, mouse_pos):
        min_pos, max_pos = self.screen_pos[0], self.screen_pos[0] + self.size[0]

        # Clamps the value to the max/min if the mouse is too far to the right/left
        if mouse_pos[0] > max_pos: self.current_value = self.max
        elif mouse_pos[0] < min_pos: self.current_value = self.min
        else: self.current_value = round((mouse_pos[0] - self.screen_pos[0]) * self.dist_percentage, 0)

    def on_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_mouse = pygame.mouse.get_pressed()[0]
        
        if self.rect.collidepoint(mouse_pos) or self.sliding:
            self.hovering = True
        if not self.rect.collidepoint(mouse_pos) and not self.sliding:
            self.hovering = False

        if self.hovering and left_mouse:
            self.sliding = True
        if self.sliding:
            self.change_value(mouse_pos)

        if not left_mouse:
            self.sliding = False

        if self.hovering:
            self.border_colour = self.hover_colour
        else:
            self.border_colour = self.original_border_colour

    def circle_position(self):
        self.circle_dist = self.current_value * (self.image.get_width() / self.max)
        self.circle_rect.center = (self.circle_dist + self.screen_pos[0], self.screen_pos[1] + self.size[1] / 2)

    def draw(self):
        text_surf = self.font.render(f"{self.desc}: {int(self.current_value)}%", True, '#202020')
        text_rect = text_surf.get_rect(topleft = self.text_pos)

        # RECTANGLE
        pygame.draw.rect(self.image, self.unfilled_colour, pygame.Rect((0, 0), (self.size[0], self.size[1]))) # UNFILLED RECTANGLE
        pygame.draw.rect(self.image, self.fill_colour, pygame.Rect((0, 0), (self.circle_dist, self.size[1]))) # FILLED RECTANGLE
        pygame.draw.rect(self.image, self.border_colour, pygame.Rect((0, 0), (self.size[0], self.size[1])), 1) # BORDER

        # CIRCLE
        pygame.draw.circle(self.circle_surface, self.unfilled_colour, (self.size[1] * 1.5, self.size[1] * 1.5), self.size[1]) # BASE CIRCLE
        pygame.draw.circle(self.circle_surface, self.border_colour, (self.size[1] * 1.5, self.size[1] * 1.5), self.size[1], 1) # BORDER

        self.display.blit(self.image, self.screen_pos)
        self.display.blit(self.circle_surface, self.circle_rect)
        self.display.blit(text_surf, text_rect)

    def update(self):
        self.circle_position()
        self.on_click()
        self.draw()