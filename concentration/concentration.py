import os
import pygame
import random

from dataclasses import dataclass

pygame.init()
pygame.font.init()
pygame.mixer.init()

@dataclass
class G:

    DISPLAY_INFO = pygame.display.Info()
    DISPLAY_WIDTH, DISPLAY_HEIGHT = DISPLAY_INFO.current_w, DISPLAY_INFO.current_h
    # Display Surface
    DISPLAY_SURFACE = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    pygame.display.set_caption("Concentration")
    pygame.display.set_icon(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "Rutgers-AgingAndBrainHealthAllianceLogo.png")))
    # Constants
    FPS = 60
    ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (128, 128, 128)
    POKER_GREEN = (0, 54, 38)
    PURPLEISH = (186, 26, 108)

@dataclass
class Cards:
    CARD_WIDTH = (G.DISPLAY_WIDTH-200)//10
    CARD_HEIGHT = CARD_WIDTH * 7//5

    CARD_BACK_IMAGE = pygame.image.load(os.path.join(G.ASSETS_PATH, "Back5.png"))
    CARD_BACK = pygame.transform.scale(CARD_BACK_IMAGE, (CARD_WIDTH, CARD_HEIGHT))


    LEFT_BOUNDARY = G.DISPLAY_SURFACE.get_rect().centerx - 2.5*CARD_WIDTH
    TOP_BOUNDARY = G.DISPLAY_SURFACE.get_rect().centery - 2.0*CARD_HEIGHT
    RIGHT_BOUNDARY = G.DISPLAY_SURFACE.get_rect().centerx + 2.5*CARD_WIDTH
    BOTTOM_BOUNDARY = G.DISPLAY_SURFACE.get_rect().centery + 2.0*CARD_HEIGHT

    CARDS_POSITIONS = []
    for i in range(4):
        for j in range (5):
            CARDS_POSITIONS.append((LEFT_BOUNDARY + j*CARD_WIDTH, TOP_BOUNDARY + i*CARD_HEIGHT))

    CARDS_RECTS = []
    for position in CARDS_POSITIONS:
        CARDS_RECTS.append(pygame.Rect(position, (CARD_WIDTH, CARD_HEIGHT)))
    
    CARDS_FACES_IMAGES = [pygame.image.load(os.path.join(G.ASSETS_PATH, "A.H.png")), # Ace of Hearts
                          pygame.image.load(os.path.join(G.ASSETS_PATH, "A.S.png")), # Ace of Spades
                          ]
    for i in range(2, 11):
        CARDS_FACES_IMAGES.append(pygame.image.load(os.path.join(G.ASSETS_PATH, str(i)+".H.png"))) # i of Hearts
        CARDS_FACES_IMAGES.append(pygame.image.load(os.path.join(G.ASSETS_PATH, str(i)+".S.png"))) # i of Spades

    CARDS_FACES = []
    for image in CARDS_FACES_IMAGES:
        CARDS_FACES.append(pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT)))
    
    # Shuffle the cards
    random.shuffle(CARDS_FACES)
    
    # Numbers on the back of the cards
    NUMBERS_FONT_SIZE = int(CARD_HEIGHT)//4
    NUMBERS_FONT = pygame.font.SysFont("timesnewroman", NUMBERS_FONT_SIZE, bold=True)
    NUMBERS_POSITIONS = []
    
    for position in CARDS_POSITIONS:
        NUMBERS_POSITIONS.append((position[0] + CARD_WIDTH/2 - NUMBERS_FONT_SIZE/2, position[1] + CARD_HEIGHT/2 - NUMBERS_FONT_SIZE/2))

    # Keep track of the cards that are flipped
    flipped_cards = [False for i in range(20)]


def draw_window():
    # Render Background
    G.DISPLAY_SURFACE.fill(G.POKER_GREEN)

    # Render cards
    for i, position in enumerate(Cards.CARDS_POSITIONS):
        if(Cards.flipped_cards[i]):
            G.DISPLAY_SURFACE.blit(Cards.CARDS_FACES[i], position)
            #pygame.draw.rect(G.DISPLAY_SURFACE, G.WHITE, Cards.CARDS_RECTS[i])
        else:
            G.DISPLAY_SURFACE.blit(Cards.CARD_BACK, position)

    # Render numbers on the back of the cards
    for i, position in enumerate(Cards.NUMBERS_POSITIONS):
        text = Cards.NUMBERS_FONT.render("", 1, G.PURPLEISH)
        if(i < 9 and not Cards.flipped_cards[i]):
            text = Cards.NUMBERS_FONT.render("0"+str(i+1), 1, G.BLACK)
        elif(not Cards.flipped_cards[i]):
            text = Cards.NUMBERS_FONT.render(str(i+1), 1, G.BLACK)

        G.DISPLAY_SURFACE.blit(text, position)

    pygame.display.update()


def main():

    clock = pygame.time.Clock()

    run = True

    while(run):


        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False
            
            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_ESCAPE):
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            
            if(event.type == pygame.MOUSEBUTTONDOWN):
                if(event.button == 1):
                    for i, card_rect in enumerate(Cards.CARDS_RECTS):
                        if(card_rect.collidepoint(event.pos)):
                            Cards.flipped_cards[i] = not Cards.flipped_cards[i]
                            break

        draw_window()

        # Makes sure loop runs at most at `G.FPS` times per second i.e 60 times per second if G.FPS = 60
        clock.tick(G.FPS)
    
    pygame.quit()


if __name__ == "__main__":
    main()
