import logging
import random
import sys
from collections import defaultdict
from os import listdir
from pathlib import Path
import pygame
import config as c
import threading
from fruit import Fruit
from button import Button
from card import Card
from enum_game_state import GameState
from text import Text

logging.basicConfig(level=logging.INFO, format="%(message)s")


class Game:
    def __init__(self):
        self.cards = []
        self.state = GameState.MAIN_MENU
        self.round_number = 0
        self.is_running_cards_animation = False
        self.previous_time = None
        self.showing_card_number = 0
        self.exit = False
        self.objects = defaultdict(list)
        self.click_handlers = defaultdict(list)
        self.clock = pygame.time.Clock()
        self.is_click_disabled = False
        self.fruits = []
        self.row = c.DEFAULT_ROW_SIZE
        self.column = c.DEFAULT_COLUMN_SIZE
        self.surface = None

        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

    def reset(self):
        self.round_number = 0
        self.is_running_cards_animation = False
        self.previous_time = None
        self.showing_card_number = 0
        self.objects = defaultdict(list)
        self.click_handlers = defaultdict(list)
        self.cards = []
        self.setup()

    def is_game_end(self):
        """
        check whether all the card have already been matched
        """
        return all(card.is_matched for card in self.cards)

    def run_cards_animation(self):
        """
        open each of the card from top to bottom, left to right for short duration for a brief duration before closing it,
        this provider user the chance try memorizing the cards
        """

        if self.is_running_cards_animation:
            # we start flipping the cards from this time
            if self.previous_time is None:
                self.previous_time = pygame.time.get_ticks()
            current_time = pygame.time.get_ticks()
            if current_time >= self.previous_time + c.MILLISECOND_TO_SHOW_EACH_CARD:
                # close the previous card
                if self.showing_card_number >= 1:
                    self.cards[self.showing_card_number - 1].is_selected = False

                # open current card
                if self.showing_card_number < len(self.cards):
                    self.cards[self.showing_card_number].is_selected = True
                    self.previous_time = current_time
                self.showing_card_number += 1

            # finished showing all the cards
            if self.showing_card_number > len(self.cards):
                self.is_running_cards_animation = False

    def read_input(self):
        """
        by default, the grid size is 3x4, check for user inputs and whether the inputs are valid and update the grid size accordingly
        """
        arg_list = sys.argv
        input_valid = False

        # no arguments were passed in
        if len(arg_list) == 1:
            pass
        else:
            try:
                input_row = int(arg_list[1])
                input_column = int(arg_list[2])

                if (
                    input_row <= 2
                    or input_column <= 3
                    or input_row * input_column > len(self.fruits) * 2
                    or input_row * input_column % 2 != 0
                ):
                    raise GridSizeError()
                self.row = input_row
                self.column = input_column
                input_valid = True

            except ValueError:
                logging.info("Invalid arguments, arguments should be type number")
                logging.info("Fall back to default values")
            except IndexError:
                logging.info("Please provide two arguments")
                logging.info("Fall back to default values")
            except GridSizeError:
                logging.info(
                    f"Invalid arguments, arguments must fulfill following values, row>=3, column>= 4, row x column <= {len(self.fruits)*2}, row*column is even"
                )

        if input_valid:
            logging.info(
                f"Board are initialized to requested grid size of {self.row}x{self.column}"
            )
        else:
            logging.info(
                f"For best experience, board are initialized to default grid size of {self.row}x{self.column}"
            )

    def setup(self):
        width = c.CARD_SIZE * self.column + c.CARD_BORDER_GAP * (self.column + 1)
        height = (
            c.TOP_BAR_GAP + c.CARD_SIZE * self.row + c.CARD_BORDER_GAP * (self.row + 1)
        )
        self.surface = pygame.display.set_mode((width, height))

        self.create_cards()
        self.create_main_menu()
        self.create_pause_menu()
        self.create_top_bar()
        self.create_end_menu()

    def create_cards(self):
        """
        create x number of cards based on the product of row and column and shuffle them
        """
        selected_fruits = random.sample(self.fruits, self.row * self.column // 2)

        # each fruit should have 2 cards to represent it so we extend
        selected_fruits.extend(selected_fruits)
        random.shuffle(selected_fruits)

        for x in range(self.row):
            for y in range(self.column):
                card_rect = pygame.Rect(
                    y * c.CARD_SIZE + (c.CARD_BORDER_GAP * y) + c.CARD_BORDER_GAP,
                    c.TOP_BAR_GAP
                    + x * c.CARD_SIZE
                    + (c.CARD_BORDER_GAP * x)
                    + c.CARD_BORDER_GAP,
                    c.CARD_SIZE,
                    c.CARD_SIZE,
                )
                fruit = selected_fruits[x * self.column + y]
                self.cards.append(Card(fruit, card_rect))

        self.objects[GameState.IN_PROGRESS].extend(self.cards)
        self.click_handlers[GameState.IN_PROGRESS].extend(self.cards)

    def create_end_menu(self):
        def on_restart():
            self.reset()
            self.state = GameState.IN_PROGRESS
            self.is_running_cards_animation = True

        def on_main_menu():
            self.state = GameState.MAIN_MENU

        round_to_finish_text = Text(
            100,
            100,
            lambda: f"Took {self.round_number} rounds to finish !",
            self.font,
            False,
        )

        restart_button = Button(
            100,
            150,
            c.BUTTON_WIDTH,
            c.BUTTON_HEIGHT,
            lambda: "Restart",
            self.font,
            on_restart,
        )
        main_menu_button = Button(
            100,
            200,
            c.BUTTON_WIDTH,
            c.BUTTON_HEIGHT,
            lambda: "Main Menu",
            self.font,
            on_main_menu,
        )

        self.click_handlers[GameState.END].extend([restart_button, main_menu_button])
        self.objects[GameState.END].extend(
            [round_to_finish_text, restart_button, main_menu_button]
        )

    def create_top_bar(self):
        def on_pause():
            self.state = GameState.PAUSED

        round_took_text = Text(
            0, 0, lambda: f"Round: {self.round_number}", self.font, False
        )
        pause_button = Button(
            self.surface.get_size()[0] - c.BUTTON_WIDTH,
            0,
            c.BUTTON_WIDTH,
            c.BUTTON_HEIGHT,
            lambda: "Pause",
            self.font,
            on_pause,
        )

        self.click_handlers[GameState.IN_PROGRESS].append(pause_button)
        self.objects[GameState.IN_PROGRESS].extend([pause_button, round_took_text])

    def create_main_menu(self):
        def on_start():
            self.reset()
            self.state = GameState.IN_PROGRESS
            self.is_running_cards_animation = True

        def on_quit():
            self.exit = True

        start_button = Button(
            100,
            100,
            c.BUTTON_WIDTH,
            c.BUTTON_HEIGHT,
            lambda: "Start",
            self.font,
            on_start,
        )
        quit_button = Button(
            100,
            150,
            c.BUTTON_WIDTH,
            c.BUTTON_HEIGHT,
            lambda: "Quit",
            self.font,
            on_quit,
        )

        self.click_handlers[GameState.MAIN_MENU].extend([start_button, quit_button])
        self.objects[GameState.MAIN_MENU].extend([start_button, quit_button])

    def create_pause_menu(self):
        def on_resume():
            self.state = GameState.IN_PROGRESS

        def on_restart():
            self.reset()
            self.state = GameState.IN_PROGRESS
            self.is_running_cards_animation = True

        def on_main_menu():
            self.state = GameState.MAIN_MENU

        resume_button = Button(
            100,
            100,
            c.BUTTON_WIDTH,
            c.BUTTON_HEIGHT,
            lambda: "Resume",
            self.font,
            on_resume,
        )
        restart_button = Button(
            100,
            150,
            c.BUTTON_WIDTH,
            c.BUTTON_HEIGHT,
            lambda: "Restart",
            self.font,
            on_restart,
        )
        main_menu_button = Button(
            100,
            200,
            c.BUTTON_WIDTH,
            c.BUTTON_HEIGHT,
            lambda: "Main Menu",
            self.font,
            on_main_menu,
        )

        self.click_handlers[GameState.PAUSED].extend(
            [resume_button, restart_button, main_menu_button]
        )
        self.objects[GameState.PAUSED].extend(
            [resume_button, restart_button, main_menu_button]
        )

    def check_two_cards_opened(self):
        """check whether there are two opened cards and if they matched, update them"""

        if self.is_click_disabled:
            return

        opened_cards = [card for card in self.cards if card.is_selected]

        if len(opened_cards) == 2:
            card1, card2 = opened_cards

            self.round_number += 1
            if card1 == card2:
                card1.is_matched = True
                card2.is_matched = True
                card1.is_selected = False
                card2.is_selected = False
            else:
                self.is_click_disabled = pygame.time.get_ticks()

                def update_disable_click_state():
                    self.is_click_disabled = not self.is_click_disabled
                    card1.is_selected = False
                    card2.is_selected = False

                timer = threading.Timer(c.DISABLE_TIME, update_disable_click_state)
                timer.start()  # after

    def is_game_finished(self):
        """check are all cards matched"""
        return all(card.is_matched for card in self.cards)

    def update(self):
        if self.exit:
            pygame.quit()
            sys.exit()

        if self.state == GameState.IN_PROGRESS:
            self.run_cards_animation()
            self.check_two_cards_opened()
            is_game_finished = self.is_game_finished()

            if is_game_finished:
                self.state = GameState.END

    def draw(self):
        for obj in self.objects[self.state]:
            obj.draw(self.surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.is_click_disabled:
                    return

                for handler in self.click_handlers[self.state]:
                    handler.on_click(event.pos)

    def get_fruits(self):
        """load images and store as hash map"""
        path = Path(__file__).parent / "fruits"
        fruit_names = listdir(path)

        for name in fruit_names:
            image = pygame.image.load(path / name)
            image = pygame.transform.scale(image, (c.CARD_SIZE, c.CARD_SIZE))
            fruit = Fruit(name, image)
            self.fruits.append(fruit)

    def run(self):
        pygame.display.set_caption("Match card game")
        self.get_fruits()
        self.read_input()
        self.setup()

        while True:
            self.surface.fill(c.BACKGROUND_COLOR)
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.flip()
            self.clock.tick(c.FPS)


class GridSizeError(Exception):
    pass


def main():
    Game().run()


if __name__ == "__main__":
    main()
