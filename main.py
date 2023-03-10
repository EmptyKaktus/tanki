import pygame
import os
import sys
import time
import random

pygame.mixer.init()

SCREEN_SIZE = [1350, 690]
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
FPS = 110


hpr_spisok = []
hpv_spisok = []
keys = []

tile_width = tile_height = 30
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
tank1 = pygame.sprite.Group()
tank2 = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
mine_group = pygame.sprite.Group()
river_group = pygame.sprite.Group()

bridge_group = pygame.sprite.Group()
home_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
hp_r = pygame.sprite.Group()
hp_v = pygame.sprite.Group()


def load_image(name, papka, colorkey=None):
    fullname = os.path.join(f'data/{papka}', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "data/levels/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('*')
    return level_map


def load_music(filename):
    filename = "data/music/" + filename
    #
    sound = pygame.mixer.Sound(filename)

    return sound


tile_images = {
    'S': load_image('wall.png', 'tiels'),
    '*': load_image('grass.png', 'tiels'),
    'W': load_image('river.png', 'tiels'),
    'D': load_image('home1.png', 'tiels'),
    'd': load_image('home2.png', 'tiels'),
    'Z': load_image('mine.png', 'tiels'),
    'M': load_image('bridge.png', 'tiels'),
    'b': load_image('bullet.png', 'tiels'),
    'b1': load_image('bullet1.png', 'tiels'),
    'crater': load_image('crater.png', 'tiels')
}

tanks_images = {
    '1': load_image('1.png', 'players'),
    '2': load_image('2.png', 'players'),
    '1c': load_image('1-copy.png', 'players'),
    '2c': load_image('2-copy.png', 'players')
}

about_images = {
    'red': load_image('red.png', 'about'),
    'violet': load_image('violet.png', 'about'),
}

music = {
    'boom': load_music('бум.ogg'),
    'popal': load_music('есть-пробитиеogg.ogg'),
    'go': load_music('звук движения.ogg'),
    'piu': load_music('выстрел.ogg'),
    'win': load_music('уничтожен.ogg'),
    'фон': load_music('фон.ogg')
}

# функция для связывания кнопку старт из меню с самой игрой


def go():
    global keys
    global k
    global start1
    music['фон'].play(-1)
    pygame.init()
    generate_level_1(load_level('Поле 1.txt'))
    generate_level_2(load_level('Поле 1.txt'))
    width1, height1 = SCREEN_SIZE
    Border(-1, -1, width1, -1)
    Border(-1, height1 + 1, width1 - -1, height1 - -1)
    Border(-1, -1, -1, height1 - 5)
    Border(width1 - -1, -1, width1 - -1, height1 - -1)
    board = Field(45, 23)
    board.set_view(1, 1, 30)
    x = 255
    for i in range(hp_tank1):
        hp = HPR(x, 5)
        x += 23
        hpr_spisok.append(hp)
    x = SCREEN_SIZE[0] - 367
    for i in range(hp_tank2):
        hp = HPV(x, SCREEN_SIZE[1] - 24)
        x += 23
        hpv_spisok.append(hp)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if k:
            start1 = time.time()
            while True:
                if time.time() - start1 >= 3:
                    break
            game()
            running = False
        keys = pygame.key.get_pressed()
        all_sprites.draw(screen)
        all_sprites.update()
        # board.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


# загрузить изображения кнопок
start_img = load_image('start_btn.png', 'menu')
exit_img = load_image('exit_btn.png', 'menu')
mg1 = load_image('n.png', 'menu')
mg2 = load_image('p.png', 'menu')
mg3 = load_image('n.png', 'menu')
mg4 = load_image('p.png', 'menu')
mg5 = load_image('n.png', 'menu')
mg6 = load_image('p.png', 'menu')
mg7 = load_image('n.png', 'menu')

# класс кнопка


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        # получить положение мыши
        pos = pygame.mouse.get_pos()

        # проверить условия наведения и нажатия
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # нарисовать кнопку на экране
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action


# создать экземпляры кнопок
start_button = Button(200, 400, start_img, 0.5)
exit_button = Button(800, 400, exit_img, 0.5)
st1_button = Button(100, 600, mg1, 0.5)
st2_button = Button(500, 600, mg2, 0.5)
st3_button = Button(100, 600, mg3, 0.5)
st4_button = Button(500, 600, mg4, 0.5)
st5_button = Button(100, 600, mg5, 0.5)
st6_button = Button(500, 600, mg6, 0.5)
st7_button = Button(100, 600, mg7, 0.5)

size1 = width, height = 1280, 690
screen1 = pygame.display.set_mode(size1)

# класс для создания окна заставки


class Mountain(pygame.sprite.Sprite):
    image = load_image("cv.jpg", 'menu')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height

# класс для снежинок


class Landing(pygame.sprite.Sprite):
    image = load_image("1111.png", 'menu')

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Landing.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        self.rect = self.rect.move(0, 1)

# функция игра


def game():
    global k
    global hp_tank1
    global hp_tank2
    im = load_image('image.png', 'menu')
    k = False
    hp_tank1 = 5
    hp_tank2 = 5
    run = True
    while run:
        screen1.blit(im, (0, 0))
        if start_button.draw(screen1):
            go()
            run = False
        if exit_button.draw(screen1):
            run = False
            rus()

        for event1 in pygame.event.get():
            # quit game
            if event1.type == pygame.QUIT:
                run = False
                sys.exit()
        pygame.display.flip()
        pygame.display.update()

# таймер снежинок для окна заставки


def main():
    pygame.init()
    start = time.time()
    Mountain()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
        if time.time() - start >= 8:
            run = False
            game()

        Landing((random.randrange(1200), random.randrange(200)))
        screen.fill('black')
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(100)
        pygame.display.flip()

# окно  правил игры на русском


def rus():
    bg_color = (0, 0, 0)
    screen1.fill(bg_color)
    rus = load_image('ccc.png', 'menu')
    zzz = load_image('20.png', 'menu')
    tu = load_image('ru.jpg', 'menu')
    run = True
    while run:
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                run = False
        screen1.blit(rus, (0, 0))
        screen1.blit(zzz, (250, 150))
        screen1.blit(tu, (20, 20))
        if st1_button.draw(screen1):
            game()
            run = False
        if st2_button.draw(screen1):
            ing()
            run = False
        clock.tick(100)
        pygame.display.flip()

# окно правил игры на английском


def ing():
    bg_color = (19, 17, 26)
    screen1.fill(bg_color)
    asd = load_image('37.png', 'menu')
    tu = load_image('an.png', 'menu')
    runn = True
    while runn:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runn = False
        screen1.blit(asd, (250, 150))
        screen1.blit(tu, (20, 20))
        if st3_button.draw(screen1):
            rus()
            runn = False
        if st4_button.draw(screen1):
            tyr()
            runn = False
        clock.tick(100)
        pygame.display.flip()

# окно правил игры на турецком


def tyr():
    bg_color = (19, 17, 26)
    screen1.fill(bg_color)
    rf = load_image('38.png', 'menu')
    tu = load_image('tu.jpg', 'menu')

    run = True
    while run:
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                run = False

        screen1.blit(rf, (250, 150))
        screen1.blit(tu, (20, 20))

        if st5_button.draw(screen1):
            ing()
            run = False
        if st6_button.draw(screen1):
            rus()
            run = False
        clock.tick(100)
        pygame.display.flip()

# жизни танков


def hp_tank(tank, hp):
    global hp_tank1, hp_tank2
    if tank == 1:
        hp_tank1 -= hp
    else:
        hp_tank2 -= hp
    if hp_tank1 <= 0 or hp_tank2 <= 0:
        music['win'].play()

# окно победы красного или фиолетового танка


def draw_win(color):
    global k
    font = pygame.font.Font(None, 50)
    if color == 'Violet':
        text = font.render(f"{color} WIN", True, (135, 23, 199))
    else:
        text = font.render(f"{color} WIN", True, (255, 0, 0))
    pygame.draw.rect(screen, (0, 0, 0),
                     (width // 2 - 150, height // 2 - 100, width // 2 - 350, height // 2 - 150))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))

    if color == 'Violet':
        pygame.draw.rect(screen, (135, 23, 199), (text_x - 10, text_y - 10,
                                                  text_w + 20, text_h + 20), 1)
    elif color == 'Red':
        pygame.draw.rect(screen, (255, 0, 0), (text_x - 10, text_y - 10,
                                               text_w + 20, text_h + 20), 1)
    music['фон'].stop()


# Создаем класс клеточек и добавляем его в tieles_group
class Tile(pygame.sprite.Sprite):
    papka = 'tiels'

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# Создаем класс первого танка и добавляем его в player_group
class Tank1(pygame.sprite.Sprite):
    papka = 'players'

    def __init__(self, color, pos_x, pos_y, direct, keyList):
        super().__init__(tank1, all_sprites)
        self.color = color
        self.direct = direct
        self.moveSpeed = 1
        self.image = tanks_images['1']
        self.image = pygame.transform.flip(self.image, False, True)
        self.name = '1'
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * 30
        self.rect.y = pos_y * 30
        self.q1, self.q2, self.q3, self.q4 = True, True, True, True

        self.bulletDamage = 1
        self.bulletSpeed = 5
        self.shotTimer = 0
        self.shotDelay = 60
        self.hp = 5

        # расписываем кнопки управления
        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]

    def update(self):
        # проверяем есть ли соприкосновения с другими объектами
        wall = pygame.sprite.spritecollideany(self, wall_group)
        river = pygame.sprite.spritecollideany(self, river_group)
        bridge = pygame.sprite.spritecollideany(self, bridge_group)
        home = pygame.sprite.spritecollideany(self, home_group)
        horizontal_bord = pygame.sprite.spritecollideany(self, horizontal_borders)
        vertical_bord = pygame.sprite.spritecollideany(self, vertical_borders)
        tank = pygame.sprite.spritecollideany(self, tank2)

        # Расписываем нажатия кнопок и проверку на соприкосновения
        if keys[self.keyLEFT]:
            if self.direct != 3:
                self.image = tanks_images[self.name]
                self.image = pygame.transform.flip(self.image, True, False)
                self.mask = pygame.mask.from_surface(self.image)
                self.direct = 3
            if (wall or river or home or horizontal_bord or vertical_bord or tank) and not bridge:
                self.q3 = False
                self.rect.x += self.moveSpeed
            if self.q3:
                self.rect.x -= self.moveSpeed
                self.q1 = True
                self.q4 = True
                self.q2 = True
                self.q3 = True
        elif keys[self.keyRIGHT]:
            if self.direct != 1:
                self.image = tanks_images[self.name]
                self.image = pygame.transform.flip(self.image, False, True)
                self.mask = pygame.mask.from_surface(self.image)
                self.direct = 1
            if (wall or river or home or horizontal_bord or vertical_bord or tank) and not bridge:
                self.q1 = False
                self.rect.x -= self.moveSpeed
            if self.q1:
                self.rect.x += self.moveSpeed
                self.q3 = True
                self.q4 = True
                self.q1 = True
                self.q2 = True
        elif keys[self.keyUP]:
            if self.direct != 2:
                self.image = tanks_images[f'{self.name}c']
                self.image = pygame.transform.flip(self.image, True, False)
                self.mask = pygame.mask.from_surface(self.image)
                self.direct = 2
            if (wall or river or home or horizontal_bord or vertical_bord or tank) and not bridge:
                self.q2 = False
                self.rect.y += self.moveSpeed
            if self.q2:
                self.rect.y -= self.moveSpeed
                self.q4 = True
                self.q1 = True
                self.q2 = True
                self.q3 = True
        elif keys[self.keyDOWN]:
            self.image = tanks_images[f'{self.name}c']
            self.direct = 2
            if self.direct != 4:
                self.image = pygame.transform.flip(self.image, False, True)
                self.mask = pygame.mask.from_surface(self.image)
                self.direct = 4
            if (wall or river or home or horizontal_bord or vertical_bord or tank) and not bridge:
                self.q4 = False
                self.rect.y -= self.moveSpeed
            if self.q4:
                self.rect.y += self.moveSpeed
                self.q2 = True
                self.q1 = True
                self.q4 = True
                self.q3 = True

        if keys[self.keySHOT] and self.shotTimer == 0:
            Bullet(self.rect.x, self.rect.y, self.bulletSpeed, self.direct)
            self.shotTimer = self.shotDelay
            music['piu'].play()

        if self.shotTimer > 0:
            self.shotTimer -= 1


# Создаем класс второго танка(игрока) и добавляем его в player_group
class Tank2(pygame.sprite.Sprite):
    papka = 'players'

    def __init__(self, color, pos_x, pos_y, direct, keyList):
        super().__init__(tank2, all_sprites)
        self.color = color
        self.direct = direct
        self.moveSpeed = 1
        self.image = tanks_images['2']
        self.image = pygame.transform.flip(self.image, True, True)
        self.name = '2'
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * 30
        self.rect.y = pos_y * 30
        self.q1, self.q2, self.q3, self.q4 = True, True, True, True

        self.bulletDamage = 1
        self.bulletSpeed = 5
        self.shotTimer = 0
        self.shotDelay = 60

        # расписываем кнопки управления
        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]

    def update(self):
        # проверяем есть ли соприкосновения с другими объектами
        wall = pygame.sprite.spritecollideany(self, wall_group)
        river = pygame.sprite.spritecollideany(self, river_group)
        bridge = pygame.sprite.spritecollideany(self, bridge_group)
        home = pygame.sprite.spritecollideany(self, home_group)
        horizontal_bord = pygame.sprite.spritecollideany(self, horizontal_borders)
        vertical_bord = pygame.sprite.spritecollideany(self, vertical_borders)
        tank = pygame.sprite.spritecollideany(self, tank1)

        # Расписываем нажатия кнопок и проверку на соприкосновения
        if keys[self.keyLEFT]:
            if self.direct != 3:
                self.image = tanks_images[self.name]
                self.image = pygame.transform.flip(self.image, True, False)
                self.mask = pygame.mask.from_surface(self.image)
                self.direct = 3
            if (wall or river or home or horizontal_bord or vertical_bord or tank) and not bridge:
                self.q3 = False
                self.rect.x += self.moveSpeed
            if self.q3:
                self.rect.x -= self.moveSpeed
                self.q1 = True
                self.q4 = True
                self.q2 = True
                self.q3 = True
        elif keys[self.keyRIGHT]:
            if self.direct != 1:
                self.image = tanks_images[self.name]
                self.image = pygame.transform.flip(self.image, False, True)
                self.mask = pygame.mask.from_surface(self.image)
                self.direct = 1
            if (wall or river or home or horizontal_bord or vertical_bord or tank) and not bridge:
                self.q1 = False
                self.rect.x -= self.moveSpeed
            if self.q1:
                self.rect.x += self.moveSpeed
                self.q3 = True
                self.q4 = True
                self.q1 = True
                self.q2 = True
        elif keys[self.keyUP]:
            if self.direct != 2:
                self.image = tanks_images[f'{self.name}c']
                self.image = pygame.transform.flip(self.image, True, False)
                self.mask = pygame.mask.from_surface(self.image)
                self.direct = 2
            if (wall or river or home or horizontal_bord or vertical_bord or tank) and not bridge:
                self.q2 = False
                self.rect.y += self.moveSpeed
            if self.q2:
                self.rect.y -= self.moveSpeed
                self.q4 = True
                self.q1 = True
                self.q2 = True
                self.q3 = True
        elif keys[self.keyDOWN]:
            self.image = tanks_images[f'{self.name}c']
            self.direct = 2
            if self.direct != 4:
                self.image = pygame.transform.flip(self.image, False, True)
                self.mask = pygame.mask.from_surface(self.image)
                self.direct = 4
            if (wall or river or home or horizontal_bord or vertical_bord or tank) and not bridge:
                self.q4 = False
                self.rect.y -= self.moveSpeed
            if self.q4:
                self.rect.y += self.moveSpeed
                self.q2 = True
                self.q1 = True
                self.q4 = True
                self.q3 = True

        if keys[self.keySHOT] and self.shotTimer == 0:
            Bullet(self.rect.x, self.rect.y, self.bulletSpeed, self.direct)
            self.shotTimer = self.shotDelay
            music['piu'].play()

        if self.shotTimer > 0:
            self.shotTimer -= 1

# класс пуля для определения поподания снаряда,снятия очков жизни и работы музыки при поподании


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, direct):
        super().__init__(bullet_group, all_sprites)
        self.speed = speed
        self.direct = direct
        if self.direct == 1:
            self.image = tile_images['b']
            self.x = x + 31
            self.y = y + 15
        elif self.direct == 2:
            self.image = tile_images['b1']
            self.x = x + 15
            self.y = y - 8
        elif self.direct == 3:
            self.image = tile_images['b']
            self.x = x - 8
            self.y = y + 15
        else:
            self.image = tile_images['b1']
            self.x = x + 15
            self.y = y + 31
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        wall = pygame.sprite.spritecollideany(self, wall_group)
        home = pygame.sprite.spritecollideany(self, home_group)
        tank_1 = pygame.sprite.spritecollideany(self, tank1)
        tank_2 = pygame.sprite.spritecollideany(self, tank2)
        if tank_1:
            hp_tank(1, 1)
            for i in bullet_group:
                if (self.rect.x <= i.rect.x <= self.rect.x + 30 and self.rect.y <= i.rect.y <= self.rect.y + 30) or \
                    (
                        self.rect.x <= i.rect.x + 7 <= self.rect.x + 30 and self.rect.y <= i.rect.y + 7 <= self.rect.y + 30):
                    i.kill()
            hpr_spisok[-1].kill()
            del hpr_spisok[-1]
            music['popal'].play()
        if tank_2:
            hp_tank(2, 1)
            for i in bullet_group:
                if (self.rect.x <= i.rect.x <= self.rect.x + 30 and self.rect.y <= i.rect.y <= self.rect.y + 30) or \
                    (
                        self.rect.x <= i.rect.x + 7 <= self.rect.x + 30 and self.rect.y <= i.rect.y + 7 <= self.rect.y + 30):
                    i.kill()
            hpv_spisok[-1].kill()
            del hpv_spisok[-1]
            music['popal'].play()
        if wall:
            for i in wall_group:
                if (i.rect.x <= self.rect.x <= i.rect.x + 30 and i.rect.y <= self.rect.y <= i.rect.y + 30) or \
                        (i.rect.x <= self.rect.x + 7 <= i.rect.x + 30 and i.rect.y <= self.rect.y + 7 <= i.rect.y + 30):
                    i.kill()
            for i in bullet_group:
                if (self.rect.x <= i.rect.x <= self.rect.x + 30 and self.rect.y <= i.rect.y <= self.rect.y + 30) or \
                    (
                        self.rect.x <= i.rect.x + 7 <= self.rect.x + 30 and self.rect.y <= i.rect.y + 7 <= self.rect.y + 30):
                    i.kill()
        if home:
            for i in bullet_group:
                if (self.rect.x <= i.rect.x <= self.rect.x + 54 and self.rect.y <= i.rect.y <= (
                        i.rect.y + 42 or i.rect.y + 73)) or \
                        (self.rect.x <= i.rect.x + 7 <= self.rect.x + 54 and self.rect.y <= i.rect.y + 7 <= (
                            i.rect.y + 42 or i.rect.y + 73)):
                    i.kill()
        if not (home and tank_1 and tank_2 and wall):
            if self.direct == 1:
                self.rect.x += self.speed
            elif self.direct == 2:
                self.rect.y -= self.speed
            elif self.direct == 3:
                self.rect.x -= self.speed
            else:
                self.rect.y += self.speed


