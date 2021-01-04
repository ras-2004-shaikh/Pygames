import pygame
wd=1024
he=512
win = pygame.display.set_mode((wd,he))
pygame.display.set_caption("Second Game")
pygame.init()
run=True
radius=5
ax=0
ay=0.001
vx=0
vy=0
resistX=0
resistY=0
elasticity=1
new_time=0
x=radius+50
y=he-radius-50
time=pygame.time.get_ticks()
print(time)
pygame.time.delay(100)
print(pygame.time.get_ticks())
while run:
    new_time=pygame.time.get_ticks()
    dt=new_time-time
    time=pygame.time.get_ticks()
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        if event.type == pygame.KEYDOWN:
            k2 = pygame.key.get_pressed()
            if k2[pygame.K_UP]:
                vy -= 0.25
            elif k2[pygame.K_DOWN]:
                if vy<0:vy=0
            if k2[pygame.K_SPACE]:
                vy*=1.05
                vx*=1.05
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ax=-0.002
    if keys[pygame.K_RIGHT]:
        ax=+0.002
    if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
        ax=0
    if (not keys[pygame.K_LEFT]) and (not keys[pygame.K_RIGHT]):
        ax=0
    if keys[pygame.K_b]:
        ax = -vx/300
    resistX=-vx/600
    resistY=-vy/600
    vx+=ax*dt #+ resistX*dt
    vy+=ay*dt #+ resistY*dt
    x+=vx*dt
    y+=vy*dt
    if y>=he-radius and vy > 0:
        y=he-radius
        vy=-vy*elasticity
    if y<=radius:
        vy=-vy*elasticity
        y=radius
    if x<=radius:
        vx=-vx*elasticity
        x=radius
    if x>=wd-radius:
        vx=-vx*elasticity
        x = wd-radius
    win.fill((0,0,0))
    pygame.draw.circle(win,(255,0,0), (x,y),radius)
    print(x,y)
    pygame.display.update()
pygame.quit()
