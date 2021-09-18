import math
import pygame as pg
import random

pg.init()
window_width = 500
window_height = 500
display = pg.display.set_mode((window_width, window_height))
clock = pg.time.Clock()
quit = False

bullets = []
asteroids = []

FRAME_RATE = 60
BULLET_SPEED = 6
MAX_BULLETS = 20
MAX_BULLET_AGE = 180
TURN_SPEED = 6  # In degrees
BULLET_RADIUS = 2
BIG_ASTEROID_RADIUS = 32
MEDIUM_ASTEROID_RADIUS = 16
MINI_ASTEROID_RADIUS = 8
TICKS_PER_ASTEROID = 90
MIN_ASTEROID_SPEED = 1
MAX_ASTEROID_SPEED = 5
SHIP_ACCELERATION = 0.1

EPSILON = 0.000000000001


def point_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def line_distance(line, point):
    px, py = point
    lx1, ly1 = line[0]
    lx2, ly2 = line[1]

    # We express both `line` and its perpendicular that passes through `point`
    # in terms of m and c, where:
    # y = mx + c
    line_m = (ly2 - ly1) / ((lx2 - lx1) or EPSILON)
    line_c = ly1 - line_m * lx1

    perp_m = -1/(line_m or EPSILON)
    # We compute perpendiculars passing through the start and end points of
    # `line` and check whether `point` lies between those two perpendiculars.
    # If so, we compute distance to the line. If not, we compute distance to
    # the two points.
    perp_c1 = ly1 - perp_m * lx1
    perp_c2 = ly2 - perp_m * lx2
    perp_c = py - perp_m * px

    if (
        (perp_c > perp_c1 and perp_c > perp_c2)
        or (perp_c < perp_c1 and perp_c < perp_c2)
    ):
        return min(point_distance(line[0], point),
                   point_distance(line[1], point))

    # We find the intercept of the two lines, i.e. where
    # y = perp_m * x + perp_c = line_m * x + line_c
    # So
    # perp_c - line_c = line_m * x - perp_m * x
    # So
    # (perp_c - line_c) / x = line_m - perp_m
    # So
    # x / (perp_c - line_c) = 1 / (line_m - perp_m)
    # So
    # x = (perp_c - line_c) / (line_m - perp_m)
    intersection_x = (perp_c - line_c) / (line_m - perp_m)
    intersection_y = line_m * intersection_x + line_c

    return point_distance((px, py), (intersection_x, intersection_y))


def all_positions(point):
    """
    Given a point that may be near the edge of the screen, returns a list of
    points, one of which is the one passed and the rest of which are the result
    of adding or subtracting the windows width or height or both to the point.

    By rendering an object at all 9 of these locations at once (most of which
    will be off-screen), we can make the object smoothly pass from one side of
    the screen to the other, without things popping in or out of existence at
    the screen edges.
    """
    x, y = point
    return [
        (x - window_width, y - window_height),
        (x, y - window_height),
        (x + window_width, y - window_height),
        (x - window_width, y),
        (x, y),
        (x + window_width, y),
        (x - window_width, y + window_height),
        (x, y + window_height),
        (x + window_width, y + window_height),
    ]


class Ship:
    def __init__(self):
        self.angle = 0  # In radians
        self.position = (window_width / 2, window_height / 2)
        self.velocity = (0, 0)

    def points(self):
        """
        Returns the co-ordinates of the points of the ship.
        """
        front_distance = 15
        bl_distance = 5
        br_distance = 5
        front_angle = self.angle
        bl_angle = self.angle - math.radians(135)
        br_angle = self.angle + math.radians(135)

        front = (self.position[0] + front_distance * math.sin(front_angle),
                 self.position[1] - front_distance * math.cos(front_angle))
        bl = (self.position[0] + bl_distance * math.sin(bl_angle),
              self.position[1] - bl_distance * math.cos(bl_angle))
        br = (self.position[0] + br_distance * math.sin(br_angle),
              self.position[1] - br_distance * math.cos(br_angle))

        return [front, bl, br]

    def lines(self):
        true_front, true_back_left, true_back_right = self.points()
        front_points = all_positions(true_front)
        back_left_points = all_positions(true_back_left)
        back_right_points = all_positions(true_back_right)
        for front, back_left, back_right in \
                zip(front_points, back_left_points, back_right_points):
            yield (front, back_right)
            yield (back_right, back_left)
            yield (back_left, front)

    def shoot(self):
        if len(bullets) >= MAX_BULLETS:
            return
        bullet_start = self.points()[0]
        bullets.append(Bullet(bullet_start, self.angle))

    def accelerate(self):
        vx, vy = self.velocity
        vx += SHIP_ACCELERATION * math.sin(self.angle)
        vy -= SHIP_ACCELERATION * math.cos(self.angle)
        self.velocity = vx, vy

    def update_position(self):
        x, y = self.position
        vx, vy = self.velocity
        x = (x + vx) % window_width
        y = (y + vy) % window_height
        self.position = x, y

    def draw(self):
        for line in self.lines():
            pg.draw.line(display, (255, 255, 255), line[0], line[1], 3)


