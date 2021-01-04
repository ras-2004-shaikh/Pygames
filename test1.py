import pygame
wd=1024
he=512
win = pygame.display.set_mode((wd,he))
pygame.display.set_caption("Second Game")
pygame.init()
run=True
r=5
ax=0
ay=0.001
vx=0
vy=0
rx=0
ry=0
e=1
m=0
x=r+50
y=he-r-50
p=pygame.time.get_ticks()
print(p)
pygame.time.delay(100)
print(pygame.time.get_ticks())
while run:
    m=pygame.time.get_ticks()
    dt=m-p
    p=pygame.time.get_ticks()
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
    rx=-vx/600
    ry=-vy/600
    vx+=ax*dt #+ rx*dt
    vy+=ay*dt #+ ry*dt
    x+=vx*dt
    y+=vy*dt
    if y>=he-r and vy > 0:
        y=he-r
        vy=-vy*e
    if y<=r:
        vy=-vy*e
        y=r
    if x<=r:
        vx=-vx*e
        x=r
    if x>=wd-r:
        vx=-vx*e
        x = wd-r
    win.fill((0,0,0))
    pygame.draw.circle(win,(255,0,0), (x,y),r)
    print(x,y)
    pygame.display.update()
pygame.quit()
