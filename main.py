import pygame
import time
import sys

pygame.init()
width, height = 841, 901
screen = pygame.display.set_mode((width, height), )
all_sprites = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
point_group = pygame.sprite.Group()
running = True
title_width = 30
title_height = 30
score_count = 0
cell = 0


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global cell, running
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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                if cell == 2:
                    terminate()
                if cell == 0:
                    running = False
            if event.key == pygame.K_DOWN:
                cell = (cell + 1) % 3
            if event.key == pygame.K_UP:
                cell = (cell - 1) % 3
            if cell == 0:
                pacmen_start_screen_sprites.update(295, 205)
            elif cell == 1:
                pacmen_start_screen_sprites.update(260, 295)
            else:
                pacmen_start_screen_sprites.update(295, 385)


class PacmenStart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(pacmen_start_screen_sprites, start_screen_sprites)
        self.image = pygame.image.load('data/start_pacman2.0.png')
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 205

    def update(self, x, y):
        self.rect.y = y
        self.rect.x = x


class Startmenuenemy(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(enemy_start_screen_sprites, start_screen_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.rect.x = (self.rect.x + 5) % width


def score_counter():
    global score_count
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 25)
    text = font.render(str(score_count), 0, (255, 255, 255))
    text_x = 750
    text_y = 330
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (255, 255, 255), (text_x - 10, text_y - 10,
                                               text_w + 20, text_h + 20), 1)


class Player(pygame.sprite.Sprite):

    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites, player_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x * title_width, y * title_width)
        self.speed_x = 6
        self.speed_y = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.prev_speed_x = self.speed_x
        self.prev_speed_y = self.speed_y

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self, x=0, y=0, direction=0):
        global score_count
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if self.rect.x < 0:
            self.rect.x = 841
        if self.rect.x > 841:
            self.rect.x = 0
        if x == 0 and y == 0:
            self.rect.x += self.speed_x
            if pygame.sprite.spritecollideany(self, wall_group):
                self.rect.x -= self.speed_x

            self.rect.y += self.speed_y
            if pygame.sprite.spritecollideany(self, wall_group):
                self.rect.y -= self.speed_y
        elif self.speed_y == y and self.speed_x == x:
            pass
        else:
            self.speed_x = x
            self.speed_y = y
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            if pygame.sprite.spritecollideany(self, wall_group):
                self.rect.x -= self.speed_x
                self.rect.y -= self.speed_y
                self.speed_y = self.prev_speed_y
                self.speed_x = self.prev_speed_x
                return
            else:
                self.prev_speed_x = self.speed_x
                self.prev_speed_y = self.speed_y
                return

        if pygame.sprite.spritecollide(self, point_group, True):
            score_count += 10


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, wall_group)
        self.image = pygame.Surface((title_width, title_height))
        pygame.draw.rect(self.image, pygame.Color('Blue'), (0, 0, title_width, title_height), 2)
        self.rect = self.image.get_rect().move(title_width * x,
                                               title_height * y)


class Point(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, point_group)
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
            if level[y][x] == '#':
                Wall(x, y)
            if level[y][x] == '@':
                Player(pygame.image.load('data/Pac-man.png'), 3, 1, x, y)


pacmen_start_screen_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
start_screen_sprites = pygame.sprite.Group()
enemy_start_screen_sprites = pygame.sprite.Group()

PacmenStart()
start_screen()
generate_level(load_level('level.txt'))
Startmenuenemy(pygame.image.load('data/start_enemy.png'), 4, 1, 0, 800)

pygame.mixer.music.load('data/pacman_beginning.mp3')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                if StartPacmenx == 300:
                    running = False
                    break
    screen.fill((0, 0, 0))
    start_screen()
    pacmen_start_screen_sprites.draw(screen)
    enemy_start_screen_sprites.draw(screen)
    enemy_start_screen_sprites.update()
    pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player_group.update(6, 0, 'right')
            if event.key == pygame.K_DOWN:
                player_group.update(0, 6, 'down')
            if event.key == pygame.K_LEFT:
                player_group.update(-6, 0, 'left')
            if event.key == pygame.K_UP:
                player_group.update(0,
                                    -6, 'up')
    screen.fill((0, 0, 0))
    score_counter()
    all_sprites.draw(screen)
    time.sleep(0.12)
    player_group.update()
    pygame.display.flip()
pygame.quit()
