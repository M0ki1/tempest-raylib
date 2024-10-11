from enum import IntEnum, auto
from src.levels import Level
from src.shared import EventManager, SCREEN_CENTER, TempestColors
from src.entities import Blaster
from src.sounds import SoundManager
from pyray import *

class GameState(IntEnum):
    START_SCREEN = auto()
    LEVEL_SELECTION = auto()
    PLAYING = auto()

class Game:

    def __init__(self, sound_manager: SoundManager) -> None:
        self.sound_manager = sound_manager
        self.game_state = GameState.START_SCREEN
        self.event_manager = EventManager()
        self.current_level = 1

    def goto_level_selection(self):
        self.game_state = GameState.LEVEL_SELECTION
    
    def select_level(self, level_number: int):
        # Init level
        self.level = Level(self.event_manager, self.sound_manager)
        self.level.load_level_data(level_number)
        
        # Init Player
        self.blaster = Blaster(self.level.world, self.event_manager, self.sound_manager)

        self.game_state = GameState.PLAYING

    def update_frame(self):
        
        match self.game_state:
            case GameState.START_SCREEN:
                if is_key_pressed(KeyboardKey.KEY_ENTER):
                    self.goto_level_selection()
                #TODO: start screen animations

            case GameState.LEVEL_SELECTION:
                if is_key_pressed(KeyboardKey.KEY_RIGHT):
                    pass
                elif is_key_pressed(KeyboardKey.KEY_LEFT):
                    pass
                elif is_key_pressed(KeyboardKey.KEY_ENTER):
                    self.select_level(self.current_level)

            case GameState.PLAYING:
                self.blaster.update_frame()
                self.level.update_frame()
                if not self.blaster.alive:
                    self.game_state = GameState.LEVEL_SELECTION
                elif self.level.is_over():
                    # TODO: check level don't pass 16
                    self.current_level += 1
                    self.select_level(self.current_level)
    
    def draw_frame(self):
        match self.game_state:
            case GameState.START_SCREEN:
                title = "ATARI TEMPEST"
                draw_text(title, int(SCREEN_CENTER.x - measure_text(title, 40) / 2), int(SCREEN_CENTER.y - 40), 40, TempestColors.PURPLE_NEON.rgba())
            case GameState.LEVEL_SELECTION:
                title = "SELECT LEVEL"
                draw_text(title, int(SCREEN_CENTER.x - measure_text(title, 40) / 2), int(SCREEN_CENTER.y - 40), 40, TempestColors.TURQUOISE_NEON.rgba())
            case GameState.PLAYING:
                self.level.draw_frame()
                self.blaster.draw_frame()

