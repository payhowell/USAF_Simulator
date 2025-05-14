import pygame
import os
from ..dialogue import DialogueBox
from ..save_manager import load_game
from usaf.engine.inventory_manager import add_item, has_item, list_inventory
from usaf.engine.dev_overlay import toggle_overlay, draw_overlay

# Give the player an item
add_item("Canteen", 1)

# Check inventory
if has_item("Canteen"):
    print("You drank from your canteen.")

# Show current inventory
print("Inventory:", list_inventory())

def resource_path(relative_path):
    return os.path.join("assets", relative_path)

def run_chapter_1(screen, font, slot=1):
    game_data = load_game(slot)
    
    #Debugging Line Below
    if game_data:
        print("Backstory", game_data["backstory"])

    dialogue = [
        ("Narrator", "So I guess you finally decided to do something with your life."),
        ("Narrator", "Choose your backstory."),
        ("???", "Who are you?"),
        ("You", "I... don't know."),
    ]

    # Load images
    bg_img_raw = pygame.image.load(resource_path("recruiting_office.png")).convert()
    screen_width, screen_height = screen.get_size()
    bg_img= pygame.transform.scale(bg_img_raw, (screen_width, screen_height))
    quantico_font_path = resource_path("Quantico.ttf")

    # Create the dialogue box first, with temporary position
    screen_width, screen_height = screen.get_size()

    dialogue_box = DialogueBox(
        bg_image_path=resource_path("dialogue_box.png"),
        font_path=quantico_font_path,
        font_size=28,            # Body font
        name_font_size=36,       # 👈 Name font
        pos=(0, 0),  # temp
        wrap_width=60,
        width=screen_width - 50  # Use full width with left/right padding
    )

    # Place it above the bottom of the screen
    box_height = dialogue_box.image.get_height()
    dialogue_box.pos = (
        25,
        screen_height - box_height - 25
    )

    index = 0
    dialogue_box.set_text(*dialogue[index])

    clock = pygame.time.Clock()
    fade_alpha = 0
    fade_speed = 5
    fading = True
    running = True

    while running:
        screen.fill((0, 0, 0))

        # Fade-in background
        if fading:
            faded_bg = bg_img.copy()
            faded_bg.set_alpha(fade_alpha)
            screen.blit(faded_bg, (0, 0))
            fade_alpha += fade_speed
            if fade_alpha >= 255:
                fade_alpha = 255
                fading = False
        else:
            screen.blit(bg_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "pause"
            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
                toggle_overlay()

            if not fading:
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
                    if not dialogue_box.finished:
                        dialogue_box.skip()
                    else:
                        index += 1
                        if index < len(dialogue):
                            dialogue_box.set_text(*dialogue[index])
                        else:
                            return "chapter_2"


        if not fading:
            dialogue_box.update()
            dialogue_box.draw(screen)
        draw_overlay(screen)
        pygame.display.flip()
        clock.tick(60)
