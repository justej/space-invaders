import pygame.image
from pygame import sprite

PROJECTILE_SPEED = 10
ENEMY_W, ENEMY_H = 90, 60
SPACESHIP_W, SPACESHIP_H = 50, 80
ENEMY_SPEED = -5
ENEMY_DY = 100


class Animation(sprite.Sprite):
    def __init__(self, images, position):
        super().__init__()
        self.position = position
        self._frames = images
        self._frame_number = 0
        self._rect = images[self._frame_number].get_rect()
        self._should_loop = False
        self._finished = False

    def draw(self, surface):
        if self._frame_number == len(self._frames):
            self._finished = True
            self._frame_number = 0

        frame = self._frames[self._frame_number]
        self._rect = frame.get_rect()
        self._rect.center = self.position
        surface.blit(frame, self._rect)
        self._frame_number += 1

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
            pygame.transform.scale(pygame.image.load("resources/spaceship.png"), (SPACESHIP_W, SPACESHIP_H))
        ]
        self.animation = Animation(self.images, position)
        self.speed = 0

    def draw(self, surface):
        self.animation.draw(surface)

    def update(self, field_size):
        if self.animation._rect.left + self.speed < 0 or self.animation._rect.right + self.speed > field_size[0]:
            self.speed = 0
        if self.speed != 0:
            self.animation.position = (self.animation.position[0] + self.speed, self.animation.position[1])

    def move(self, speed):
        self.speed = speed


class Enemy(sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("resources/invader.png"), (ENEMY_W, ENEMY_H))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.speed = ENEMY_SPEED
        # self.animation

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, field_size):
        w, h = field_size
        if self.rect.left + self.speed < 0 or self.rect.right + self.speed > w:
            self.rect.centery += ENEMY_DY
            self.speed = -self.speed
        else:
            self.rect.centerx += self.speed

        if self.rect.bottom + ENEMY_DY > h:
            self.rect.centery -= ENEMY_DY
            old_center = self.rect.center
            self.image = pygame.transform.scale(pygame.image.load("resources/explosion.png"), (150, 150))
            self.rect = self.image.get_rect()
            self.rect.center = old_center
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
