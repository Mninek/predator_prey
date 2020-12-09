import pygame

class Spritesheet:
    def __init__(self, file, kind):
        self.file = file
        self.sprite_sheet = pygame.image.load(self.file).convert()
        self.kind = kind

    #x, y is basically where in the sprite sheet were are cutting this out of
    def get_sprite(self, x, y):
        if self.kind == "lord":
            sprite = pygame.Surface((269, 247))
            sprite.set_colorkey((85, 255, 33))
            sprite.blit(self.sprite_sheet, (0,0), (x,y,269,247))
            return sprite
