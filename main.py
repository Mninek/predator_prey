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
        self.ate_sound.set_volume(.05)
        self.cat_vision = 100
        self.speed = 4

    def get_img(self):
        return self.img

    def get_tup(self):
        return (self.x, self.y)
        
    def move(self, mx, my):
        self.x += mx
        self.y += my

    def search_predators(self, cats):
        closest = 1000000
        cx, cy = 0,0
        cindex = 0
        for index, cat in enumerate(cats):
            tup = cat.get_tup()
            fx, fy = tup[0], tup[1]
            dist = math. sqrt( (self.x - fx)**2 + (self.y - fy)**2 )
            if dist < closest:
                closest = dist
                cx, cy = fx, fy
                cindex = index
            index +=1
        if closest <= self.cat_vision:
            #if positive, cat is to left, o.w. cat to right
            horizontal = self.x - cx
            #if positive cat is above, o.w. cat is below
            vertical = self.y - cy
            mx, my = 0,0
            if horizontal > 0:
                mx = self.speed
            else:
                mx = -self.speed
            if vertical > 0:
                my = self.speed
            else:
                my = -self.speed
            self.move(mx, my)   
            
        
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
            r = self.speed + 1
            if -r <= mx <= r and -r <= my <= r:
                self.eat_food(foods, cindex)
            if mx != 0 and mx <= r:
                mx  = -r
            else:
                mx = r
            if my != 0 and my <= r:
                my = -r
            else:
                my = r
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
        self.img = pygame.transform.scale(pygame.image.load('sprites/devilish.png'), (40,30))
        self.vision = 300
        self.hunting = False
        self.hunt_sound = pygame.mixer.Sound('sounds/puma.wav')
        self.ate_sound = pygame.mixer.Sound('sounds/cutemeow.wav')
        self.hunt_sound.set_volume(.05)
        self.ate_sound.set_volume(.05)
        self.speed = 6

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
            r = self.speed + 1
            if mx <= r and mx >= -r and my <= r and my >= -r:
                self.eat_prey(preys, cindex)
            if mx != 0 and mx <= r:
                mx  = -self.speed
            else:
                mx = self.speed
            if my != 0 and my <= r:
                my = -self.speed
            else:
                my = self.speed
            self.move(mx, my)            
            
            
    def hunt(self):
        self.img = pygame.transform.scale(pygame.image.load('sprites/evil eye.png'), (40,30))
        self.hunt_sound.play()
        self.hunting = True 

    def eat_prey(self, preys, index):
        print("GOODBYE TECH")
        preys.pop(index)
        self.img = pygame.transform.scale(pygame.image.load('sprites/devilish.png'), (40,30))
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
    lup = True
    squid_sprite = Spritesheet('sprites/squid/squid.png', 'squid')
    squid = lord_sprite.get_sprite(0,0)
    squid_w = 200
    squid_h = 600
    sup = True
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
            tech.search_predators(cats)

        for cat in cats:
            surface.blit(cat.get_img(), cat.get_tup())
            cat.find_prey(techs)
            
        surface.blit(lord, (lord_w,lord_h))
        if lup:
            lord_h -= 10
            if lord_h == 0:
                lup = False
        else:
            lord_h += 10
            if lord_h == y-200:
                lup = True
        lord = lord_sprite.get_sprite(0,0)
        
        surface.blit(squid, (squid_w,squid_h))
        if sup:
            squid_h -= 10
            if squid_h == 0:
                sup = False
        else:
            squid_h += 10
            if squid_h == y-200:
                sup = True
        squid = squid_sprite.get_sprite(0,0)
        window.update()
        clock.tick(15)
    pygame.quit()

if __name__ == '__main__':
    main()




