# Создаем класс мины и добавляем его в mine_group
class Mine(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(mine_group, all_sprites)
        self.image = tile_images['Z']
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y

    # действия мины
    def update(self):
        global k
        tank_1 = pygame.sprite.spritecollideany(self, tank1)
        tank_2 = pygame.sprite.spritecollideany(self, tank2)
        if tank_1:
            hp_tank(1, 2)
            for i in mine_group:
                if (self.rect.x <= i.rect.x <= self.rect.x + 20 and self.rect.y <= i.rect.y <= self.rect.y + 20) or \
                        (self.rect.x <= i.rect.x + 30 <= self.rect.x + 20 and self.rect.y <= i.rect.y + 30 <= self.rect.y + 20):
                    i.kill()
            for i in range(2):
                if len(hpr_spisok) > 0:
                    hpr_spisok[-1].kill()
                    del hpr_spisok[-1]
            music['boom'].play()
        if tank_2:
            hp_tank(2, 2)
            for i in mine_group:
                if (self.rect.x <= i.rect.x <= self.rect.x + 20 and self.rect.y <= i.rect.y <= self.rect.y + 20) or \
                        (self.rect.x <= i.rect.x + 30 <= self.rect.x + 20 and self.rect.y <= i.rect.y + 30 <= self.rect.y + 20):
                    i.kill()
            for i in hp_v:
                if i.rect.x == (SCREEN_SIZE[0] - 367) + (3 * (hp_tank2 - 1)) + (hp_tank2 * 20):
                    i.kill()
            for i in range(2):
                if len(hpv_spisok) > 0:
                    hpv_spisok[-1].kill()
                    del hpv_spisok[-1]
            music['boom'].play()
        if hp_tank1 <= 0:
            for i in tank1:
                i.kill()
            draw_win('Violet')
            k = True
        elif hp_tank2 <= 0:
            for i in tank2:
                i.kill()
            draw_win('Red')
            k = True


# Создаем класс стены(препятствия) и добавляем его в wall_group
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(wall_group, all_sprites)
        self.image = tile_images['S']
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y


# Создаем класс реки и добавляем его в river_group
class River(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(river_group, all_sprites)
        self.image = tile_images['W']
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)
        self.mask = pygame.mask.from_surface(self.image)


# Создаем класс моста и добавляем его в bridge_group
class Bridge(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(bridge_group, all_sprites)
        self.image = tile_images['M']
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)
        self.mask = pygame.mask.from_surface(self.image)


# Создаем класс дома и добавляем его в home_group
class Home(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__(home_group, all_sprites)
        self.image = tile_images[name]
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)
        self.mask = pygame.mask.from_surface(self.image)
        self.image1 = tile_images[name]
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)
        self.mask = pygame.mask.from_surface(self.image1)

