import pygame
import random

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
pygame.init()

class Prey(pygame.sprite.Sprite):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = pygame.transform.scale(pygame.image.load('sprites/tech.png'), (40,40))

    def get_img(self):
        return self.img

    def get_tup(self):
        return (self.x, self.y)
        
    def move(self):
        self.x += random.randint(-1,1)
        self.y += random.randint(-1,1)
        
class Food(pygame.sprite.Sprite):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = pygame.transform.scale(pygame.image.load('sprites/tech.png'), (20,20))

    def get_img(self):
        return self.img

    def get_tup(self):
        return (self.x, self.y)

def main():
    x = 1200
    y = 800
    
    window = pygame.display
    window.set_caption("Predators and Prey")
    surface = window.set_mode([x,y])
    
    game = True
    
    clock = pygame.time.Clock()
    techs = []
    for i in range(3):
        i = (i+1)*200
        for j in range(3):
            j = (j+1)*200
            techs.append(Prey(i,j))
    background = pygame.transform.scale(pygame.image.load('sprites/background.png'), (x,y))
    font = pygame.font.SysFont("timesnewroman",20)
    while game:
        #fill surface
        surface.fill(white)
        #background
        surface.blit(background, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        for tech in techs:
            surface.blit(tech.get_img(), tech.get_tup())
            tech.move()
        window.update()
        clock.tick(15)
    pygame.quit()

if __name__ == '__main__':
    main()




















