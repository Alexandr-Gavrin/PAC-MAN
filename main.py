import pygame

pygame.init()
width, height = 841, 901
screen = pygame.display.set_mode((width, height))
all_sprites = pygame.sprite.Group()
wall_group = pygame.sprite.Group()

title_width = 30
title_height = 30


def start_screen():
    title = pygame.image.load('data/title.png')
    screen.blit(title, (200, 0))
    start_screen_text = ["Начать", "",
                         "Настройки", "",
                         "Выход"]

    font = pygame.font.Font(None, 50)
    text_coord = 200
    for string in start_screen_text:
        line_rendered = font.render(string, 1, pygame.Color('yellow'))
        intro_rect = line_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = width // 2 - line_rendered.get_width() // 2
        text_coord += intro_rect.height
        screen.blit(line_rendered, intro_rect)


class PacmenStart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(pacmen_start_screen_sprites)
        self.image = pygame.image.load('data/start_pacman2.0.png')
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 205

    def update(self, x, y):
        self.rect.y += y
        self.rect.x += x


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, num=0):
        super().__init__(all_sprites, wall_group)
        if num == 0:
            self.image = pygame.Surface((title_width, 2))
            self.image.fill(pygame.Color('Blue'))
            self.rect = self.image.get_rect().move(title_width * x,
                                                   title_height * y)
        if num == 1:
            self.image = pygame.Surface((2, title_height))
            self.image.fill(pygame.Color('Blue'))
            self.rect = self.image.get_rect().move(title_width * x,
                                                   title_height * y)

        if num == 2:
            self.image = pygame.Surface((title_width, 2))
            self.image.fill(pygame.Color('Blue'))
            self.rect = self.image.get_rect().move(title_width * x,
                                                   title_height * y + title_height)

        if num == 3:
            self.image = pygame.Surface((2, title_height))
            self.image.fill(pygame.Color('Blue'))
            self.rect = self.image.get_rect().move(title_width * x + title_width,
                                                   title_height * y)

        if len(pygame.sprite.spritecollide(self, all_sprites, False)) > 3:
            self.kill()


class Point(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, wall_group)
        self.image = pygame.Surface((title_width - 10, title_height - 10))
        pygame.draw.circle(self.image, (255, 255, 173), (15, 15), 5, 0)
        self.rect = self.image.get_rect().move(title_width * x,
                                               title_height * y)


def load_level(filename):
    filename = 'data/' + filename
    with open(filename, 'r') as mapFile:
        level_map = [line for line in mapFile]
    return level_map


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Point(x, y)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Wall(x, y, num=0)
                Wall(x, y, num=1)
                Wall(x, y, num=2)
                Wall(x, y, num=3)


generate_level(load_level('level.txt'))
all_sprites = pygame.sprite.Group()
start_screen_sprites = pygame.sprite.Group()
pacmen_start_screen_sprites = pygame.sprite.Group()
enemy_start_screen_sprites = pygame.sprite.Group()
PacmenStart()
running = True
start_screen()
StartPacmenx = 300
StartPacmeny = 205
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if StartPacmenx == 300:
                    pacmen_start_screen_sprites.update(-35, 90)
                    StartPacmenx += 90
                elif StartPacmenx == 390:
                    pacmen_start_screen_sprites.update(35, 90)
                    StartPacmenx += 90
                elif StartPacmenx == 480:
                    pacmen_start_screen_sprites.update(0, -180)
                    StartPacmenx -= 180
            if event.key == pygame.K_UP:
                if StartPacmenx == 300:
                    pacmen_start_screen_sprites.update(0, 180)
                    StartPacmenx += 180
                elif StartPacmenx == 390:
                    pacmen_start_screen_sprites.update(35, -90)
                    StartPacmenx -= 90
                elif StartPacmenx == 480:
                    pacmen_start_screen_sprites.update(-35, -90)
                    StartPacmenx -= 90
    screen.fill((0, 0, 0))
    start_screen()
    pacmen_start_screen_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
