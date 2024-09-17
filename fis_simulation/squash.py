from re import X
import pygame
from pygame.locals import *
import math
from logging import DEBUG
from servizio import log_setup
import os
from characters import Bullet, AutoPlayer, GravitationalBullet, Player, Paddle, Ball
from costanti import (
    SCALE,
    WIDTH,
    HEIGHT,
    TIMESTEP,
    RED,
    BLUE,
    YELLOW,
    BLUEISH,
    REDISH,
    BLACK,
    WHITE,
)
from random import randint, choice, randrange
import numpy as np
import datetime as dt

# [x]] migliorare l'angolo di rimbalzo sulla racchetta - OK

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile=DEBUG, name=__name__)
logger.info("Inizio")

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tutorial")
FONT_SCORE = pygame.font.SysFont("comicsans", 40)
TEXT_AGAIN = pygame.font.SysFont("comicsans", 40).render(
    "Play Again? (y/n)", 1, WHITE)
total_score = 0
INTRO = 0
LEVEL_01 = 1
GAME_OVER = 99
status = INTRO
paddle_width, paddle_height = (20, 5)
timer = dt.datetime.now()
verify_hit = True
initial_angles = [-x * math.pi / 12 for x in range(1, 12)]

picture = pygame.image.load(os.path.join(
    "media", "Background_02.png")).convert()
pic_game_over = pygame.image.load(
    os.path.join("media", "gameover2.png")).convert()
picture = pygame.transform.scale(picture, (WIDTH, HEIGHT))
# try:
#     music = pygame.mixer.music.load(os.path.join("media", "Inner Peace.mid"))
#     pygame.mixer.music.play(-1)  # -1 will ensure the song keeps looping
#     hitSound = pygame.mixer.Sound(os.path.join("media", "squeak2.wav"))
# except:
#     pass


def update_scores(hit):
    global total_score
    total_score += hit
    text = FONT_SCORE.render(f"Score {total_score}", 1, WHITE)
    SCREEN.blit(text, (10, 10))


def check_collision(paddle, ball):
    global verify_hit
    if pygame.sprite.collide_rect(paddle, ball):
        verify_hit = False
        print(ball.rect.center, paddle.rect.center)
        diff_x = ball.rect.centerx - paddle.rect.centerx
        print("diff_x", diff_x)
        angle_rad = np.interp(
            diff_x, [-paddle_width, paddle_width], [-math.pi /
                                                    12 * 11, -math.pi / 12]
        )
        print("angle_rad", angle_rad)
        ball.x_vel = ball.velocity * math.cos(angle_rad)
        ball.y_vel = ball.velocity * math.sin(angle_rad)
        print("int(ball.x_vel/20)", int(ball.x_vel / 20))
        print("int(ball.y_vel/20)", int(ball.y_vel / 20))
        return 1
    return 0


def intro():
    global status
    status = LEVEL_01


def level_01():
    global status
    global timer
    global verify_hit
    global status
    global paddle_1
    global ball_1
    global all_sprites

    hit = 0
    if (dt.datetime.now() - timer).total_seconds() > 1:
        verify_hit = True
    if verify_hit:
        hit = check_collision(paddle_1, ball_1)
        timer = dt.datetime.now()
    update_scores(hit)
    if ball_1.rect.top > SCREEN.get_height():
        status = GAME_OVER
    all_sprites.update()
    all_sprites.draw(SCREEN)

    pygame.display.update()


def game_over():
    x = WIDTH / 2 - pic_game_over.get_width() / 2
    y = HEIGHT / 2 - pic_game_over.get_height() / 2
    SCREEN.blit(pic_game_over, (x, y))
    xx = WIDTH / 2 - TEXT_AGAIN.get_width() / 2
    yy = HEIGHT / 2 + pic_game_over.get_height()
    SCREEN.blit(TEXT_AGAIN, (xx, yy))
    pygame.display.update()


def manage_status():
    global status
    if status == INTRO:
        intro()
    if status == GAME_OVER:
        all_sprites.empty()
        game_over()
    if status != GAME_OVER and status != INTRO:
        level_01()


def main():
    global paddle_1
    global ball_1
    global all_sprites
    global status
    all_sprites = pygame.sprite.Group()
    paddle_1 = Paddle(paddle_width, paddle_height)
    ball_1 = Ball(paddle_1.rect.centerx, paddle_1.rect.top,
                  100, choice(initial_angles))
    all_sprites.add(paddle_1, ball_1)
    running = True
    clock = pygame.time.Clock()
    while running:
        SCREEN.blit(picture, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_y and status == GAME_OVER:
                    status = LEVEL_01
                    paddle_1 = Paddle(paddle_width, paddle_height)
                    ball_1 = Ball(
                        paddle_1.rect.centerx,
                        paddle_1.rect.top,
                        100,
                        choice(initial_angles),
                    )
                    all_sprites.add(paddle_1, ball_1)
                if event.key == K_n and status == GAME_OVER:
                    running = False
        manage_status()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if PROVA:
            logger.info(e, exc_info=True)
        else:
            logger.critical(e, exc_info=True)
