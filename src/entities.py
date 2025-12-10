import pygame
import random
from settings import *
from src.utils import load_image

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [load_image(img, scale=1.5) for img in BIRD_IMAGES]
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel = 0
        self.clicked = False
        self.rotation = 0

    def update(self, flying=True):
        if flying:
            self.vel += GRAVITY
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < SCREEN_HEIGHT - 100:
                self.rect.y += int(self.vel)

        if not flying:
            if self.rect.bottom < SCREEN_HEIGHT - 100:
                self.rect.y += int(self.vel)
                self.vel += GRAVITY

        if pygame.mouse.get_pressed()[0] == 1 or pygame.key.get_pressed()[pygame.K_SPACE]:
            if not self.clicked and flying:
                self.clicked = True
                self.vel = JUMP_STRENGTH 
        else:
            self.clicked = False

        self.counter += 1
        flap_cooldown = 5

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        
        self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        new_rect = self.image.get_rect(center = self.rect.center)
        self.rect = new_rect
        self.mask = pygame.mask.from_surface(self.image)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(PIPE_TOP if position == 1 else PIPE_BOTTOM, scale=1.5)
        self.rect = self.image.get_rect()
        
        if position == 1:
            self.rect.bottomleft = (x, y - PIPE_GAP // 2) 
        if position == -1:
            self.rect.topleft = (x, y + PIPE_GAP // 2) 
            
        self.mask = pygame.mask.from_surface(self.image)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()

from src.ai.brain import Perceptron

class AutoBird(Bird):
    def __init__(self, x, y, brain=None):
        super().__init__(x, y)
        self.brain = brain if brain else Perceptron()
        self.score = 0
        self.fitness = 0

    def update(self, pipes, flying=True):
        if flying:
            self.vel += GRAVITY
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < SCREEN_HEIGHT - 100:
                self.rect.y += int(self.vel)
            nearest_pipe = None
            min_dist = 9999
            
            for pipe in pipes:
                if pipe.rect.right > self.rect.x:
                    dist = pipe.rect.left - self.rect.x
                    if dist < min_dist:
                        min_dist = dist
                        nearest_pipe = pipe
            
            if nearest_pipe:                
                pipe_pair = [p for p in pipes if p.rect.x == nearest_pipe.rect.x]
                
                top_pipe = None
                bottom_pipe = None
                
                if len(pipe_pair) >= 2:
                    p1 = pipe_pair[0]
                    p2 = pipe_pair[1]
                    if p1.rect.top < p2.rect.top:
                        top_pipe = p1
                        bottom_pipe = p2
                    else:
                        top_pipe = p2
                        bottom_pipe = p1
                
                if top_pipe and bottom_pipe:
                    d_top = self.rect.y - top_pipe.rect.bottom
                    
                    d_hor = top_pipe.rect.left - self.rect.x
                    
                    d_bot = bottom_pipe.rect.top - (self.rect.y + self.rect.height)
                    
                    inputs = [
                        d_top / SCREEN_HEIGHT, 
                        d_hor / SCREEN_WIDTH, 
                        d_bot / SCREEN_HEIGHT
                    ]
                    
                    prob = self.brain.predict(inputs)
                    
                    is_falling = self.vel > 0
                    if prob > 0.5 and is_falling:
                        self.jump()

        if not flying:
            if self.rect.bottom < SCREEN_HEIGHT - 100:
                self.rect.y += int(self.vel)
                self.vel += GRAVITY
        
        self.counter += 1
        flap_cooldown = 5

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        
        self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        new_rect = self.image.get_rect(center = self.rect.center)
        self.rect = new_rect
        self.mask = pygame.mask.from_surface(self.image)

    def jump(self):
        self.vel = JUMP_STRENGTH

