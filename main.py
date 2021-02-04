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
BLUE_COLOR = 0, 0, 255
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
NUMBER_OF_CARDS = ROW * COLUMN // 2
FPS = 30
MILLISECOND_TO_SHOW_EACH_CARD = 300
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
show_card = True
previous_time = None
showing_card_number = 0


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
        # flip open the cards so user can have a glimpse at each of them.
        if show_card:
            if previous_time is None:
                # we start flipping the cards from this time
                previous_time = pygame.time.get_ticks()
            current_time = pygame.time.get_ticks()
            if current_time >= previous_time + MILLISECOND_TO_SHOW_EACH_CARD:
                # close the previous card
                if showing_card_number >= 1:
                    cards[showing_card_number - 1].is_selected = False

                # open current card
                if showing_card_number < NUMBER_OF_CARDS * 2:
                    cards[showing_card_number].is_selected = True
                    previous_time = current_time
                showing_card_number += 1

            if showing_card_number > NUMBER_OF_CARDS * 2:
                # finished showing all the cards
                show_card = False

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
            if card.is_selected or card.is_matched:
                screen.fill(WHITE_COLOR, card.rect)
                screen.blit(fruit_images[card.name], card.rect)
            else:
                screen.fill(BLUE_COLOR, card.rect)

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
        round_number_text = font.render(
            f"Took {round_number} rounds to finish !", True, (10, 10, 10)
        )
        round_number_text_pos = round_number_text.get_rect()
        round_number_text_pos.center = screen_rect.center

        restart_text_pos = restart_text.get_rect()
        restart_text_pos.center = tuple(
            map(sum, zip((0, 50), round_number_text_pos.center))
        )

        main_menu_text_pos = main_menu_text.get_rect()
        main_menu_text_pos.center = tuple(
            map(sum, zip((0, 50), restart_text_pos.center))
        )

        screen.fill(BACKGROUND_COLOR)
        screen.blit(round_number_text, round_number_text_pos.topleft)

        screen.fill(BUTTON_COLOR, restart_text_pos)
        screen.blit(restart_text, restart_text_pos.topleft)

        screen.fill(BUTTON_COLOR, main_menu_text_pos)
        screen.blit(main_menu_text, main_menu_text_pos.topleft)

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
        # if the UI is still showing the cards, dun react to clicking events
        if not show_card:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()

                    if option_text_pos.collidepoint(pos):
                        game_state = GameState.PAUSED

                    for card in cards:
                        if card.rect.collidepoint(pos) and not card.is_matched:
                            card.is_selected = True

            # check whether two opened cards are match while ignoring matched card
            opened_card_count = 0
            opened_cards = []
            for card in cards:
                if card.is_selected:
                    opened_card_count += 1
                    opened_cards.append(card)

            if opened_card_count == 2:
                card1, card2 = opened_cards
                if card1.name == card2.name:
                    card1.is_matched = True
                    card2.is_matched = True
                card1.is_selected = False
                card2.is_selected = False
                round_number += 1

            # check are all cards matched
            for card in cards:
                if not card.is_matched:
                    break
            else:
                game_state = GameState.END

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
                    show_card = True
                    game_state = GameState.IN_PROGRESS
                    showing_card_number = 0
                elif main_menu_text_pos.collidepoint(pos):
                    cards = create_cards()
                    round_number = 0
                    show_card = True
                    game_state = GameState.MAIN_MENU
                    showing_card_number = 0

    elif game_state == GameState.END:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()

                if restart_text_pos.collidepoint(pos):
                    cards = create_cards()
                    round_number = 0
                    show_card = True
                    game_state = GameState.IN_PROGRESS
                    showing_card_number = 0
                elif main_menu_text_pos.collidepoint(pos):
                    cards = create_cards()
                    round_number = 0
                    show_card = True
                    game_state = GameState.MAIN_MENU
                    showing_card_number = 0

    pygame.display.flip()
