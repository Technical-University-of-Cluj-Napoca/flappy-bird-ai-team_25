import pygame
import os
from settings import *

def load_image(path, scale=1.0):
    try:
        img = pygame.image.load(path).convert_alpha()
        if scale != 1.0:
            width = int(img.get_width() * scale)
            height = int(img.get_height() * scale)
            img = pygame.transform.scale(img, (width, height))
        return img
    except Exception as e:
        print(f"Error loading image at {path}: {e}")
        surf = pygame.Surface((50, 50))
        surf.fill((255, 0, 255))
        return surf

def load_font(path, size):
    try:
        return pygame.font.Font(path, size)
    except Exception as e:
        print(f"Error loading font at {path}: {e}")
        return pygame.font.SysFont("arial", size)

def draw_text(surface, text, font, color, x, y, align="center"):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "center":
        text_rect.center = (x, y)
    elif align == "left":
        text_rect.topleft = (x, y)
    elif align == "right":
        text_rect.topright = (x, y)
    elif align == "midtop":
        text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)
    return text_rect
