# CONFIG IMPORTS:
import os
from typing import List
# DATA CONFIG:
from Data.config import *
# IMPORTS:
from abc import ABC, abstractmethod
import json
# ENUMS:
from Enums.ColorType import ColorType
from Enums.ButtonType import ButtonType

# PYGAME INITIALIZE:
pygame.init()

# GAME IS RUNNING BOOL:
running = False

# OBSERVER INTERFACE:
class Observer(ABC):
    @abstractmethod
    def update(self):
        pass

# CONCERTE IMPLEMENTATION OF OBSERVER:
class GameBoard(Observer):
    def __init__(self, game_board):
        self.game_board_state = game_board

    def set_game_board_state(self, game_board):
        self.game_board_state = game_board

    def get_game_board_state(self):
        return self.game_board_state

    def draw_grid(self):
        for y in range(0, height, cell_height):
            for x in range(0, width, cell_width):
                cell = pygame.Rect(x, y, cell_width, cell_height)
                pygame.draw.rect(screen, ColorType.GRAY.value, cell, 1)

    def draw_cells(self):
        game_state = game_board.get_game_board_state()
        for y in range(n_cells_y):
            for x in range(n_cells_x):
                cell = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
                if game_state[x, y] == 1:
                    pygame.draw.rect(screen, ColorType.BLACK.value, cell)

    # LOAD ALL GAME LOGIC DATA:
    def load_game_data(self):
        screen.fill(ColorType.WHITE.value)
        self.draw_grid()
        self.draw_cells()
        draw_buttons()
        pygame.display.flip()

    # SAVE GAME STATE:
    def save_game_state(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.game_board_state.tolist(), file)

    # LOAD GAME STATE:
    def load_game_state(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                self.game_board_state = np.array(json.load(file))
                notifyObservers()
        else:
            print(f"File '{filename}' not found. Game state not loaded.")

    # UPDATE IMPLEMENTATION:
    def update(self):
        self.load_game_data()

# GAME STATE:
game_state = np.random.choice([0, 1], size=(n_cells_x, n_cells_y), p=[0.8, 0.2])
# GAME BOARD INSTANCE:
game_board = GameBoard(game_state)
# OBSERVER LIST:
observers: List[Observer] = [GameBoard(game_state)]
# NOTIFY OBSERVERS FUNCTION:
def notifyObservers():
    for observer in observers:
        observer.update()

def next_generation():
    game_state = game_board.get_game_board_state()
    new_state = np.copy(game_state)
    # NEXT ITERATION LOGIC:
    for y in range(n_cells_y):
        for x in range(n_cells_x):
            n_neighbors = game_state[(x - 1) % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x)     % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x - 1) % n_cells_x, (y)     % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y)     % n_cells_y] + \
                          game_state[(x - 1) % n_cells_x, (y + 1) % n_cells_y] + \
                          game_state[(x)     % n_cells_x, (y + 1) % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y + 1) % n_cells_y]

            if game_state[x, y] == 1 and (n_neighbors < 2 or n_neighbors > 3):
                new_state[x, y] = 0
            elif game_state[x, y] == 0 and n_neighbors == 3:
                new_state[x, y] = 1
    # SET NEW GAME STATE:
    game_board.set_game_board_state(new_state)
    notifyObservers()

# BASE ABSTRACT BUTTON CLASS:
class Button(ABC):
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text

    @abstractmethod
    def handle_event(self, event):
        pass

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 26)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))
        screen.blit(text, text_rect)

# BUTTON CLASS FACTORY WITH PARAMETRIZED MEHTOD:
class ButtonFactory:
    @staticmethod
    def create_button(button_type, x, y, width, height, color, text):
        if button_type == ButtonType.SAVE:
            return SaveButton(x, y, width, height, color, text)
        elif button_type == ButtonType.LOAD:
            return LoadButton(x, y, width, height, color, text)
        elif button_type == ButtonType.STOP:
            return StopButton(x, y, width, height, color, text)
        elif button_type == ButtonType.START:
            return StartButton(x, y, width, height, color, text)
        elif button_type == ButtonType.NEXT:
            return NextButton(x, y, width, height, color, text)
        else:
            raise ValueError("Invalid button type")

# BUTTONS: SAVE / LOAD / START / STOP / NEXT
class SaveButton(Button):
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            game_board.save_game_state("game_saves/game_state.json")

class LoadButton(Button):
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            game_board.load_game_state("game_saves/game_state.json")

class StopButton(Button):
    def handle_event(self, event):
        global running
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            running = False

class StartButton(Button):
    def handle_event(self, event):
        global running
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            running = True

class NextButton(Button):
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            next_generation()

button_factory = ButtonFactory()

buttons = [
    button_factory.create_button(ButtonType.NEXT, (width - button_width) // 2, height - button_height - 10, button_width, button_height, ColorType.BLUE.value, "Next Generation"),
    button_factory.create_button(ButtonType.START, (width - button_width) // 2 - button_width - button_spacing, height - button_height - 10, button_width, button_height, ColorType.GREEN.value, "Start"),
    button_factory.create_button(ButtonType.STOP, (width - button_width) // 2 + button_width + button_spacing, height - button_height - 10, button_width, button_height, ColorType.RED.value, "Stop"),
    button_factory.create_button(ButtonType.SAVE, (width - button_width) // 2 - 2 * button_width - 2 * button_spacing, height - button_height - 10, button_width, button_height, ColorType.GRAY.value, "Save"),
    button_factory.create_button(ButtonType.LOAD, (width - button_width) // 2 + 2 * button_width + 2 * button_spacing, height - button_height - 10, button_width, button_height, ColorType.GRAY.value, "Load")
]

def draw_buttons():
    for button in buttons:
        button.draw()

def handle_button_events(event):
    for button in buttons:
        button.handle_event(event)

# MAIN WHILE LOOP TO SET UP AND RUN THE GAME LOOP:
def main():
    game_board.load_game_data()
    while True:
        # CLICK EVENT LISTENER:
        for event in pygame.event.get():
            # QUIT GAME EVENT:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # BUTTON CLICK EVENT CHECK:
            handle_button_events(event)

            # CELL CLICK EVENT:
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_state = game_board.get_game_board_state()
                x, y = event.pos[0] // cell_width, event.pos[1] // cell_height
                game_state[x, y] = not game_state[x, y]
                notifyObservers()

        # START / STOP - IS GAME RUNNING VARIABLE:
        if running:
            # 0.5 SEC. DELAY BETWEEN NEXT ITERATIONS:
            pygame.time.delay(500)
            next_generation()

if __name__ == "__main__":
    main()
