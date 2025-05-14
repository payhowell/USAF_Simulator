import pygame
from usaf.engine.game_state import game_state
from usaf.engine.inventory_manager import list_inventory
from usaf.screens.pause import resource_path  # For font loading
import time

log_entries = []

overlay_enabled = False

def log_event(message, duration=3):
    log_entries.append({
        "message": message,
        "time": time.time(),
        "duration": duration
    })

def toggle_overlay():
    global overlay_enabled
    overlay_enabled = not overlay_enabled

def draw_overlay(screen):
    if not overlay_enabled:
        return

    font = pygame.font.Font(resource_path("assets/Quantico.ttf"), 20)
    x, y = 20, 20
    line_height = 25

    def draw_line(text, color=(255, 255, 255)):
        nonlocal y
        screen.blit(font.render(text, True, color), (x, y))
        y += line_height

    draw_line("[DEV OVERLAY]", (255, 255, 0))
    draw_line(f"Mental State: {game_state.mental_state}", (255, 100, 100))
    draw_line(f"Morality Score: {game_state.morality_score}")
    draw_line(f"Rank: {game_state.rank}  |  XP: {game_state.xp}  |  Level: {game_state.level}")
    draw_line(f"Chapter: {game_state.chapter}  |  Slot: {game_state.slot}")
    draw_line(f"Name: {game_state.player_name}  |  Backstory: {game_state.backstory}")
    draw_line("")

    draw_line("Stats:")
    for key, val in game_state.stats.items():
        draw_line(f"  {key.capitalize()}: {val}")

    draw_line("")
    draw_line("Inventory:")
    for item, qty in list_inventory():
        draw_line(f"  - {item} ({qty})")
    now = time.time()
    log_y = 600
    for entry in log_entries[:]:
        age = now - entry["time"]
        if age > entry["duration"]:
            log_entries.remove(entry)
            continue

        alpha = max(0, 255 - int((age / entry["duration"]) * 255))
        color = (255, 255, 255, alpha)
        surf = font.render(entry["message"], True, (255, 255, 255))
        screen.blit(surf, (20, log_y))
        log_y += 25

