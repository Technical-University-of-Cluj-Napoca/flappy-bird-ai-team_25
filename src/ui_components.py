import pygame
from settings import *
from src.utils import draw_text

class Button:
    def __init__(self, x, y, image, scale=1.0):
        if scale != 1.0:
            width = int(image.get_width() * scale)
            height = int(image.get_height() * scale)
            self.image = pygame.transform.scale(image, (width, height))
        else:
            self.image = image
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action

class HighScorePopup:
    def __init__(self, bg_image, font):
        self.image = bg_image
        if self.image:
            self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        else:
            self.rect = pygame.Rect(0, 0, 300, 400)
            self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.font = font
        self.close_btn = None 

    
    def draw(self, surface, scores):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        surface.blit(overlay, (0, 0))

        if self.image:
             surface.blit(self.image, self.rect)
        else:
             pygame.draw.rect(surface, (222, 216, 149), self.rect, border_radius=10)
             pygame.draw.rect(surface, (84, 56, 71), self.rect, 4, border_radius=10)

        draw_text(surface, "High Scores", self.font, (255, 128, 0), self.rect.centerx, self.rect.top + 30)

        y_offset = 80
        for i, score in enumerate(scores):
            if i >= 3: break
            draw_text(surface, f"{i+1}. {score}", self.font, WHITE, self.rect.centerx, self.rect.top + y_offset)
            y_offset += 40
        
        draw_text(surface, "Click to Close", self.font, (200, 200, 200), self.rect.centerx, self.rect.bottom - 20)

