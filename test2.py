import pygame

pygame.init()
size = {'x':1024 , 'y':800}
back_color=(0,0,0)

win=pygame.display.set_mode((size['x'],size['y']))

#pysics machine/world
class physicsworld:
    def __init__(self,gravity,elasticity,resistance,normal,brake_resistance,push,resistance_present=True):
        self.gravity=gravity
        self.elasticity=elasticity
        self.resistance=resistance * int(resistance_present)
        self.jump_normal=normal
        self.brake_resistance=brake_resistance
        self.push=push

#bouncy ball
class ball:
    def __init__(self,color,pos,radius,elasticity,resistance,response,key_set,world):
        self.pos={'x':pos[0],'y':pos[1]}
        self.radius=radius
        self.elasticity=elasticity
        self.resistance=resistance
        self.response=response
        self.world=world
        self.left_key=key_set[0]
        self.right_key=key_set[1]
        self.jump_key=key_set[2]
        self.brake_key=key_set[3]
        self.brake_jump_key=key_set[4]
        self.speeding_key=key_set[5]
        self.color=color
        self.right=False
        self.left=False
        self.braking=False
        self.speeding=False
        self.velocity={'x':0,'y':0}
        self.acceleration={'x':0,'y':self.world.gravity}
    def move(self,dt):
        if self.left:
            self.acceleration['x']=-self.response * self.world.push
        elif self.right:
            self.acceleration['x']=self.response * self.world.push
        else:
            self.acceleration['x']=0
        if self.left and self.right:
            self.acceleration['x']=0
        if self.braking:
            self.acceleration['x'] = -self.world.brake_resistance * self.velocity['x']
        if self.speeding:
            self.velocity['x']*=1.0005
            self.velocity['y']*=1.0005
        self.velocity['x']+=(self.acceleration['x'] - self.velocity['x']*self.resistance*self.world.resistance) * dt
        self.velocity['y']+=(self.acceleration['y'] - self.velocity['y']*self.resistance*self.world.resistance) * dt
        self.pos['x']+=self.velocity['x']*dt
        self.pos['y']+=self.velocity['y']*dt
        if self.pos['x'] <= self.radius:
            self.bounce('x')
            self.pos['x']=self.radius
        elif self.pos['x'] >= size['x'] - self.radius:
            self.bounce('x')
            self.pos['x']=size['x'] - self.radius
        if self.pos['y'] <= self.radius:
            self.bounce('y')
            self.pos['y']=self.radius*1.00005
        elif self.pos['y'] >= size['y'] - self.radius:
            self.bounce('y')
            self.pos['y']=size['y'] - self.radius
    def bounce(self,direction):
        self.velocity[direction]*=-self.elasticity*self.world.elasticity
    def event_Manager(self,event,keys):
        if event.type==pygame.KEYDOWN:
            if keys[self.jump_key]:
                self.jump()
            if keys[self.brake_jump_key]:
                self.brake_jump()
    def general_operations_manager(self,keys,dt):
        self.left=keys[self.left_key]
        self.right=keys[self.right_key]
        self.braking=keys[self.brake_key]
        self.speeding=keys[self.speeding_key]
        self.move(dt)
    def jump(self):
        self.velocity['y']-=self.response*self.world.jump_normal
    def brake_jump(self):
        if self.velocity['y']<0:
            self.velocity['y']=0
    def redraw(self,win):
        pygame.draw.circle(win,self.color,(self.pos['x'],self.pos['y']),self.radius)

def redraw_screen():
    win.fill(back_color)
    for obj in objects:
        obj.redraw(win)
    pygame.display.update()


#main loop
run=True
world= physicsworld(gravity=0.001,elasticity=1,resistance=0.1,normal=250,brake_resistance=1/300,push=2,resistance_present=False)
objects = []
objects.append(ball(color=(255,0,0),pos=(50,450),radius=5,elasticity=1,resistance=0.001,response=0.001,key_set=(pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_b,pygame.K_DOWN,pygame.K_SPACE),world=world))
prev_time = pygame.time.get_ticks()
time=0
while run:
    pygame.time.delay(1)
    time=pygame.time.get_ticks()
    dt = time-prev_time
    prev_time=time
    #event checker / Single key presses / quit
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        keys=pygame.key.get_pressed()
        for obj in objects:
            obj.event_Manager(event,keys)
    #long press checker
    keys=pygame.key.get_pressed()
    for obj in objects:
        obj.general_operations_manager(keys,dt)
    redraw_screen()

pygame.quit()