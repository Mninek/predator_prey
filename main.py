import pygame
import random
import math
from pygame import mixer
from spritesheet import Spritesheet

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
        self.vision = 250
        self.eaten = 0

    def get_img(self):
        return self.img

    def get_tup(self):
        return (self.x, self.y)
        
    def move(self, mx, my):
        self.x += mx
        self.y += my
        
    def search_foods(self, foods):
        closest = 10000000
        cx, cy = 0,0
        cindex = 0
        for index, food in enumerate(foods):
            tup = food.get_tup()
            fx, fy = tup[0], tup[1]
            #https://stackoverflow.com/questions/5228383/how-do-i-find-the-distance-between-two-points
            dist = math. sqrt( (self.x - fx)**2 + (self.y - fy)**2 )
            if dist < closest:
                closest = dist
                cx, cy = fx, fy
                cindex = index
            index +=1
                
        if closest <= self.vision:
            mx = -self.x + cx
            my = -self.y + cy

            #TODO: MAKE LESS RETARDED
            #HAVE 'FINESE' WHEN HE GETS CLOSE TO STEAKS
            if mx <= 5 and mx >= -5 and my <= 5 and my >= -5:
                self.eat_food(foods, cindex)
            if mx != 0 and mx <= 5:
                mx  = -4
            else:
                mx = 4
            if my != 0 and my <= 5:
                my = -4
            else:
                my = 4
            self.move(mx, my)
        else:
            #TODO: BETTER RANDOM ALG SO HE MOVES IN ONE DIRECTION FOR SOME TIME
            self.move(random.randint(-1,1), random.randint(-1,1))

    def eat_food(self, foods, index):
        self.eaten += 1
        print("OM NOM NOM NOM MOTHA FUCKA")
        print("total eaten: " + str(self.eaten))
        print(index)
        foods.pop(index)
        
        
class Food(pygame.sprite.Sprite):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = pygame.transform.scale(pygame.image.load('sprites/beef.png'), (30,30))

    def get_img(self):
        return self.img

    def get_tup(self):
        return (self.x, self.y)

def main():
    x = 1200
    y = 800

    #window
    window = pygame.display
    window.set_caption("Predators and Prey")
    surface = window.set_mode([x,y])
    #TEST
    infoObject = pygame.display.Info()
    print(infoObject)
    #TEST
    #clock
    clock = pygame.time.Clock()

    #techs babyy
    techs = []
    techs.append(Prey(600,450))
    #foods
    foods = []
    for i in range(3):
        i = (i+1)*200
        for j in range(3):
            j = (j+1)*200
            foods.append(Food(i,j))


    game = True        
    background = pygame.transform.scale(pygame.image.load('sprites/background.png'), (x,y))
    font = pygame.font.SysFont("timesnewroman",20)

    lord_sprite = Spritesheet('sprites/the_lord/sprite.png', 'lord')
    lord = lord_sprite.get_sprite(0,0)
    while game:
        #fill surface
        surface.fill(white)
        #background
        surface.blit(background, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        for food in foods:
            surface.blit(food.get_img(), food.get_tup())
        for tech in techs:
            surface.blit(tech.get_img(), tech.get_tup())
            tech.search_foods(foods)
        surface.blit(lord, (1100,700))
        window.update()
        clock.tick(15)
    pygame.quit()

if __name__ == '__main__':
    main()




















