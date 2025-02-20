import pygame
import random


# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
OBSTACLE_SIZE = 50
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Load images
player_image = pygame.image.load(r"C:\Users\RENU  SRI MEDICHARLA\OneDrive\Documents\boy.png")
player_image = pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE))

obstacle_image = pygame.image.load(r"C:\Users\RENU  SRI MEDICHARLA\OneDrive\Documents\rock.png")
obstacle_image = pygame.transform.scale(obstacle_image, (OBSTACLE_SIZE, OBSTACLE_SIZE))

background_image = pygame.image.load(r"C:\Users\RENU  SRI MEDICHARLA\OneDrive\Documents\Background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("cave crave")

# Player
player_x = WIDTH // 2 - PLAYER_SIZE // 2
player_y = HEIGHT - PLAYER_SIZE - 10

# Obstacles
obstacles = []

# Button
button_rect = pygame.Rect(10, 10, 150, 50)
button_font = pygame.font.Font(None, 36)
button_text = button_font.render("Start", True, WHITE)
button_color = GREEN

# Quit Button
quit_button_rect = pygame.Rect(WIDTH - 160, 10, 150, 50)
quit_button_font = pygame.font.Font(None, 36)
quit_button_text = quit_button_font.render("Quit", True, WHITE)


# Score
score = 0
score_font = pygame.font.Font(None, 36)

# Game state
game_running = False
paused = False


# Function to reset game state
def reset_game():
    global player_x, player_y, obstacles, game_running, paused
    player_x = WIDTH // 2 - PLAYER_SIZE // 2
    player_y = HEIGHT - PLAYER_SIZE - 10
    obstacles = []
    game_running = True
    paused = False
    score = 0

    # Load special character image
    special_character_image = pygame.image.load(r"C:\Users\RENU  SRI MEDICHARLA\OneDrive\Documents\boy.png")
    special_character_image = pygame.transform.scale(special_character_image, (OBSTACLE_SIZE, OBSTACLE_SIZE))

    # Special character
    special_character_x = random.randint(0, WIDTH - OBSTACLE_SIZE)
    special_character_y = 0 - OBSTACLE_SIZE
    special_character_active = True

    # Inside game loop:
    if event.type == pygame.MOUSEBUTTONDOWN:
        if button_rect.collidepoint(event.pos):
        # Start/Pause button logic
          if not game_running:
             reset_game()
             button_text = button_font.render("Pause", True, WHITE)
             button_color = RED
          else:
             paused = not paused
             if paused:
                button_text = button_font.render("Resume", True, WHITE)
                button_color = BLUE
             else:
                button_text = button_font.render("Pause", True, WHITE)
                button_color = RED
    elif quit_button_rect.collidepoint(event.pos):
        # Quit button logic
        pygame.quit()
        sys.exit()
 
        
    # Generate special character
    if special_character_active:
        screen.blit(special_character_image, (special_character_x, special_character_y))
        special_character_y += 5
        # Collision detection with player
        if (player_x < special_character_x + OBSTACLE_SIZE and player_x + PLAYER_SIZE > special_character_x
            and player_y < special_character_y + OBSTACLE_SIZE and player_y + PLAYER_SIZE > special_character_y):
            score += 100  # Increase score when the special character is touched
            special_character_active = False  # Deactivate special character
            special_character_x = random.randint(0, WIDTH - OBSTACLE_SIZE)
            special_character_y = 0 - OBSTACLE_SIZE



# Game loop
running = True
while running:
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                if not game_running:
                    reset_game()
                    button_text = button_font.render("Pause", True, WHITE)
                    button_color = RED
                else:
                    paused = not paused
                    if paused:
                        button_text = button_font.render("Resume", True, WHITE)
                        button_color = BLUE
                    else:
                        button_text = button_font.render("Pause", True, WHITE)
                        button_color = RED
            elif game_running and not paused and event.button == 3:
                print("Game Over!")
                reset_game()
                button_text = button_font.render("Start", True,GREEN)
                button_color = GREEN
    if game_running and not paused:
        # Player controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= 5
        if keys[pygame.K_RIGHT] and player_x < WIDTH - PLAYER_SIZE:
            player_x += 5

        # Update obstacles
        for obstacle in obstacles:
            obstacle[1] += 5
            screen.blit(obstacle_image, (obstacle[0], obstacle[1]))

        # Generate new obstacles
        if random.randint(0, 100) < 5:
            obstacle_x = random.randint(0, WIDTH - OBSTACLE_SIZE)
            obstacle_y = 0 - OBSTACLE_SIZE
            obstacles.append([obstacle_x, obstacle_y, OBSTACLE_SIZE, OBSTACLE_SIZE])

        # Collision detection
        for obstacle in obstacles:
            if (
                player_x < obstacle[0] + OBSTACLE_SIZE
                and player_x + PLAYER_SIZE > obstacle[0]
                and player_y < obstacle[1] + OBSTACLE_SIZE
                and player_y + PLAYER_SIZE > obstacle[1]
            ):
                print("Game Over!")
                button_text = button_font.render("Game Over!", True, WHITE)
                game_running = False

        # Update score
        score += 1

        # Draw the player
        screen.blit(player_image, (player_x, player_y))

        # Remove obstacles that are off-screen
        obstacles = [obstacle for obstacle in obstacles if obstacle[1] < HEIGHT]

    # Draw the button
    pygame.draw.rect(screen, button_color, button_rect)
    screen.blit(button_text, (WIDTH // 2 - 35, HEIGHT // 2 - 15))

    # Draw the quit button
    pygame.draw.rect(screen, RED, quit_button_rect)
    screen.blit(quit_button_text, (WIDTH - 15, 15))

    # Draw the scoreboard
    score_text = score_font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (WIDTH - 200, 20))

    pygame.display.flip()
    pygame.display.update()
    pygame.time.Clock().tick(FPS)


# Quit Pygame
pygame.quit()
sys.exit()
