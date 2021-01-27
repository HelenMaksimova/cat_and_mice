import pygame
import os
from random import randint
from mobs import Mob, Player, Bar, Wall

# константы
WIDTH = 1500
HEIGHT = 1000
BAR_HEIGHT = 50
AN_TIME = 300
FPS = 60

PLAYER_STEP = 3
PLAYER_TRIES = 3
PLAYER_STARS = 10

MOB_STEP = 2
MOB_SIZE = 50
DESTINATION = 100

TREES_COUNT = 15

DOG_COUNT = 6
MOUSE_COUNT = 10


# создание мобов и объектов
def spawn_foods(num):
    for _ in range(num):
        start_x = randint(MOB_SIZE // 2, WIDTH - MOB_SIZE // 2)
        start_y = randint(BAR_HEIGHT + MOB_SIZE // 2, HEIGHT - MOB_SIZE // 2)
        food = Mob(image_mouse, MOB_STEP, DESTINATION, start_x, start_y, WIDTH, HEIGHT, (0, BAR_HEIGHT))
        while True:
            hits = pygame.sprite.spritecollide(food, mobs, False, pygame.sprite.collide_circle)
            if hits:
                start_x = randint(MOB_SIZE // 2, WIDTH - MOB_SIZE // 2)
                start_y = randint(BAR_HEIGHT + MOB_SIZE // 2, HEIGHT - MOB_SIZE // 2)
                food.rect.x = start_x
                food.rect.y = start_y
                hits.clear()
            else:
                break
        all_sprites.add(food)
        foods.add(food)
        mobs.add(food)


def spawn_dogs(num):
    for _ in range(num):
        start_x = randint(MOB_SIZE // 2, WIDTH - MOB_SIZE // 2)
        start_y = randint(BAR_HEIGHT + MOB_SIZE // 2, HEIGHT - MOB_SIZE // 2)
        dog = Mob(image_dog, MOB_STEP, DESTINATION, start_x, start_y, WIDTH, HEIGHT, (0, BAR_HEIGHT))
        while True:
            hits = pygame.sprite.spritecollide(dog, mobs, False, pygame.sprite.collide_circle)
            if hits:
                start_x = randint(MOB_SIZE // 2, WIDTH - MOB_SIZE // 2)
                start_y = randint(BAR_HEIGHT + MOB_SIZE // 2, HEIGHT - MOB_SIZE // 2)
                dog.rect.x = start_x
                dog.rect.y = start_y
                hits.clear()
            else:
                break
        all_sprites.add(dog)
        dogs.add(dog)
        mobs.add(dog)


def spawn_trees(num):
    for _ in range(num):
        idx = randint(0, len(image_tree) - 1)
        start_x = randint(MOB_SIZE, WIDTH - MOB_SIZE)
        start_y = randint(BAR_HEIGHT + MOB_SIZE, HEIGHT - MOB_SIZE)
        tree = Wall(image_tree[idx], start_x, start_y, WIDTH, HEIGHT, (0, BAR_HEIGHT))
        all_sprites.add(tree)
        trees.add(tree)
        mobs.add(tree)


# взаимодействие игрока с мобами
def eat_mouse():
    eaten = pygame.sprite.spritecollide(cat, foods, True, pygame.sprite.collide_circle)
    for _ in eaten:
        cat.count += 1
        bar.star_fill(cat.count - 1, image_star)
    if eaten:
        cat.animation = True
        cat.status = 'eat'
        cat.start_animation = pygame.time.get_ticks()


def bite_dog():
    bitten = pygame.sprite.spritecollide(cat, dogs, True, pygame.sprite.collide_circle)
    for _ in bitten:
        cat.tries -= 1
        bar.player_tries_less(cat.tries, image_empty_catty)
        spawn_dogs(1)
    if bitten:
        cat.animation = True
        cat.status = 'bitten'
        cat.start_animation = pygame.time.get_ticks()


# проверка столкновений игрока с препятствиями и мобов друг с другом и препятствиями
def collide_mobs():
    for elem in mobs:
        new_list = mobs.copy()
        new_list.remove(elem)
        hits = pygame.sprite.spritecollide(elem, new_list, False, pygame.sprite.collide_circle)
        if hits:
            elem.change_direct()


def collide_player():
    hit_trees = pygame.sprite.spritecollide(cat, trees, False, pygame.sprite.collide_circle)
    if hit_trees:
        cat.rect.x = cat_x
        cat.rect.y = cat_y


# функции по работе с экраном и крупными событиями
def pause():
    global game_pause, running
    draw_text(screen, 'PAUSE', 100, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    while game_pause:
        clock.tick(FPS)
        for pause_event in pygame.event.get():
            if pause_event.type == pygame.QUIT:
                running = False
                game_pause = False
            if pause_event.type == pygame.KEYDOWN:
                if pause_event.key == pygame.K_SPACE:
                    game_pause = False


def win():
    global running
    if cat.count == PLAYER_STARS:
        waiting = True
        screen.fill((0, 0, 0))
        screen.blit(image_fon, image_fon_rect)
        draw_text(screen, 'YOU WIN!', 100, WIDTH // 2, HEIGHT // 2)
        draw_text(screen, 'Press SPACE to restart game', 50, WIDTH // 2, HEIGHT * 0.75)
        pygame.display.flip()
        while waiting:
            for pause_event in pygame.event.get():
                if pause_event.type == pygame.QUIT:
                    running = False
                    waiting = False
                if pause_event.type == pygame.KEYDOWN:
                    if pause_event.key == pygame.K_SPACE:
                        waiting = False
                        new_game()


def loose():
    global running
    if cat.tries == 0:
        waiting = True
        screen.fill((0, 0, 0))
        screen.blit(image_fon, image_fon_rect)
        draw_text(screen, 'GAME OVER', 100, WIDTH // 2, HEIGHT // 2)
        draw_text(screen, 'Press SPACE to restart game', 50, WIDTH // 2, HEIGHT * 0.75)
        pygame.display.flip()
        while waiting:
            for pause_event in pygame.event.get():
                if pause_event.type == pygame.QUIT:
                    running = False
                    waiting = False
                if pause_event.type == pygame.KEYDOWN:
                    if pause_event.key == pygame.K_SPACE:
                        waiting = False
                        new_game()


def start_screen():
    global running
    screen.fill((0, 0, 0))
    screen.blit(image_start, image_fon_rect)
    draw_text(screen, 'Press SPACE to start', 50, WIDTH // 2, HEIGHT * 0.15)
    pygame.display.flip()
    start = True
    while start:
        clock.tick(FPS)
        for pause_event in pygame.event.get():
            if pause_event.type == pygame.QUIT:
                running = False
                start = False
            if pause_event.type == pygame.KEYDOWN:
                if pause_event.key == pygame.K_SPACE:
                    start = False


def new_game():
    global all_sprites, foods, dogs, mobs, cat, bar, trees, running
    all_sprites = pygame.sprite.Group()
    foods = pygame.sprite.Group()
    dogs = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    trees = pygame.sprite.Group()
    spawn_trees(TREES_COUNT)
    bar = Bar(all_sprites, 0, 0, WIDTH, BAR_HEIGHT)
    bar.stars_locate(PLAYER_STARS, image_empty_star, all_sprites)
    bar.player_tries_locate(PLAYER_TRIES, image_catty, all_sprites)
    spawn_foods(MOUSE_COUNT)
    spawn_dogs(DOG_COUNT)
    cat = Player(all_sprites, image_cat, PLAYER_STEP, WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT, (0, BAR_HEIGHT))
    pygame.sprite.spritecollide(cat, trees, True)
    cat.tries = PLAYER_TRIES


# вспомогательные функции
def draw_text(surf, text, size, x, y, color=(255, 200, 0)):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surf.blit(text_surface, text_rect)


def player_animation():
    if cat.animation and cat.status == 'bitten':
        cat.change_image(image_bitten_cat, AN_TIME)
    elif cat.animation and cat.status == 'eat':
        cat.change_image(image_eat_cat, AN_TIME)


def dog_animation():
    pass


def mouse_animation():
    pass


# инициализация основного окна
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Square')
clock = pygame.time.Clock()

# загрузка картинок
font_name = pygame.font.match_font('segoe script', True)
image_cat = pygame.image.load('img/cat.png').convert_alpha()
image_bitten_cat = pygame.image.load('img/bitten_cat.png').convert_alpha()
image_eat_cat = pygame.image.load('img/eat_cat.png').convert_alpha()
image_mouse = pygame.image.load('img/mouse.png').convert_alpha()
image_star = pygame.image.load('img/mousy.png').convert_alpha()
image_empty_star = pygame.image.load('img/empty_mousy.png').convert_alpha()
image_catty = pygame.image.load('img/catty.png').convert_alpha()
image_empty_catty = pygame.image.load('img/empty_catty.png').convert_alpha()
image_dog = pygame.image.load('img/dog.png').convert_alpha()
image_fon = pygame.image.load('img/fon.png').convert_alpha()
image_start = pygame.image.load('img/start.png').convert_alpha()
image_fon_rect = image_fon.get_rect()
image_doghouse = pygame.image.load('img/doghouse.png').convert_alpha()
trees_list = ['tree1.png', 'tree2.png', 'tree3.png', 'tree4.png', 'tree5.png']
image_tree = [pygame.image.load(os.path.join('img/', img)).convert_alpha() for img in trees_list]

# группы спрайтов
all_sprites = pygame.sprite.Group()
foods = pygame.sprite.Group()
dogs = pygame.sprite.Group()
mobs = pygame.sprite.Group()
trees = pygame.sprite.Group()

# создание спрайтов
spawn_trees(TREES_COUNT)
bar = Bar(all_sprites, 0, 0, WIDTH, BAR_HEIGHT)
bar.stars_locate(PLAYER_STARS, image_empty_star, all_sprites)
bar.player_tries_locate(PLAYER_TRIES, image_catty, all_sprites)
spawn_foods(MOUSE_COUNT)
spawn_dogs(DOG_COUNT)
cat = Player(all_sprites, image_cat, PLAYER_STEP, WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT, (0, BAR_HEIGHT))
pygame.sprite.spritecollide(cat, trees, True)
cat.tries = PLAYER_TRIES

game_pause = False
running = True

start_screen()

while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)

    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_pause = True
                pause()

    # Обновление
    cat_x = cat.rect.x
    cat_y = cat.rect.y
    all_sprites.update()
    eat_mouse()
    bite_dog()
    collide_mobs()
    collide_player()
    player_animation()
    loose()
    win()

    # Рендеринг
    screen.fill((0, 0, 0))
    screen.blit(image_fon, image_fon_rect)
    all_sprites.draw(screen)

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
