from random import Random

import pygame

from objects import *

MAX_PROJECTILES_NUMBER = 5
MAX_ENEMIES_NUMBER = 10
MIN_DISTANCE_BETWEEN_ENEMIES = 100

BG_COLOR = pygame.Color(0, 0, 255)
FG_COLOR = pygame.Color(255, 255, 255)

FPS = 60
FONT_SIZE = 30

random_generator = Random()


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._size = self.width, self.height = 640, 400
        self._ship = Spaceship((self.width / 2, self.height - SPACESHIP_H / 2))
        self._background = pygame.image.load("resources/background.png")
        self._invaders = [self.spawn_invader()]
        self._invader_spawn_counter = 0
        self._projectiles = []
        self._score = Score()

    def spawn_invader(self):
        x = random_generator.randint(INVADER_W / 2, self.width - INVADER_W / 2)
        return Invader((x, INVADER_H), random_generator.randint(0, 1))

    def spawn_projectile(self, position):
        return Projectile(position)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self._size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        pygame.time.Clock().tick(FPS)
        pygame.display.set_caption("Space invaders")

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self._ship.move(-SHIP_SPEED)
        elif keys[pygame.K_RIGHT]:
            self._ship.move(SHIP_SPEED)
        else:
            self._ship.move(0)

        if keys[pygame.K_SPACE]:
            if len(self._projectiles) < MAX_PROJECTILES_NUMBER and \
                    (len(self._projectiles) == 0 or (self._projectiles[-1].rect().centery < self._size[1] - SPACESHIP_H)):
                self._score.shot()
                rect = self._ship.rect()
                self._projectiles.append(self.spawn_projectile(rect.center))

    def on_loop(self):
        self._ship.update(self._size)

        for invader in self._invaders:
            if invader.finished():
                self._invaders.remove(invader)
                self._invaders.append(self.spawn_invader())
            else:
                invader.update(self._size)

        for projectile in self._projectiles:
            projectile.update(self._size)
            if projectile.finished():
                self._projectiles.remove(projectile)

            for invader in self._invaders:
                if not invader.is_exploding() and invader.rect().colliderect(projectile.rect()):
                    invader.explode()
                    self._score.inveder_hit()
                    self._projectiles.remove(projectile)
                    break

        self._invader_spawn_counter += 1
        if len(self._invaders) < MAX_ENEMIES_NUMBER and self._invader_spawn_counter % 100 == 0:
            self._invaders.append(self.spawn_invader())

    def on_render(self):
        pygame.time.Clock().tick(FPS)
        self._display_surf.fill(BG_COLOR)
        self._display_surf.blit(self._background, self._background.get_rect())
        self._ship.draw(self._display_surf)

        for invader in self._invaders:
            invader.draw(self._display_surf)

        for projectile in self._projectiles:
            projectile.draw(self._display_surf)

        self._score.draw(self._display_surf, self._size)

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


class Score(object):
    def __init__(self):
        self._projectiles_count = 0
        self._invaders_count = 0

        pygame.font.init()
        self._font = pygame.font.SysFont('Comic Sans MS', FONT_SIZE)

    def shot(self):
        self._projectiles_count += 1

    def inveder_hit(self):
        self._invaders_count += 1

    def draw(self, surface, field_size):
        text_invaders = self._font.render(f"HIT: {str(self._invaders_count)}", False, FG_COLOR)
        surface.blit(text_invaders, (FONT_SIZE * 2, 0))
        text_projectiles = self._font.render(f"SHOT: {str(self._projectiles_count)}", False, FG_COLOR)
        surface.blit(text_projectiles, (field_size[0] - FONT_SIZE * 6, 0))


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
