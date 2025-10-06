import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        
        # Sound effects
        try:
            pygame.mixer.init()
            self.paddle_sound = pygame.mixer.Sound("sounds/paddle_hit.wav")
            self.wall_sound = pygame.mixer.Sound("sounds/wall_bounce.wav")
            self.score_sound = pygame.mixer.Sound("sounds/score.wav")
        except:
            # If sound files don't exist, create dummy sounds or None
            self.paddle_sound = None
            self.wall_sound = None
            self.score_sound = None

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Enhanced wall collision with sound
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            if self.wall_sound:
                self.wall_sound.play()

    def check_collision(self, player, ai):
        # Enhanced collision detection to prevent ball passing through paddles
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()
        
        # Check collision with more precise detection
        if ball_rect.colliderect(player_rect) and self.velocity_x < 0:
            self.velocity_x = abs(self.velocity_x)  # Ensure ball moves away from player
            if self.paddle_sound:
                self.paddle_sound.play()
        elif ball_rect.colliderect(ai_rect) and self.velocity_x > 0:
            self.velocity_x = -abs(self.velocity_x)  # Ensure ball moves away from AI
            if self.paddle_sound:
                self.paddle_sound.play()

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])
        if self.score_sound:
            self.score_sound.play()

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
