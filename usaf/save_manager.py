import json
import os
from datetime import datetime

SAVE_DIR = "saves"
MAX_SLOTS = 3

# Ensure save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

def get_slot_path(slot):
    return os.path.join(SAVE_DIR, f"slot{slot}.json")

def save_game(data, slot):
    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(get_slot_path(slot), "w") as f:
        json.dump(data, f, indent=4)

def save_current_game(slot):
    from usaf.engine.game_state import game_state
    data = {
        "player_name": game_state.player_name,
        "backstory": game_state.backstory,
        "stats": game_state.stats,
        "rank": game_state.rank,
        "level": game_state.level,
        "xp": game_state.xp,
        "inventory": game_state.inventory,
        "mental_state": game_state.mental_state,
        "morality_score": game_state.morality_score,
        "chapter": game_state.chapter,
        "flags": game_state.flags
    }

    save_game(data, game_state.slot)

def load_game(slot):
    path = get_slot_path(slot)
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)

def load_all_slots():
    return [
        load_game(i + 1) for i in range(MAX_SLOTS)
    ]

def delete_game(slot):
    path = get_slot_path(slot)
    if os.path.exists(path):
        os.remove(path)

