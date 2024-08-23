import pygame.image
from pygame import sprite

PROJECTILE_SPEED = 10

ENEMY_W, ENEMY_H = 90, 60
ENEMY_DX = -5
ENEMY_DY = 100

SPACESHIP_W, SPACESHIP_H = 50, 80
SHIP_SPEED = 10

EXPLOSION_W, EXPLOSION_H = 150, 150


class Animation(sprite.Sprite):
    def __init__(self, images, position, times_per_frame=1, should_loop=True):
        super().__init__()
        self.position = position
        self._frames = images
        self._frame_number = 0
        self._rect = images[self._frame_number].get_rect()
        self._should_loop = should_loop
        self._finished = False
        self._draw_counter = 0
        self._times_per_frame = times_per_frame

    def draw(self, surface):
        if self._finished:
            return

        frame = self._frames[self._frame_number]
        self._rect = frame.get_rect()
        self._rect.center = self.position
        surface.blit(frame, self._rect)

        self._draw_counter += 1
        if self._draw_counter > self._times_per_frame:
            self._draw_counter = 0
            self._frame_number += 1
            if self._frame_number == len(self._frames):
                self._finished = not self._should_loop
                self._frame_number = 0

    def reset(self):
        self._frame_number = 0
        self._finished = False

    def finished(self):
        return self._finished

    def should_loop(self, should_loop=None):
        if should_loop is not None:
            self._should_loop = should_loop
        return self.should_loop


class Spaceship(object):
    def __init__(self, position):
        self.images = [
            pygame.transform.scale(pygame.image.load("resources/spaceship.png"), (SPACESHIP_W, SPACESHIP_H)),
        ]
        self.animation = Animation(self.images, position)
        self.speed = 0

    def draw(self, surface):
        self.animation.draw(surface)

    def update(self, field_size):
        if self.animation.position[0] - SPACESHIP_W / 2 + self.speed < 0 or self.animation.position[0] + SPACESHIP_W / 2 + self.speed > field_size[0]:
            self.speed = 0
        if self.speed != 0:
            self.animation.position = (self.animation.position[0] + self.speed, self.animation.position[1])

    def move(self, speed):
        self.speed = speed


class Enemy(sprite.Sprite):
    def __init__(self, position, move_left):
        super().__init__()
        self._enemy_images = [
            pygame.transform.scale(pygame.image.load("resources/invader.png"), (ENEMY_W, ENEMY_H)),
        ]
        explosion = pygame.image.load("resources/explosion.png")
        self._explode_images = [
            pygame.transform.scale(explosion, (EXPLOSION_W / 2, EXPLOSION_H / 2)),
            pygame.transform.scale(explosion, (EXPLOSION_W / 1.9, EXPLOSION_H / 1.9)),
            pygame.transform.scale(explosion, (EXPLOSION_W / 1.7, EXPLOSION_H / 1.7)),
            pygame.transform.scale(explosion, (EXPLOSION_W / 1.5, EXPLOSION_H / 1.5)),
            pygame.transform.scale(explosion, (EXPLOSION_W / 1.3, EXPLOSION_H / 1.3)),
            pygame.transform.scale(explosion, (EXPLOSION_W / 1.1, EXPLOSION_H / 1.1)),
            pygame.transform.scale(explosion, (EXPLOSION_W, EXPLOSION_H)),
            pygame.transform.scale(explosion, (EXPLOSION_W / 1.1, EXPLOSION_H / 1.1)),
            pygame.transform.scale(explosion, (EXPLOSION_W / 1.3, EXPLOSION_H / 1.3)),
            pygame.transform.scale(explosion, (EXPLOSION_W / 1.5, EXPLOSION_H / 1.5)),
            pygame.transform.scale(explosion, (EXPLOSION_W / 1.7, EXPLOSION_H / 1.7)),
            pygame.transform.scale(explosion, (EXPLOSION_W / 1.9, EXPLOSION_H / 1.9)),
            pygame.transform.scale(explosion, (EXPLOSION_W / 2, EXPLOSION_H / 2)),
        ]
        self.animation = Animation(self._enemy_images, position)
        self.speed = ENEMY_DX if move_left else -ENEMY_DX

    def draw(self, surface):
        self.animation.draw(surface)

    def update(self, field_size):
        w, h = field_size
        if self.animation.position[0] - ENEMY_W / 2 + self.speed < 0 or self.animation.position[0] + ENEMY_W / 2 + self.speed > w:
            self.animation.position = (self.animation.position[0], self.animation.position[1] + ENEMY_DY)
            self.speed = -self.speed
        else:
            self.animation.position = (self.animation.position[0] + self.speed, self.animation.position[1])

        if self.animation.position[1] + ENEMY_H / 2 + ENEMY_DY > h:
            self.animation.position = (self.animation.position[0] + self.speed, self.animation.position[1] - ENEMY_DY)
            self.animation = Animation(self._explode_images, self.animation.position, 5, False)
            self.speed = 0


class Projectile(sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("resources/projectile.png")
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):
        position = self.rect.center
        self.rect.center = (position[0], position[1] - PROJECTILE_SPEED)


class Bomb(sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("resources/bomb.png")
        self.rect = self.image.get_rect()
        self.rect.center = position
