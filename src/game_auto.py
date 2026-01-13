import pygame
import sys
import random
from settings import *
from src.utils import load_image, draw_text, load_font
from src.entities import Pipe, AutoBird 
from src.ui_components import Button
from src.ai.genetic import Population

from src.score_manager import ScoreManager

class GameAuto:
    def __init__(self, screen, score_manager):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.score_manager = score_manager
        self.font = load_font(FONT_PATH, 40)
        self.small_font = load_font(FONT_PATH, 25)
        
        self.generation = 1
        
        self.population_size = 50 
        self.population = Population(self.population_size)
        
        self.birds = [] 
        self.pipe_group = pygame.sprite.Group()
        self.pipe_frequency = PIPE_FREQUENCY
        self.last_pipe = pygame.time.get_ticks()
        
        self.bg_img = load_image(BG_IMAGE)
        self.bg_img = pygame.transform.scale(self.bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.ground_img = load_image(GROUND_IMAGE, scale=2.0)
        self.ground_scroll = 0
        
        self.session_best_score = 0
        
        self.reset_game() 
        self.btn_back = Button(10, 10, load_image(BTN_BACK, scale=0.6))

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
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0: 
                    self.running = False

    def reset_game(self):
        self.pipe_group.empty()
        self.birds = []
        self.bird_group = pygame.sprite.Group() 
        for brain in self.population.brains:
            bird = AutoBird(100, SCREEN_HEIGHT // 2, brain)
            self.birds.append(bird)
            self.bird_group.add(bird)
            
        self.last_pipe = pygame.time.get_ticks() - self.pipe_frequency 
        self.current_fitness_max = 0 
        self.pipe_score = 0

    def update(self):
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

        self.pipe_group.update()

        alive_birds = [b for b in self.birds if b.alive()]
        
        if not alive_birds:
            self.population.evolve()
            self.generation = self.population.generation
            self.reset_game()
            return
            
        pipes_list = self.pipe_group.sprites()
        
        for bird in alive_birds:
            bird.update(pipes_list)            
            collided = False
            for pipe in pipes_list:
                if pygame.sprite.collide_mask(bird, pipe):
                    collided = True
                    break
            
            if bird.rect.top < -100 or bird.rect.bottom >= SCREEN_HEIGHT - 100:
                collided = True
                
            if collided:
                bird.kill() 
                pass
            
            for pipe in pipes_list:
                 if pipe.rect.centerx < 100 and not hasattr(pipe, 'scored'):
                     pipe.scored = True
                     self.pipe_score += 0.5
                     if int(self.pipe_score) > self.session_best_score:
                         self.session_best_score = int(self.pipe_score)
        
        for bird in alive_birds:
            bird.brain.fitness += 1
            if bird.brain.fitness > self.current_fitness_max:
                self.current_fitness_max = bird.brain.fitness

    def draw(self):
        self.screen.blit(self.bg_img, (0, 0))
        
        self.pipe_group.draw(self.screen)
        
        self.screen.blit(self.ground_img, (self.ground_scroll, SCREEN_HEIGHT - 100))
        
        for bird in self.birds:
            if bird.alive():
                self.screen.blit(bird.image, bird.rect)

        draw_text(self.screen, f"Gen: {self.generation}", self.small_font, WHITE, 70, 20, align="left")
        draw_text(self.screen, f"Alive: {len([b for b in self.birds if b.alive()])}", self.small_font, WHITE, 70, 50, align="left")
        draw_text(self.screen, f"Fitness: {self.current_fitness_max}", self.small_font, WHITE, 70, 80, align="left")
        draw_text(self.screen, f"Score: {self.pipe_score}", self.small_font, WHITE, 70, 110, align="left")
        draw_text(self.screen, f"Session Best: {self.session_best_score}", self.small_font, WHITE, 70, 140, align="left")
        
        if self.btn_back.draw(self.screen):
            self.score_manager.save_score(self.session_best_score)
            self.running = False
        
        pygame.display.update()
