from re import X
import pygame
from pygame.locals import *
import math
from logging import DEBUG
from servizio import log_setup
import os
from characters import Bullet, AutoPlayer, GravitationalBullet, Player
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
from random import randint
from random import choice

# TODO Mettere un'immagine come player e farlo muovere con i tasti
# TODO I proiettili farli comparire da soli quando escono fuori dallo schermo


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


FONT_HIT = pygame.font.SysFont("comicsans", 16)

FONT_SCORE = pygame.font.SysFont("comicsans", 40)
total_score = 0


def update_scores(hit):
    global total_score
    total_score += hit
    text = FONT_SCORE.render(f"Score {total_score}", 1, WHITE)
    SCREEN.blit(text, (WIDTH - text.get_width() - 10, 10))


def check_collision(player, all_bullets):
    # if pygame.sprite.spritecollide(player, all_bullets_h, False) or pygame.sprite.spritecollide(player, all_bullets_v, False):
    #     return 1
    # else:
    #     return 0
    for sprite in all_bullets:
        if sprite != player:
            if player.rect.colliderect(sprite.rect):
                text = FONT_HIT.render("Hit", 1, WHITE)
                SCREEN.blit(text, (sprite.rect.right, sprite.rect.top))
                sprite.kill()
                return 1
    return 0


def main():
    running = True
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    all_bullets_h = pygame.sprite.Group()
    all_bullets_v = pygame.sprite.Group()
    all_bullets = pygame.sprite.Group()

    gbullet = GravitationalBullet(20, HEIGHT - 20, 5, YELLOW, 30, -100)
    all_sprites.add(gbullet)
    all_bullets.add(gbullet)

    bullet_h1 = Bullet(
        x=0 * SCALE + WIDTH / 2,
        y=30 * SCALE + HEIGHT / 2,
        radius=5,
        color=REDISH,
        velocity=1,
        angle=0,
    )
    bullet_h2 = Bullet(
        x=0 * SCALE + WIDTH / 2,
        y=-20 * SCALE + HEIGHT / 2,
        radius=5,
        color=BLUEISH,
        velocity=-1,
        angle=0,
    )
    all_sprites.add(bullet_h1)
    all_sprites.add(bullet_h2)
    all_bullets_h.add(bullet_h1)
    all_bullets_h.add(bullet_h2)
    all_bullets.add(bullet_h1)
    all_bullets.add(bullet_h2)

    player = Player()
    all_sprites.add(player)

    while running:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if len(all_bullets_h) <= 5:
                        bullet_h = Bullet(
                            x=randint(10, WIDTH - 10),
                            y=randint(10, HEIGHT - 10),
                            radius=5,
                            color=choice([RED, BLUE, YELLOW, BLUEISH, REDISH]),
                            velocity=choice([-1, 1]),
                            angle=0,
                        )
                        all_bullets_h.add(bullet_h)
                        all_bullets.add(bullet_h)
                        all_sprites.add(bullet_h)
                if event.key == K_RETURN:
                    if len(all_bullets_v) <= 5:
                        bullet_v = Bullet(
                            x=randint(10, WIDTH - 10),
                            y=0,
                            radius=10,
                            color=choice([RED, BLUE, YELLOW, BLUEISH, REDISH]),
                            velocity=1,
                            angle=math.pi / 2,
                        )
                        all_bullets_v.add(bullet_v)
                        all_bullets.add(bullet_v)
                        all_sprites.add(bullet_v)
                if event.key == K_LEFT:
                    pass
                if event.key == K_RIGHT:
                    pass
                if event.key == K_UP:
                    pass
                if event.key == K_DOWN:
                    pass
        hit = check_collision(player, all_bullets)
        update_scores(hit)
        all_sprites.update()
        all_sprites.draw(SCREEN)
        pygame.display.update()
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
