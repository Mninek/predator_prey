import pygame

black = (0,0,0)

class Spritesheet:
    def __init__(self, file, kind):
        self.file = file
        self.sprite_sheet = pygame.image.load(self.file).convert()
        self.kind = kind
        if self.kind == "lord":
            self.w = 269
            self.h = 247
            self.mw = 1345
            self.mh = 12350
            self.x = 0
            self.y = 0
            self.dance = True

    #x, y is basically where in the sprite sheet were are cutting this out of
    def get_sprite(self, x, y):
        if self.dance:
            sprite = pygame.Surface((self.w, self.h))
            sprite.set_colorkey(black)
            sprite.blit(self.sprite_sheet, (0,0), (self.x,self.y,self.w,self.h))
            self.dance_sprite()
            return sprite

    def dance_sprite(self):
        self.x = (self.x + self.w) % self.mw
        self.y = (self.y + self.h) % self.mh
        
