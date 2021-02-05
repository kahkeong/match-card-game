from os import listdir
from card import Card
from enum_game_state import GameState
import sys
import random
import pygame
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")


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


class GridSizeError(Exception):
    pass


def read_input():
    argList = sys.argv
    row = DEFAULT_ROW_SIZE
    column = DEFAULT_COLUMN_SIZE
    input_row = None
    input_column = None
    valid = False

    if len(argList) == 1:
        pass
    else:
        logging.info("Note that the minimum grid size is limited to 2x3")
        try:
            input_row = int(argList[1])
            input_column = int(argList[2])
            fruits = listdir("fruits")
            size = len(fruits)
            # print(size)
            # maximum cards available are <= size*2
            if input_row < 2 or input_column < 3 or input_row * input_column > size * 2:
                raise GridSizeError()
            row = input_row
            column = input_column
            valid = True
        except ValueError:
            logging.info("Invalid arguments, arguments should be type number")
            logging.info("Fall back to default values")
        except IndexError:
            logging.info("Please provide two arguments")
            logging.info("Fall back to default values")
        except GridSizeError:
            logging.info(
                f"Invalid arguments, Row value must be >=2 and Column value must be >= 3 and Row x Column should not exceed {size*2}"
            )

    if valid:
        logging.info(f"Board are initialized to requested grid size of {row}x{column}")
    else:
        logging.info(
            f"For best experience, board are initialized to default grid size of {row}x{column}"
        )
    return row, column


pygame.init()
pygame.display.set_caption("Match card game")
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
DEFAULT_ROW_SIZE = 3
DEFAULT_COLUMN_SIZE = 4
ROW, COLUMN = read_input()
# 4 X 3 map
WIDTH = CARD_SIZE * COLUMN + CARD_BORDER_GAP * (COLUMN + 1)
HEIGHT = TOP_BAR_GAP + CARD_SIZE * ROW + CARD_BORDER_GAP * (ROW + 1)


# UI stuff
font = pygame.font.Font(None, 36)
match_card_game_text = font.render("Match Card Game", True, (10, 10, 10))
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
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # update screen code start here
    if game_state == GameState.MAIN_MENU:
        screen.fill(BACKGROUND_COLOR)
        match_card_game_pos = match_card_game_text.get_rect()
        match_card_game_pos.center = screen_rect.center

        start_text_pos = start_text.get_rect()
        # position start_text center +50y from match_card_games_text center
        start_text_pos.center = tuple(
            map(sum, zip((0, 50), match_card_game_pos.center))
        )
        quit_text_pos = quit_text.get_rect()
        quit_text_pos.center = tuple(map(sum, zip((0, 50), start_text_pos.center)))

        screen.blit(match_card_game_text, match_card_game_pos.topleft)

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

        # logging.info(f"Round: {round_number}")
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
                    logging.info(f"{card1.name} is matched")
                else:
                    logging.info(f"{card1.name} and {card2.name} are not a match")
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
