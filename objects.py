import pygame.image
from pygame import sprite


class Animation(sprite.Sprite):
    def __init__(self, images, position, times_per_frame=1, should_loop=True):
        super().__init__()
        self.position = position
        self._frames = images
        self._frame_number = 0
        self._rect = images[self._frame_number].get_rect()
        self._rect.center = position
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
    W, H = 50, 80
    SPEED = 10
    EXPLOSION_W, EXPLOSION_H = 150, 150

    def __init__(self, position):
        self._images = [
            pygame.transform.scale(pygame.image.load("resources/spaceship.png"), (Spaceship.W, Spaceship.H)),
        ]
        explosion = pygame.image.load("resources/explosion.png")
        self._explode_images = [
            pygame.transform.scale(explosion, (Spaceship.EXPLOSION_W / 2, Spaceship.EXPLOSION_H / 2)),
            pygame.transform.scale(explosion, (Spaceship.EXPLOSION_W / 1.9, Spaceship.EXPLOSION_H / 1.9)),
            pygame.transform.scale(explosion, (Spaceship.EXPLOSION_W / 1.7, Spaceship.EXPLOSION_H / 1.7)),
            pygame.transform.scale(explosion, (Spaceship.EXPLOSION_W / 1.5, Spaceship.EXPLOSION_H / 1.5)),
            pygame.transform.scale(explosion, (Spaceship.EXPLOSION_W / 1.3, Spaceship.EXPLOSION_H / 1.3)),
            pygame.transform.scale(explosion, (Spaceship.EXPLOSION_W / 1.1, Spaceship.EXPLOSION_H / 1.1)),
            pygame.transform.scale(explosion, (Spaceship.EXPLOSION_W, Spaceship.EXPLOSION_H)),
            pygame.transform.scale(explosion, (Spaceship.EXPLOSION_W / 1.1, Spaceship.EXPLOSION_H / 1.1)),
            pygame.transform.scale(explosion, (Spaceship.EXPLOSION_W / 1.3, Spaceship.EXPLOSION_H / 1.3)),
            pygame.transform.scale(explosion, (Spaceship.EXPLOSION_W / 1.5, Spaceship.EXPLOSION_H / 1.5)),
            pygame.transform.scale(explosion, (Spaceship.EXPLOSION_W / 1.7, Spaceship.EXPLOSION_H / 1.7)),
            pygame.transform.scale(explosion, (Spaceship.EXPLOSION_W / 1.9, Spaceship.EXPLOSION_H / 1.9)),
            pygame.transform.scale(explosion, (Spaceship.EXPLOSION_W / 2, Spaceship.EXPLOSION_H / 2)),
        ]
        self._animation = Animation(self._images, position)
        self._speed = 0
        self._is_exploding = False

    def draw(self, surface):
        self._animation.draw(surface)

    def update(self, field_size):
        if self._animation.position[0] - Spaceship.W / 2 + self._speed < 0 or \
                self._animation.position[0] + Spaceship.W / 2 + self._speed > field_size[0]:
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
    W, H = 90, 60
    DX = -5
    DY = 100
    EXPLOSION_W, EXPLOSION_H = 150, 150

    def __init__(self, position, move_left):
        super().__init__()
        self._invader_images = [
            pygame.transform.scale(pygame.image.load("resources/invader.png"), (Invader.W, Invader.H)),
        ]
        explosion = pygame.image.load("resources/explosion.png")
        self._explode_images = [
            pygame.transform.scale(explosion, (Invader.EXPLOSION_W / 2, Invader.EXPLOSION_H / 2)),
            pygame.transform.scale(explosion, (Invader.EXPLOSION_W / 1.9, Invader.EXPLOSION_H / 1.9)),
            pygame.transform.scale(explosion, (Invader.EXPLOSION_W / 1.7, Invader.EXPLOSION_H / 1.7)),
            pygame.transform.scale(explosion, (Invader.EXPLOSION_W / 1.5, Invader.EXPLOSION_H / 1.5)),
            pygame.transform.scale(explosion, (Invader.EXPLOSION_W / 1.3, Invader.EXPLOSION_H / 1.3)),
            pygame.transform.scale(explosion, (Invader.EXPLOSION_W / 1.1, Invader.EXPLOSION_H / 1.1)),
            pygame.transform.scale(explosion, (Invader.EXPLOSION_W, Invader.EXPLOSION_H)),
            pygame.transform.scale(explosion, (Invader.EXPLOSION_W / 1.1, Invader.EXPLOSION_H / 1.1)),
            pygame.transform.scale(explosion, (Invader.EXPLOSION_W / 1.3, Invader.EXPLOSION_H / 1.3)),
            pygame.transform.scale(explosion, (Invader.EXPLOSION_W / 1.5, Invader.EXPLOSION_H / 1.5)),
            pygame.transform.scale(explosion, (Invader.EXPLOSION_W / 1.7, Invader.EXPLOSION_H / 1.7)),
            pygame.transform.scale(explosion, (Invader.EXPLOSION_W / 1.9, Invader.EXPLOSION_H / 1.9)),
            pygame.transform.scale(explosion, (Invader.EXPLOSION_W / 2, Invader.EXPLOSION_H / 2)),
        ]
        self._animation = Animation(self._invader_images, position)
        self._speed = Invader.DX if move_left else -Invader.DX
        self._is_exploding = False

    def draw(self, surface):
        self._animation.draw(surface)

    def update(self, field_size):
        w, h = field_size
        if self._animation.position[0] - Invader.W / 2 + self._speed < 0 or self._animation.position[0] + Invader.W / 2 + self._speed > w:
            self._animation.position = (self._animation.position[0], self._animation.position[1] + Invader.DY)
            self._speed = -self._speed
        else:
            self._animation.position = (self._animation.position[0] + self._speed, self._animation.position[1])

        if self._animation.position[1] + Invader.H / 2 + Invader.DY > h:
            self._animation.position = (self._animation.position[0] + self._speed, self._animation.position[1] - Invader.DY)
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
    W, H = 11, 17
    SPEED = 10

    def __init__(self, position):
        super().__init__()
        self._image = pygame.transform.scale(pygame.image.load("resources/projectile.png").convert(), (Projectile.W, Projectile.H))
        self._rect = self._image.get_rect()
        self._rect.center = position
        self._finished = False

    def update(self, field_size):
        if self._finished:
            return

        position = self._rect.center
        self._rect.center = (position[0], position[1] - Projectile.SPEED)
        if self._rect.bottom < 0:
            self._finished = True

    def draw(self, surface):
        surface.blit(self._image, self._rect)

    def finished(self):
        return self._finished

    def rect(self):
        return self._rect.copy()


class Bomb(sprite.Sprite):
    W, H = 30, 37
    SPEED = 5

    def __init__(self, position):
        super().__init__()
        self._image = pygame.transform.scale(pygame.image.load("resources/bomb.png"), (Bomb.W, Bomb.H))
        self._rect = self._image.get_rect()
        self._rect.center = position
        self._finished = False

    def update(self, field_size):
        if self._finished:
            return

        position = self._rect.center
        self._rect.center = (position[0], position[1] + Bomb.SPEED)
        if self._rect.top > field_size[1]:
            self._finished = True

    def draw(self, surface):
        surface.blit(self._image, self._rect)

    def finished(self):
        return self._finished

    def rect(self):
        return self._rect.copy()
