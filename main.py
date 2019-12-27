import pygame
import time
import random
import sys

pygame.init()
width, height = 841, 901
screen = pygame.display.set_mode((width, height), )
all_sprites = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
point_group = pygame.sprite.Group()
end_screen_enemy = pygame.sprite.Group()
particles = pygame.sprite.Group()
running = True
title_width = 30
gravity = 0.5
title_height = 30
score_count = 0
cell = 0
coord_x = 0
coord_y = 0
fl_death = False
screen_rect = (0, 0, width, height)
prev_pac_man = 'right'
rotate_pacman = False
r, g, b = 0, 0, 0
arr_color = [r, g, b]


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
    random_num = random.randrange(0, 3)
    arr_color[random_num] = (arr_color[random_num] + 9) % 255

    for string in start_screen_text:
        line_rendered = font.render(string, 1, (arr_color[0], arr_color[1], arr_color[2]))
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


def end_screen(fl):
    if fl:
        game_over_image = pygame.image.load('data/game_over.png')
        screen.blit(game_over_image, (225, 325))
        end_screen_enemy.draw(screen)
        end_screen_enemy.update()
    else:
        win_image = pygame.image.load('data/win.png')
        screen.blit(win_image, (275, 325))
        create_particles((random.randint(0, 800), 0), random.randint(0, 5))
        particles.draw(screen)
        particles.update()


class Particle(pygame.sprite.Sprite):
    fire = [pygame.image.load("data/star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(particles)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = gravity

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position, count):
    numbers = range(-5, 6)
    for _ in range(count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class End_screen_enemies(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(end_screen_enemy)
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
        time.sleep(0.03)


class PacmenStart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(pacmen_start_screen_sprites, start_screen_sprites)
        self.image = pygame.image.load('data/start_pacman2.0.png')
        self.rect = self.image.get_rect()
        self.rect.x = 295
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
        time.sleep(0.03)


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
    def __init__(self, sheet, columns, rows, x, y, speed_x=6, speed_y=0):
        for player in all_sprites:
            try:
                if player.can_kill == True:
                    all_sprites.remove(player)
            except:
                pass
        super().__init__(all_sprites, player_group)
        self.frames = []
        self.can_kill = True
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x * title_width, y * title_width)
        self.speed_x = speed_x
        self.speed_y = speed_y
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
        global coord_x, coord_y, score_count
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
                self.cur_frame = 2
                if rotate_pacman:
                    self.cur_frame = 1
            self.rect.y += self.speed_y
            if pygame.sprite.spritecollideany(self, wall_group):
                self.rect.y -= self.speed_y
                self.cur_frame = 2
                if rotate_pacman:
                    self.cur_frame = 1

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
                self.cur_frame = 2
                if rotate_pacman:
                    self.cur_frame = 1
                return
            else:
                self.prev_speed_x = self.speed_x
                self.prev_speed_y = self.speed_y
                return

        if pygame.sprite.spritecollide(self, point_group, True):
            score_count += 10
        coord_x = self.rect.x
        coord_y = self.rect.y

    def update_image(self, sheet, rows, col):
        x, y = self.rect.x, self.rect.y
        self.cur_frame = 0
        self.frames = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() // col, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(col):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
        self.rect = self.rect.move(x, y)

    def wall(self, x, y):
        self.rect.x += x
        self.rect.y += y
        if pygame.sprite.spritecollideany(self, wall_group):
            self.rect.x -= x
            self.rect.y -= y
            return True
        self.rect.x -= x
        self.rect.y -= y
        return False


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, wall_group)
        self.image = pygame.Surface((title_width - 3, title_height - 3))
        pygame.draw.rect(self.image, pygame.Color('Blue'), (0, 0, title_width - 3, title_height - 3), 2)
        self.rect = self.image.get_rect().move(title_width * x,
                                               title_height * y)


class Point(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, point_group)
        self.image = pygame.Surface((title_width - 10, title_height - 10))
        pygame.draw.circle(self.image, (255, 255, 173), (15, 15), 5, 0)
        self.rect = self.image.get_rect().move(title_width * x,
                                               title_height * y)


class Right_Enemy(pygame.sprite.Sprite):
    def __init__(self, sheet, color, columns, rows, x, y):
        super().__init__(all_sprites, left_enemy_group)
        self.frames = []
        self.color_enemy = color
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x * title_width, y * title_width)
        self.speed_x = 6
        self.speed_y = 0
        self.start_enemy_motion = True
        self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        if self.rect.x <= 402 and not pygame.sprite.spritecollideany(self, wall_group):
            self.x_coord = self.rect.x
            self.y_coord = self.rect.y
            self.frames = []
            self.cut_sheet(pygame.image.load(self.color_enemy + '_up.png'), 2, 1)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
            self.rect.x = self.x_coord
            self.rect.y = self.y_coord
            self.rect.y -= 6
        elif self.start_enemy_motion and not pygame.sprite.spritecollideany(self, wall_group):
            self.rect.x -= 6
        elif pygame.sprite.spritecollideany(self, player_group):
            pass  # Проигрыш


