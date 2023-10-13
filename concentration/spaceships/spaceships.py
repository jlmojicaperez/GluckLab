import pygame
import os
from dataclasses import dataclass

pygame.font.init()
pygame.mixer.init()

@dataclass
class G:
    # Constants
    ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    FPS = 60
    HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
    WINNER_FONT = pygame.font.SysFont("comicsans", 100)
    BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join(ASSETS_PATH, "Grenade+1.mp3"))
    BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join(ASSETS_PATH, "Gun+Silencer.mp3"))

    # Window
    WIDTH, HEIGHT = 900, 500
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Spaceships")

    # Spaceships
    SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
    VELOCITY = 5
    BULLET_VELOCITY = 7
    MAX_BULLETS = 3

    YELLOW_HIT = pygame.USEREVENT + 1
    RED_HIT = pygame.USEREVENT + 2

    YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join(ASSETS_PATH, "spaceship_yellow.png"))
    YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
    YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP, 90)

    RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join(ASSETS_PATH, "spaceship_red.png"))
    RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
    RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP, 270)

    # Border
    BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

    # Space background
    SPACE = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "space.png")), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    G.WIN.blit(G.SPACE, (0, 0))
    pygame.draw.rect(G.WIN, G.BLACK, G.BORDER)

    # Draw health bars
    red_health_text = G.HEALTH_FONT.render("Health: " + str(red_health), 1, G.WHITE)
    yellow_health_text = G.HEALTH_FONT.render("Health: " + str(yellow_health), 1, G.WHITE)
    G.WIN.blit(red_health_text, (G.WIDTH - red_health_text.get_width() - 10, 10))
    G.WIN.blit(yellow_health_text, (10, 10))

    G.WIN.blit(G.YELLOW_SPACESHIP, (yellow.x, yellow.y))
    G.WIN.blit(G.RED_SPACESHIP, (red.x, red.y))
    


    # Draw bullets on screen
    for bullet in red_bullets:
        pygame.draw.rect(G.WIN, G.RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(G.WIN, G.YELLOW, bullet)

    pygame.display.update()

def handle_yellow_movement(keys_pressed, yellow):
    if(keys_pressed[pygame.K_a] and yellow.x - G.VELOCITY > 0): # Left
        yellow.x -= G.VELOCITY
    if(keys_pressed[pygame.K_d] and yellow.x + G.VELOCITY + yellow.width < G.BORDER.x + G.BORDER.width): # Right
        yellow.x += G.VELOCITY
    if(keys_pressed[pygame.K_w] and yellow.y - G.VELOCITY > 0):  # Up
        yellow.y -= G.VELOCITY
    if(keys_pressed[pygame.K_s] and yellow.y + G.VELOCITY + yellow.height < G.HEIGHT - 15): # Down
        yellow.y += G.VELOCITY

def handle_red_movement(keys_pressed, red):
    if(keys_pressed[pygame.K_LEFT] and red.x - G.VELOCITY > G.BORDER.x + G.BORDER.width): # Left
        red.x -= G.VELOCITY
    if(keys_pressed[pygame.K_RIGHT] and red.x + G.VELOCITY + red.width < G.WIDTH + 20): # Right
        red.x += G.VELOCITY
    if(keys_pressed[pygame.K_UP] and red.y - G.VELOCITY > 0): # Up
        red.y -= G.VELOCITY
    if(keys_pressed[pygame.K_DOWN] and red.y + G.VELOCITY + red.height < G.HEIGHT - 15): # Down
        red.y += G.VELOCITY

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += G.BULLET_VELOCITY
        if(red.colliderect(bullet)):
            pygame.event.post(pygame.event.Event(G.RED_HIT))
            yellow_bullets.remove(bullet)
        elif(bullet.x > G.WIDTH):
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= G.BULLET_VELOCITY
        if(yellow.colliderect(bullet)):
            pygame.event.post(pygame.event.Event(G.YELLOW_HIT))
            red_bullets.remove(bullet)
        elif(bullet.x < 0):
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = G.WINNER_FONT.render(text, 1, G.WHITE)
    G.WIN.blit(draw_text, (G.WIDTH/2 - draw_text.get_width()/2, G.HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():

    # Create clock to control FPS
    clock = pygame.time.Clock()

    red_bullets = []
    yellow_bullets = []

    # Game loop variable
    run = True
    
    red = pygame.Rect(700, 300, G.SPACESHIP_WIDTH, G.SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, G.SPACESHIP_WIDTH, G.SPACESHIP_HEIGHT)

    red_health = 10
    yellow_health = 10


    # Main game loop
    while run:
        # Makes sure loop runs at `FPS` times per second i.e 60 times per second if FPS = 60
        # if computer cannot keep up with FPS, it will run as fast as it can.
        clock.tick(G.FPS)
        # Check for events
        for event in pygame.event.get():
            # If user quits, exit game loop
            if(event.type == pygame.QUIT):
                run = False
                pygame.quit()
            
            # Fire bullets
            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_LCTRL and len(yellow_bullets) < G.MAX_BULLETS):
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    G.BULLET_FIRE_SOUND.play()
                if(event.key == pygame.K_RCTRL and len(red_bullets) < G.MAX_BULLETS):
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    G.BULLET_FIRE_SOUND.play()
            
            if(event.type == G.RED_HIT):
                red_health -= 1
                G.BULLET_HIT_SOUND.play()
            if(event.type == G.YELLOW_HIT):
                yellow_health -= 1
                G.BULLET_HIT_SOUND.play()

        winner_text = ""
        # Check for winner
        if(red_health <= 0):
            winner_text = "Yellow Wins!"
        elif(yellow_health <= 0):
            winner_text = "Red Wins!"
        
        if(winner_text != ""):
            draw_winner(winner_text)
            break

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        keys_pressed = pygame.key.get_pressed()

        # Handle players movement
        handle_yellow_movement(keys_pressed, yellow)
        handle_red_movement(keys_pressed, red)

        # Draw window
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()

if __name__ == "__main__":
    main()
