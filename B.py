import pygame
import random
import sys
import os
import time


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
    return image


pygame.init()
#загрузить изображения кнопок
start_img = load_image('start_btn.png')
exit_img = load_image('exit_btn.png')
mg1 = load_image('n.png')
mg2 = load_image('p.png')
mg3 = load_image('n.png')
mg4 = load_image('p.png')
mg5 = load_image('n.png')
mg6 = load_image('p.png')
mg7 = load_image('n.png')

size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()


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
		#получить положение мыши
		pos = pygame.mouse.get_pos()

		#проверить условия наведения и нажатия
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#нарисовать кнопку на экране
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action


#создать экземпляры кнопок
start_button = Button(200, 400, start_img, 0.5)
exit_button = Button(800, 400 , exit_img, 0.5)
st1_button = Button(100, 600, mg1, 0.5)
st2_button = Button(500, 600, mg2, 0.5)
st3_button = Button(100, 600, mg3, 0.5)
st4_button = Button(500, 600, mg4, 0.5)
st5_button = Button(100, 600, mg5, 0.5)
st6_button = Button(500, 600, mg6, 0.5)
st7_button = Button(100, 600, mg7, 0.5)

class Mountain(pygame.sprite.Sprite):
    image = load_image("cv.jpg")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height


class Landing(pygame.sprite.Sprite):
    image = load_image("1111.png")

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Landing.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        self.rect = self.rect.move(0, 1)


def game():
    im = load_image('image.png')

    run = True
    while run:

        screen.blit(im, (0, 0))

        if start_button.draw(screen):
            print('START')
        if exit_button.draw(screen):
            print('INFO')
            run = False
            qwe()
        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                run = False
        pygame.display.flip()

        pygame.display.update()


def main():
    pygame.init()
    start = time.time()

    Mountain()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
        if time.time() - start >= 8:
            running = False
            game()

        Landing((random.randrange(1200), random.randrange(200)))
        screen.fill('black')
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(100)
        pygame.display.flip()


def qwe():
    bg_color = (0, 0, 0)
    screen.fill(bg_color)
    qwe = load_image('ccc.png')
    zzz = load_image('20.png')
    tu = load_image('ru.jpg')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

        screen.blit(qwe, (0, 0))
        screen.blit(zzz, (250, 150))
        screen.blit(tu, (20, 20))
        if st1_button.draw(screen):
            game()
            running = False
        if st2_button.draw(screen):
            asd()
            running = False
        clock.tick(100)
        pygame.display.flip()


def asd():

    bg_color = (19, 17, 26)
    screen.fill(bg_color)
    asd = load_image('37.png')
    tu = load_image('an.png')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
        screen.blit(asd, (250, 150))
        screen.blit(tu, (20, 20))
        if st3_button.draw(screen):
            qwe()
            running = False
        if st4_button.draw(screen):
            rf()
            running = False
        clock.tick(100)
        pygame.display.flip()


def rf():

    bg_color = (19, 17, 26)
    screen.fill(bg_color)
    rf = load_image('38.png')
    tu = load_image('tu.jpg')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

        screen.blit(rf, (250, 150))
        screen.blit(tu, (20, 20))

        if st5_button.draw(screen):
            asd()
            running = False
        if st6_button.draw(screen):
            qwe()
            running = False
        clock.tick(100)
        pygame.display.flip()





if __name__ == '__main__':
    main()
