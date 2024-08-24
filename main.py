import time
from random import Random

import pygame

from objects import *

MAX_PROJECTILES_NUMBER = 5
BG_COLOR = pygame.Color(0, 0, 255)
FPS = 60

rand = Random()


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400
        self.ship = Spaceship((self.width / 2, self.height - SPACESHIP_H / 2))
        self.background = pygame.image.load("resources/background.png")
        self.enemies = [self.spawn_enemy()]
        self.projectiles = []

    def spawn_enemy(self):
        return Enemy((self.width / 2, ENEMY_H), rand.randint(0, 1))

    def spawn_projectile(self, position):
        return Projectile(position)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        pygame.time.Clock().tick(FPS)
        pygame.display.set_caption("Space invaders")

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.ship.move(-SHIP_SPEED)
        elif keys[pygame.K_RIGHT]:
            self.ship.move(SHIP_SPEED)
        else:
            self.ship.move(0)

        if keys[pygame.K_SPACE]:
            if len(self.projectiles) < MAX_PROJECTILES_NUMBER and (
                    len(self.projectiles) == 0 or (self.projectiles[-1]._rect[1] < self.size[1] - 100)):
                self.projectiles.append(self.spawn_projectile(self.ship.animation.position))
            print(time.time(), len(self.projectiles), self.projectiles[-1]._rect[1], self.size[1] - 60, tuple(p._rect[1] for p in self.projectiles))

    def on_loop(self):
        self.ship.update(self.size)

        for enemy in self.enemies:
            if enemy.animation.finished():
                self.enemies.remove(enemy)
                self.enemies.append(self.spawn_enemy())
            else:
                enemy.update(self.size)

        for projectile in self.projectiles:
            projectile.update(self.size)
            if projectile.finished():
                self.projectiles.remove(projectile)
                print(len(self.projectiles))

    def on_render(self):
        pygame.time.Clock().tick(FPS)
        self._display_surf.fill(BG_COLOR)
        self._display_surf.blit(self.background, self.background.get_rect())
        self.ship.draw(self._display_surf)

        for enemy in self.enemies:
            enemy.draw(self._display_surf)

        for projectile in self.projectiles:
            projectile.draw(self._display_surf)
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
