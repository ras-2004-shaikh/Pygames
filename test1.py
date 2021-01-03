import pygame

win = pygame.display.set_mode((500,500))
pygame.display.set_caption("Second Game")

run=True
x=50
y=450
r=10
ax=0
ay=1
vx=0
vy=0
rx=0
ry=0
while run:
    pygame.time.delay(75)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        if event.type == pygame.KEYDOWN:
            k2 = pygame.key.get_pressed()
            if k2[pygame.K_UP]:
                vy -= 10
            elif k2[pygame.K_DOWN]:
                if vy<0:vy=0
            if k2[pygame.K_SPACE]:
                vy*=1.05
                vx*=1.05
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ax=-3
    if keys[pygame.K_RIGHT]:
        ax=+3
    if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
        ax=0
    if (not keys[pygame.K_LEFT]) and (not keys[pygame.K_RIGHT]):
        ax=0
    if keys[pygame.K_b]:
        ax = -vx/3
    rx=-vx/50
    ry=-vy/50
    vx+=ax #+ rx
    vy+=ay #+ ry
    x+=vx
    y+=vy
    if y>=490 and vy > 0:
        y=490
        vy=-vy
    if y<=10:
        vy=-vy
        y=10
    if x<=10:
        vx=-vx
        x=10
    if x>=490:
        vx=-vx
        x = 490
    win.fill((0,0,0))
    pygame.draw.circle(win,(255,0,0), (x,y),r)
    print(x,y)
    pygame.display.update()
pygame.quit()
