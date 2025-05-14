import pygame
import os
import sys

from usaf.save_manager import load_all_slots

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def run_menu(screen, font, music_path, menu_bg, selected, hover_sound, click_sound, pointer_frames):
    clock = pygame.time.Clock()

    # Track last hovered and selected item (to prevent sound spam)
    if not hasattr(run_menu, "last_selected"):
        run_menu.last_selected = -1
        run_menu.last_hovered = -1

    if not hasattr(run_menu, "frame_index"):
        run_menu.frame_index = 0
        run_menu.last_update_time = pygame.time.get_ticks()
    
    # Start playing music if not already playing
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)  # -1 = loop forever

    options = ["New Enlistment", "Reenlist", "Options", "Quit"]
    

    screen.blit(menu_bg, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    click = False
    has_save = any(slot is not None for slot in load_all_slots())

    #Render Title
    text = font.render("USAF SIMULATOR", True, (255, 255, 255))
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 100))

    hovered_index = None  # New: index being hovered by mouse
    click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit", selected

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                selected = (selected + 1) % len(options)
                if selected != run_menu.last_selected:
                    hover_sound.play()
                    run_menu.last_selected = selected
            elif event.key == pygame.K_w:
                selected = (selected - 1) % len(options)
                if selected != run_menu.last_selected:
                    hover_sound.play()
                    run_menu.last_selected = selected
            elif event.key == pygame.K_RETURN:
                click_sound.play()
                if options[selected] == "New Enlistment":
                    pygame.mixer.music.stop()
                    return "backstory", selected
                elif options[selected] == "Reenlist":
                    if has_save:
                        return "load", selected
                elif options[selected] == "Options":
                    pass  # You can add this screen later
                elif options[selected] == "Quit":
                    return "quit", selected

    # Render each option
    for i, option in enumerate(options):
        now = pygame.time.get_ticks()
        if now - run_menu.last_update_time > 100:  # 100 ms per frame
            run_menu.frame_index = (run_menu.frame_index + 1) % len(pointer_frames)
            run_menu.last_update_time = now

        y = 250 + i * 100

        # Determine final color
        if option == "Reenlist" and not has_save:
            color = (100, 100, 100)  # Grayed out if no save
        elif i == selected:
            color = (255, 255, 0)    # Highlight
        else:
            color = (255, 255, 255)  # Default

        # Render the text for this option
        text_surface = font.render(option, True, color)
        rect = text_surface.get_rect(center=(screen.get_width() // 2, y))

        # Detect if the mouse is hovering this option
        if rect.collidepoint(mouse_pos):
            if i != run_menu.last_hovered:
                hover_sound.play()
                run_menu.last_hovered = i

        # If not hovering anything, reset hover state


        # Draw the text
        screen.blit(text_surface, rect.topleft)

        # Draw animated pointer next to the selected option
        if i == selected:
            pointer_img = pointer_frames[run_menu.frame_index]
            pointer_rect = pointer_img.get_rect()
            pointer_rect.centery = rect.centery
            pointer_rect.right = rect.left - 20  # Adjust spacing if needed
            screen.blit(pointer_img, pointer_rect)

        # Handle click
        if click and hovered_index == i:
            if option == "Reenlist" and not has_save:
                continue  # Disabled; do nothing
            click_sound.play()
            pygame.mixer.music.stop()
            if option == "New Enlistment":
                return "backstory", selected
            elif option == "Reenlist":
                return "load", selected
            elif option == "Options":
                pass
            elif option == "Quit":
                return "quit", selected
    if hovered_index is None:
        run_menu.last_hovered = -1

    pygame.display.flip()
    click = False
    clock.tick(60)
    return "menu", selected
