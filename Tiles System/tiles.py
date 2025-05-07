import pygame
import random
import sys

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize mixer for sound

# Screen dimensions and settings
SCREEN_WIDTH = 400  # Width of the game window
SCREEN_HEIGHT = 600  # Height of the game window
TILE_WIDTH = SCREEN_WIDTH // 4  # Width of each tile (4 columns)
TILE_HEIGHT = 150  # Height of each tile
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create the game window
pygame.display.set_caption("Piano Tiles Clone")  # Set the title of the game window

# Colors
WHITE = (255, 255, 255)  # Background color
BLACK = (0, 0, 0)  # Tile color
RED = (255, 0, 0)  # Game over text color
BLUE = (0, 0, 255)  # Main menu background color

# Frame rate
FPS = 60  # Frames per second for smooth gameplay
clock = pygame.time.Clock()  # Clock to manage the frame rate

# Font for displaying text
FONT = pygame.font.Font(None, 36)  # Default font and size

# Game variables
tiles = []  # List to store the falling tiles
TILE_SPEED = 5  # Speed of the falling tiles
score = 0  # Player's score
game_over = False  # Flag to check if the game is over
paused = False  # Flag to check if the game is paused

# Load music and sound effects
pygame.mixer.music.load("Sparkle _ Your Name AMV.mp3")  # Replace with your background music file
tile_hit_sound = pygame.mixer.Sound("sfx_hit.wav")  # Replace with your tile hit sound effect
game_over_sound = pygame.mixer.Sound("sfx_die.wav")  # Replace with your game over sound effect


# Function to play background music
def play_background_music():
    pygame.mixer.music.play(-1)  # Play music in a loop (-1 means infinite loop)


# Function to draw the tiles on the screen
def draw_tiles(tiles):
    for tile in tiles:  # Loop through each tile
        pygame.draw.rect(SCREEN, BLACK, tile)  # Draw the tile as a black rectangle


# Main menu screen
def main_menu():
    play_background_music()  # Start background music
    while True:
        SCREEN.fill(BLACK)  # Fill the screen with black for the main menu
        title_text = FONT.render("Black Tile", True, WHITE)  # Display the game title
        play_text = FONT.render("Press P to Play", True, WHITE)  # Display play option
        quit_text = FONT.render("Press Q to Quit", True, WHITE)  # Display quit option

        # Position the text in the center of the screen
        SCREEN.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        SCREEN.blit(play_text, (SCREEN_WIDTH // 2 - play_text.get_width() // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()  # Update the display

        # Event handling for the main menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Start the game
                    main_game()
                if event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    sys.exit()


# Main gameplay function
def main_game():
    global tiles, TILE_SPEED, score, game_over, paused

    # Initialize tiles, score, and speed
    tiles = []  # Reset the tiles list
    for i in range(5):  # Generate initial tiles
        col = random.randint(0, 3)  # Random column for the tile
        tiles.append(pygame.Rect(col * TILE_WIDTH, -i * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))

    TILE_SPEED = 5  # Reset the tile speed
    score = 0  # Reset the score
    game_over = False  # Reset game over flag
    paused = False  # Reset paused flag

    running = True  # Game loop flag
    while running:
        SCREEN.fill(WHITE)  # Fill the screen with white

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Pause or unpause the game
                    paused = not paused
                if not paused and not game_over:
                    if event.key in [pygame.K_a, pygame.K_s, pygame.K_k, pygame.K_l]:  # Check for valid keys
                        col = [pygame.K_a, pygame.K_s, pygame.K_k, pygame.K_l].index(event.key)
                        # Check if the tile at the bottom matches the pressed key
                        if tiles and tiles[0].y + TILE_HEIGHT >= SCREEN_HEIGHT:
                            if tiles[0].x == col * TILE_WIDTH:  # Correct key press
                                tiles.pop(0)  # Remove the matched tile
                                score += 1  # Increase the score
                                TILE_SPEED += 0.1  # Gradually increase the tile speed
                                tile_hit_sound.play()  # Play tile hit sound
                            else:  # Wrong key press
                                game_over = True
                                game_over_sound.play()  
                                
        if paused:
            pause_text = FONT.render("Paused - Press P to Resume", True, RED)
            SCREEN.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            clock.tick(FPS)
            continue  

        if not game_over:
            for tile in tiles:  
                tile.y += TILE_SPEED

            if tiles and tiles[-1].y >= TILE_HEIGHT:
                col = random.randint(0, 3)  
                tiles.append(pygame.Rect(col * TILE_WIDTH, -TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))

            if tiles and tiles[0].y > SCREEN_HEIGHT:  
                game_over = True
                game_over_sound.play() 

        draw_tiles(tiles)


        score_text = FONT.render(f"Score: {score}", True, BLACK)
        SCREEN.blit(score_text, (10, 10))

        if game_over:
            running = False  
            game_over_screen(score)

        pygame.display.flip()
        clock.tick(FPS)


def game_over_screen(score):
    while True:
        SCREEN.fill(BLACK) 
        game_over_text = FONT.render("Game Over!", True, RED) 
        score_text = FONT.render(f"Your Score: {score}", True, WHITE)
        restart_text = FONT.render("Press W to Restart", True, WHITE)  
        main_menu_text = FONT.render("Press M for Main Menu", True, WHITE)  
        quit_text = FONT.render("Press Q to Quit", True, WHITE)

        SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 150))
        SCREEN.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        SCREEN.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(main_menu_text, (SCREEN_WIDTH // 2 - main_menu_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        SCREEN.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

        pygame.display.flip()  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:  
                    main_game()
                if event.key == pygame.K_m:  
                    main_menu()
                if event.key == pygame.K_q:  
                    pygame.quit()
                    sys.exit()


main_menu()
