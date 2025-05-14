import pygame

def run_chapter_2(screen, font, slot=1):
    dialogue = [
        ("Narrator", "Chapter Two begins with a question."),
        ("You", "Where am I now...?"),
        ("Voice", "You've passed the first trial."),
        ("You", "What trial?"),
    ]

    index = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill((0, 0, 0))  # Add background later

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                index += 1
                if index >= len(dialogue):
                    return "menu"  # Placeholder return (or "chapter_3")

        if index < len(dialogue):
            name, line = dialogue[index]
            name_surface = font.render(name, True, (255, 255, 0))
            line_surface = font.render(line, True, (255, 255, 255))

            screen.blit(name_surface, (50, 600))
            screen.blit(line_surface, (50, 650))

        pygame.display.flip()
        clock.tick(60)

    return "chapter_2"
