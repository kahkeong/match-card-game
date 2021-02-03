from os import listdir
from card import Card
from enum_game_state import GameState
import sys
import random
import pygame


def create_cards():
    selected_fruits = random.sample(fruits, NUMBER_OF_CARDS)

    # each fruit should have 2 instances so we extend
    selected_fruits.extend(selected_fruits)
    random.shuffle(selected_fruits)
    new_cards = []
    index = 0

    for x in range(ROW):
        for y in range(COLUMN):
            card_rect = pygame.Rect(
                y * CARD_SIZE + (CARD_BORDER_GAP * y) + CARD_BORDER_GAP,
                TOP_BAR_GAP + x * CARD_SIZE + (CARD_BORDER_GAP * x) + CARD_BORDER_GAP,
                CARD_SIZE,
                CARD_SIZE,
            )
            new_cards.append(Card(selected_fruits[index], card_rect))
            index += 1

    return new_cards


pygame.init()
# colors
BUTTON_COLOR = 153, 255, 200
WHITE_COLOR = 255, 255, 255
BACKGROUND_COLOR = 255, 153, 51
TOP_BAR_BACKGROUND_COLOR = 102, 102, 153

# UI sizes
TOP_BAR_GAP = 30
CARD_SIZE = 90
CARD_BORDER_GAP = 10
ROW = 3
COLUMN = 4
# 4 X 3 map
WIDTH = CARD_SIZE * COLUMN + CARD_BORDER_GAP * (COLUMN + 1)
HEIGHT = TOP_BAR_GAP + CARD_SIZE * ROW + CARD_BORDER_GAP * (ROW + 1)

# UI stuff
font = pygame.font.Font(None, 36)
memory_game_text = font.render("Memory Game", True, (10, 10, 10))
start_text = font.render("Start", True, (10, 10, 10))
quit_text = font.render("Quit", True, (10, 10, 10))
option_text = font.render("Option", True, (10, 10, 10))
resume_text = font.render("Resume", True, (10, 10, 10))
restart_text = font.render("Restart", True, (10, 10, 10))
main_menu_text = font.render("Main Menu", True, (10, 10, 10))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = screen.get_rect()

# other constants
NUMBER_OF_CARDS = 6
FPS = 30
clock = pygame.time.Clock()
# fruits image location
fruits = listdir("fruits")
# load images and store as hash map
fruit_images = {}
for fruit in fruits:
    image = pygame.image.load("fruits/" + fruit)
    image = pygame.transform.scale(image, (CARD_SIZE, CARD_SIZE))
    fruit_images[fruit] = image

# initial state
game_state = GameState.MAIN_MENU
cards = create_cards()
round_number = 0


create_cards()
# game loop
while True:
    clock.tick(FPS)

    # update screen code start here
    if game_state == GameState.MAIN_MENU:
        screen.fill(BACKGROUND_COLOR)
        memory_game_pos = memory_game_text.get_rect()
        memory_game_pos.center = screen_rect.center

        start_text_pos = start_text.get_rect()
        # position start_text center +50y from memory_game_text center
        start_text_pos.center = tuple(map(sum, zip((0, 50), memory_game_pos.center)))
        quit_text_pos = quit_text.get_rect()
        quit_text_pos.center = tuple(map(sum, zip((0, 50), start_text_pos.center)))

        screen.blit(memory_game_text, memory_game_pos.topleft)

        screen.fill(BUTTON_COLOR, start_text_pos)
        screen.blit(start_text, start_text_pos.topleft)

        screen.fill(BUTTON_COLOR, quit_text_pos)
        screen.blit(quit_text, quit_text_pos.topleft)

    elif game_state == GameState.IN_PROGRESS:
        round_number_text = font.render(f"Round: {round_number}", True, (10, 10, 10))
        round_number_text_pos = round_number_text.get_rect()
        option_text_pos = option_text.get_rect(left=WIDTH * 3 // 4)

        screen.fill(BACKGROUND_COLOR)
        screen.fill(
            TOP_BAR_BACKGROUND_COLOR, rect=pygame.Rect(0, 0, WIDTH, TOP_BAR_GAP)
        )
        screen.blit(round_number_text, round_number_text_pos)
        screen.fill(BUTTON_COLOR, option_text_pos)
        screen.blit(option_text, option_text_pos)

        for card in cards:
            screen.fill(WHITE_COLOR, card.rect)
            screen.blit(fruit_images[card.name], card.rect)

    elif game_state == GameState.PAUSED:
        resume_text_pos = resume_text.get_rect()
        resume_text_pos.center = screen_rect.center

        restart_text_pos = restart_text.get_rect()
        restart_text_pos.center = tuple(map(sum, zip((0, 50), resume_text_pos.center)))

        main_menu_text_pos = main_menu_text.get_rect()
        main_menu_text_pos.center = tuple(
            map(sum, zip((0, 50), restart_text_pos.center))
        )

        screen.fill(BACKGROUND_COLOR)
        screen.fill(BUTTON_COLOR, resume_text_pos)
        screen.blit(resume_text, resume_text_pos.topleft)

        screen.fill(BUTTON_COLOR, restart_text_pos)
        screen.blit(restart_text, restart_text_pos.topleft)

        screen.fill(BUTTON_COLOR, main_menu_text_pos)
        screen.blit(main_menu_text, main_menu_text_pos.topleft)

    elif game_state == GameState.END:
        restart_text_pos = restart_text.get_rect()
        restart_text_pos.center = tuple(map(sum, zip((0, 50), resume_text_pos.center)))

        main_menu_text_pos = main_menu_text.get_rect()
        main_menu_text_pos.center = tuple(
            map(sum, zip((0, 50), restart_text_pos.center))
        )

        screen.fill(BUTTON_COLOR, restart_text_pos)
        screen.blit(main_menu_text, main_menu_text_pos.topleft)

        screen.fill(BUTTON_COLOR, main_menu_text_pos)
        screen.blit(quit_text, main_menu_text_pos.topleft)

    # logic code start here
    if game_state == GameState.MAIN_MENU:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()

                if start_text_pos.collidepoint(pos):
                    game_state = GameState.IN_PROGRESS

                if quit_text_pos.collidepoint(pos):
                    pygame.quit()
                    sys.exit()

    elif game_state == GameState.IN_PROGRESS:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()

                if option_text_pos.collidepoint(pos):
                    game_state = GameState.PAUSED

    elif game_state == GameState.PAUSED:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()

                if resume_text_pos.collidepoint(pos):
                    game_state = GameState.IN_PROGRESS
                elif restart_text_pos.collidepoint(pos):
                    cards = create_cards()
                    round_number = 0
                    game_state = GameState.IN_PROGRESS
                elif main_menu_text_pos.collidepoint(pos):
                    cards = create_cards()
                    round_number = 0
                    game_state = GameState.MAIN_MENU

    elif game_state == GameState.END:
        pass

    pygame.display.flip()
