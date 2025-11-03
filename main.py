import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Invaders')
pygame_icon = pygame.image.load('resources\\ufo-1.png')
#32x32
pygame.display.set_icon(pygame_icon)


class Bullet:
    def __init__(self, x=0, y=0):
        self.bullet_state = 'ready'
        self.x = x
        self.y = y
        self.image = pygame.image.load('resources\\bullet.png')
        self.change = -2
        self.rotate = pygame.transform.rotate(self.image, 90)

    def shoot(self):
        self.bullet_state = 'fire'
        screen.blit(self.rotate, (self.x, self.y))

    def move(self):
        if self.bullet_state == 'fire':
            self.y += self.change
            screen.blit(self.rotate, (self.x, self.y))
        if self.y <= 0:
            self.bullet_state = 'ready'
            self.y = 600 - 69


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
        self.x_change = 0.3
        self.y_change = 20

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.x_change
        if self.x <= 0:
            self.x_change = 1
            self.y += self.y_change
        elif self.x >= 736:
            self.x_change = -1
            self.y += self.y_change

    def is_hit(self, bullet):
        distance = (math.sqrt((self.x - bullet.x) ** 2 + (self.y - bullet.y) ** 2))
        if distance < 27:
            return True
        return False


player = Player(368)
enemy = Enemy(random.randint(0, 736), random.randint(0, 236))
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
                if bullet.bullet_state == 'ready':
                    bullet.x = player.x + 16
                    bullet.y = player.y - 10
                    bullet.shoot()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.change = 0
        
    player.move()
    player.draw()

    enemy.draw()
    enemy.move()


    bullet.move()

    pygame.display.flip()