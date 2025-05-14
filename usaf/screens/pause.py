import pygame
from usaf.save_manager import save_game
import os
import sys
from usaf.engine.inventory_manager import list_inventory

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

quantico_font_path = resource_path("assets/Quantico.ttf")

def run_pause(screen, slot=1, chapter=0):
    clock = pygame.time.Clock()
    width, height = screen.get_size()

    # Load and scale pause box image
    box_img = pygame.image.load(resource_path("assets/pause_box.png")).convert_alpha()

    # Scale to 90% of screen size
    box_width = int(width * 0.90)
    box_height = int(height * 0.90)
    box_img = pygame.transform.scale(box_img, (box_width, box_height))

    # Center horizontally, start bottom vertically
    box_x = (width - box_width) // 2
    box_y = height  # start off-screen
    target_y = (height - box_height) // 2


    font = pygame.font.Font(quantico_font_path, 36)
    options = ["Resume", "Save Game", "Quit"]
    selected = 0

    background_snapshot = screen.copy()

    running = True
    while running:
        #screen_copy = screen.copy()  # capture previous screen
        screen.blit(background_snapshot, (0, 0))  # keep background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_s:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "Resume":
                        return "game"
                    elif options[selected] == "Save Game":
                        from usaf.save_manager import load_game

                        existing = load_game(slot) or {}
                        save_game({
                            "player_name": existing.get("player_name", ""),
                            "backstory": existing.get("backstory", ""),
                            "chapter": chapter 
                        }, slot)

                    elif options[selected] == "Quit":
                        return "quit"

        # Slide the pause box up
        if box_y > target_y:
            box_y -= 60  # speed

        screen.blit(box_img, (box_x, box_y))

        # Draw options inside the box
        base_color = (104, 255, 113)
        highlight_color = (255, 255, 0)

        for i, opt in enumerate(options):
            color = highlight_color if i == selected else base_color
            txt = font.render(opt, True, color)    
            txt_rect = txt.get_rect(center=(width // 2, box_y + 150 + i * 60))
            screen.blit(txt, txt_rect)

        pygame.display.flip()
        clock.tick(60)

        inventory_lines = list_inventory()
        
        inv_font = pygame.font.Font(resource_path("assets/Quantico.ttf"), 20)

        # Position inventory list on the pause menu
        inv_x, inv_y = 50, 300
        screen.blit(inv_font.render("Inventory:", True, (255, 255, 255)), (inv_x, inv_y))
        for i, (item, qty) in enumerate(inventory_lines):
            item_text = f"- {item} ({qty})"
            screen.blit(inv_font.render(item_text, True, (255, 255, 255)), (inv_x, inv_y + 30 + i * 25))

    return "pause"

