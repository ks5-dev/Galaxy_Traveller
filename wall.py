import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self,wall_prop, wall_x, wall_y):
        super().__init__()
        x_len = wall_prop[0]
        y_len = wall_prop[1]
        x_pos = wall_prop[2]
        y_pos = wall_prop[3]
        if x_len > y_len :
            image = pygame.image.load(wall_x).convert_alpha()
            self.image = pygame.transform.scale(image, (x_len,y_len))
        if x_len < y_len :
            image = pygame.image.load(wall_y).convert_alpha()
            self.image = pygame.transform.scale(image, (x_len,y_len))
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.pos = pygame.Vector2(self.rect.center)