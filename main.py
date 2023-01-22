import pygame
import os
import sys

SCREEN_SIZE = [1350, 690]
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
tile_width = tile_height = 30
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
mine_group = pygame.sprite.Group()
river_group = pygame.sprite.Group()
bridge_group = pygame.sprite.Group()
home_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
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


papka = 'tiels'
tile_images = {
    'S': load_image('wall.png'),
    '*': load_image('grass.png'),
    'W': load_image('river.png'),
    'D': load_image('home1.png'),
    'd': load_image('home2.png'),
    'Z': load_image('mine.png'),
    'M': load_image('bridge.png'),
}

papka = 'players'
tanks_images = {
    '1': load_image('1.png'),
    '2': load_image('2.png'),
    '3': load_image('3.png'),
    '4': load_image('4.png'),
    '1c': load_image('1-copy.png'),
    '2c': load_image('2-copy.png'),
    '3c': load_image('3-copy.png'),
    '4c': load_image('4-copy.png'),
}

papka = 'about'
about_image = {
    'inform': load_image('inform.png'),
    'pause': load_image('pause.png'),
    'volume_f': load_image('volume false.png'),
    'volume_t': load_image('volume true.png'),
}


class Tile(pygame.sprite.Sprite):
    papka = 'tiels'

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Tank1(pygame.sprite.Sprite):
    papka = 'players'

    def __init__(self, color, pos_x, pos_y, direct, keyList):
        super().__init__(player_group, all_sprites)
        self.color = color
        self.direct = direct
        self.moveSpeed = 1
        self.image = tanks_images['1']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * 30
        self.rect.y = pos_y * 30
        self.q1, self.q2, self.q3, self.q4 = True, True, True, True

        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]

    def update(self):
        wall = pygame.sprite.spritecollideany(self, wall_group)
        river = pygame.sprite.spritecollideany(self, river_group)
        bridge = pygame.sprite.spritecollideany(self, bridge_group)
        if keys[self.keyLEFT]:
            if self.direct != 3:
                self.image = tanks_images['1']
                self.mask = pygame.mask.from_surface(self.image)
                self.image = pygame.transform.flip(self.image, True, True)
                self.direct = 3
            if (wall or river) and not bridge:
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
                self.image = tanks_images['1']
                self.mask = pygame.mask.from_surface(self.image)
                self.image = pygame.transform.flip(self.image, False, True)
                self.direct = 1
            if (wall or river) and not bridge:
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
                self.image = tanks_images['1c']
                self.mask = pygame.mask.from_surface(self.image)
                self.direct = 2
            if (wall or river) and not bridge:
                self.q2 = False
                self.rect.y += self.moveSpeed
            if self.q2:
                self.rect.y -= self.moveSpeed
                self.q4 = True
                self.q1 = True
                self.q2 = True
                self.q3 = True
        elif keys[self.keyDOWN]:
            self.image = tanks_images['1c']
            self.direct = 2
            if self.direct != 4:
                self.mask = pygame.mask.from_surface(self.image)
                self.image = pygame.transform.flip(self.image, False, True)
                self.direct = 4
            if (wall or river) and not bridge:
                self.q4 = False
                self.rect.y -= self.moveSpeed
            if self.q4:
                self.rect.y += self.moveSpeed
                self.q2 = True
                self.q1 = True
                self.q4 = True
                self.q3 = True


class Tank2(pygame.sprite.Sprite):
    papka = 'players'

    def __init__(self, color, pos_x, pos_y, direct, keyList):
        super().__init__(player_group, all_sprites)
        self.color = color
        self.direct = direct
        self.moveSpeed = 1
        self.image = tanks_images['1']
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * 30
        self.rect.y = pos_y * 30

        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]

    def update(self, ):
        if keys[self.keyLEFT]:
            if self.direct != 3:
                self.image = tanks_images['1']
                self.image = pygame.transform.flip(self.image, True, True)
                self.direct = 3
            self.rect.x -= self.moveSpeed
        elif keys[self.keyRIGHT]:
            if self.direct != 1:
                self.image = tanks_images['1']
                self.image = pygame.transform.flip(self.image, False, True)
                self.direct = 1
            self.rect.x += self.moveSpeed
        elif keys[self.keyUP]:
            if self.direct != 2:
                self.image = tanks_images['1c']
                self.direct = 2
            self.rect.y -= self.moveSpeed
        elif keys[self.keyDOWN]:
            self.image = tanks_images['1c']
            self.direct = 2
            if self.direct != 4:
                self.image = pygame.transform.flip(self.image, False, True)
                self.direct = 4
            self.rect.y += self.moveSpeed


class Mine(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(mine_group, all_sprites)
        pass

    def boom(self):
        pass


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(wall_group, all_sprites)
        self.image = tile_images['S']
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)
        self.mask = pygame.mask.from_surface(self.image)

    def crash(self):
        pass


class River(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(river_group, all_sprites)
        self.image = tile_images['W']
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)
        self.mask = pygame.mask.from_surface(self.image)


class Bridge(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(bridge_group, all_sprites)
        self.image = tile_images['M']
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)
        self.mask = pygame.mask.from_surface(self.image)


# Генерируем тарву и реку
def generate_level_1(level):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'W' or level[y][x] == 'M':
                River(x, y)
            if level[y][x] == 'M':
                Bridge(x, y)
            if level[y][x] == 'd' or level[y][x] == 'D' or level[y][x] == 'S' or level[y][x] == 'Z' or level[y][x] == '*' or level[y][x] == 'T':
                Tile('*', x, y)
    return x, y


# Генерируем все остальное
def generate_level_2(level):
    player_1, player_2, x, y, wall, mine = None, None, None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'S':
                wall = Wall(x, y)
            elif level[y][x] == 'Z':
                Tile('Z', x, y)
            elif level[y][x] == 'K':
                Tile('K', x, y)
            elif level[y][x] == 'k':
                Tile('k', x, y)
            elif level[y][x] == 'D':
                Tile('D', x, y)
            elif level[y][x] == 'd':
                Tile('d', x, y)
            elif level[y][x] == 'T':
                player_1 = Tank1('blue', x, y, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
    return player_1, player_2, wall, mine, x, y


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


class About:
    def __init__(self):
        pass

    def pause(self):
        pass

    def volume(self):
        pass

    def information(self):
        pass


if __name__ == '__main__':
    pygame.init()
    level_x, level_y = generate_level_1(load_level('Поле 1.txt'))
    player1, player2, wall, mine, level_x1, level_y1 = generate_level_2(load_level('Поле 1.txt'))
    board = Field(45, 23)
    board.set_view(1, 1, 30)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        all_sprites.draw(screen)
        all_sprites.update()
        # board.render(screen)
        pygame.display.flip()
    pygame.quit()