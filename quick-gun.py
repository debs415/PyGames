import pygame as pg
import random
col_green = (0, 255, 0)
col_blue = (0, 0, 255)
col_white = (255, 255, 255)
col_red = (255, 0, 0)
col_grey = (200, 200, 200)
col_black = (0,0,0)

win_dim = (700, 400)
clock_freq = 60

pg.init()
display = pg.display.set_mode(win_dim)
pg.display.set_caption('Quick Gun')
clock = pg.time.Clock()

class bullet_down:
    def __init__(self, x, y):
        self.x = x       
        self.y = y

    def draw(self):
        pg.draw.rect(display, col_white, (self.x, self.y, 10, 10))
    def update_position(self):
        self.y+=15

class bullet_up:
    def __init__(self, x, y):
        self.x = x
        self.y = y
            
    def draw(self): 
        pg.draw.rect(display, col_white, (self.x, self.y, 10, 10))
    def update_position(self):
        self.y-=15
running = True
x = 100
x2 = 100
i = 0
is_red = True
left_is_down = False
right_is_down = False
left2_is_down = False
right2_is_down = False
ticks_per_block = 2* clock_freq
ticks_to_next_block = 0
bullets1 = []
bullets2 = []
while running:
   
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            break
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
                break
            if event.key == pg.K_RIGHT:
                right_is_down = True
            if event.key == pg.K_LEFT:
                left_is_down = True
            if event.key == pg.K_a:
                left2_is_down = True
            if event.key == pg.K_d:
                right2_is_down = True
            if event.key == pg.K_UP:
                bullets1.append(bullet_up(x+49, 350))
                i +=  1
            if event.key == pg.K_w:
                bullets2.append(bullet_down(x2+49,0))

        if event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                right_is_down = False
            if event.key == pg.K_LEFT:
                left_is_down = False
            if event.key == pg.K_d:
                right2_is_down = False
            if event.key == pg.K_a:
                left2_is_down = False

    if right_is_down:
        x+=10
        if x>730:
            x = 0
    if left_is_down:
        x-=10
        if x<-30:
            x = 700

    if right2_is_down:
        x2+=10
        if x2>730:
            x2 = 0

    if left2_is_down:
        x2-=10
        if x2<-30:
            x2 = 700

    for bullet in bullets1:
        bullet.update_position()
        if not((bullet.y>50) or (bullet.x + 10)<x2 or bullet.x > (x2 + 100)):
            running = False
            print('Lower player wins')
        if (bullet.y < 0):
                bullets1.pop();
    for bullet in bullets2:
         bullet.update_position()  
         if not((bullet.y<350) or (bullet.x + 10)<x or bullet.x > (x + 100)):
            running = False
            print('Upper player wins')
         if (bullet.y > 400):
                bullets2.pop();
    display.fill(col_black)
    for bullet in bullets1:
        bullet.draw()
    for bullet in bullets2:
        bullet.draw()
    pg.draw.rect(display, col_red, (x, 350, 100, 50))
    pg.draw.rect(display, col_red, (x2, 0, 100, 50))
    pg.display.update()
    clock.tick(clock_freq)

pg.quit()
quit()



# print('bx: ', bullet.x)
        # print('by: ', bullet.y)
        # print('x: ', x)
        # print((bullet.y + 10)>0, )
        # print((bullet.y>10))
        # print(bullet.x > (x + 100))
