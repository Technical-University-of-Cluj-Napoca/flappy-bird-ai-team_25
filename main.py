import pygame
import sys
from settings import *
from src.start_screen import StartScreen
from src.tutorial_screen import TutorialScreen
from src.game_manual import GameManual
from src.game_auto import GameAuto
from src.score_manager import ScoreManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird AI")

    current_state = "START"
    mode_selected = None 
    
    clock = pygame.time.Clock()
    score_manager = ScoreManager()
    score_manager.clear_scores() 

    while True:
        if current_state == "START":
            start_screen = StartScreen(screen, score_manager)
            action = start_screen.run()
            if action:
                if action == "MANUAL":
                    mode_selected = "MANUAL"
                    current_state = "TUTORIAL"
                elif action == "AUTO":
                    mode_selected = "AUTO"
                    current_state = "TUTORIAL"
                else: 
                    pass
            else:
                break 

        elif current_state == "TUTORIAL":
            tutorial = TutorialScreen(screen, mode_selected)
            action = tutorial.run()
            if action:
                if action == "GAME_MANUAL":
                    current_state = "GAME_MANUAL"
                elif action == "GAME_AUTO":
                    current_state = "GAME_AUTO"
            else:
                break
        
        elif current_state == "GAME_MANUAL":
            game = GameManual(screen, score_manager)
            action = game.run() 
            if action == "START":
                current_state = "START"
            else:
                break

        elif current_state == "GAME_AUTO":
            game = GameAuto(screen, score_manager)
            action = game.run()
            if action == "START":
                current_state = "START"
            else:
                break

        else:
            print(f"State {current_state} not implemented yet.")
            break
            
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
