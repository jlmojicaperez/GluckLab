import os
import pygame
import random

from dataclasses import dataclass

pygame.init()
pygame.font.init()
pygame.mixer.init()

@dataclass
class G:
    '''
    Keeps track of globals, game constants and variables not related to the players or the cards.

    Fields:
        FPS: The number of times the game loop runs per second
        ASSETS_PATH: The path to the assets folder
        DISPLAY_INFO: The display info of the display surface
        DISPLAY_WIDTH: The width of the display surface
        DISPLAY_HEIGHT: The height of the display surface
        DISPLAY_SURFACE: The display surface
        BRAIN_IMAGE: The pixelated image of the brain
        BACKGROUND_IMAGE: The background image
        WHITE: The color white
        BLACK: The color black
        GREY: The color grey
        RED: The color red
        BLUE: The color blue
        POKER_GREEN: The color poker green
        PURPLEISH: A purpleish color
        FONTS_PATH: The path to the fonts folder
        FONT_SIZE: The font size of the main font
        FONT: The main font
        MEDIUM_FONT: A smaller version of the main font
        SOUNDS_PATH: The path to the sounds folder
        FLIP_SOUND: The sound that plays when a card is flipped
        CORRECT_SOUND: The sound that plays when two cards match
        WRONG_SOUND: The sound that plays when two cards don't match
        WINNER_SOUND: The sound that plays when someone wins
        TIE_SOUND: The sound that plays when it's a tie
        ROUND1_SOUND: The sound that plays when round 1 starts
        ROUND2_SOUND: The sound that plays when round 2 starts
        ROUND3_SOUND: The sound that plays when round 3 starts
        ROUNDS: The number of rounds
        curr_round: The current round number

    Methods:
        reset_game: Resets the game
        next_round: Increments the current round number and loads the cards of the next round
    '''

    # Constants
    FPS = 60
    ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

    # Display Surface
    DISPLAY_INFO = pygame.display.Info()
    DISPLAY_WIDTH, DISPLAY_HEIGHT = DISPLAY_INFO.current_w, DISPLAY_INFO.current_h
    DISPLAY_SURFACE = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    pygame.display.set_caption("Concentration")
    BRAIN_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "PixelatedBrain.png")),
                                         (DISPLAY_HEIGHT//2, DISPLAY_HEIGHT//2))
    pygame.display.set_icon(pygame.transform.scale(BRAIN_IMAGE, (32, 32)))

    # Background
    BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "background.png")),
                                              (DISPLAY_WIDTH, DISPLAY_HEIGHT))


    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (128, 128, 128)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    POKER_GREEN = (0, 54, 38)
    PURPLEISH = (186, 26, 108)

    # Fonts
    FONTS_PATH = os.path.join(ASSETS_PATH, "fonts")
    FONT_SIZE = DISPLAY_HEIGHT//10
    FONT = pygame.font.Font(os.path.join(FONTS_PATH, "pixeloid_sans", "PixeloidSansBold-PKnYd.ttf"), FONT_SIZE)
    MEDIUM_FONT = pygame.font.Font(os.path.join(FONTS_PATH, "pixeloid_sans", "PixeloidSansBold-PKnYd.ttf"), FONT_SIZE//2)
    
    # Sounds
    SOUNDS_PATH = os.path.join(ASSETS_PATH, "sounds")
    FLIP_SOUND = pygame.mixer.Sound(os.path.join(SOUNDS_PATH,"flipcard.mp3"))
    CORRECT_SOUND = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, "correct.mp3"))
    WRONG_SOUND = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, "wrong.mp3"))
    WINNER_SOUND = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, "winner.mp3"))
    TIE_SOUND = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, "tie.mp3"))
    ROUND1_SOUND = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, "round1_bell.mp3"))
    ROUND2_SOUND = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, "round2_bell.mp3"))
    ROUND3_SOUND = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, "round3_bell.mp3"))

    # Game stuff
    ROUNDS = 3
    curr_round = 0

    def reset_game():
        Cards.flipped_cards = [False for i in range(20)]
        Cards.matched_cards = [False for i in range(20)]
        Cards.current_guess = None
        Players.reset_scores()
        Players.current_player = Players.p1
        Players.winner = None
    
    def next_round():
        G.curr_round += 1
        Cards.CARDS_FACES, Cards.CARDS_NAMES = Cards.load_cards(G.curr_round)
        Cards.CARDS_FACES, Cards.CARDS_NAMES = Cards.shuffle_cards(CARDS_FACES=Cards.CARDS_FACES, CARDS_NAMES=Cards.CARDS_NAMES)
        Cards.flipped_cards = [False for i in range(20)]
        Cards.matched_cards = [False for i in range(20)]
        Cards.current_guess = None
        Players.current_player = Players.p1 if Players.current_player == Players.p2 else Players.p2

