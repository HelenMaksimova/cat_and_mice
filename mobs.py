import pygame
from random import choice


class Player(pygame.sprite.Sprite):

    def __init__(self, group, image, step=0, x=0, y=0, scr_width=0, scr_height=0, null_point=(0, 0)):
        super().__init__()
        self.null_point = null_point
        self.scr_width = scr_width
        self.scr_height = scr_height
        self.count = 0
        self.tries = 1
        self.direction = 'up'
        self.step = step
        self.speed = 0
        self.base_image = image
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 2 * 0.9
        self.rect.center = (x, y)
        self.status = 'normal'
        self.animation = False
        self.start_animation = 0
        group.add(self)

    def update(self):
        self.move()

    def move(self):
        self.speed = 0
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:
            self.speed = self.step
            self.to_left()
        elif key_state[pygame.K_RIGHT]:
            self.speed = self.step
            self.to_right()
        elif key_state[pygame.K_UP]:
            self.speed = self.step
            self.to_up()
        elif key_state[pygame.K_DOWN]:
            self.speed = self.step
            self.to_down()

    def to_right(self):
        self.image = pygame.transform.rotate(self.base_image, -90)
        if not self.rect.right >= self.scr_width:
            self.rect.x += self.speed

    def to_left(self):
        self.image = pygame.transform.rotate(self.base_image, 90)
        if not self.rect.left <= self.null_point[0]:
            self.rect.x -= self.speed

    def to_up(self):
        self.image = self.base_image
        if not self.rect.top <= self.null_point[1]:
            self.rect.y -= self.speed

    def to_down(self):
        self.image = pygame.transform.rotate(self.base_image, 180)
        if not self.rect.bottom >= self.scr_height:
            self.rect.y += self.speed

    def change_image(self, image, period):
        if self.animation:
            now = pygame.time.get_ticks()
            if now - self.start_animation < period:
                self.image = image
            else:
                self.animation = False
                self.status = 'normal'
                self.image = self.base_image


class Mob(pygame.sprite.Sprite):

    def __init__(self, image, step=0, destination=0, x=0, y=0, scr_width=0, scr_height=0, null_point=(0, 0)):
        super().__init__()
        self.null_point = null_point
        self.scr_width = scr_width
        self.scr_height = scr_height
        self.DESTINATION = destination
        self.destination = self.DESTINATION
        self.DIRECTIONS = {'right': self.to_right, 'left': self.to_left, 'up': self.to_up, 'down': self.to_down}
        self.step = step
        self.direction = 'right'
        self.base_image = image
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 2 * 0.9
        self.rect.center = (x, y)
        self.status = 'normal'
        self.animation = False
        self.start_animation = 0

    def update(self):
        self.destination -= 1
        if not self.destination:
            self.random_way()
            self.destination = self.DESTINATION
        self.DIRECTIONS[self.direction]()

    def to_right(self):
        self.image = pygame.transform.rotate(self.base_image, -90)
        if self.rect.right >= self.scr_width:
            self.random_way()
        else:
            self.rect.x += self.step

    def to_left(self):
        self.image = pygame.transform.rotate(self.base_image, 90)
        if self.rect.left <= self.null_point[0]:
            self.random_way()
        else:
            self.rect.x -= self.step

    def to_up(self):
        self.image = self.base_image
        if self.rect.top <= self.null_point[1]:
            self.random_way()
        else:
            self.rect.y -= self.step

    def to_down(self):
        self.image = pygame.transform.rotate(self.base_image, 180)
        if self.rect.bottom >= self.scr_height:
            self.random_way()
        else:
            self.rect.y += self.step

    def random_way(self):
        self.direction = choice(list(self.DIRECTIONS.keys()))

    def change_direct(self):
        change_dict = {'right': 'left', 'left': 'right', 'up': 'down', 'down': 'up'}
        self.direction = change_dict[self.direction]
        self.DIRECTIONS[self.direction]()

    def change_image(self, image, period):
        if self.animation:
            now = pygame.time.get_ticks()
            if now - self.start_animation < period:
                self.image = image
            else:
                self.animation = False
                self.status = 'normal'
                self.image = self.base_image


class Bar(pygame.sprite.Sprite):
    def __init__(self, group, x=0, y=0, width=1, height=1, color=(148, 148, 148)):
        super().__init__()
        self.width = width
        self.height = height
        self.stars = list()
        self.tries = list()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        group.add(self)

    def stars_locate(self, num, image, group):
        x = 0
        for _ in range(num):
            star = pygame.sprite.Sprite()
            star.image = image
            star.rect = star.image.get_rect()
            star.rect.topleft = (x, 0)
            x += star.rect.width + 3
            self.stars.append(star)
            group.add(star)

    def star_fill(self, idx, image):
        self.stars[idx].image = image

    def player_tries_locate(self, num, image, group):
        x = self.width - 53
        for _ in range(num):
            plr_try = pygame.sprite.Sprite()
            plr_try.image = image
            plr_try.rect = plr_try.image.get_rect()
            plr_try.rect.topleft = (x, 0)
            x -= plr_try.rect.width + 3
            self.tries.append(plr_try)
            group.add(plr_try)

    def player_tries_less(self, idx, image):
        self.tries[idx].image = image


class Wall(pygame.sprite.Sprite):

    def __init__(self, image, x=0, y=0, scr_width=0, scr_height=0, null_point=(0, 0)):
        super().__init__()
        self.null_point = null_point
        self.scr_width = scr_width
        self.scr_height = scr_height
        self.base_image = image
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 2 * 0.8
        self.rect.center = (x, y)
        self.status = 'normal'
        self.animation = False
        self.start_animation = 0

    def change_direct(self):
        pass

    def change_image(self, image, period):
        if self.animation:
            now = pygame.time.get_ticks()
            if now - self.start_animation < period:
                self.image = image
            else:
                self.animation = False
                self.status = 'normal'
                self.image = self.base_image
