from random import Random

import pygame

from objects import *

MAX_PROJECTILES_NUMBER = 5
MAX_ENEMIES_NUMBER = 10
MIN_DISTANCE_BETWEEN_ENEMIES = 100

BG_COLOR = pygame.Color(0, 0, 255)
FPS = 60

random_generator = Random()


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400
        self.ship = Spaceship((self.width / 2, self.height - SPACESHIP_H / 2))
        self.background = pygame.image.load("resources/background.png")
        self.invaders = [self.spawn_invader()]
        self.invader_spawn_counter = 0
        self.projectiles = []

    def spawn_invader(self):
        x = random_generator.randint(INVADER_W / 2, self.width - INVADER_W / 2)
        return Invader((x, INVADER_H), random_generator.randint(0, 1))

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
                    len(self.projectiles) == 0 or (self.projectiles[-1].rect().centery < self.size[1] - SPACESHIP_H)):
                self.projectiles.append(self.spawn_projectile(self.ship.animation.position))

    def on_loop(self):
        self.ship.update(self.size)

        for invader in self.invaders:
            if invader.finished():
                self.invaders.remove(invader)
                self.invaders.append(self.spawn_invader())
            else:
                invader.update(self.size)

        for projectile in self.projectiles:
            projectile.update(self.size)
            if projectile.finished():
                self.projectiles.remove(projectile)

            for invader in self.invaders:
                if not invader.is_exploding() and invader.rect().colliderect(projectile.rect()):
                    invader.explode()
                    self.projectiles.remove(projectile)
                    break

        self.invader_spawn_counter += 1
        if len(self.invaders) < MAX_ENEMIES_NUMBER and self.invader_spawn_counter > 100:
            self.invaders.append(self.spawn_invader())
            self.invader_spawn_counter = 0

    def on_render(self):
        pygame.time.Clock().tick(FPS)
        self._display_surf.fill(BG_COLOR)
        self._display_surf.blit(self.background, self.background.get_rect())
        self.ship.draw(self._display_surf)

        for invader in self.invaders:
            invader.draw(self._display_surf)

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
