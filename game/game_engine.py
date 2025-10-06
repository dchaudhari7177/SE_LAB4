import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 48)
        self.small_font = pygame.font.SysFont("Arial", 20)
        
        # Game state management
        self.game_state = "playing"  # "playing", "game_over", "replay_menu"
        self.winning_score = 5
        self.winner = ""

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if self.game_state == "playing":
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)
        elif self.game_state == "replay_menu":
            if keys[pygame.K_3]:
                self.start_new_game(3)
            elif keys[pygame.K_5]:
                self.start_new_game(5)
            elif keys[pygame.K_7]:
                self.start_new_game(7)
            elif keys[pygame.K_ESCAPE]:
                pygame.quit()
                exit()

    def start_new_game(self, best_of):
        self.winning_score = (best_of + 1) // 2  # Best of 3 = first to 2, etc.
        self.player_score = 0
        self.ai_score = 0
        self.game_state = "playing"
        self.ball.reset()
        
    def check_game_over(self):
        if self.player_score >= self.winning_score:
            self.winner = "Player"
            self.game_state = "game_over"
        elif self.ai_score >= self.winning_score:
            self.winner = "AI"
            self.game_state = "game_over"

    def update(self):
        if self.game_state == "playing":
            self.ball.move()
            self.ball.check_collision(self.player, self.ai)

            if self.ball.x <= 0:
                self.ai_score += 1
                self.ball.reset()
                self.check_game_over()
            elif self.ball.x >= self.width:
                self.player_score += 1
                self.ball.reset()
                self.check_game_over()

            self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        if self.game_state == "playing":
            # Draw paddles and ball
            pygame.draw.rect(screen, WHITE, self.player.rect())
            pygame.draw.rect(screen, WHITE, self.ai.rect())
            pygame.draw.ellipse(screen, WHITE, self.ball.rect())
            pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

            # Draw score
            player_text = self.font.render(str(self.player_score), True, WHITE)
            ai_text = self.font.render(str(self.ai_score), True, WHITE)
            screen.blit(player_text, (self.width//4, 20))
            screen.blit(ai_text, (self.width * 3//4, 20))
            
        elif self.game_state == "game_over":
            # Display winner
            winner_text = self.big_font.render(f"{self.winner} Wins!", True, GREEN if self.winner == "Player" else RED)
            winner_rect = winner_text.get_rect(center=(self.width//2, self.height//2 - 50))
            screen.blit(winner_text, winner_rect)
            
            # Display final score
            score_text = self.font.render(f"Final Score: Player {self.player_score} - AI {self.ai_score}", True, WHITE)
            score_rect = score_text.get_rect(center=(self.width//2, self.height//2))
            screen.blit(score_text, score_rect)
            
            # Show replay options
            replay_text = self.small_font.render("Press 3 for Best of 3, 5 for Best of 5, 7 for Best of 7, ESC to Exit", True, WHITE)
            replay_rect = replay_text.get_rect(center=(self.width//2, self.height//2 + 50))
            screen.blit(replay_text, replay_rect)
            
            # Transition to replay menu after showing winner
            pygame.time.wait(100)  # Small delay to prevent immediate input
            self.game_state = "replay_menu"
            
        elif self.game_state == "replay_menu":
            # Display replay options
            title_text = self.big_font.render("Game Over", True, WHITE)
            title_rect = title_text.get_rect(center=(self.width//2, self.height//2 - 100))
            screen.blit(title_text, title_rect)
            
            option1 = self.font.render("Press 3 - Best of 3", True, WHITE)
            option2 = self.font.render("Press 5 - Best of 5", True, WHITE)
            option3 = self.font.render("Press 7 - Best of 7", True, WHITE)
            option4 = self.font.render("Press ESC - Exit Game", True, RED)
            
            screen.blit(option1, (self.width//2 - 100, self.height//2 - 40))
            screen.blit(option2, (self.width//2 - 100, self.height//2 - 10))
            screen.blit(option3, (self.width//2 - 100, self.height//2 + 20))
            screen.blit(option4, (self.width//2 - 100, self.height//2 + 50))
