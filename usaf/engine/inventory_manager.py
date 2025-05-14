from usaf.engine.game_state import game_state

def add_item(name, qty=1):
    for item in game_state.inventory:
        if item["name"] == name:
            item["qty"] += qty
            return
    game_state.inventory.append({"name": name, "qty": qty})

def remove_item(name, qty=1):
    for item in game_state.inventory:
        if item["name"] == name:
            item["qty"] -= qty
            if item["qty"] <= 0:
                game_state.inventory.remove(item)
            return

def has_item(name):
    return any(i["name"] == name and i["qty"] > 0 for i in game_state.inventory)

def list_inventory():
    return [(item["name"], item["qty"]) for item in game_state.inventory]
