import pygame
import os
from ..save_manager import load_all_slots, load_game, delete_game

def run_reenlist_menu(screen, font, menu_bg, hover_sound, click_sound, pointer_frames):
    clock = pygame.time.Clock()
    selected = 0
    confirm_delete = False
    running = True

    pointer_index = 0
    last_update_time = pygame.time.get_ticks()

    while running:
        screen.blit(menu_bg, (0, 0))

        # Animate pointer
        now = pygame.time.get_ticks()
        if now - last_update_time > 100:
            pointer_index = (pointer_index + 1) % len(pointer_frames)
            last_update_time = now

        slots = load_all_slots()
        slot_texts = []

        for i, slot in enumerate(slots):
            if slot:
                label = f"Reenlistment Bonus {i+1}: {slot['player_name']} - {slot['backstory']}"
            else:
                label = f"Reenlistment Bonus {i+1}: EMPTY"
            slot_texts.append(label)

        for i, text in enumerate(slot_texts):
            y = 300 + i * 100
            color = (255, 255, 0) if i == selected else (104, 255, 113)
            text_surf = font.render(text, True, color)
            rect = text_surf.get_rect(center=(screen.get_width() // 2, y))
            screen.blit(text_surf, rect)

            if i == selected:
                pointer = pointer_frames[pointer_index]
                pointer_rect = pointer.get_rect()
                pointer_rect.centery = rect.centery
                pointer_rect.right = rect.left - 20
                screen.blit(pointer, pointer_rect)

        if confirm_delete:
            confirm_text = font.render("Delete this save? Press Enter to confirm, Backspace to cancel", True, (255, 100, 100))
            screen.blit(confirm_text, confirm_text.get_rect(center=(screen.get_width() // 2, 800)))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", None
            elif event.type == pygame.KEYDOWN:
                if confirm_delete:
                    if event.key == pygame.K_RETURN:
                        delete_game(selected + 1)
                        confirm_delete = False
                    elif event.key == pygame.K_BACKSPACE:
                        confirm_delete = False
                else:
                    if event.key == pygame.K_s:
                        selected = (selected + 1) % 3
                        hover_sound.play()
                    elif event.key == pygame.K_w:
                        selected = (selected - 1) % 3
                        hover_sound.play()
                    elif event.key == pygame.K_RETURN:
                        if slots[selected]:
                            click_sound.play()
                            return "game", load_game(selected + 1)
                    elif event.key == pygame.K_BACKSPACE:
                        return "menu", 0
                    elif event.key == pygame.K_ESCAPE:
                        if slots[selected]:
                            confirm_delete = True
        clock.tick(60)
