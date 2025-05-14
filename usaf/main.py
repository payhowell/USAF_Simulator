import pygame
import sys
import os

from usaf.screens.menu import run_menu
from usaf.screens.game import run_game
from usaf.screens.pause import run_pause
from usaf.screens.backstory import run_backstory
from usaf.save_manager import save_game, load_game, load_all_slots
from usaf.dialogue import DialogueBox
from usaf.screens.reenlist import run_reenlist_menu
from usaf.engine.game_state import game_state
from usaf.engine.stat_manager import apply_backstory_stats

# Support both script and PyInstaller .exe runs
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # Temporary directory used by PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

#Initializing Pygame
pygame.init()
pygame.mixer.init()

#Screen Characteristics
width, height = 1920, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Pygame")

#Load Resources
game_bg_raw = pygame.image.load(resource_path("assets/chapter_1_background.jpg"))
game_bg = pygame.transform.scale(game_bg_raw, (width, height))

menu_bg_raw = pygame.image.load(resource_path("assets/menu_background.jpg"))
menu_bg = pygame.transform.scale(menu_bg_raw, (width, height))

menu_font_path = resource_path("assets/SairaStencilOne-Regular.ttf")
menu_font = pygame.font.Font(menu_font_path, 72)
music_path = resource_path("assets/menu_music.mp3")

hover_sound = pygame.mixer.Sound(resource_path("assets/highlight_beep.mp3"))
click_sound = pygame.mixer.Sound(resource_path("assets/select_beep.mp3"))

pointer_frames = []
for i in range(8):  # Replace with actual number
    path = resource_path(f"assets/pointer_{i}.gif")
    pointer_frames.append(pygame.image.load(path).convert_alpha())

#Screen Definitions
MENU = "menu"
GAME = "game"
PAUSE = "pause"

current_screen = MENU
current_chapter = 0


#Main Loop 
running = True
selected = 0
while running:
    
    if current_screen == "menu":
        current_screen, selected = run_menu(screen, menu_font, music_path, menu_bg, selected, hover_sound, click_sound, pointer_frames)
    
    elif current_screen == "backstory":
        current_screen, selected_data = run_backstory(screen, menu_font)
        if selected_data:
            slots = load_all_slots()
            slot_index = next((i for i, s in enumerate(slots) if s is None), 0)

            save_game({
                "player_name": selected_data["player_name"],
                "backstory": selected_data["backstory"]["title"],
                "chapter": 0
            }, slot_index + 1)
            
            apply_backstory_stats(selected_data["backstory"]["title"])

            current_slot = slot_index + 1

    elif current_screen == "load":
        current_screen, loaded_data = run_reenlist_menu(screen, menu_font, menu_bg, hover_sound, click_sound, pointer_frames)
        if current_screen == "game" and loaded_data:
            pygame.mixer.music.stop()
            current_slot = loaded_data.get("slot", 1)
            current_chapter = loaded_data.get("chapter", 0)

            game_state.slot = current_slot
            game_state.chapter = current_chapter
            game_state.player_name = loaded_data.get("player_name", "")
            game_state.backstory = loaded_data.get("backstory", "")
            game_state.stats = loaded_data.get("stats", {})
            game_state.rank = loaded_data.get("rank", "Airman")
            game_state.level = loaded_data.get("level", 1)
            game_state.xp = loaded_data.get("xp", 0)
            game_state.inventory = loaded_data.get("inventory", [])
            game_state.mental_state = loaded_data.get("mental_state", 100)
            game_state.morality_score = loaded_data.get("morality_score", 0)
            game_state.flags = loaded_data.get("flags", {})

    elif current_screen == "game":
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                current_screen = "pause"
                break
            else:
                current_screen, current_chapter = run_game(screen, game_bg, current_chapter, current_slot)
    
    elif current_screen == "pause":
        current_screen = run_pause(screen, current_slot, current_chapter)
    
    elif current_screen == "quit":
        running = False

pygame.QUIT()