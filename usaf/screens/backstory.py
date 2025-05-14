import pygame
import os
import sys
from ..dialogue import DialogueBox
from ..save_manager import save_game, load_all_slots


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_name_input(screen, font, prompt_text="Enter your name:"):
    name = ""
    entering = True
    while entering:
        screen.fill((0, 0, 0))
        prompt = font.render(prompt_text, True, (255, 255, 255))
        name_display = font.render(name + "|", True, (104, 255, 113))

        prompt_rect = prompt.get_rect(center=(screen.get_width() // 2, 200))
        name_rect = name_display.get_rect(center=(screen.get_width() // 2, 300))

        screen.blit(prompt, prompt_rect)
        screen.blit(name_display, name_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    entering = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 20:
                        name += event.unicode

        pygame.display.flip()
        pygame.time.Clock().tick(30)
    return name.strip()


backstories = [
    {
        "title": "Military Family",
        "description": "Raised on base, disciplined and precise. Knows chain of command."
    },
    {
        "title": "College Dropout",
        "description": "Grew up rural. Tough, resourceful, instinct-driven."
    },
    {
        "title": "Straight Outta Highschool",
        "description": "Ex-PMC pilot with a dark past and elite training."
    }
]

def run_backstory(screen, font, hover_sound=None, click_sound=None):
    dialogue = [
        ("Narrator", "Every path to the cockpit starts somewhere..."),
        ("Narrator", "Before your training begins, tell us your story."),
    ]

    bg_img_raw = pygame.image.load(resource_path("assets/recruiting_office.png")).convert()
    bg_img = pygame.transform.scale(bg_img_raw, screen.get_size())

    dialogue_box = DialogueBox(
        bg_image_path=resource_path("assets/dialogue_box.png"),
        font_path=resource_path("assets/Quantico.ttf"),
        font_size=28,
        name_font_size=36,
        pos=(0, 0),
        wrap_width=60,
        width=screen.get_width() - 50
    )

    dialogue_box.pos = (
        25,
        screen.get_height() - dialogue_box.image.get_height() - 25
    )

    index = 0
    dialogue_box.set_text(*dialogue[index])

    selected = 0
    click = False
    clock = pygame.time.Clock()
    showing_choices = False

    running = True
    player_name = ""
    while running:
        screen.blit(bg_img, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", None
            elif event.type == pygame.KEYDOWN:
                if not showing_choices:
                    if not dialogue_box.finished:
                        dialogue_box.skip()
                    else:
                        index += 1
                        if index < len(dialogue):
                            dialogue_box.set_text(*dialogue[index])
                        else:
                            # Prompt for name
                            player_name = get_name_input(screen, font)
                            if not player_name:
                                return "quit", None
                            showing_choices = True
                else:
                    if event.key == pygame.K_s:
                        selected = (selected + 1) % len(backstories)
                        if hover_sound:
                            hover_sound.play()
                    elif event.key == pygame.K_w:
                        selected = (selected - 1) % len(backstories)
                        if hover_sound:
                            hover_sound.play()
                    elif event.key == pygame.K_RETURN:
                        if click_sound:
                            click_sound.play()

                        # Save into first available slot
                        #slots = load_all_slots()
                        #slot_index = next((i for i, s in enumerate(slots) if s is None), 0)

                        #save_game({
                            #"player_name": player_name,
                            #"backstory": backstories[selected]["title"],
                            #"chapter": 0
                        #}, slot_index + 1)

                        return "game", {
                            "backstory": backstories[selected],
                            "player_name": player_name
                        }
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        if not showing_choices:
            dialogue_box.update()
            dialogue_box.draw(screen)
        else:
            for i, b in enumerate(backstories):
                y = 200 + i * 140
                title_color = (255, 255, 0) if i == selected else (200, 200, 200)
                desc_color = (180, 255, 180) if i == selected else (120, 120, 120)

                title_surface = font.render(b["title"], True, title_color)
                desc_surface = font.render(b["description"], True, desc_color)

                title_rect = title_surface.get_rect(center=(screen.get_width() // 2, y))
                desc_rect = desc_surface.get_rect(center=(screen.get_width() // 2, y + 30))

                if title_rect.collidepoint(mouse_pos):
                    if selected != i and hover_sound:
                        hover_sound.play()
                    selected = i
                    if click and click_sound:
                        click_sound.play()
                        return "game", backstories[i]

                screen.blit(title_surface, title_rect)
                screen.blit(desc_surface, desc_rect)

        pygame.display.flip()
        clock.tick(60)
