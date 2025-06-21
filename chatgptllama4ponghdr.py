import pygame
import sys
import random
import numpy as np

# Pygame Initialization
pygame.init()
pygame.mixer.init()

# Screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle properties
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5

# Ball properties
BALL_SIZE = 10
BALL_SPEED = 5

# Initialize font for scoring
font = pygame.font.Font(None, 72)
small_font = pygame.font.Font(None, 36)

def play_bounce_sound(frequency, duration):
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    note = np.sin(frequency * t * 2 * np.pi)
    audio = note * (32767 / max(np.abs(note)))
    audio = audio.astype(np.int16)
    pygame.mixer.Sound(buffer=audio.tobytes()).play()

class Paddle(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED

    def move_up(self):
        self.y -= self.speed
        if self.y < 0:
            self.y = 0

    def move_down(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height

class Ball(pygame.Rect):
    def __init__(self):
        super().__init__(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, BALL_SIZE, BALL_SIZE)
        self.x_speed = BALL_SPEED * random.choice([-1, 1])
        self.y_speed = BALL_SPEED * random.choice([-1, 1])

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

        if self.y < 0 or self.y > SCREEN_HEIGHT - self.height:
            self.y_speed *= -1
            play_bounce_sound(800, 0.1)

    def bounce(self):
        self.x_speed *= -1
        play_bounce_sound(1000, 0.1)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def play_score_sound(frequency):
    play_bounce_sound(frequency, 0.5)

def main():
    clock = pygame.time.Clock()

    paddle1 = Paddle(0, SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2)
    paddle2 = Paddle(SCREEN_WIDTH - PADDLE_WIDTH, SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2)

    ball = Ball()
    score1 = 0
    score2 = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_y:
                    game_over = False
                    score1 = 0
                    score2 = 0
                    ball.x = SCREEN_WIDTH / 2
                    ball.y = SCREEN_HEIGHT / 2
                    ball.x_speed = BALL_SPEED * random.choice([-1, 1])
                    ball.y_speed = BALL_SPEED * random.choice([-1, 1])
                elif event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()

        if not game_over:
            mouse_y = pygame.mouse.get_pos()[1]
            paddle1.y = mouse_y - PADDLE_HEIGHT / 2
            if paddle1.y < 0:
                paddle1.y = 0
            elif paddle1.y > SCREEN_HEIGHT - PADDLE_HEIGHT:
                paddle1.y = SCREEN_HEIGHT - PADDLE_HEIGHT

            # Simple AI for paddle2
            if paddle2.centery < ball.centery:
                paddle2.move_down()
            elif paddle2.centery > ball.centery:
                paddle2.move_up()

            ball.move()

            # Collision with paddles
            if ball.colliderect(paddle1) or ball.colliderect(paddle2):
                ball.bounce()

            # Ball out of bounds, scoring
            if ball.x < 0:
                score2 += 1
                play_score_sound(200)
                ball.x = SCREEN_WIDTH / 2
                ball.y = SCREEN_HEIGHT / 2
                ball.x_speed = BALL_SPEED
                ball.y_speed = BALL_SPEED * random.choice([-1, 1])
            elif ball.x > SCREEN_WIDTH - ball.width:
                score1 += 1
                play_score_sound(600)
                ball.x = SCREEN_WIDTH / 2
                ball.y = SCREEN_HEIGHT / 2
                ball.x_speed = -BALL_SPEED
                ball.y_speed = BALL_SPEED * random.choice([-1, 1])

            if score1 >= 5 or score2 >= 5:
                game_over = True

        screen.fill(BLACK)
        if not game_over:
            pygame.draw.rect(screen, WHITE, paddle1)
            pygame.draw.rect(screen, WHITE, paddle2)
            pygame.draw.ellipse(screen, WHITE, ball)
            pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))
            draw_text(str(score1), font, WHITE, screen, SCREEN_WIDTH / 2 - 50, 20)
            draw_text(str(score2), font, WHITE, screen, SCREEN_WIDTH / 2 + 30, 20)
        else:
            draw_text("Game Over!", font, "Game Over!".center(12), WHITE, screen, SCREEN_WIDTH / 2 - 120, SCREEN_HEIGHT / 2 - 36)
            if score1 >= 5:
                draw_text("You Win!", small_font, WHITE, screen, SCREEN_WIDTH / 2 - 60, SCREEN_HEIGHT / 2 + 20)
            else:
                draw_text("AI Wins!", small_font, WHITE, screen, SCREEN_WIDTH / 2 - 60, SCREEN_HEIGHT / 2 + 20)
            draw_text("Restart? (Y/N)", small_font, WHITE, screen, SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 2 + 60)

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
