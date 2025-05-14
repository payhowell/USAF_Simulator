import pygame
from usaf.chapters import chapter_1, chapter_2

chapters = [
    chapter_1.run_chapter_1,
    chapter_2.run_chapter_2,
]

def run_game(screen, game_bg, chapter_index=0, slot=1):
    font = pygame.font.Font(None, 48)

    if chapter_index >= len(chapters):
        print(f"No such chapter: {chapter_index}")
        return "menu", chapter_index

    # Run the correct chapter
    result = chapters[chapter_index](screen, font, slot)

    # If the result is a chapter transition like "chapter_2", increment
    if result.startswith("chapter_"):
        return "game", chapter_index + 1

    return result, chapter_index
