import pygame
import random
pygame.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800
WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
Font =pygame.font.SysFont("comicsansms",25,True)

#pysics machine/world
class Physicsworld:
    def __init__(self,gravity,elasticity,resistance,normal,brake_resistance,push,resistance_present=True):
        self.gravity=gravity
        self.elasticity=elasticity
        self.resistance=resistance * int(resistance_present)
        self.jump_normal=normal
        self.brake_resistance=brake_resistance
        self.push=push

class Player:
    def __init__(self,world,x,y,jump_velocity):
        self.x=x
        self.y=y
        self.jump_velocity=jump_velocity
        self.velocity_x=0
        self.velocity_y=0
        self.acceleration_x=0
        self.acceleration_y=0
        self.walking=False
        self.right=False
        self.left=False
        self.on_platform=True
        self.time=0
        self.world=world
        self.upforce=-self.world.gravity
        self.score=0
        #temp
        self.radius=10
        pass
    def event_manager(self,event,keys):
        if event.type==pygame.KEYDOWN:
            if keys[pygame.K_UP]:
                self.jump()
    def general_operations_manager(self,keys,dt):
        if keys[pygame.K_RIGHT]:
            self.walking=True
            self.left=False
            self.right=True
        elif keys[pygame.K_LEFT]:
            self.walking = True
            self.left = True
            self.right=False
        else:
            self.walking=False
        self.move(dt)
        self.time+=dt
    def move(self,dt):
        if self.walking:
            if self.right:
                self.acceleration_x=self.world.push - self.velocity_x*abs(self.velocity_x)*self.world.resistance
            elif self.left:
                self.acceleration_x=-self.world.push - self.velocity_x*abs(self.velocity_x)*self.world.resistance
        else:
            self.acceleration_x = 0
        self.acceleration_y=self.world.gravity+self.upforce - self.velocity_y*abs(self.velocity_y)*self.world.resistance
        self.velocity_x+=self.acceleration_x*dt
        self.velocity_y+=self.acceleration_y*dt
        if self.x<=self.radius:
            self.x=self.radius+1
            self.velocity_x*=-self.world.elasticity
        elif self.x + self.radius>=WIN_WIDTH:
            self.x = WIN_WIDTH-self.radius-1
            self.velocity_x*=-self.world.elasticity
        self.x+=self.velocity_x*dt
        self.y+=self.velocity_y*dt
    def jump(self):
        if self.on_platform:
            self.velocity_y=-self.jump_velocity*self.world.jump_normal
            self.on_platform=False
            self.upforce=0
    def get_mask(self):
        pass
    def redraw(self):
        pygame.draw.circle(WIN,(255,0,0),(self.x,self.y),self.radius)

class Platform:
    def __init__(self,player,x=0,y=0,thickness=0,size=0,range=0,random=True):
        self.player=player
        if random:
            self.x=0
            self.y=y
            self.range=range
            self.size=0
            self.set_rect()
            self.thickness=0
            self.set_thickness()
        else:
            self.x=x
            self.y=y
            self.range=0
            self.size=size
            self.thickness=thickness
        self.landed=False

    def set_rect(self):
        self.size=random.randrange(75,175)
        self.x=random.randrange(-5,WIN_WIDTH-self.size+5)
        self.y=random.randrange(round(self.y-self.range/2),round(self.y+self.range/2))
    def set_thickness(self):
        self.thickness=random.randrange(100,200)/10
    def event_manager(self,event,keys):
        pass
    def general_operations_manager(self,keys,dt):
        self.detect_landed()
        self.detect_fell()
        pass
    def move(self):
        pass
    def detect_landed(self):
        if self.player.y+self.player.radius>self.y and self.player.y+self.player.radius<self.y+self.thickness*0.5 and self.player.x>self.x and self.player.x<self.x+self.size and self.player.velocity_y>=0:
            self.player.on_platform=True
            self.player.velocity_y=0
            self.player.y = self.y-self.player.radius
            self.player.upforce=-self.player.world.gravity
            self.landed=True
    def detect_fell(self):
        if self.landed and (self.player.x < self.x or self.player.x>self.x+self.size or self.player.y+self.player.radius<self.y-5):
            self.player.on_platform=False
            self.player.upforce=0
            self.landed=False
    def redraw(self):
        pygame.draw.rect(WIN,(0,0,200),(self.x,self.y,self.size,self.thickness))

def redraw_screen():
    WIN.fill((200,200,200))
    for obj in objects:
        obj.redraw()
    text=Font.render(f"Score: {player.score}",1,(255,255,0))
    WIN.blit(text,(25,25))
    pygame.display.update()

def move_all(dt):
    global objects
    global SCROLL_VELOCITY
    global next_plat
    for obj in objects:
        obj.y-=SCROLL_VELOCITY*dt
    next_plat-=SCROLL_VELOCITY*dt
#main loop
run =True
game_started=False
objects=[]
platforms=[]
next_plat=WIN_HEIGHT-150
SCROLL_VELOCITY=-50
now=0
then=0
dt=0
clock=pygame.time.Clock()
world= Physicsworld(gravity=900,elasticity=0.5,resistance=9*10**(-4),normal=300,brake_resistance=1/300,push=500,resistance_present=True)
player=Player(world,250,WIN_HEIGHT-25,2)
floor=Platform(player,0,WIN_HEIGHT-20,20,500,random=False)
platforms.append(floor)
objects.append(player)
objects.append(floor)
while run:
    clock.tick(64)
    now=pygame.time.get_ticks()
    dt=now-then
    dt/=1000
    then=now
    #event handler
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        keys=pygame.key.get_pressed()
        if not game_started and event.type==pygame.KEYDOWN:
            game_started=True
        for object in objects:
            object.event_manager(event,keys)

    #general operations
    keys = pygame.key.get_pressed()
    for object in objects:
        object.general_operations_manager(keys,dt)

    #spawn platforms
    for i,plat in enumerate(platforms):
        if plat.landed and i==len(platforms)-1:
            new_plat=Platform(player,y=next_plat,range=50)
            platforms.append(new_plat)
            objects.append(new_plat)
            next_plat-=90
            if i>0 and i<len(platforms)-1:
                objects.remove(platforms.pop(i-1))
                player.score+=5
    if game_started: move_all(dt)
    redraw_screen()

