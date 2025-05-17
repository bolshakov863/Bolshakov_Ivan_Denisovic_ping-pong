

import sys
from all_colors import *
import pygame
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Пинг_понг")

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 10

BALL_SIZE = 10
BALL_SPEED_X = 10
BALL_SPEED_Y = 10

paddle1_rect = pygame.Rect(0, SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

paddle2_rect = pygame.Rect(SCREEN_WIDTH - PADDLE_WIDTH, SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

ball_rect = pygame.Rect(SCREEN_WIDTH//2 - BALL_SIZE//2, SCREEN_HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

score1 = 0
score2 = 0

font = pygame.font.SysFont(None, 32)

FPS = 60
clock = pygame.time.Clock()
running = True

ai_mode = True
if len(sys.argv) > 1:
    if sys.argv[1] == '--human':
        ai_mode = False

def update_ai():
    if ball_rect.x > SCREEN_WIDTH//2:
        if ball_rect.centery < paddle2_rect.centery:
            paddle2_rect.y -= PADDLE_SPEED
        elif ball_rect.centery >paddle2_rect.centery:
            paddle2_rect.y += PADDLE_SPEED

        if paddle2_rect.top < 0:
            paddle2_rect.top = 0
        if paddle2_rect.bottom > SCREEN_WIDTH:
            paddle2_rect.bottom = SCREEN_HEIGHT
    else:
        paddle2_rect.centery += (SCREEN_HEIGHT//2 - paddle2_rect.centery)/ PADDLE_SPEED

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if  keys[pygame.K_w]:
        paddle1_rect.y -= PADDLE_SPEED
        if paddle1_rect.top <= 0:
            paddle1_rect.top = 0

    if  keys[pygame.K_s]:
        paddle1_rect.y += PADDLE_SPEED
        if paddle1_rect.bottom >= SCREEN_HEIGHT:
            paddle1_rect.bottom = SCREEN_HEIGHT

    if not ai_mode and keys[pygame.K_UP]:
        paddle2_rect.y -= PADDLE_SPEED
        if paddle2_rect.top <= 0:
            paddle2_rect.top = 0

    if not ai_mode and keys[pygame.K_DOWN]:
        paddle2_rect.y += PADDLE_SPEED
        if paddle2_rect.bottom >= SCREEN_HEIGHT:
            paddle2_rect.bottom = SCREEN_HEIGHT

    if ai_mode:
        update_ai()

    ball_rect.x += BALL_SPEED_X
    ball_rect.y += BALL_SPEED_Y

    if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
        BALL_SPEED_Y *= -1


 # Если поверхность мяча столкнулась с поверхностью первой акетки илиповерхность мяча столкнулась с повехность втор ракетки скорость мяча умнож на -1
    if paddle1_rect.colliderect(ball_rect) or paddle2_rect.colliderect(ball_rect):
        if BALL_SPEED_X > 0:
            BALL_SPEED_X += 1
        if BALL_SPEED_X < 0:
            BALL_SPEED_X -= 1
        BALL_SPEED_X *= -1


    if ball_rect.left <= 0:
        score2 += 1
        ball_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

    if ball_rect.right >= SCREEN_WIDTH:
        score1 += 1
        ball_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

    if paddle1_rect.colliderect(ball_rect) or paddle2_rect.colliderect(ball_rect):
        if BALL_SIZE > 9:
            BALL_SIZE += 1
        if BALL_SIZE < 9:
            BALL_SIZE -= 1
        BALL_SIZE*= -1

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle1_rect)
    pygame.draw.rect(screen, WHITE, paddle2_rect)
    pygame.draw.ellipse(screen, WHITE, ball_rect)
    pygame.draw.line(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

    score_text1 = font.render(f'{score1} : {score2}', True, WHITE)
    screen.blit(score_text1, (SCREEN_WIDTH // 2 - score_text1.get_width() // 2, 10))
    score_text2 = font.render(f'Скорость:{BALL_SPEED_X}', True, WHITE)
    screen.blit(score_text2, (SCREEN_WIDTH // 1.5 - score_text2.get_width() // 2, 10))


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()