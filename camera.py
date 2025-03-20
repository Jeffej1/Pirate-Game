import pygame

class Camera:
    def __init__(self, player_pos):
        self.pos = (0,0)
        self.player_pos = player_pos
        self.display = pygame.display.get_surface()
        self.size = pygame.Vector2(self.display.get_size())
        self.all_sprites = pygame.sprite.Group()

    def mergesort(self, list):
        if len(list) <= 1:
            return list
        sorted_list = []
        i, j = 0, 0
        sorted_list.sort()

        mid = len(list) // 2
        left = self.mergesort(list[:mid])
        right = self.mergesort(list[mid:])

        while i < len(left) and j < len(right):
            if left[i][1] >= right[j][1]:
                sorted_list.append(right[j])
                j += 1
            else:
                sorted_list.append(left[i])
                i += 1
        sorted_list += left[i:]
        sorted_list += right[j:]

        return sorted_list

    def render(self, *items):
        draw_order = []
        for item in items:
            self.all_sprites.add(item)

        for sprite in self.all_sprites:
            draw_order.append([sprite, sprite.zlayer])

        draw_order = self.mergesort(draw_order)

        for sprite in draw_order:
            new_pos = pygame.Vector2(sprite[0].pos.x - self.player_pos.x, -sprite[0].pos.y + self.player_pos.y) + self.size / 2
            sprite[0].rect = sprite[0].image.get_rect(center = new_pos)
            self.display.blit(sprite[0].image, sprite[0].rect)

    def update(self):
        self.pos = self.player_pos