import pygame.image
from pygame import sprite

PROJECTILE_W, PROJECTILE_H = 11, 17
PROJECTILE_SPEED = 10
BOMB_SPEED = 5

INVADER_W, INVADER_H = 90, 60
INVADER_DX = -5
INVADER_DY = 100

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

    def rect(self):
        return self._rect.copy()


class Spaceship(object):
    def __init__(self, position):
        self._images = [
            pygame.transform.scale(pygame.image.load("resources/spaceship.png"), (SPACESHIP_W, SPACESHIP_H)),
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
        self._animation = Animation(self._images, position)
        self._speed = 0
        self._is_exploding = False

    def draw(self, surface):
        self._animation.draw(surface)

    def update(self, field_size):
        if self._animation.position[0] - SPACESHIP_W / 2 + self._speed < 0 or \
                self._animation.position[0] + SPACESHIP_W / 2 + self._speed > field_size[0]:
            self._speed = 0
        if self._speed != 0:
            self._animation.position = (self._animation.position[0] + self._speed, self._animation.position[1])

    def move(self, speed):
        self._speed = speed

    def rect(self):
        return self._animation.rect()

    def explode(self):
        self._animation = Animation(self._explode_images, self._animation.position, 1, False)
        self._speed = 0
        self._is_exploding = True

    def finished(self):
        return self._animation.finished()

    def is_exploding(self):
        return self._is_exploding


class Invader(sprite.Sprite):
    def __init__(self, position, move_left):
        super().__init__()
        self._invader_images = [
            pygame.transform.scale(pygame.image.load("resources/invader.png"), (INVADER_W, INVADER_H)),
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
        self._animation = Animation(self._invader_images, position)
        self._speed = INVADER_DX if move_left else -INVADER_DX
        self._is_exploding = False

    def draw(self, surface):
        self._animation.draw(surface)

    def update(self, field_size):
        w, h = field_size
        if self._animation.position[0] - INVADER_W / 2 + self._speed < 0 or self._animation.position[0] + INVADER_W / 2 + self._speed > w:
            self._animation.position = (self._animation.position[0], self._animation.position[1] + INVADER_DY)
            self._speed = -self._speed
        else:
            self._animation.position = (self._animation.position[0] + self._speed, self._animation.position[1])

        if self._animation.position[1] + INVADER_H / 2 + INVADER_DY > h:
            self._animation.position = (self._animation.position[0] + self._speed, self._animation.position[1] - INVADER_DY)
            self.explode()

    def rect(self):
        return self._animation.rect()

    def explode(self):
        self._animation = Animation(self._explode_images, self._animation.position, 1, False)
        self._speed = 0
        self._is_exploding = True

    def finished(self):
        return self._animation.finished()

    def is_exploding(self):
        return self._is_exploding


class Projectile(sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self._image = pygame.transform.scale(pygame.image.load("resources/projectile.png").convert(), (PROJECTILE_W, PROJECTILE_H))
        self._rect = self._image.get_rect()
        self._rect.center = position
        self._finished = False

    def update(self, field_size):
        if self._finished:
            return

        position = self._rect.center
        self._rect.center = (position[0], position[1] - PROJECTILE_SPEED)
        if self._rect.bottom < 0:
            self._finished = True

    def draw(self, surface):
        surface.blit(self._image, self._rect)

    def finished(self):
        return self._finished

    def rect(self):
        return self._rect.copy()


class Bomb(sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self._image = pygame.image.load("resources/bomb.png")
        self._rect = self._image.get_rect()
        self._rect.center = position
