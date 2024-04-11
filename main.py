import pygame
import random
import sys
import math

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
ENEMY_SPEED = 0.5
FONT_SIZE = 30
PLAYER_POS = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
PLAYER_RADIUS = 10
PERIMETER_RADIUS = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 3
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Initialization
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Type to Shoot')
font = pygame.font.Font(None, FONT_SIZE)
clock = pygame.time.Clock()

# Game state variables
enemies = []
typed_text = ""
score = 0

# Enemy class
class Enemy:
    def __init__(self):
        self.word = random.choice(["enemy", "invader", "attacker", "destroyer", "threat"])
        self.health = len(self.word)
        self.pos = self.spawn_at_edge()
        self.velocity = self.calculate_velocity()

    def spawn_at_edge(self):
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            return [random.randint(0, SCREEN_WIDTH), 0]
        elif edge == "bottom":
            return [random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT]
        elif edge == "left":
            return [0, random.randint(0, SCREEN_HEIGHT)]
        else:  # edge == "right"
            return [SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT)]

    def calculate_velocity(self):
        direction = [PLAYER_POS[0] - self.pos[0], PLAYER_POS[1] - self.pos[1]]
        length = math.sqrt(direction[0]**2 + direction[1]**2)
        return [ENEMY_SPEED * direction[0] / length, ENEMY_SPEED * direction[1] / length]

    def move(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

    def draw(self, screen):
        # Draw word
        word_surf = font.render(self.word, True, WHITE)
        screen.blit(word_surf, self.pos)

        # Draw health bar
        health_bar_length = 50
        health_bar_height = 5
        current_health_length = health_bar_length * (self.health / len(self.word))
        pygame.draw.rect(screen, RED, [self.pos[0], self.pos[1] - 10, health_bar_length, health_bar_height])
        pygame.draw.rect(screen, GREEN, [self.pos[0], self.pos[1] - 10, current_health_length, health_bar_height])

    def hit(self):
        self.health -= 1
        return self.health <= 0

# Main game loop
while True:
    screen.fill((0, 0, 0))

    # Draw perimeter and player
    pygame.draw.circle(screen, BLUE, PLAYER_POS, PERIMETER_RADIUS, 1)
    pygame.draw.circle(screen, RED, PLAYER_POS, PLAYER_RADIUS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and typed_text:
                typed_text = typed_text[:-1]
            elif event.unicode:
                next_letter = typed_text + event.unicode
                hit_any = False
                for enemy in enemies:
                    if enemy.word.startswith(next_letter):
                        typed_text = next_letter
                        hit_any = True
                        if enemy.hit():
                            enemies.remove(enemy)
                            score += 1
                if not hit_any:
                    typed_text = ""  # Reset if no enemy word starts with typed text

    # Update game state
    if len(enemies) < 5:
        enemies.append(Enemy())

    for enemy in enemies[:]:
        enemy.move()
        if math.hypot(enemy.pos[0] - PLAYER_POS[0], enemy.pos[1] - PLAYER_POS[1]) < PLAYER_RADIUS + FONT_SIZE:
            pygame.quit()
            sys.exit(f"Game Over! Score: {score}")

    # Draw everything
    for enemy in enemies:
        enemy.draw(screen)
    score_surf = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surf, (10, 10))
    typed_text_surf = font.render(typed_text, True, RED)
    screen.blit(typed_text_surf, (10, SCREEN_HEIGHT - 40))

    pygame.display.flip()
    clock.tick(60)
