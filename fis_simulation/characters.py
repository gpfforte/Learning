import pygame
from pygame.locals import *
from costanti import SCALE, WIDTH, HEIGHT, TIMESTEP, GREEN, GRAVITY, WHITE
import math

class Paddle(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pygame.image.load('media/bar2_blue.png')
        self.rect = self.image.get_rect()
        self.x_vel = 5
        self.y_vel = 5
        self.rect.center = (WIDTH // 2, HEIGHT - self.height)        
    
    def update(self):
        if self.rect.right < WIDTH and pygame.key.get_pressed()[K_RIGHT]:
            self.rect.x += self.x_vel
        if self.rect.left > 0 and pygame.key.get_pressed()[K_LEFT]:
            self.rect.x -= self.x_vel
        if self.rect.bottom < HEIGHT and pygame.key.get_pressed()[K_DOWN]:
            self.rect.y +=0
        if self.rect.top > 0 and pygame.key.get_pressed()[K_UP]:
            self.rect.y -= 0

class Ball(pygame.sprite.Sprite):
    """
    Define a Ball that jumps on the left, top and right border
    """
    def __init__(self, x, y, velocity, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('media/ball_red.png')
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_rect()
        self.velocity = velocity
        self.x_vel = int(velocity * math.cos(angle))
        self.y_vel = int(velocity * math.sin(angle))
        # print(self.x_vel, self.y_vel)
        self.rect.centerx, self.rect.bottom = (x, y)

    def update(self):
        self.rect.x += int(self.x_vel/20)
        self.rect.y += int(self.y_vel/20)
        if self.rect.right > WIDTH and self.x_vel > 0:
            self.x_vel*=-1
        if self.rect.left < 0 and self.x_vel < 0:
            self.x_vel*=-1
        if self.rect.top < 0 and self.y_vel < 0:
            self.y_vel*=-1
        if self.rect.bottom > HEIGHT+15 and self.y_vel > 0:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    """
    Define a bullet that can be either vertical or horizontal, the rect is completely
    transparent so that the circle is not surrounded by a black border.
    """
    def __init__(self, x, y, radius, color, velocity, angle):
        pygame.sprite.Sprite.__init__(self)
        self.width = radius*2
        self.height = radius*2
        self.image = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA)   # per-pixel alpha
        self.image.fill((*color, 0))
        # self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.radius = radius
        self.color = color
        self.velocity = velocity
        self.x_vel = int(velocity * math.cos(angle))
        self.y_vel = int(velocity * math.sin(angle))
        # print(self.x_vel, self.y_vel)
        self.rect.center = (x, y)
        pygame.draw.circle(self.image, self.color,
                           (self.width//2, self.height//2), self.radius)


    def update(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        if self.rect.right > WIDTH and self.x_vel > 0:
            self.kill()
        if self.rect.left < 0 and self.x_vel < 0:
            self.kill()
        if self.rect.top < 0 and self.y_vel < 0:
            self.kill()
        if self.rect.bottom > HEIGHT and self.y_vel > 0:
            self.kill()

    def __str__(self):
        return f"Bullet {self.color} redius {self.radius}"


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.walkRight = [pygame.image.load('media/R1.png'), pygame.image.load('media/R2.png'), pygame.image.load('media/R3.png'), pygame.image.load('media/R4.png'), pygame.image.load(
            'media/R5.png'), pygame.image.load('media/R6.png'), pygame.image.load('media/R7.png'), pygame.image.load('media/R8.png'), pygame.image.load('media/R9.png')]
        self.walkLeft = [pygame.image.load('media/L1.png'), pygame.image.load('media/L2.png'), pygame.image.load('media/L3.png'), pygame.image.load('media/L4.png'), pygame.image.load(
            'media/L5.png'), pygame.image.load('media/L6.png'), pygame.image.load('media/L7.png'), pygame.image.load('media/L8.png'), pygame.image.load('media/L9.png')]
        self.char = pygame.image.load('media/standing.png')
        # self.width = 20
        # self.height = 20
        # self.color = WHITE
        # self.image = pygame.Surface((self.width, self.height))
        self.image = self.char
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.x_vel = 5
        self.y_vel = 5
        # pygame.draw.circle(self.image, self.color,
        #                    (self.width//2, self.height//2), max(self.width//2, self.height//2))
        self.left = False
        self.right = False
        self.walkCount = 0

    def update(self):
        # self.rect.x += self.x_vel
        # self.rect.y += self.y_vel
        if self.walkCount >= 26:
            self.walkCount = 0
        if self.rect.right < WIDTH and pygame.key.get_pressed()[K_RIGHT]:
            self.rect.x += self.x_vel
            self.left = False
            self.right = True
            self.walkCount += 1
            self.image = self.walkRight[self.walkCount//3]
        elif self.rect.left > 0 and pygame.key.get_pressed()[K_LEFT]:
            self.rect.x -= self.x_vel
            self.left = True
            self.right = False
            self.walkCount += 1
            self.image = self.walkLeft[self.walkCount//3]
        else:
            self.left = False
            self.right = False
            self.walkCount = 0
            self.image = self.char
        if self.rect.bottom < HEIGHT and pygame.key.get_pressed()[K_DOWN]:
            self.rect.y += self.x_vel
        if self.rect.top > 0 and pygame.key.get_pressed()[K_UP]:
            self.rect.y -= self.x_vel


class AutoPlayer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 20
        self.height = 20
        self.color = GREEN
        self.image = pygame.Surface((self.width, self.height))
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.x_vel = 5
        self.y_vel = 5
        pygame.draw.circle(self.image, self.color,
                           (self.width//2, self.height//2), max(self.width//2, self.height//2))

    def update(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        if self.rect.right > WIDTH:
            self.x_vel = -self.x_vel
        if self.rect.left < 0:
            self.x_vel = -self.x_vel
        if self.rect.top < 0:
            self.y_vel = -self.y_vel
        if self.rect.bottom > HEIGHT:
            self.y_vel = -self.y_vel


class GravitationalBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color, velocity_x, velocity_y):
        pygame.sprite.Sprite.__init__(self)
        self.width = radius*2
        self.height = radius*2
        self.image = pygame.Surface((self.width, self.height))
        # self.image.fill(color)
        self.rect = self.image.get_rect()
        self.radius = radius
        self.color = color
        self.rect.center = (x, y)
        self.x_vel = velocity_x
        self.y_vel = velocity_y
        pygame.draw.circle(self.image, self.color,
                           (self.width//2, self.height//2), self.radius)

    def update(self):
        self.y_vel = self.y_vel + GRAVITY * TIMESTEP
        self.rect.x += self.x_vel * TIMESTEP
        self.rect.y += self.y_vel * TIMESTEP
        if self.rect.right > WIDTH:
            self.kill()
        if self.rect.left < 0:
            self.kill()
        if self.rect.top < 0:
            self.kill()
        if self.rect.bottom > HEIGHT:
            self.kill()