@dataclass
class Cards:
    '''
    Keeps track of the cards, their positions, their names, their faces, their backs, their numbers and their rectangles.
    
    Fields:
        CARD_WIDTH: The width of the card
        CARD_HEIGHT: The height of the card
        CARD_BACK_IMAGE: The image of the back of the card
        CARD_BACK: The scaled image of the back of the card
        LEFT_BOUNDARY: The left boundary of the card grid
        TOP_BOUNDARY: The top boundary of the card grid
        RIGHT_BOUNDARY: The right boundary of the card grid
        BOTTOM_BOUNDARY: The bottom boundary of the card grid
        CARDS_POSITIONS: A list of tuples that represent the positions of the cards
        CARDS_RECTS: A list of rectangles on the positions of the cards used to detect mouse clicks
        CARDS_FACES: A list of images of the faces of the cards
        CARDS_NAMES: A list of strings that represent the names of the cards. This is what is compared to see if two cards match.
        NUMBERS_FONT_SIZE: The font size of the numbers on the back of the cards
        NUMBERS_FONT: The font of the numbers on the back of the cards
        NUMBERS_POSITIONS: A list of tuples that represent the positions of the numbers on the back of the cards
        flipped_cards: A list of booleans that represent if a card is flipped or not
        matched_cards: A list of booleans that represent if a card is matched or not
        current_guess: The index of the current guess. This is used to compare two cards to see if they match.

    Methods:
        load_cards: Loads the cards of the current round. This is called when the round changes.
        shuffle_cards: Shuffles the cards
    '''
    CARD_WIDTH = (G.DISPLAY_WIDTH)//12
    CARD_HEIGHT = CARD_WIDTH * 7//5

    CARD_BACK_IMAGE = pygame.image.load(os.path.join(G.ASSETS_PATH, "cards", "Back3.png"))
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
    

    def load_cards(curr_round, CARD_WIDTH=CARD_WIDTH, CARD_HEIGHT=CARD_HEIGHT):
        CARDS_FACES_IMAGES = []
        CARDS_FACES =[]
        for i in range(10):
            CARDS_FACES_IMAGES.append(pygame.image.load(os.path.join(G.ASSETS_PATH, "cards", f"round{curr_round}", f"{i}.png")))

        for image in CARDS_FACES_IMAGES:
            # Append twice because there are two cards of each type
            CARDS_FACES.append(pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT)))
            CARDS_FACES.append(pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT)))

        CARDS_NAMES = []
        for i in range(10):
            CARDS_NAMES.append(str(i))
            CARDS_NAMES.append(str(i))
        
        return CARDS_FACES, CARDS_NAMES
    
    # Shuffle the cards
    def shuffle_cards(CARDS_FACES, CARDS_NAMES):
        CARDS_FACES, CARDS_NAMES = zip(*random.sample(list(zip(CARDS_FACES, CARDS_NAMES)), len(CARDS_FACES)))
        return CARDS_FACES, CARDS_NAMES
    
    CARDS_FACES, CARDS_NAMES = load_cards(1)
    CARDS_FACES, CARDS_NAMES = shuffle_cards(CARDS_FACES, CARDS_NAMES)  

    # Numbers on the back of the cards
    NUMBERS_FONT_SIZE = int(CARD_WIDTH)//2
    NUMBERS_FONT = pygame.font.Font(os.path.join(G.FONTS_PATH, "pixeloid_sans", "PixeloidSansBold-PKnYd.ttf"), NUMBERS_FONT_SIZE)

    NUMBERS_POSITIONS = []
    # put numbers in the middle of each card
    for position in CARDS_POSITIONS:
        NUMBERS_POSITIONS.append((position[0] + CARD_WIDTH/2 - NUMBERS_FONT_SIZE/1.5 - 3, position[1] + CARD_HEIGHT/2 - NUMBERS_FONT_SIZE/2))

    # Keep track of the cards that are flipped
    flipped_cards = [False for i in range(20)]
    matched_cards = [False for i in range(20)]

    current_guess = None


class Player:
    '''
    Keeps track of the player's name, score and color.

    Fields:
        name: The name of the player
        score: The score of the player
        color: The color of the player

    Methods:
        increase_score: Increases the score of the player by 1
        reset_score: Resets the score of the player to 0
        get_score: Returns the score of the player
        get_name: Returns the name of the player
        get_color: Returns the color of the player
    '''
    def __init__(self, name, color=G.RED):
        self.name = name
        self.score = 0
        self.color = color

    def increase_score(self):
        self.score += 1

    def reset_score(self):
        self.score = 0

    def get_score(self):
        return self.score

    def get_name(self):
        return self.name
    
    def get_color(self):
        return self.color

    def __str__(self):
        '''
        Returns a string representation of the player in the format:
        `name: score`

        This is used to display the score of the player on the screen.
        This is what is called when a string representation of the player is needed by a function.
        '''
        return f"{self.name}: {self.score}"

