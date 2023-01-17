import pygame
import os
import sys

SCREEN_SIZE = [1540, 810]
tile_width = tile_height = 30


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_images = {
    'S': load_image('wall.png'),
    '*': load_image('grass.png'),
    'W': load_image('river.png'),
    'K': load_image('bush1.png'),
    'k': load_image('bush2.png'),
    'D': load_image('home1.png'),
    'd': load_image('home2.png'),
    'Z': load_image('mine.png'),
    'M': load_image('bridge.png'),
    's': load_image('wall1.png')
}
player_image = {
    '1': load_image('1.png'),
    '2': load_image('2.png'),
    '3': load_image('3.png'),
    '4': load_image('4.png'),
    '5': load_image('3.png')
}
about_image = {
    'inform': load_image('inform.png'),
    'pause': load_image('pause.png'),
    'volume_f': load_image('volume false.png'),
    'volume_t': load_image('volume true.png'),
    'icon': load_image('icon.png')
}


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('*')
    return level_map


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 95, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image['1']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level_1(level):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'W' or level[y][x] == 'M':
                Tile('W', x, y)
            else:
                Tile('*', x, y)
    return x, y


def generate_level_2(level):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'S':
                Tile('S', x, y)
            if level[y][x] == 's':
                Tile('s', x, y)
            if level[y][x] == 'M':
                Tile('M', x - 1, y)
            if level[y][x] == 'Z':
                Tile('Z', x, y)
            if level[y][x] == 'K':
                Tile('K', x, y)
            if level[y][x] == 'k':
                Tile('k', x, y)
            if level[y][x] == 'D':
                Tile('D', x, y)
            if level[y][x] == 'd':
                Tile('d', x, y)
    return x, y


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
    size = SCREEN_SIZE
    screen = pygame.display.set_mode(size)
    screen.fill((187, 232, 247))
    level_x, level_y = generate_level_1(load_level('Поле 1.txt'))
    level_x1, level_y1 = generate_level_2(load_level('Поле 1.txt'))
    #board = Field(45, 23)
    #board.set_view(95, 1, 30)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.draw(screen)
        #board.render(screen)
        pygame.display.flip()
    pygame.quit()