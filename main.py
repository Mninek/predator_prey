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
        self.ate_sound = pygame.mixer.Sound('sounds/burger.wav')

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

            #THANK U BALLOD
            if -5 <= mx <= 5 and -5 <= my <= 5:
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
        foods.pop(index)
        self.ate_sound.play()

class Predator(pygame.sprite.Sprite):

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = pygame.transform.scale(pygame.image.load('sprites/evil eye.png'), (40,30))
        self.vision = 300
        self.hunting = False
        self.hunt_sound = pygame.mixer.Sound('sounds/puma.wav')
        self.ate_sound = pygame.mixer.Sound('sounds/cutemeow.wav')

    def get_img(self):
        return self.img

    def get_tup(self):
        return (self.x, self.y)

    def move(self, mx, my):
        self.x += mx
        self.y += my

    def find_prey(self, preys):
        closest = 10000000
        cx, cy = 0,0
        cindex = 0
        for index, prey in enumerate(preys):
            tup = prey.get_tup()
            fx, fy = tup[0], tup[1]
            #https://stackoverflow.com/questions/5228383/how-do-i-find-the-distance-between-two-points
            dist = math. sqrt( (self.x - fx)**2 + (self.y - fy)**2 )
            if dist < closest:
                closest = dist
                cx, cy = fx, fy
                cindex = index
            index +=1
            
        if closest <= self.vision:
            if not self.hunting:
                self.hunt()
            mx = -self.x + cx
            my = -self.y + cy

            #TODO: MAKE LESS RETARDED
            #HAVE 'FINESE' WHEN HE GETS CLOSE TO STEAKS
            if mx <= 5 and mx >= -5 and my <= 5 and my >= -5:
                self.eat_prey(preys, cindex)
            if mx != 0 and mx <= 6:
                mx  = -5
            else:
                mx = 5
            if my != 0 and my <= 6:
                my = -5
            else:
                my = 5
            self.move(mx, my)
            
    def hunt(self):
        self.img = pygame.transform.scale(pygame.image.load('sprites/devilish.png'), (40,30))
        self.hunt_sound.play()
        self.hunting = True 

    def eat_prey(self, preys, index):
        print("GOODBYE TECH")
        preys.pop(index)
        self.img = pygame.transform.scale(pygame.image.load('sprites/evil eye.png'), (40,30))
        self.ate_sound.play()
        self.hunting = False

        
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

    #CATS
    cats = []
    cats.append(Predator(200,300))

    #music
    mixer.music.load('sounds/ccmall_trap.wav')
    mixer.music.set_volume(.05)
    mixer.music.play(-1)

    game = True        
    background = pygame.transform.scale(pygame.image.load('sprites/background.png'), (x,y))
    font = pygame.font.SysFont("timesnewroman",20)

    lord_sprite = Spritesheet('sprites/the_lord/sprite.png', 'lord')
    lord = lord_sprite.get_sprite(0,0)
    lord_w = 1000
    lord_h = 600
    up = True
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

        for cat in cats:
            surface.blit(cat.get_img(), cat.get_tup())
            cat.find_prey(techs)
            
        surface.blit(lord, (lord_w,lord_h))
        if up:
            lord_h -= 10
            if lord_h == 0:
                up = False
        else:
            lord_h += 10
            if lord_h == y-200:
                up = True
        lord = lord_sprite.get_sprite(0,0)
        window.update()
        clock.tick(15)
    pygame.quit()

if __name__ == '__main__':
    main()




















