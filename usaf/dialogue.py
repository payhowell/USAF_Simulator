import pygame
import os
import textwrap
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


#Loads Resources
BLIP_SOUND = None
class DialogueBox:
    def __init__(self, bg_image_path, font_path, font_size, pos, wrap_width=60, width=None, name_font_size=None):
        raw_img = pygame.image.load(resource_path(bg_image_path)).convert_alpha()
        if width:
            original_width, original_height = raw_img.get_size()
            # Force exact dimensions
            new_width = width
            new_height = int(original_height * 1.3)  # fixed height for cockpit-style bar

            self.image = pygame.transform.scale(raw_img, (new_width, new_height))
        else:
            self.image = raw_img

        self.pos = pos
        self.font = pygame.font.Font(font_path, font_size)
        if name_font_size is None:
            name_font_size = font_size + 4  # default: slightly larger
        self.name_font = pygame.font.Font(font_path, name_font_size)
        
        #Debugging Lines

        print("[DEBUG] Dialogue font path:", font_path)
        print("[DEBUG] Dialogue font object:", self.font)
        print("[DEBUG] Name font object:", self.name_font)

        self.name = ""
        self.full_text = ""
        self.current_text = ""
        self.char_index = 0
        self.wrap_width = wrap_width
        self.finished = False
        self.char_timer = 0
        self.char_delay = 30
        self.last_update = pygame.time.get_ticks()
        global BLIP_SOUND
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        if BLIP_SOUND is None:
            BLIP_SOUND = pygame.mixer.Sound(os.path.join("assets", "blip.mp3"))
        self.blip = BLIP_SOUND

    def set_text(self, name, text):
        self.name = name
        self.full_text = text
        self.wrapped_lines = textwrap.wrap(text, self.wrap_width)
        self.current_text = ""
        self.char_index = 0
        self.finished = False
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if not self.finished and now - self.last_update > self.char_delay:
            if self.char_index < len(self.full_text):
                self.current_text = self.full_text[:self.char_index + 1]
                self.char_index += 1
                self.last_update = now
                self.blip.play()
            else:
                self.finished = True

    def skip(self):
        self.current_text = self.full_text
        self.char_index = len(self.full_text)
        self.finished = True

    def draw(self, screen):
        #The line below is for debugging
        #pygame.draw.rect(screen, (0, 255, 0), (*self.pos, self.image.get_width(), self.image.get_height()), 2)

        screen.blit(self.image, self.pos)

        text_color = (104, 255, 113)

        # === Name placement ===
        name_padding = (215, 32)  # (x, y) relative to box top-left — tweak as needed
        name_x = self.pos[0] + name_padding[0]
        name_y = self.pos[1] + name_padding[1]

        if self.name:

                name_surface = self.name_font.render(self.name, True, text_color)

                # 🧭 Define a sub-region: Left half of the dialogue box
                zone_left = self.pos[0]
                zone_width = self.image.get_width() // 2

                center_x = zone_left + zone_width // 2 - 190
                center_y = self.pos[1] + 50  # offset from top of dialogue box
                
                #Debug lines below
                #pygame.draw.line(screen, (255, 0, 0), (center_x, 0), (center_x, screen.get_height()))
                #pygame.draw.line(screen, (255, 0, 0), (0, center_y), (screen.get_width(), center_y))

                name_rect = name_surface.get_rect(center=(center_x, center_y))
                screen.blit(name_surface, name_rect)

        # === Dialogue placement ===
        text_padding = (150, 150)  # (x, y) relative to box top-left — lower inside the box
        text_x = self.pos[0] + text_padding[0]
        text_y = self.pos[1] + text_padding[1]

        for line in self.current_text.splitlines():
            line_surface = self.font.render(line, True, text_color)
            screen.blit(line_surface, (text_x, text_y))
            text_y += line_surface.get_height() + 6

