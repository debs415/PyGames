import pygame as pg
import random

col_green = (0, 255, 0)
col_blue = (0, 0, 255)
col_white = (255, 255, 255)
col_red = (255, 0, 0)
col_grey = (200, 200, 200)

win_dim = (600, 400)
frame_rate = 60

pg.init()
display = pg.display.set_mode(win_dim)
clock = pg.time.Clock()

running = True
height = 50
player_x = 0
player_y = (win_dim[1] - height) / 2
width = 50
up_is_pressed = False
down_is_pressed = False
c=0
bullet_speed=6
bullet_height=5
bullet_width=5
class Bullet:
    def __init__(self,bullet_x,bullet_y):
        self.x=bullet_x
        self.y=bullet_y
bullets=[]
bullets.append(Bullet(win_dim[0],250))
bullets.append(Bullet(win_dim[0],175))


while running:
    # If you don't loop over the event loop your pygame app will not work!
    c=c+1
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            break
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                down_is_pressed = True
            if event.key == pg.K_UP:
                up_is_pressed = True
        if event.type == pg.KEYUP:
            if event.key == pg.K_DOWN:
                down_is_pressed = False
            if event.key == pg.K_UP:
                up_is_pressed = False
    for bullet in bullets:
        bullet.x-=bullet_speed
    if up_is_pressed == True:
        player_y-=10
        if player_y<=-5:
            player_y=395
    if down_is_pressed == True:
        player_y+=10
        if player_y>=400:
            player_y=0
    display.fill(col_blue)
    for bullet in bullets:
        pg.draw.rect(display, col_green, (bullet.x, bullet.y, bullet_width, bullet_height))
    pg.draw.rect(display, col_red, (player_x, player_y, width, height))
    pg.display.update()
    clock.tick(frame_rate)
    rand = random.randint(0,400)
    if c%15==0:
        bullets.append(Bullet(win_dim[0],rand))
    for bullet in bullets:
        if bullet.y>=player_y and bullet.y<=player_y+50 and player_x+50==bullet.x:
            running=False
            break


pg.quit()
quit()
