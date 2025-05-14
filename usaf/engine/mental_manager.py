def degrade_mental_state(amount, reason=""):
    from usaf.engine.game_state import game_state
    game_state.mental_state = max(0, game_state.mental_state - amount)

    # Optional: track causes or log internally
    print(f"Mental state -{amount} ({reason}) → {game_state.mental_state}")