class Left_Enemy(pygame.sprite.Sprite):
    def __init__(self, sheet, color, columns, rows, x, y):
        super().__init__(all_sprites, left_enemy_group)
        self.frames = []
        self.color_enemy = color
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x * title_width, y * title_width)
        self.speed_x = 6
        self.speed_y = 0
        self.way_enemy = None
        self.start_enemy_motion = True
        self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        if self.start_enemy_motion and self.rect.x == 402:
            self.x_coord = self.rect.x
            self.y_coord = self.rect.y
            self.frames = []
            self.cut_sheet(pygame.image.load(self.color_enemy + '_up.png'), 2, 1)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
            self.rect.x = self.x_coord
            self.rect.y = self.y_coord
            self.rect.y -= 6
            if pygame.sprite.spritecollideany(self, wall_group):
                self.start_enemy_motion = False
        elif self.start_enemy_motion and not pygame.sprite.spritecollideany(self, wall_group):
            self.rect.x += 6
        elif not self.start_enemy_motion:
            if self.way_enemy is None:
                self.way_enemy = random.choice(['straight'])
            if self.way_enemy == 'straight':
                self.x_coord = self.rect.x
                self.y_coord = self.rect.y
                self.frames = []
                self.cut_sheet(pygame.image.load(self.color_enemy + '_left.png'), 2, 1)
                self.cur_frame = 0
                self.image = self.frames[self.cur_frame]
                self.rect.x = self.x_coord
                self.rect.y = self.y_coord
                if pygame.sprite.spritecollideany(self, wall_group):
                    self.rect.x -= 6
            else:
                pass
        elif pygame.sprite.spritecollideany(self, player_group):
            pass  # Проигрыш


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
                Player(pygame.image.load('data/Pac-man_right.png'), 3, 1, x, y)
            if level[y][x] == '%':
                color_enemy = random.choice(['data/orange_enemy',
                                             'data/blue_enemy',
                                             'data/pink_enemy',
                                             'data/red_enemy'])
                Right_Enemy(pygame.image.load(color_enemy + '_left.png'), color_enemy,
                            2, 1, x, y)
            if level[y][x] == '$':
                color_enemy = random.choice(['data/orange_enemy',
                                             'data/blue_enemy',
                                             'data/pink_enemy',
                                             'data/red_enemy'])
                Left_Enemy(pygame.image.load(color_enemy + '_right.png'), color_enemy,
                           2, 1, x, y)


pacmen_start_screen_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
start_screen_sprites = pygame.sprite.Group()
enemy_start_screen_sprites = pygame.sprite.Group()
left_enemy_group = pygame.sprite.Group()

PacmenStart()
start_screen()
generate_level(load_level('level.txt'))
Startmenuenemy(pygame.image.load('data/start_enemy.png'), 4, 1, 0, 800)

while running:
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
                for i in player_group:
                    if not i.wall(6, 0) and prev_pac_man != 'right':
                        player_group = pygame.sprite.Group()
                        Player(pygame.image.load('data/Pac-man_right.png'), 3, 1,
                               coord_x / title_width, coord_y / title_height, 6, 0)
                        prev_pac_man = 'right'
                        rotate_pacman = False

            if event.key == pygame.K_DOWN:
                for i in player_group:
                    if not i.wall(0, 6) and prev_pac_man != 'down':
                        player_group = pygame.sprite.Group()
                        Player(pygame.image.load('data/Pac-man_down.png'), 1, 3,
                               coord_x / title_width, coord_y / title_height, 0, 6)
                        prev_pac_man = 'down'
                        rotate_pacman = False

            if event.key == pygame.K_LEFT:
                for i in player_group:
                    if not i.wall(-6, 0) and prev_pac_man != 'left':
                        player_group = pygame.sprite.Group()
                        Player(pygame.image.load('data/Pac-man_left.png'), 3, 1,
                               coord_x / title_width, coord_y / title_height, -6, 0)
                        prev_pac_man = 'left'
                        rotate_pacman = True

            if event.key == pygame.K_UP:
                for i in player_group:
                    if not i.wall(0, -6) and prev_pac_man != 'up':
                        player_group = pygame.sprite.Group()
                        Player(pygame.image.load('data/Pac-man_up.png'), 1, 3,
                               coord_x / title_width, coord_y / title_height, 0, -6)
                        prev_pac_man = 'up'
                        rotate_pacman = True
    screen.fill((0, 0, 0))
    score_counter()
    all_sprites.draw(screen)
    time.sleep(0.12)
    player_group.update()
    left_enemy_group.update()
    pygame.display.flip()
    if fl_death is True or len(point_group) == 0:
        running = False

running = True
End_screen_enemies(pygame.image.load('data/end_screen_error.png'), 2, 1, 0, 516)
End_screen_enemies(pygame.image.load('data/end_screen_error2.png'), 2, 1, 0, 290)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    screen.fill((0, 0, 0))
    end_screen(fl_death)
    pygame.display.flip()
pygame.quit()
