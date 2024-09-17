from logging import DEBUG
from datetime import datetime, timedelta
from servizio import log_setup
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator
from matplotlib import cm
import numpy as np
import os
from time import perf_counter
import os

start = perf_counter()
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile="DEBUG", name=__name__)
logger.info("Inizio")

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")


def contourf_f():
    x = np.linspace(-10, 10, 100)
    y = np.linspace(-10, 10, 100)
    xv, yv = np.meshgrid(x, y)
    zv = np.sin(np.sqrt(xv**2 + yv**2))
    plt.contourf(xv, yv, zv, levels=30)
    plt.colorbar()
    plt.show()
    print(xv)
    print(yv)


def plot_wireframe_f():
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    x = np.linspace(-10, 10, 100)
    y = np.linspace(-10, 10, 100)
    xv, yv = np.meshgrid(x, y)
    zv = np.sin(np.sqrt(xv**2 + yv**2))
    # Plot the surface.
    surf = ax.plot_wireframe(xv, yv, zv, rstride=3, cstride=3)
    # Customize the z axis.
    ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter("{x:.02f}")
    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()


def surface_f():
    # fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # set up a figure twice as wide as it is tall
    fig = plt.figure(figsize=plt.figaspect(0.5))

    # =============
    # First subplot
    # =============
    # set up the axes for the first plot
    # ax = fig.add_subplot(1, 2, 2, projection='3d')
    ax = fig.add_subplot(projection="3d")
    x = np.linspace(-10, 10, 100)
    y = np.linspace(-10, 10, 100)
    xv, yv = np.meshgrid(x, y)
    zv = np.sin(np.sqrt(xv**2 + yv**2))
    # Plot the surface.
    surf = ax.plot_surface(xv, yv, zv, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    # Customize the z axis.
    ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter("{x:.02f}")
    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)
    # rotate the axes and update
    # for angle in range(0, 360):
    #     ax.view_init(30, angle)
    #     plt.draw()
    #     plt.pause(.001)

    plt.show()


def main():
    # contourf_f()
    surface_f()
    # plot_wireframe_f()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if PROVA:
            logger.info(e, exc_info=True)
        else:
            logger.critical(e, exc_info=True)
logger.info("Fine")
end = perf_counter()
print("Elapsed Time: ", end - start)
