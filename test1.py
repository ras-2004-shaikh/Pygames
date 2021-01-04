import pygame

win = pygame.display.set_mode((500,500))
pygame.display.set_caption("Second Game")
pygame.init()
run=True
x=50
y=450
r=10
ax=0
ay=0.001
vx=0
vy=0
rx=0
ry=0
e=1
m=0
p=pygame.time.get_ticks()
print(p)
pygame.time.delay(100)
print(pygame.time.get_ticks())
while run:
    m=pygame.time.get_ticks()
    dt=m-p
    p=pygame.time.get_ticks()
    print(dt)
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        if event.type == pygame.KEYDOWN:
            k2 = pygame.key.get_pressed()
            if k2[pygame.K_UP]:
                vy -= 0.5
            elif k2[pygame.K_DOWN]:
                if vy<0:vy=0
            if k2[pygame.K_SPACE]:
                vy*=1.05
                vx*=1.05
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ax=-0.005
    if keys[pygame.K_RIGHT]:
        ax=+0.005
    if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
        ax=0
    if (not keys[pygame.K_LEFT]) and (not keys[pygame.K_RIGHT]):
        ax=0
    if keys[pygame.K_b]:
        ax = -vx/300
    rx=-vx/500
    ry=-vy/500
    vx+=ax*dt #+ rx*dt
    vy+=ay*dt #+ ry*dt
    x+=vx*dt
    y+=vy*dt
    if y>=490 and vy > 0:
        y=490
        vy=-vy*e
    if y<=10:
        vy=-vy*e
        y=10
    if x<=10:
        vx=-vx*e
        x=10
    if x>=490:
        vx=-vx*e
        x = 490
    win.fill((0,0,0))
    pygame.draw.circle(win,(255,0,0), (x,y),r)
    print(x,y)
    pygame.display.update()
pygame.quit()