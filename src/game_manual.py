import pygame
import sys
import random
from settings import *
from src.utils import load_image, draw_text, load_font
from src.entities import Bird, Pipe
from src.ui_components import Button, HighScorePopup

from src.score_manager import ScoreManager

class GameManual:
    def __init__(self, screen, score_manager):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = load_font(FONT_PATH, 40)
        self.small_font = load_font(FONT_PATH, 20)

        self.game_active = True
        self.score = 0
        
        self.bg_img = load_image(BG_IMAGE)
        self.bg_img = pygame.transform.scale(self.bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.ground_img = load_image(GROUND_IMAGE, scale=2.0)
        self.ground_scroll = 0
        
        self.game_over_img = load_image(GAME_OVER_IMAGE, scale=1.5)
        self.game_over_rect = self.game_over_img.get_rect(center=(SCREEN_WIDTH // 2,
                                                                  SCREEN_HEIGHT // 2 - 200))
        
        self.score_board = load_image(POPUP_SCORE, scale=1.5)
        self.score_board_rect = self.score_board.get_rect(center=(SCREEN_WIDTH // 2,
                                                                  SCREEN_HEIGHT // 2))
        
        self.medal_bronze = load_image(MEDAL_BRONZE, scale=1.5)
        self.medal_silver = load_image(MEDAL_SILVER, scale=1.5)
        self.medal_gold = load_image(MEDAL_GOLD, scale=1.5)
        self.medal_platinum = load_image(MEDAL_PLATINUM, scale=1.5)
        
        self.score_manager = score_manager
        self.score_saved = False
        self.best_score = 0
        
        self.highscore_popup = HighScorePopup(None, self.font)
        self.show_highscore = False
      
        restart_img = load_image(BTN_START, scale=1.0)
        highscore_img = load_image(BTN_TOP3, scale=1.0)

        button_spacing = 40 
        
        total_width = restart_img.get_width() + highscore_img.get_width() + button_spacing
        start_x = SCREEN_WIDTH // 2 - total_width // 2
        y = SCREEN_HEIGHT // 2 + 100

        self.btn_restart = Button(start_x, y, restart_img)
        self.btn_highscore = Button(start_x + restart_img.get_width() + button_spacing,
                                    y,
                                    highscore_img)
        
        self.btn_back = Button(10, 10, load_image(BTN_BACK, scale=0.6))
        
        self.bird_group = pygame.sprite.GroupSingle()
        self.bird = Bird(100, SCREEN_HEIGHT // 2)
        self.bird_group.add(self.bird)
        
        self.pipe_group = pygame.sprite.Group()
        self.pipe_frequency = PIPE_FREQUENCY
        self.last_pipe = pygame.time.get_ticks()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
            if not self.running:
                return "START"
        return None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if not self.show_highscore:
                if event.type == pygame.KEYDOWN and not self.game_active:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()

                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_active:
                     pass 
            
            if event.type == pygame.MOUSEBUTTONDOWN and self.show_highscore:
                 self.show_highscore = False

    def reset_game(self):
        self.game_active = True
        self.pipe_group.empty()
        self.bird.rect.center = (100, SCREEN_HEIGHT // 2)
        self.bird.vel = 0
        self.score = 0
        self.last_pipe = pygame.time.get_ticks()
        self.running = True
        self.score_saved = False

    def update(self):
        if self.game_active:
            self.ground_scroll -= SCROLL_SPEED
            if abs(self.ground_scroll) > 35:
                self.ground_scroll = 0
            
            current_time = pygame.time.get_ticks()
            if current_time - self.last_pipe > self.pipe_frequency:
                pipe_height = random.randint(-100, 100)
                btm_pipe = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT // 2 + pipe_height, -1)
                top_pipe = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT // 2 + pipe_height, 1)
                self.pipe_group.add(btm_pipe)
                self.pipe_group.add(top_pipe)
                self.last_pipe = current_time

            self.bird_group.update()
            self.pipe_group.update()

            if pygame.sprite.groupcollide(self.bird_group, self.pipe_group, False, False,
                                          pygame.sprite.collide_mask) or self.bird.rect.top < -100:
                self.game_active = False
            
            if self.bird.rect.bottom >= SCREEN_HEIGHT - 100:
                self.game_active = False
                self.bird.rect.bottom = SCREEN_HEIGHT - 100

            for pipe in self.pipe_group:
                if pipe.rect.centerx < self.bird.rect.centerx and not hasattr(pipe, 'scored'):
                    pipe.scored = True
                    self.score += 0.5
        
        else:
            if self.bird.rect.bottom < SCREEN_HEIGHT - 100:
                self.bird.update(flying=False)

    def draw(self):
        self.screen.blit(self.bg_img, (0, 0))
        
        self.pipe_group.draw(self.screen)
        self.screen.blit(self.ground_img, (self.ground_scroll, SCREEN_HEIGHT - 100))
        self.bird_group.draw(self.screen)
        
        if self.game_active:
            draw_text(self.screen, str(int(self.score)), self.font, WHITE, SCREEN_WIDTH // 2, 50)
        
        if self.btn_back.draw(self.screen):
            self.running = False
        
        if not self.game_active:

            if not self.score_saved:
                self.score_manager.save_score(int(self.score))
                self.best_score = self.score_manager.get_best_score()
                self.score_saved = True
            
            if self.show_highscore:
                self.highscore_popup.draw(self.screen, self.score_manager.get_top_scores())
            else:
                self.screen.blit(self.game_over_img, self.game_over_rect)
                
                self.screen.blit(self.score_board, self.score_board_rect)
                
                current_score = int(self.score)
                medal_img = None
                
                if current_score >= 40:
                    medal_img = self.medal_platinum
                elif current_score >= 30:
                    medal_img = self.medal_gold
                elif current_score >= 20:
                    medal_img = self.medal_silver
                elif current_score >= 10:
                    medal_img = self.medal_bronze
                
                if medal_img:
                    medal_rect = medal_img.get_rect()
                    medal_rect.center = (
                        self.score_board_rect.left + self.score_board_rect.width * 0.225, 
                        self.score_board_rect.centery + 17
                    )
                    self.screen.blit(medal_img, medal_rect)
                
                draw_text(self.screen, str(current_score), self.font, WHITE,
                        self.score_board_rect.right - 50,
                        self.score_board_rect.top + 80,
                        align="right")

                draw_text(self.screen, str(self.best_score), self.font, WHITE,
                        self.score_board_rect.right - 50,
                        self.score_board_rect.bottom  - 100,
                        align="right")
                if self.btn_restart.draw(self.screen):
                    self.reset_game()

                if self.btn_highscore.draw(self.screen):
                    self.show_highscore = True

        pygame.display.update()
