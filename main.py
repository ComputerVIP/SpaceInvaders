import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Invaders')
pygame_icon = pygame.image.load('resources\\ufo-1.png')
#32x32
pygame.display.set_icon(pygame_icon)

class Player:
    def __init__(self, x, change = 0):
        self.x = x
        self.y = 600 - 69
        self.image = pygame.image.load('resources\\spaceship.png')
        self.change = change

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.change
        if self.x <= 0:
            self.x = 0
        elif self.x >= 736:
            self.x = 736

class Enemy:
    def __init__(self, x, y, change = 0):
        self.x = x
        self.y = y
        self.image = pygame.image.load('resources\\alien.png')
        self.change = change

class Bullet:
    def __init__(self, x, y, change_y = 1):
        self.x = x
        self.y = y
        self.image = pygame.image.load('resources\\bullet.png')
        self.change_y = change_y

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
    
    def move(self):
        self.y -= self.change_y

player = Player(368)
bullet = Bullet(player.x + 16, player.y)





running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_LEFT]:
                player.change = -1
            if keys[pygame.K_RIGHT]:
                player.change = 1
            if keys[pygame.K_SPACE]:
                bullet.draw()
                bullet.move()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.change = 0
        
    player.move()
    player.draw()


    bullet.move()

    pygame.display.flip()