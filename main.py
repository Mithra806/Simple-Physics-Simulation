import pygame as pg

pg.init() 

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
    def __init__(self, x, y, radius, color, mass, retention, y_speed, x_speed, ball_id, friction):
        self.xpos=x
        self.ypos=y
        self.rad=radius
        self.color=color
        self.mass=mass
        self.ret=retention
        self.ys=y_speed
        self.xs=x_speed
        self.id=ball_id
        self.circle=''
        self.selected = False
        self.friction = friction

    def draw(self):
        self.circle = pg.draw.circle(screen, self.color, (self.xpos, self.ypos), self.rad)

    def check_gravity(self):
        if not self.selected:
            if self.ypos < HEIGHT - self.rad - (wall_thickness/2):
                self.ys += gravity
            else:
                if self.ys > bounce_stop:
                    self.ys = self.ys * -self.ret
                else:
                    if abs(self.ys) <= bounce_stop:
                        self.ys = 0
        if(self.xpos < self.rad + (wall_thickness/2) and self.xs < 0) or (self.x_pos > WIDTH -self.radius -wall_thickness and self.xs > 0):   
            self.xs *= -1 * self.ret
            if abs(self.xs) < bounce_stop:
                self.x_speed = 0
        if self.ys == 0 and self.xs != 0:
            if self.xs > 0:
                self.xs -= self.friction
            elif self.x_speed < 0:
                self.x_speed += self.friction
        else:
            self.xs = x_push
            self.ys = y_push
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

def draw_walls():
    left=pg.draw.line(screen, 'white',(0,0), (0, HEIGHT), wall_thickness)
    right=pg.draw.line(screen, 'white',(WIDTH,0), (WIDTH, HEIGHT), wall_thickness)
    top=pg.draw.line(screen, 'white',(0,0), (WIDTH, 0), wall_thickness)
    bottom=pg.draw.line(screen, 'white',(0,HEIGHT), (WIDTH, HEIGHT), wall_thickness)
    return left, right, top, bottom

def calc_motion_vector():
    x_speed = 0
    y_speed = 0
    if len(mouse_trajectory) >10:
        x_speed = (mouse_trajectory[-1][0] - mouse_trajectory[0][0]) /len(mouse_trajectory)
        X_speed = (mouse_trajectory[-1][1] -mouse_trajectory[0][1])/len(mouse_trajectory)
    return x_speed, y_speed


ball1=Ball(50, 50, 30, 'orange', 100, 0.6, 0, 0, 1, 0.02);
ball2=Ball(500, 500, 50, 'blue', 300, 1.0, 0, 0, 2, 0.03);
ball3=Ball(300, 300, 50, 'yellow', 300, 0.8, 0, 0, 3, 0.04);
ball4=Ball(700, 700, 50, 'red', 300, 0.9, 0, 0, 4, 0.05);
balls = [ball1, ball2, ball3, ball4]

run = True
while run: 
    timer.tick(fps)
    screen.fill('black')
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

    ball1.ys = ball1.check_gravity()
    ball2.ys = ball2.check_gravity()
    ball3.ys = ball3.check_gravity()
    ball4.ys = ball4.check_gravity()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if ball1.check_interaction(event.pos) or ball2.check_interaction(event.pos) or ball3.check_interaction(event.pos) or ball4.check_interaction(event.pos):
                    active_select=True
        if event.type == pg.MOUSEBUTTONUP:
            if event.button==1:
                active_select=False
                for i in range(len(balls)):
                    balls[i].check_interaction((-1000, -1000))

    pg.display.flip()
pg.quit()

