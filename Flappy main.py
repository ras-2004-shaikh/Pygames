import pygame
import os
import neat
import random
pygame.init()
game_started=False
start=pygame.time.get_ticks()
count1=0
count2=0
class Physicsworld:
    def __init__(self,gravity,elasticity,resistance,normal,brake_resistance,push,resistance_present=True):
        self.gravity=gravity
        self.elasticity=elasticity
        self.resistance=resistance * int(resistance_present)
        self.jump_normal=normal
        self.brake_resistance=brake_resistance
        self.push=push

class Bird:
    IMGS = [pygame.transform.scale(pygame.image.load("Flappy/Bird1.png"),(50,27)),pygame.transform.scale(pygame.image.load("Flappy/Bird1.png"),(50,27)),pygame.transform.scale(pygame.image.load("Flappy/Bird2.png"),(50,27)),pygame.transform.scale(pygame.image.load("Flappy/Bird3.png"),(50,27))]
    MAX_ROTATION=25
    ANIMATION_TIME=0.18
    ROT_VEL=100
    def __init__(self,pos,size,response,world,keys=(pygame.K_SPACE,0)):
        self.tag="player"
        self.pos={'x':pos[0],'y':pos[1]}
        self.size = {'x': size[0], 'y': size[1]}
        self.response=response
        self.jump_key=keys[0]
        self.velocity=0
        self.world=world
        self.acceleration=self.world.gravity
        self.anime_count=0
        self.tilt=0
        self.img=self.IMGS[0]
    def redraw(self,screen):
        self.img=self.IMGS[int(self.anime_count/self.ANIMATION_TIME)%4]
        if self.tilt<=-60:
            self.img=self.IMGS[2]
        rotated_img=pygame.transform.rotate(self.img,self.tilt)
        new_rect=rotated_img.get_rect(center=self.img.get_rect(topleft=(self.pos['x'],self.pos['y'])).center)
        screen.blit(rotated_img,new_rect)
        if self.anime_count/self.ANIMATION_TIME >=4:
            self.anime_count=0
        pygame.display.update()
    def event_manager(self,event,keys):
        global game_started
        global start
        if event.type == pygame.KEYDOWN:
            if keys[self.jump_key]:
                if not game_started:
                    game_started=True
                    start=pygame.time.get_ticks()
                self.jump()
    def general_operations_manager(self,keys,dt):
        self.move(dt)
        pass
    def move(self,dt):
        global game_started
        if game_started:
            self.velocity+=(self.acceleration - self.velocity * abs(self.velocity) * self.world.resistance)*dt
            self.pos['y']+=self.velocity*dt
            if self.velocity<0:
                self.tilt=self.MAX_ROTATION
            else:
                if self.tilt>-90:
                    self.tilt-=self.ROT_VEL*dt
        else:
            pass
        self.anime_count+=dt
    def jump(self):
        self.velocity=-self.response*self.world.jump_normal
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Screen:
    def __init__(self,pos,size,objects=[],velocity=500):
        self.pos={'x':pos[0],'y':pos[1]}
        self.size={'x':size[0],'y':size[1]}
        self.rect=(pos[0],pos[1],size[0],size[1])
        self.WIN = pygame.display.set_mode((600, 600))
        self.BG = pygame.image.load("Flappy/BG.png")
        self.BG.set_alpha(175)
        self.scroll = self.pos['x'] + self.size['x']/2
        self.scroll_vel = velocity
        self.BG_pos = [(0, 0)]
        self.objects=objects
        self.dir=0
    def event_manager(self,event,keys):
        pass
    def general_operations_manager(self,keys,dt):
        self.dir=-1
        self.move(dt)
    def move(self,dt):
        self.scroll += self.scroll_vel * self.dir*dt
        self.scroll %= 600
        if self.scroll < 300:
            self.BG_pos = [(self.scroll - 300, 0), (self.scroll + 300, 0)]
        elif self.scroll > 300:
            self.BG_pos = [(self.scroll - 300, 0), (self.scroll - 900, 0)]
        else:
            self.BG_pos = [(0, 0)]
    def redraw(self):
        global count2
        self.WIN.fill((235,240,255))
        for rect in self.BG_pos:
            self.WIN.blit(self.BG, rect)
        for obj in self.objects:
            if obj.tag=="enemy" and obj.passed:
                self.objects.remove(obj)
            obj.redraw(self.WIN)
        count2+=1
        pygame.display.update()

class Pipe:
    GAP = 100
    def __init__(self,screen,x,player):
        self.tag="enemy"
        self.x=x
        self.player = player
        self.screen=screen
        self.PIPE_BOTTOM = pygame.image.load("Flappy/Pipe.png")
        self.PIPE_TOP = pygame.transform.rotate(self.PIPE_BOTTOM, 180)
        self.vel=self.screen.scroll_vel
        self.height=0
        self.top=0
        self.bottom=0
        self.width=self.PIPE_TOP.get_width()
        self.length=self.PIPE_TOP.get_height()
        self.passed=False
        self.set_height()
    def set_height(self):
        self.height = random.randrange(50,380)
        self.top=self.height - self.PIPE_TOP.get_height()
        self.bottom=self.height+self.GAP
    def event_manager(self,event,keys):
        pass
    def general_operations_manager(self,keys,dt):
        self.move(dt)
    def move(self,dt):
        self.x-=self.vel*dt
        if self.x + self.width <= self.player.pos['x']:
            self.passed=True
    def redraw(self,window):
        global count1
        window.blit(self.PIPE_TOP,(self.x,self.top,self.width,self.length))
        window.blit(self.PIPE_BOTTOM,(self.x,self.bottom,self.width,self.length))
        count1+=1

#Main loop
run=True
clock=pygame.time.Clock()
world=Physicsworld(gravity=1200,elasticity=1,resistance=0.00390625,normal=105,brake_resistance=1/300,push=2,resistance_present=True)
bird1=Bird((100,50),(50,27),3.5,world,(pygame.K_SPACE,0))
game_objects=[]
game_objects.append(bird1)
SCREEN = Screen((0,0),(600,600),game_objects,400)
prev_time=pygame.time.get_ticks()
while run:
    clock.tick(200)
    time=pygame.time.get_ticks()
    dt = time-prev_time
    dt/=1000.0
    prev_time=time
    #event checker / Single key presses / quit
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        keys=pygame.key.get_pressed()
        for obj in SCREEN.objects:
            obj.event_manager(event,keys)
        SCREEN.event_manager(event,keys)
    #long press checker
    keys=pygame.key.get_pressed()
    for obj in SCREEN.objects:
        obj.general_operations_manager(keys,dt)
    SCREEN.general_operations_manager(keys,dt)
    if pygame.time.get_ticks() >= start+1000 and game_started:
        print("here")
        pipe = Pipe(SCREEN,650,bird1)
        SCREEN.objects.append(pipe)
        start=pygame.time.get_ticks()
    SCREEN.redraw()
pygame.quit()

