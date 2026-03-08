import pygame

pygame.init()

LINE_X = 999
LINE_Y = 796
WITH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WITH, HEIGHT))

fps = 60
timer = pygame.time.Clock()

#game variables
wall_thickness = 10
gravity = 0.5
bounce_stop = 0.3

mouse_trajectory = []

class Ball:
    def __init__(self, x_pos, y_pos, radius, color, mass, velocity_x, velocity_y, retention,id, friction):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.color = color
        self.mass = mass
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.retention = retention
        self.id = id
        self.circle = None
        self.select = False
        self.friction = friction

        if self.id == 1:
            self.image = pygame.image.load('images/cat.jpg')
            self.image = pygame.transform.scale(self.image, (int(self.radius * 5), int(self.radius * 2)))
        elif self.id == 2:
            self.image = pygame.image.load('images/another_cat.jpg')
            self.image = pygame.transform.scale(self.image, (int(self.radius * 4), int(self.radius * 6)))
        elif self.id == 3:
            self.image = pygame.image.load('images/Microwave.jpg')
            self.image = pygame.transform.scale(self.image, (int(self.radius * 5), int(self.radius * 5)))
        elif self.id == 4:
            self.image = pygame.image.load('images/wierd_cat.jpg')
            self.image = pygame.transform.scale(self.image, (int(self.radius * 3), int(self.radius * 3)))
        elif self.id == 5:
            self.image = pygame.image.load('images/cat_on_drugs.jpg')
            self.image = pygame.transform.scale(self.image, (int(self.radius * 8), int(self.radius * 5)))

    def draw(self):
        if hasattr(self, 'image'):
            screen.blit(self.image, (self.x_pos - self.image.get_width()/2, self.y_pos - self.image.get_height()/2))
        else:
            self.circle = pygame.draw.circle(screen, self.color, (int(self.x_pos), int(self.y_pos)), self.radius)
            self.hitbox = self.circle
    
    def check_gravity(self):
        if not self.select:
            if self.y_pos < HEIGHT - self.radius - (wall_thickness/2):
                self.velocity_y += gravity
            else:
                if self.velocity_y > bounce_stop:
                    self.velocity_y = self.velocity_y * -1 * self.retention
                else:
                    if abs(self.velocity_y) <= bounce_stop:
                        self.velocity_y = 0
            if (self.x_pos < self.radius + (wall_thickness/2) and self.velocity_x < 0) or (self.x_pos > WITH - self.radius - (wall_thickness/2) and self.velocity_x > 0):
                self.velocity_x *= -1 * self.retention
                if abs(self.velocity_x) < bounce_stop:
                    self.velocity_x = 0
            if self.velocity_y == 0 and self.velocity_x != 0:
                if self.velocity_x > 0:
                    self.velocity_x -= self.friction
                elif self.velocity_x < 0:
                    self.velocity_x += self.friction
        else:
            self.velocity_y = y_push
            self.velocity_x = x_push
        return self.velocity_y
    
    def update_position(self, mouse):
        if not self.select:
            self.x_pos += self.velocity_x
            self.y_pos += self.velocity_y
        else:
            self.x_pos = min(mouse[0], LINE_X - self.radius)
            self.y_pos = min(mouse[1], LINE_Y - self.radius)

    def check_select(self, pos):
        self.select = False
        if hasattr(self, 'image'):
            rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
            if rect.collidepoint(pos):
                self.select = True
                return True
        else:
            if self.circle.collidepoint(pos):
                self.select = True
                return True
        return self.select

def draw_walls():
    left= pygame.draw.line(screen, (255, 255, 255), (0, 0), (0, HEIGHT), wall_thickness)
    right = pygame.draw.line(screen, (255, 255, 255), (WITH, 0), (WITH, HEIGHT), wall_thickness)
    top = pygame.draw.line(screen, (255, 255, 255), (0, 0), (WITH, 0), wall_thickness)
    bottom = pygame.draw.line(screen, (255, 255, 255), (0, HEIGHT), (WITH, HEIGHT), wall_thickness)

    wall_list = [left, right, top, bottom]
    return wall_list

def calc_motion_vector():
    x_velocity = 0
    y_velocity = 0
    if len(mouse_trajectory) > 10:
        x_velocity = (mouse_trajectory[-1][0] - mouse_trajectory[0][0]) / len(mouse_trajectory)
        y_velocity = (mouse_trajectory[-1][1] - mouse_trajectory[0][1]) / len(mouse_trajectory)

    return x_velocity, y_velocity

ball1 = Ball(50, 50,90, (104, 0, 0), 500, 0, 0, 0.9,1,0.02)
ball2 = Ball(500, 500,50, (50, 0, 0), 300, 0, 0, 0.7,2,0.03)
ball3 = Ball(200, 200,40, (150, 0, 0), 200, 0, 0, 0.5,3,0.04)
ball4 = Ball(300, 300,30, (200, 0, 0), 100, 0, 0, 1,4,0.05)
ball5 = Ball(400, 400,20, (255, 0, 0), 50, 0, 0, 0.8,5,0.06)
ball_list = [ball1, ball2, ball3, ball4, ball5]

#main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill((0, 0, 0))
    mouse_coords = pygame.mouse.get_pos()
    mouse_trajectory.append(mouse_coords)
    if len(mouse_trajectory) > 20:
        mouse_trajectory.pop(0)
    x_push, y_push = calc_motion_vector()

    walls = draw_walls()
    ball1.draw()
    ball2.draw()
    ball3.draw()
    ball4.draw()
    ball5.draw()
    ball1.update_position(mouse_coords)
    ball2.update_position(mouse_coords)
    ball3.update_position(mouse_coords)
    ball4.update_position(mouse_coords)
    ball5.update_position(mouse_coords)
    ball1.velocity_y = ball1.check_gravity()
    ball2.velocity_y = ball2.check_gravity()
    ball3.velocity_y = ball3.check_gravity()
    ball4.velocity_y = ball4.check_gravity()
    ball5.velocity_y = ball5.check_gravity()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:        
            if event.button == 1:
                if ball1.check_select(event.pos) or ball2.check_select(event.pos) or ball3.check_select(event.pos) or ball4.check_select(event.pos) or ball5.check_select(event.pos):
                    active_select = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_select = False
                for i in range(len(ball_list)):
                        ball_list[i].check_select((-100, -100))

    pygame.display.flip()
pygame.quit()