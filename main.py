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

class Ball:
    def __init__(self, x, y, radius, color, mass, retention, y_speed, x_speed, ball_id):
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

    def draw(self):
        self.circle = pg.draw.circle(screen, self.color, (self.xpos, self.ypos), self.rad)

    def check_gravity(self):
        if self.ypos < HEIGHT - self.rad - (wall_thickness/2):
            self.ys += gravity
        else:
            if self.ys > bounce_stop:
                self.ys = self.ys * -self.ret
            else:
                if abs(self.ys) <= bounce_stop:
                    self.ys = 0
        return self.ys

    def update_pos(self):
        self.ypos += self.ys
        self.xpos += self.xs

def draw_walls():
    left=pg.draw.line(screen, 'white',(0,0), (0, HEIGHT), wall_thickness)
    right=pg.draw.line(screen, 'white',(WIDTH,0), (WIDTH, HEIGHT), wall_thickness)
    top=pg.draw.line(screen, 'white',(0,0), (WIDTH, 0), wall_thickness)
    bottom=pg.draw.line(screen, 'white',(0,HEIGHT), (WIDTH, HEIGHT), wall_thickness)
    return left, right, top, bottom

ball1=Ball(50, 50, 30, 'orange', 100, 0.6, 0, 0, 1);
ball2=Ball(500, 500, 50, 'blue', 300, 1.0, 0, 0, 2);
ball3=Ball(300, 300, 50, 'yellow', 300, 0.8, 0, 0, 3);
ball4=Ball(700, 700, 50, 'red', 300, 0.9, 0, 0, 4);
balls = [ball1, ball2, ball3, ball4]

run = True
while run: 
    timer.tick(fps)
    screen.fill('black')

    walls= draw_walls()
    for ball in balls:
        ball.draw()
    for ball in balls:
        ball.update_pos()

    ball1.ys = ball1.check_gravity()
    ball2.ys = ball2.check_gravity()
    ball3.ys = ball3.check_gravity()
    ball4.ys = ball4.check_gravity()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if ball1.check_select(event.pos) or ball2.check_select(event.pos) or ball3.check_select(event.pos) or ball4.check_select(event.pos):
                    active_select=True
        if event.type == pg.MOUSEBUTTONUP:
            if event.button==1:
                active_select=False
                for i in range(len(balls)):
                    balls[i].check_select((-1000, -1000))

    pg.display.flip()
pg.quit()
