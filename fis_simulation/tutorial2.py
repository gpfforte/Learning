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
from random import randint, choice, randrange


# TODO Mettere un'immagine come player e farlo muovere con i tasti - OK
# TODO I proiettili farli comparire da soli quando escono fuori dallo schermo - OK
# TODO Fare Game Over quando un proiettile tocca il fondo
# TODO Far aumentare i proiettili o la velocità degli stessi di livello in livello
# TODO Salendo di livello si può fare in modo che il player debba invece stare lontano dai proiettili che
# possono aumentare sempre più di numero e velocità, in quel caso lo score aumenta man mano che i proiettili
# toccano il fondo

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


TEXT_HIT = pygame.font.SysFont("comicsans", 16).render("Hit", 1, WHITE)

FONT_SCORE = pygame.font.SysFont("comicsans", 40)
total_score = 0


# This goes outside the while loop, near the top of the program
picture = pygame.image.load(os.path.join("media", "space.png")).convert()
picture = pygame.transform.scale(picture, (WIDTH, HEIGHT))
try:
    music = pygame.mixer.music.load(os.path.join("media", "Inner Peace.mid"))
    pygame.mixer.music.play(-1)  # -1 will ensure the song keeps looping
    bulletSound = pygame.mixer.Sound(
        os.path.join("media", "flak_gun_sound.ogg"))
    hitSound = pygame.mixer.Sound(os.path.join("media", "squeak2.wav"))
except:
    pass


def update_scores(hit):
    global total_score
    total_score += hit
    text = FONT_SCORE.render(f"Score {total_score}", 1, WHITE)
    SCREEN.blit(text, (10, 10))


def check_collision(player, all_bullets):
    sprite_list = pygame.sprite.spritecollide(
        player, all_bullets, True, collided=None)
    for sprite in sprite_list:
        SCREEN.blit(TEXT_HIT, (sprite.rect.right, sprite.rect.top))
        try:
            hitSound.play()
        except:
            pass
        return 1
    return 0


CREATEBULLET = USEREVENT

pygame.time.set_timer(CREATEBULLET, randrange(1000, 2000))
# print (NOEVENT , USEREVENT, NUMEVENTS)


def main():
    running = True
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    all_bullets_v = pygame.sprite.Group()
    all_bullets = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)

    while running:
        SCREEN.blit(picture, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == CREATEBULLET:
                pygame.time.set_timer(CREATEBULLET, randrange(1000, 2000))
                if len(all_bullets_v) <= 5:
                    try:
                        bulletSound.play()
                    except:
                        pass
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
