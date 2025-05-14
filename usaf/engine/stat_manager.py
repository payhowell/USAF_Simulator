def apply_backstory_stats(backstory_id):
    # Example stats per backstory
    presets = {
        "son_of_a_colonel": {
            "leadership": 3, "charisma": 2, "composure": 2,
            "intelligence": 1, "strength": 1, "tactical_sense": 2
        },
        "trailer_park_kid": {
            "strength": 3, "composure": 1, "charisma": 1,
            "tactical_sense": 2, "intelligence": 1, "leadership": 0
        },
    }

    from usaf.engine.game_state import game_state
    game_state.stats = presets.get(backstory_id, {})
