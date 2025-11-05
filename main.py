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


class Button:
    def __init__(self, text, x, y):
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = text
        self.x = x
        self.y = y
        self.rendered_text = self.font.render(self.text, True, (255, 255, 255))
        self.rect = self.rendered_text.get_rect(center=(self.x, self.y))

    def draw(self):
        screen.blit(self.rendered_text, self.rect)

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

    def get_rect(self):
        return self.rotate.get_rect(topleft=(self.x, self.y))




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
    def __init__(self, x, y, speed = 1):
        self.x = x
        self.y = y
        self.image = pygame.image.load('resources\\alien.png')
        self.speed = speed
        self.x_change = 0.5 * self.speed
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

        

def start():
    game_over = False
    player = Player(368)
    enemy = Enemy(random.randint(0, 736), random.randint(0, 236))
    bullet = Bullet(player.x + 16, player.y)
    scores_show = Button('Scores', 700, 50)
    enemies = []
    for i in range(6):
        enemy_x = random.randint(0, 736)
        enemy_y = random.randint(0, 236)
        enemies.append(Enemy(enemy_x + i*10, enemy_y))
    return player, enemy, bullet, enemies, game_over, scores_show

import csv

def score_menu():
    # Make sure we use the same screen from main game
    global screen  
    running = True
    print("Score menu opened")

    # Fonts and colors
    font_title = pygame.font.Font('freesansbold.ttf', 48)
    font_entry = pygame.font.Font('freesansbold.ttf', 32)
    title_text = font_title.render("HIGH SCORES", True, (255, 255, 0))
    background_color = (0, 0, 30)

    # Load scores
    scores = []
    try:
        with open('scores.csv') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header: name,score
            for row in reader:
                if len(row) >= 2:
                    name, score_str = row[0].strip(), row[1].strip()
                    if score_str.isdigit():
                        scores.append((name, int(score_str)))
    except Exception as e:
        print("Error reading scores.csv:", e)

    # Sort descending
    scores.sort(key=lambda x: x[1], reverse=True)

    # Loop for score menu
    while running:
        screen.fill(background_color)
        screen.blit(title_text, (230, 60))

        # Draw each score line
        y_offset = 150
        for i, (name, score) in enumerate(scores[:10]):  # top 10
            entry_text = font_entry.render(f"{i+1}. {name} - {score}", True, (255, 255, 255))
            screen.blit(entry_text, (250, y_offset))
            y_offset += 40

        # Instructions
        small_font = pygame.font.Font('freesansbold.ttf', 20)
        exit_text = small_font.render("Press ESC or click to return", True, (200, 200, 200))
        screen.blit(exit_text, (270, 520))

        pygame.display.flip()

        # Handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False





game_over_font = pygame.font.Font('freesansbold.ttf', 64)
game_over_txt = game_over_font.render('GAME OVER', True, (255, 0, 0))

restart = game_over_font.render('Restart', True, (255,255,255))
exit = game_over_font.render('Exit', True, (255,255,255))
game_over = False
restart_rect = restart.get_rect(center=(500, 300))
exit_rect = exit.get_rect(center=(100, 300))

player, enemy, bullet, enemies, game_over, scores_show = start()

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left mouse button
                if scores_show.rect.collidepoint(event.pos):
                    print("Scores button clicked!")
                    score_menu()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.change = 0
        
    player.move()
    player.draw()

    scores_show.draw()

    for enemy in enemies:
        if player.score % 10 == 0 and player.score != 0:
            for e in enemies:
                # Only increase once per score milestone
                if not hasattr(e, "speed_boosted") or not e.speed_boosted:
                    e.speed += 1
                    e.x_change = 0.5 * e.speed if e.x_change > 0 else -0.5 * e.speed
                    e.speed_boosted = True
        else:
            # Reset flag so we can boost again next milestone
            for e in enemies:
                if hasattr(e, "speed_boosted"):
                    e.speed_boosted = False

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
        screen.blit(game_over_txt, (200, 150))
        screen.blit(restart, (500, 300))
        screen.blit(exit, (100,300))
        enemies.clear()

        bullet_rect = bullet.get_rect()
        
        if bullet_rect.colliderect(restart_rect):
            print("Restarting Game")
            player, enemy, bullet, enemies, game_over, score_show = start()

        elif bullet_rect.colliderect(exit_rect):
            print("Exiting Game")
            running = False

    bullet.move()
    

    pygame.display.flip()
