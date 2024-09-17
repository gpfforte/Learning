from re import X
import pygame
import math
from logging import DEBUG
from servizio import log_setup
import os

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

WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sping Simulation")


BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
SCALE = 100
TIMESTEP = 0.1
FONT = pygame.font.SysFont("comicsans", 16)


class Spring:
    def __init__(self, x, y, radius, color, mass, kappa):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.kappa = kappa
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x_scaled = self.x * SCALE + WIDTH / 2
        y_scaled = self.y * SCALE + HEIGHT / 2

        pygame.draw.circle(win, self.color, (x_scaled, y_scaled), self.radius)

    def update_position(self):
        fx = -self.kappa * self.x
        fy = -self.kappa * self.y
        self.x_vel += fx / self.mass * TIMESTEP
        self.y_vel += fy / self.mass * TIMESTEP
        self.x += self.x_vel * TIMESTEP
        self.y += self.y_vel * TIMESTEP


def main():
    run = True
    clock = pygame.time.Clock()

    molla1 = Spring(-1, -1, 16, BLUE, 1, 1)
    molla2 = Spring(2, -2, 16, RED, 2, 0.5)
    molle = [molla1, molla2]
    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for molla in molle:
            molla.update_position()
            molla.draw(WIN)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if PROVA:
            logger.info(e, exc_info=True)
        else:
            logger.critical(e, exc_info=True)