# класс для ограничения границ


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)

# класс жизни красного танка


class HPR(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(hp_r, all_sprites)
        self.x = x
        self.y = y
        self.image = about_images['red']
        self.rect = self.image.get_rect().move(self.x, self.y)

# класс жизни фиолетового танка


class HPV(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(hp_v, all_sprites)
        self.x = x
        self.y = y
        self.image = about_images['violet']
        self.rect = self.image.get_rect().move(self.x, self.y)


# Генерируем траву, мост и реку
def generate_level_1(level):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'W' or level[y][x] == 'M':
                River(x, y)
            if level[y][x] == 'M':
                Bridge(x, y)
            if level[y][x] == 'd' or level[y][x] == 'D' or level[y][x] == 'S' or level[y][x] == 'Z' or level[y][
                    x] == '*' or level[y][x] == 'T' or level[y][x] == 't':
                Tile('*', x, y)
    return x, y


# Генерируем все остальное
def generate_level_2(level):
    player_1, player_2, x, y = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'S':
                Wall(x, y)
            elif level[y][x] == 'Z':
                Mine(x, y)
            elif level[y][x] == 'K':
                Tile('K', x, y)
            elif level[y][x] == 'k':
                Tile('k', x, y)
            elif level[y][x] == 'D':
                Home('D', x, y)
            elif level[y][x] == 'd':
                Home('d', x, y)
            elif level[y][x] == 'T':
                player_1 = Tank1('blue', x, y, 1, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
            elif level[y][x] == 't':
                player_2 = Tank2('red', x, y, 3,
                                 (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP_ENTER)
                                 )
    return player_1, player_2, x, y


# клетчатое поле для разметки
class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 10

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, 'black', (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)


if __name__ == '__main__':
    main()
