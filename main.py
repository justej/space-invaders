from random import Random

import pygame

from objects import *


class App:
    FPS = 60
    BG_COLOR = pygame.Color(0, 0, 255)
    INVADER_SPAWN_FREQUENCY = 100
    INVADER_BOMB_SHELL_FREQUENCY = 50
    FIELD_SIZE = 640, 400
    MAX_PROJECTILES_NUMBER = 5
    MAX_INVADERS_NUMBER = 10
    random_generator = Random()

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._size = self.width, self.height = App.FIELD_SIZE
        self._background = pygame.image.load("resources/background.png")

        self._ship = None
        self._invaders = None
        self._invader_spawn_counter = 0
        self._projectiles = None
        self._bombs = None
        self._score = None
        self._game_over = None
        self._menu = None

    def spawn_invader(self):
        x = App.random_generator.randint(Invader.W / 2, self.width - Invader.W / 2)
        return Invader((x, Invader.H), App.random_generator.randint(0, 1))

    def spawn_projectile(self, position):
        return Projectile(position)

    def init_game(self):
        self._ship = Spaceship((self.width / 2, self.height - Spaceship.H / 2))
        self._invaders = [self.spawn_invader()]
        self._invader_spawn_counter = 0
        self._projectiles = []
        self._bombs = []
        self._score = Score()
        self._game_over = GameOver()
        self._menu = Menu()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self._size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        pygame.time.Clock().tick(App.FPS)
        pygame.display.set_caption("Space invaders")
        pygame.font.init()
        self.init_game()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            return

        if event.type not in (pygame.KEYDOWN, pygame.KEYUP):
            return

        keys = pygame.key.get_pressed()

        if self._menu.show:
            if keys[pygame.K_UP]:
                self._menu.selected_item -= 1
            if keys[pygame.K_DOWN]:
                self._menu.selected_item += 1

            if self._menu.selected_item < 0:
                self._menu.selected_item = 0
            if self._menu.selected_item > 1:
                self._menu.selected_item = 1

            if keys[pygame.K_SPACE]:
                if self._menu.selected_item == 0:
                    self.init_game()
                if self._menu.selected_item == 1:
                    self._running = False
            return

        if keys[pygame.K_LEFT]:
            self._ship.move(-Spaceship.SPEED)
        elif keys[pygame.K_RIGHT]:
            self._ship.move(Spaceship.SPEED)
        else:
            self._ship.move(0)

        if keys[pygame.K_SPACE]:
            if len(self._projectiles) < App.MAX_PROJECTILES_NUMBER and \
                    (len(self._projectiles) == 0 or (self._projectiles[-1].rect().centery < self._size[1] - Spaceship.H)):
                self._score.shot()
                rect = self._ship.rect()
                self._projectiles.append(Projectile(rect.center))

    def on_loop(self):
        if self._game_over.unfortunately:
            self._game_over.update()
            self._menu.update()
            return

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
                continue

            for invader in self._invaders:
                if not invader.is_exploding() and invader.rect().colliderect(projectile.rect()):
                    invader.explode()
                    self._score.inveder_hit()
                    self._projectiles.remove(projectile)
                    break

        self._invader_spawn_counter += 1
        if len(self._invaders) < App.MAX_INVADERS_NUMBER and self._invader_spawn_counter % App.INVADER_SPAWN_FREQUENCY == 0:
            self._invaders.append(self.spawn_invader())

        if len(self._invaders) > 0 and self._invader_spawn_counter % App.INVADER_BOMB_SHELL_FREQUENCY == 0:
            n = App.random_generator.randint(0, len(self._invaders) - 1)
            if self._invaders[n].is_exploding():
                self._invader_spawn_counter -= 1
            else:
                invader_rect = self._invaders[n].rect()
                self._bombs.append(Bomb((invader_rect.center[0], invader_rect.bottom)))

        for bomb in self._bombs:
            bomb.update(self._size)
            if bomb.finished():
                self._bombs.remove(bomb)
                continue

            if not self._ship.is_exploding() and bomb.rect().colliderect(self._ship.rect()):
                self._bombs.remove(bomb)
                self._ship.explode()

        if self._ship.finished():
            self._game_over.unfortunately = True
            self._menu.show = True

    def on_render(self):
        pygame.time.Clock().tick(App.FPS)
        self._display_surf.fill(App.BG_COLOR)
        self._display_surf.blit(self._background, self._background.get_rect())
        self._ship.draw(self._display_surf)

        for invader in self._invaders:
            invader.draw(self._display_surf)

        for projectile in self._projectiles:
            projectile.draw(self._display_surf)

        for bomb in self._bombs:
            bomb.draw(self._display_surf)

        self._score.draw(self._display_surf, self._size)
        self._game_over.draw(self._display_surf, self._size)
        self._menu.draw(self._display_surf, self._size)

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
    FONT_SIZE = 30
    COLOR = pygame.Color(255, 255, 255)

    def __init__(self):
        self._projectiles_count = 0
        self._invaders_count = 0
        self._font = pygame.font.SysFont('Comic Sans MS', Score.FONT_SIZE)

    def shot(self):
        self._projectiles_count += 1

    def inveder_hit(self):
        self._invaders_count += 1

    def draw(self, surface, field_size):
        text_invaders = self._font.render(f"HIT: {str(self._invaders_count)}", False, Score.COLOR)
        surface.blit(text_invaders, (Score.FONT_SIZE * 2, 0))
        text_projectiles = self._font.render(f"SHOT: {str(self._projectiles_count)}", False, Score.COLOR)
        surface.blit(text_projectiles, (field_size[0] - Score.FONT_SIZE * 6, 0))


class GameOver(object):
    FONT_SIZE = 60
    COLOR = pygame.Color(255, 255, 255)
    BLINK_FREQUENCY = 10

    def __init__(self):
        self.unfortunately = False
        font = pygame.font.SysFont('Comic Sans MS', GameOver.FONT_SIZE)
        self._text = font.render("Game Over", False, GameOver.COLOR)
        self._show = True
        self._show_counter = 0

    def update(self):
        if not self.unfortunately:
            return

        self._show_counter += 1
        if self._show_counter % GameOver.BLINK_FREQUENCY == 0:
            self._show = not self._show

    def draw(self, surface, field_size):
        if self.unfortunately and self._show:
            text_size = self._text.get_size()
            surface.blit(self._text, ((field_size[0] - text_size[0]) / 2, (field_size[1] - text_size[1]) / 2))


class Menu(object):
    FONT_SIZE = 40
    COLOR = pygame.Color(0, 255, 255)

    def __init__(self):
        font = pygame.font.SysFont('Comic Sans MS', Menu.FONT_SIZE)
        self.show = False
        self._text = {
            0: font.render('New game', False, Menu.COLOR),
            1: font.render('Exit', False, Menu.COLOR),
        }
        self.selected_item = 0

    def update(self):
        pass

    def draw(self, surface, field_size):
        if self.show:
            for i, text in self._text.items():
                text_size = text.get_size()
                x = (field_size[0] - text_size[0]) / 2
                y = (field_size[1] - GameOver.FONT_SIZE) / 2 + (1.3 * i + 2) * Menu.FONT_SIZE
                surface.blit(text, (x, y))
                if i == self.selected_item:
                    pygame.draw.rect(surface, Menu.COLOR, (x - 5, y, text_size[0] + 10, text_size[1]), 5)


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
