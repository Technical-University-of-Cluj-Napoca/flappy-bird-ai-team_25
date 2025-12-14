import pygame
import sys
from settings import *
from src.utils import load_image, draw_text

class TutorialScreen:
    def __init__(self, screen, mode):
        self.screen = screen
        self.mode = mode
        self.clock = pygame.time.Clock()
        self.running = True
        self.next_state = None
        self.bg_img = load_image(BG_IMAGE)
        self.bg_img = pygame.transform.scale(self.bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.ground_img = load_image(GROUND_IMAGE, scale=2.0)
        self.ground_scroll = 0
        self.get_ready_img = load_image(GET_READY_IMAGE, scale=1.5)
        self.get_ready_rect = self.get_ready_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5))

        if self.mode == "MANUAL":
            self.tut_img = load_image(TUTORIAL_TAP, scale=1.5)
            self.instruction_text = "Tap or Press Space to Jump"
        else: 
            raw_img = load_image(TUTORIAL_AUTO, scale=1.0)
            target_width = 300
            scale = target_width / raw_img.get_width()
            new_size = (int(raw_img.get_width() * scale), int(raw_img.get_height() * scale))
            self.tut_img = pygame.transform.scale(raw_img, new_size)
            self.instruction_text = "Tap or Press Space to see the AI magic xD" 
        
        self.tut_rect = self.tut_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self.bird_img = load_image(BIRD_IMAGES[1], scale=1.5)
        self.bird_rect = self.bird_img.get_rect(center=(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))

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
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_state = "GAME_" + self.mode
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.next_state = "GAME_" + self.mode

    def update(self):
        self.ground_scroll -= SCROLL_SPEED
        if abs(self.ground_scroll) > 35:
            self.ground_scroll = 0
            
    def draw(self):
        self.screen.blit(self.bg_img, (0, 0))
        self.screen.blit(self.bird_img, self.bird_rect)
        self.screen.blit(self.ground_img, (self.ground_scroll, SCREEN_HEIGHT - 100))
        self.screen.blit(self.get_ready_img, self.get_ready_rect)
        self.screen.blit(self.tut_img, self.tut_rect)
        from src.utils import load_font 
        font = load_font(FONT_PATH, 30)
        
        if self.mode == "MANUAL":
            draw_text(self.screen, "Fly, Fabby, Fly!", font, WHITE, SCREEN_WIDTH // 2, self.tut_rect.bottom + 50)
        else:
            draw_text(self.screen, "Tap or Press Space to see the AI magic xD...", font, WHITE, SCREEN_WIDTH // 2, self.tut_rect.bottom + 50)

        pygame.display.update()