class Bullet:
    def __init__(self, position, angle):
        self.position = position
        self.angle = angle
        self.age = 0  # Number of ticks this bullet has existed for

    def update(self):
        self.age += 1
        x, y = self.position
        if self.age > MAX_BULLET_AGE:
            bullets.remove(self)
        else:
            self.position = (
                (x + BULLET_SPEED * math.sin(self.angle)) % window_width,
                (y - BULLET_SPEED * math.cos(self.angle)) % window_height,
            )

    def draw(self):
        for x, y in all_positions(self.position):
            pg.draw.circle(display,
                           (180, 180, 180),
                           (round(x), round(y)),
                           BULLET_RADIUS)


class Asteroid:
    def __init__(self, position, angle, speed, radius):
        self.position = position
        self.angle = angle
        self.speed = speed
        self.radius = radius

    def update(self):
        x, y = self.position
        self.position = (
            (x + self.speed * math.sin(self.angle)) % window_width,
            (y - self.speed * math.cos(self.angle)) % window_height,
        )

    def draw(self):
        for x, y in all_positions(self.position):
            pg.draw.circle(display,
                           (165, 42, 42),
                           (round(x), round(y)),
                           self.radius)

    def explode(self):
        """
        If this asteroid is big or medium, split it into two smaller asteroids
        travelling in random directions.

        Otherwise, destroy it completely.
        """
        asteroids.remove(self)
        if self.radius == MINI_ASTEROID_RADIUS:
            return
        if self.radius == BIG_ASTEROID_RADIUS:
            new_radius = MEDIUM_ASTEROID_RADIUS
        else:
            new_radius = MINI_ASTEROID_RADIUS
        for i in range(2):
            random_angle = random.random() * math.tau
            new_asteroid = \
                Asteroid(self.position, random_angle, self.speed, new_radius)
            asteroids.append(new_asteroid)

    @staticmethod
    def add_random_asteroid():
        # Insert the asteroid from a randomly-selected edge
        if random.random() < 0.5:
            random_position = (
                random.random() * window_width,
                0
            )
        else:
            random_position = (
                0,
                random.random() * window_height
            )
        random_angle = random.random() * math.tau
        random_speed = (MIN_ASTEROID_SPEED
                        + random.random() * (MAX_ASTEROID_SPEED
                                             - MIN_ASTEROID_SPEED))

        asteroid = Asteroid(
            random_position,
            random_angle,
            random_speed,
            BIG_ASTEROID_RADIUS
        )
        asteroids.append(asteroid)


ship = Ship()

left = False
right = False
space = False
up = False
ship_destroyed = False
ticks_to_next_asteroid = TICKS_PER_ASTEROID
survival_ticks = 0

while not quit:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                left = True
            if event.key == pg.K_RIGHT:
                right = True
            if event.key == pg.K_UP:
                up = True
            if event.key == pg.K_SPACE and not space:
                space = True
                ship.shoot()
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                left = False
            if event.key == pg.K_RIGHT:
                right = False
            if event.key == pg.K_UP:
                up = False
            if event.key == pg.K_SPACE:
                space = False
    if left and not right:
        ship.angle -= math.radians(TURN_SPEED)
    if right and not left:
        ship.angle += math.radians(TURN_SPEED)

    ticks_to_next_asteroid -= 1
    if ticks_to_next_asteroid <= 0:
        Asteroid.add_random_asteroid()
        ticks_to_next_asteroid = TICKS_PER_ASTEROID

    display.fill((30, 0, 100))
    if up:
        ship.accelerate()
    ship.update_position()
    ship.draw()

    for asteroid in asteroids.copy():
        for line in ship.lines():
            ship_distance = line_distance(line, asteroid.position)
            if ship_distance < asteroid.radius:
                ship_destroyed = True

        for bullet in bullets.copy():
            bullet_distance = point_distance(bullet.position, asteroid.position)
            if bullet_distance < asteroid.radius + BULLET_RADIUS:
                asteroid.explode()
                bullets.remove(bullet)
                break

    for bullet in bullets:
        bullet.update()
        bullet.draw()
    for asteroid in asteroids:
        asteroid.update()
        asteroid.draw()

    pg.display.update()
    clock.tick(FRAME_RATE)
    if ship_destroyed:
        break
    survival_ticks += 1

display.fill((255, 0, 0))
survival_time = int(survival_ticks / FRAME_RATE)
font = pg.font.Font(None,55)
text = font.render("You survived for:", True , (255, 255, 255))
text2 = font.render("%i seconds" % survival_time, True, (255, 255, 255))
display.blit(text, ((window_width - text.get_size()[0]) / 2, 85))
display.blit(text2, ((window_width - text2.get_size()[0]) / 2, 185))
pg.display.update()
while not quit:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit = True
            break