@dataclass
class Players:
    '''
    Keeps track of the players and the current player. 
    Also keeps track of the whose turn is it and the winner of the game.

    Fields:
        p1: Player 1
        p2: Player 2
        current_player: The current player
        winner: The winner of the game
    
    Methods:
        switch_players: Switches the current player
        reset_scores: Resets the scores of both players
    '''
    p1 = Player("Player 1", G.RED)
    p2 = Player("Player 2", G.BLUE)

    current_player = p1

    winner = None

    def switch_players():
        if(Players.current_player == Players.p1):
            Players.current_player = Players.p2
        else:
            Players.current_player = Players.p1
    
    def reset_scores():
        Players.p1.reset_score()
        Players.p2.reset_score()

    # player font
    PLAYER_FONT_SIZE = int(Cards.CARD_HEIGHT)//4
    PLAYER_FONT = pygame.font.Font(os.path.join(G.FONTS_PATH, "pixeloid_sans", "PixeloidSansBold-PKnYd.ttf"), PLAYER_FONT_SIZE)
    
def draw_game_screen():
    '''
    Draws the game screen. Draws the background, the cards, the numbers on the back of the cards, the current player and the scores.
    '''
    # Render Background
    G.DISPLAY_SURFACE.blit(G.BACKGROUND_IMAGE, (0,0))

    # Render cards
    for i, position in enumerate(Cards.CARDS_POSITIONS):
        if(Cards.flipped_cards[i]):
            G.DISPLAY_SURFACE.blit(Cards.CARDS_FACES[i], position)
        else:
            G.DISPLAY_SURFACE.blit(Cards.CARD_BACK, position)

    # Render numbers on the back of the cards
    for i, position in enumerate(Cards.NUMBERS_POSITIONS):
        text = Cards.NUMBERS_FONT.render("", 1, G.BLACK)
        if(i < 9 and not Cards.flipped_cards[i]):
            text = Cards.NUMBERS_FONT.render("0"+str(i+1), 1, G.BLACK)
        elif(not Cards.flipped_cards[i]):
            text = Cards.NUMBERS_FONT.render(str(i+1), 1, G.BLACK)

        G.DISPLAY_SURFACE.blit(text, position)

    # Render current player
    color = G.WHITE
    if(Players.current_player == Players.p1):
        color = G.RED
    else:
        color = G.BLUE

    text = Players.PLAYER_FONT.render(Players.current_player.get_name() + "'s turn", 1, color)
    G.DISPLAY_SURFACE.blit(text, (G.DISPLAY_WIDTH//2 - text.get_width()//2, Cards.TOP_BOUNDARY - text.get_height()))

    # Render scores
    text = Players.PLAYER_FONT.render(str(Players.p1), 1, G.RED)
    G.DISPLAY_SURFACE.blit(text, ((Cards.LEFT_BOUNDARY - text.get_width())//2, G.DISPLAY_HEIGHT//2 - text.get_height() - 10))
    text = Players.PLAYER_FONT.render(str(Players.p2), 1, G.BLUE)
    G.DISPLAY_SURFACE.blit(text, ((G.DISPLAY_WIDTH + Cards.RIGHT_BOUNDARY)//2 - text.get_width()//2, G.DISPLAY_HEIGHT//2 - text.get_height() - 10))

    pygame.display.update()


def handle_card_click(i):
    '''
    Handles a card click depending on if its an initial guess or a second guess. 
    Handles if user clicks on the same card twice or if the card is already matched.
    Handles if the two cards match or not.

    Args:
        i: The index of the card that was clicked
    Returns:
        None
    '''
    if(Cards.matched_cards[i] or i == Cards.current_guess): # Card is already matched or it's the current guess
        return
    else:
        Cards.flipped_cards[i] = not Cards.flipped_cards[i]
        # Play sound
        pygame.mixer.Sound.play(G.FLIP_SOUND)

    if(Cards.current_guess == None): # First card out of the available cards (the ones that haven't matched yet) is flipped
        Cards.current_guess = i

    elif(Cards.CARDS_NAMES[Cards.current_guess] == Cards.CARDS_NAMES[i]): # Two cards are flipped and they match
        Cards.matched_cards[i] = True
        Cards.matched_cards[Cards.current_guess] = True
        Cards.current_guess = None

        # Show the cards for 1 second
        draw_game_screen()
        pygame.time.delay(1000)

        # Play sound
        pygame.mixer.Sound.play(G.CORRECT_SOUND)
        Players.current_player.increase_score()
        
    else: # Two cards are flipped and they don't match

        # Show the cards for 1 second
        draw_game_screen()
        pygame.time.delay(1000)
        
        # Play sound
        pygame.mixer.Sound.play(G.WRONG_SOUND)

        # Just in case. I don't think this is necessary
        Cards.matched_cards[i] = False
        Cards.matched_cards[Cards.current_guess] = False

        # Then filp them back
        Cards.flipped_cards[i] = False
        Cards.flipped_cards[Cards.current_guess] = False
        Cards.current_guess = None

        Players.switch_players()



def is_win(matched_cards):
    '''
    Checks if all cards are matched
    
    Args:
        matched_cards: A list of booleans that represent if a card is matched or not
    Returns:
        True if all cards are matched, False otherwise
    '''
    for card in matched_cards:
        if(not card):
            return False
    return True

def draw_start_screen():
    '''
    Draws the start screen. Waits for the user to press any key to start the game.
    if the user presses the escape key or closes the window, the game exits.
    '''
    while True:
        G.DISPLAY_SURFACE.blit(G.BACKGROUND_IMAGE, (0,0))
        G.DISPLAY_SURFACE.blit(G.BRAIN_IMAGE,
                               (G.DISPLAY_WIDTH//2 - G.BRAIN_IMAGE.get_width()//2, G.DISPLAY_HEIGHT//2 - G.BRAIN_IMAGE.get_height()//2))
        text = G.FONT.render("Concentration", 1, G.WHITE)
        G.DISPLAY_SURFACE.blit(text, (G.DISPLAY_WIDTH//2 - text.get_width()//2, 60))
        text = G.MEDIUM_FONT.render("Press any key to start", 1, G.WHITE)
        G.DISPLAY_SURFACE.blit(text, (G.DISPLAY_WIDTH//2 - text.get_width()//2, G.DISPLAY_HEIGHT - (text.get_height()+20)))
        pygame.display.update()
        for event in pygame.event.get():
            if(event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                pygame.quit()
                exit()
            if(event.type == pygame.KEYDOWN):
                return

def draw_win_screen():
    '''
    Draws the win screen. Also plays the appropriate sound depending if someone won or it's a tie.
    '''
    G.DISPLAY_SURFACE.blit(G.BACKGROUND_IMAGE, (0,0))
    if(Players.winner == None):
        text = G.FONT.render("It's a tie!", 1, G.WHITE)
        pygame.mixer.Sound.play(G.TIE_SOUND)
    else:
        text = G.FONT.render(f"{Players.winner.get_name()} wins!", 1, Players.winner.get_color())
        pygame.mixer.Sound.play(G.WINNER_SOUND)
    G.DISPLAY_SURFACE.blit(text, (G.DISPLAY_WIDTH//2 - text.get_width()//2, G.DISPLAY_HEIGHT//2 - text.get_height()//2))
    pygame.display.update()

def draw_round_screen(curr_round):
    '''
    Draws the round transition screen. Also plays the appropriate sound for each round.

    Args:
        curr_round: The current round number
    Returns:
        None
    '''
    G.DISPLAY_SURFACE.blit(G.BACKGROUND_IMAGE, (0,0))
    text = G.FONT.render(f"Round {curr_round}", 1, G.WHITE)
    G.DISPLAY_SURFACE.blit(text, (G.DISPLAY_WIDTH//2 - text.get_width()//2, G.DISPLAY_HEIGHT//2 - text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)
    if(G.curr_round == 1):
        pygame.mixer.Sound.play(G.ROUND1_SOUND)
    elif(G.curr_round == 2):
        pygame.mixer.Sound.play(G.ROUND2_SOUND)
    elif(G.curr_round == 3):
        pygame.mixer.Sound.play(G.ROUND3_SOUND)

def main():
    '''
    Main function
    Creates the game loop and handles events
    '''

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
                            handle_card_click(i)
                            break
            
        if(G.curr_round == 0):
            draw_start_screen()
            G.curr_round += 1
            draw_round_screen(G.curr_round)
            pygame.time.delay(300)
            draw_game_screen()


        if(is_win(Cards.matched_cards) and G.curr_round >= G.ROUNDS):
            if(Players.p1.get_score() == Players.p2.get_score()):
                Players.winner = None
            elif(Players.p1.get_score() > Players.p2.get_score()):
                Players.winner = Players.p1
            else:
                Players.winner = Players.p2
            draw_game_screen()
            pygame.time.delay(1000)
            draw_win_screen()
            pygame.time.delay(3000)
            run = False
        elif(is_win(Cards.matched_cards) and G.curr_round < G.ROUNDS):
            G.next_round()
            draw_round_screen(G.curr_round)
            pygame.time.delay(300)
            draw_game_screen()
        else:
            draw_game_screen()

        # Makes sure loop runs at most at `G.FPS` times per second i.e 60 times per second if G.FPS = 60
        clock.tick(G.FPS)
    
    pygame.quit()


if __name__ == "__main__":
    main()
