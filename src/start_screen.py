import pygame
import sys
from settings import *
from src.utils import load_image, load_font, draw_text
from src.ui_components import Button, HighScorePopup

from src.score_manager import ScoreManager

class StartScreen:
    def __init__(self, screen, score_manager):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = load_font(FONT_PATH, 40)
        self.small_font = load_font(FONT_PATH, 25)
        self.running = True
        self.next_state = None
        self.score_manager = score_manager
        self.bg_img = load_image(BG_IMAGE)
        self.bg_img = pygame.transform.scale(self.bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))      
        self.ground_img = load_image(GROUND_IMAGE, scale=2.0)
        self.ground_scroll = 0
        self.title_img = load_image(TITLE_IMAGE, scale=1.5)
        self.title_rect = self.title_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

        self.bird_imgs = [load_image(img, scale=1.5) for img in BIRD_IMAGES]
        self.bird_index = 0
        self.bird_timer = 0
        self.bird_rect = self.bird_imgs[0].get_rect(center=(SCREEN_WIDTH // 2, self.title_rect.bottom + 50))
        
        center_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 2
        
        self.btn_manual = Button(center_x - 100, start_y, load_image(BTN_MANUAL), scale=1.5)
        self.btn_auto = Button(center_x - 100, start_y + 80, load_image(BTN_AUTO), scale=1.5)
        self.btn_highscore = Button(center_x - 100, start_y + 160, load_image(BTN_HIGHSCORE), scale=1.5)
        
        self.highscore_popup = HighScorePopup(None, self.font)
        self.show_popup = False

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
            if self.next_state:
                return self.next_state
        return None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and self.show_popup:
                self.show_popup = False

    def update(self):
        self.ground_scroll -= SCROLL_SPEED
        if abs(self.ground_scroll) > 35:
            self.ground_scroll = 0


        self.bird_timer += 1
        if self.bird_timer > 5:
            self.bird_index = (self.bird_index + 1) % len(self.bird_imgs)
            self.bird_timer = 0
            offset = 5 if self.bird_index == 1 else 0
            self.bird_rect.centery = self.title_rect.bottom + 50 + offset

    def draw(self):
        # Draw Background
        self.screen.blit(self.bg_img, (0, 0))
        
        # Draw Title
        self.screen.blit(self.title_img, self.title_rect)
        
        # Draw Bird
        self.screen.blit(self.bird_imgs[self.bird_index], self.bird_rect)

        # Draw Ground
        self.screen.blit(self.ground_img, (self.ground_scroll, SCREEN_HEIGHT - 100))
        
        # Draw Copyright
        draw_text(self.screen, COPYRIGHT_TEXT, self.small_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)

        # Draw UI
        if not self.show_popup:
            # Button logic here to capture clicks
            # Centering buttons correction
            # Re-center buttons dynamically if needed, but rects set in __init__
            # My logic in __init__ for x might be off (topleft), let's fix render if needed.
            # Assuming Button takes topleft.
            # Let's adjust Button x in __init__?
            # self.btn_manual.rect.centerx = SCREEN_WIDTH // 2 (Cannot set centerx directly easily unless we access rect)
            # Accessing rect directly:
            self.btn_manual.rect.centerx = SCREEN_WIDTH // 2
            self.btn_auto.rect.centerx = SCREEN_WIDTH // 2
            self.btn_highscore.rect.centerx = SCREEN_WIDTH // 2
            
            if self.btn_manual.draw(self.screen):
                print("Manual Mode Selected")
                self.next_state = "MANUAL"
            
            if self.btn_auto.draw(self.screen):
                print("Auto Mode Selected")
                self.next_state = "AUTO"
            
            if self.btn_highscore.draw(self.screen):
                self.show_popup = True

        else:
            # Draw Popup
            self.highscore_popup.draw(self.screen, self.score_manager.get_top_scores())
        
        pygame.display.update()
