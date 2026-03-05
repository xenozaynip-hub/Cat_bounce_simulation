import pygame

pygame.init()

WITH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WITH, HEIGHT))

fps = 60
timer = pygame.time.Clock()

#game variables
wall_thickness = 10
gravity = 0.5
bounce_stop = 0.3

class Ball:
    def __init__(self, x_pos, y_pos, radius, color, mass, velocity_x, velocity_y, retention,id):
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
    

    def draw(self):
        self.circle = pygame.draw.circle(screen, self.color, (int(self.x_pos), int(self.y_pos)), self.radius)
    
    def check_gravity(self):
        if self.y_pos < HEIGHT - self.radius - (wall_thickness/2):
            self.velocity_y += gravity
        else:
            if self.velocity_y > bounce_stop:
                self.velocity_y = self.velocity_y * -1 * self.retention
            else:
                if abs(self.velocity_y) <= bounce_stop:
                    self.velocity_y = 0

        return self.velocity_y
    
    def update_position(self, mouse):
        if not self.select:
            self.x_pos += self.velocity_x
            self.y_pos += self.velocity_y
        else:
            self.x_pos = mouse[0]
            self.y_pos = mouse [1]

    def check_select(self, pos):
        self.select = False
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

ball1 = Ball(50, 50,30, (104, 0, 0), 100, 0, 0, 0.9,1)
ball2 = Ball(500, 500,50, (50, 0, 0), 300, 0, 0, 0.9,2)
ball3 = Ball(200, 200,40, (150, 0, 0), 200, 0, 0, 0.9,3)
ball_list = [ball1, ball2, ball3]

#main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill((0, 0, 0))
    mouse_coords = pygame.mouse.get_pos()

    walls = draw_walls()
    ball1.draw()
    ball2.draw()
    ball3.draw()
    ball1.update_position(mouse_coords)
    ball2.update_position(mouse_coords)
    ball3.update_position(mouse_coords)
    ball1.velocity_y = ball1.check_gravity()
    ball2.velocity_y = ball2.check_gravity()
    ball3.velocity_y = ball3.check_gravity()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:        
            if event.button == 1:
                if ball1.check_select(event.pos) or ball2.check_select(event.pos) or ball3.check_select(event.pos):
                    active_select = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_select = False
                for i in range(len(ball_list)):
                        ball_list[i].check_select((-100, -100))

                

            
    pygame.display.flip()
pygame.quit()