import pygame as pg
import math
import random

pg.init()

font = pg.font.SysFont('arial', 24) 

WIDTH= 1000
HEIGHT = 800
screen=pg.display.set_mode([WIDTH, HEIGHT])

fps =60
timer= pg.time.Clock()

wall_thickness = 10
gravity = 0.5
bounce_stop = 0.3
mouse_trajectory = []


class Ball:
    def __init__(self, x, y, radius, color, mass, retention, x_speed, y_speed, friction, planet):
        self.xpos=x
        self.ypos=y
        self.rad=radius
        self.color=color
        self.mass=mass
        self.ret=retention
        self.ys=y_speed
        self.xs=x_speed
        self.circle=''
        self.selected = False
        self.friction = friction
        self.planet = planet

    def draw(self):
        shadow_color = tuple(max(c-80, 0) for c in pg.Color(self.color)[:3])
        pg.draw.circle(screen, shadow_color, (self.xpos + self.rad * 0.15, self.ypos + self.rad * 0.15), self.rad)
        self.circle = pg.draw.circle(screen, self.color, (self.xpos, self.ypos), self.rad)
        


    def check_gravity(self):
        if self.ypos < self.rad + (wall_thickness/2) and self.ys < 0:
            self.ys *= -1 * self.ret
            if abs(self.ys) < bounce_stop:
                self.ys = 0
        if not self.selected:
            if self.ypos < HEIGHT - self.rad - (wall_thickness/2):
                self.ys += gravity
            else:
                if self.ys > bounce_stop:
                    self.ys = self.ys * -self.ret
                else:
                    if abs(self.ys) <= bounce_stop:
                        self.ys = 0
        if(self.xpos < self.rad + (wall_thickness/2) and self.xs < 0) or (self.xpos > WIDTH - self.rad - wall_thickness and self.xs > 0):
            self.xs *= -1 * self.ret
            if abs(self.xs) < bounce_stop:
                self.xs = 0
        if self.ys == 0 and self.xs != 0:
            if self.xs > 0:
                self.xs -= self.friction
            elif self.xs < 0:
                self.xs += self.friction
        return self.ys

    def update_pos(self, mouse):
        if not self.selected:
            self.ypos += self.ys
            self.xpos += self.xs
        else:
            self.xpos = mouse[0]
            self.ypos = mouse[1]

    def check_interaction(self, pos):
        self.selected = False
        if self.circle.collidepoint(pos):
            self.selected = True
        return self.selected

    def release(self, x_speed, y_speed):
        self.xs = x_speed
        self.ys = y_speed

def draw_walls():
    left=pg.draw.line(screen, 'white',(0,0), (0, HEIGHT), wall_thickness)
    right=pg.draw.line(screen, 'white',(WIDTH,0), (WIDTH, HEIGHT), wall_thickness)
    top=pg.draw.line(screen, 'white',(0,0), (WIDTH, 0), wall_thickness)
    bottom=pg.draw.line(screen, 'white',(0,HEIGHT), (WIDTH, HEIGHT), wall_thickness)
    return left, right, top, bottom

def calc_motion_vector():
    x_speed = 0
    y_speed = 0
    if len(mouse_trajectory) > 10:
        x_speed = (mouse_trajectory[-1][0] - mouse_trajectory[0][0]) / len(mouse_trajectory)
        y_speed = (mouse_trajectory[-1][1] - mouse_trajectory[0][1]) / len(mouse_trajectory)
    return x_speed, y_speed

def handle_colissions(balls):
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            ball1 = balls[i]
            ball2 = balls[j]
            dx = ball2.xpos - ball1.xpos
            dy = ball2.ypos - ball1.ypos
            dist = math.hypot(dx, dy)
            min_dist = ball2.rad + ball1.rad
            if dist < min_dist and dist > 0:
                nx = dx/dist
                ny = dy/dist

                overlap = min_dist - dist
                ball1.xpos -= nx * overlap / 2
                ball1.ypos -= ny * overlap / 2
                ball2.xpos += nx * overlap / 2 
                ball2.ypos += ny * overlap / 2

                dvx = ball2.xs - ball1.xs
                dvy = ball2.ys - ball1.ys
                vel_along_normal = dvx * nx + dvy * ny

                if vel_along_normal > 0:
                    continue

                restitution = min(ball1.ret, ball2.ret)
                impulse = -(1+restitution) * vel_along_normal / (1/ball1.mass + 1/ball2.mass)

                ball1.xs -= (impulse * nx) / ball1.mass
                ball1.ys -= (impulse * ny) / ball1.mass
                ball2.xs += (impulse * nx) / ball2.mass
                ball2.ys += (impulse * ny) / ball2.mass


ball1=Ball(112, 50, 50, 'rosybrown', 37.7, 0.55, 0, 0, 0.015, "Mercury")
ball2=Ball(237, 50, 50, 'burlywood', 90.4, 0.35, 0, 0, 0.09, "Venus")
ball3=Ball(362, 50, 50, 'darkgreen', 100, 0.65, 0, 0, 0.04, "Earth")
ball4=Ball(487, 50, 50, 'firebrick', 37.9, 0.5, 0, 0, 0.025, "Mars")
ball5=Ball(599, 50, 50, 'darkorange', 252.7, 0.85, 0, 0, 0.01, "Jupiter")
ball6=Ball(711, 50, 50, 'darkgoldenrod', 106.4, 0.8, 0, 0, 0.012, "Saturn")
ball7=Ball(823, 50, 50, 'teal', 88.6, 0.9, 0, 0, 0.008, "Uranus")
ball8=Ball(935, 50, 50, 'blue', 113.7, 0.92, 0, 0, 0.007, "Neptune")


balls = [ball1, ball2, ball3, ball4, ball5, ball6, ball7, ball8]

stars = []
for i in range(20):
    for i in range(20):
        star_x = random.randint(0, WIDTH)
        star_y = random.randint(0, HEIGHT)
        star_size = random.choice([1, 1, 1, 2])
        stars.append((star_x, star_y, star_size))

run = True
while run: 
    timer.tick(fps)
    screen.fill('black')
    for star in stars:
        pg.draw.circle(screen, 'white', (star[0], star[1]), star[2])

    mouse_coords = pg.mouse.get_pos()
    mouse_trajectory.append(mouse_coords)
    if len(mouse_trajectory) > 20:
        mouse_trajectory.pop(0)
    x_push, y_push = calc_motion_vector()

    walls= draw_walls()
    for ball in balls:
        ball.draw()
    for ball in balls:
        ball.update_pos(pg.mouse.get_pos())

    y_offset = 10
    for ball in balls:
        label = font.render(f"{ball.planet}: mass {ball.mass}", True, ball.color)
        screen.blit(label, (WIDTH-label.get_width()- 10, y_offset))
        y_offset += 30

    handle_colissions(balls)

    for ball in balls:
        ball.ys = ball.check_gravity()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for ball in balls:
                    ball.check_interaction(event.pos)

        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                for ball in balls:
                    if ball.selected:
                        ball.release(x_push, y_push)
                for ball in balls:
                    ball.check_interaction((-1000, -1000))

    pg.display.flip()
pg.quit()

