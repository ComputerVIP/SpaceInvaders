import pygame
import random
import math
from pygame import mixer

pygame.init()

background = pygame.image.load('resources\\background-1.jpg')
background = pygame.transform.scale(background, (800, 600))

mixer.music.load('resources\\background.wav')
mixer.music.play(-1)

score_font = pygame.font.Font('freesansbold.ttf', 32)


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
        self.score = 0
        self.lives = 3

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
        self.x_change = 0.5 
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
        distance = math.sqrt((self.x - bullet.x) ** 2 + (self.y - bullet.y) ** 2)
        if distance < 48:
            return True
        return False
    
    def check_game_over(self):
        if self.y > 540:
            return True
        return False
    
class GameOver:
    def __init__(self):
        pass


player = Player(368)
enemy = Enemy(random.randint(0, 736), random.randint(0, 236))
bullet = Bullet(player.x + 16, player.y)
enemies = []
for i in range(6):
    enemy_x = random.randint(0, 736)
    enemy_y = random.randint(0, 236)
    enemies.append(Enemy(enemy_x + i*10, enemy_y))




game_over_font = pygame.font.Font('freesansbold.ttf', 64)
game_over_txt = game_over_font.render('GAME OVER', True, (255, 0, 0))
game_over = False



running = True
while running:
    score_display = score_font.render(f'Score: {player.score}  Lives: {player.lives}', True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(score_display, (10, 10))
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
                    mixer.Sound('resources\\laser.wav').play()
                    bullet.x = player.x + 16
                    bullet.y = player.y - 10
                    bullet.shoot()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.change = 0
        
    player.move()
    player.draw()
    for enemy in enemies:
        if player.score >= 20:
            enemy.y_change = 60
        enemy.draw()
        enemy.move()
        if enemy.check_game_over():
            player.lives -= 1
            enemy.x = random.randint(0, 736)
            enemy.y = random.randint(0, 236)
            if player.lives <= 0:
                game_over = True
        elif enemy.is_hit(bullet) and bullet.bullet_state == 'fire':
            player.score += 1
            mixer.Sound('resources\\explosion.wav').play()
            bullet.bullet_state = 'ready'
            bullet.y = 600 - 69
            enemy.x = random.randint(0, 736)
            enemy.y = random.randint(0, 236)
    if game_over:
        screen.blit(game_over_txt, (200, 250))
        enemies.clear()

    bullet.move()
    

    pygame.display.flip()