import pygame

class Timer():
    def __init__(self, duration_ms):
        self.duration = duration_ms
        self.reset()

    def finished(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.initial_time >= self.duration:
            return True
        else:
            return False

    def reset(self):
        self.initial_time = pygame.time.get_ticks()
        self.current_time = pygame.time.get_ticks()