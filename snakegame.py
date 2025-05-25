import pygame
import sys
import random

pygame.init()

# sound clips
start_sound = pygame.mixer.Sound("game-start.wav")      #3sec
eat_sound = pygame.mixer.Sound("apple-eaten.wav")       #1sec
game_over_sound = pygame.mixer.Sound("game-over.wav")   #3sec


# Screen size
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock
clock = pygame.time.Clock()

# Snake and Apple setup
snake = [(100, 100), (80, 100), (60, 100)]
direction = (20, 0)
apple = (300, 200)
score = 0

def move_snake(snake, direction):
    head = snake[0]
    new_head = (head[0] + direction[0], head[1] + direction[1])
    snake.insert(0, new_head)
    return snake

def check_collision(snake):
    head = snake[0]
    return (head in snake[1:] or
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT)

def spawn_apple():
    return (
        random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
        random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
    )

def game_over_screen(score):
    font = pygame.font.SysFont(None, 48)
    text = font.render(f"Game Over! Final Score: {score}", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.fill(BLACK)
    screen.blit(text, text_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False



# Show "Get Ready!" message
screen.fill(BLACK)
font = pygame.font.SysFont(None, 48)
text = font.render("Get Ready!", True, WHITE)
screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
pygame.display.flip()


# Play the start sound and wait
start_sound.play()
pygame.time.set_timer(pygame.USEREVENT, int(start_sound.get_length() * 1000))

# Temporary loop to let sound play
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.USEREVENT:
            waiting = False

# Game loop
running = True
while running:
    clock.tick(10)
    screen.fill(BLACK)

    # Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 20):
                direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                direction = (CELL_SIZE, 0)

    # Move snake
    snake = move_snake(snake, direction)

    # Check collision
    if check_collision(snake):
        
        
        game_over_sound.play()
        game_over_screen(score)
        pygame.time.delay(3000)  # Let the game over sound play fully
        
        break

    # Eat apple
    if snake[0] == apple:
        apple = spawn_apple()
        score += 10
        eat_sound.play()  # Play apple-eaten sound

    else:
        snake.pop()

    # Draw apple
    pygame.draw.rect(screen, RED, (*apple, CELL_SIZE, CELL_SIZE))

    # Draw snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

    # Draw score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 150, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
