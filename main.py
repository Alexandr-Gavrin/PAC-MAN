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
pygame.mouse.set_visible(False)
end_screen_enemy = pygame.sprite.Group()
particles = pygame.sprite.Group()
settings_group = pygame.sprite.Group()
change_value = pygame.sprite.Group()
running = True
fl_HESOYAM = False
fl_GOD = False
title_width = 30
gravity = 0.5
settings_running = False
title_height = 30
score_count = 0
cell = 0
coord_x = 0
coord_y = 0
fl_death = False
win_music = False
screen_rect = (0, 0, width, height)
prev_pac_man = 'right'
stars = ['data/star.png', 'data/green_star.png', 'data/Communist_star.png', 'data/red_star.png']
rotate_pacman = False
change_coord_pacman_menu = False
is_load_level = False
r, g, b = 0, 0, 0
level = 1
level = 'Лёгкий'
arr_color = [r, g, b]

volume = 0.5
pygame.mixer.music.load('data/pacman_beginning.mp3')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(volume)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global cell, menu_running, level, is_load_level, game_running, settings_running
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
                if cell == 1:
                    settings_running = True
                    while settings_running:
                        screen.fill((0, 0, 0))
                        start_settings()
                        pacmen_start_screen_sprites.draw(screen)
                        enemy_start_screen_sprites.draw(screen)
                        enemy_start_screen_sprites.update()
                        pygame.display.flip()
                if cell == 0:
                    if not is_load_level:
                        generate_level(load_level('level.txt'))
                        is_load_level = True
                    game_running = True
                    menu_running = False
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


# Настройки
def start_settings():
    global cell, running, change_coord_pacman_menu, volume, \
        push_enter, level, push_enter_level, settings_running

    if not change_coord_pacman_menu:
        pacmen_start_screen_sprites.update(100, 295)
        change_coord_pacman_menu = True
    title = pygame.image.load('data/settings.png')
    screen.blit(title, (0, 0))
    start_screen_text = ["Громкость    " + str(volume), "",
                         "Уровень сложности   " + str(level), "",
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
                    settings_running = False
                    change_coord_pacman_menu = False
            if event.key == pygame.K_LEFT and cell == 0:
                if float(volume) != 0.0:
                    volume_float = []
                    for i in str(float(volume)):
                        try:
                            volume_float.append(int(i))
                        except ValueError:
                            volume_float.append(i)
                    if volume_float[0] == 1:
                        volume_float[0] -= 1
                        volume_float[2] += 9
                    else:
                        volume_float[2] -= 1
                    for i in range(len(volume_float)):
                        volume_float[i] = str(volume_float[i])
                    volume = ''.join(volume_float)
                    volume = float(volume)
                pygame.mixer.music.set_volume(float(volume))
            if event.key == pygame.K_RIGHT and cell == 0:  # Изменение громкости музыки
                if float(volume) != 1.0:
                    volume_float = []
                    for i in str(float(volume)):
                        try:
                            volume_float.append(int(i))
                        except ValueError:
                            volume_float.append(i)
                    if volume_float[2] == 9:
                        volume_float[0] += 1
                        volume_float[2] -= 9
                    else:
                        volume_float[2] += 1
                    for i in range(len(volume_float)):
                        volume_float[i] = str(volume_float[i])
                    volume = ''.join(volume_float)
                    volume = float(volume)
                pygame.mixer.music.set_volume(float(volume))
            if event.key == pygame.K_RIGHT and cell == 1:  # Изменение уровня сложности
                if level != 'Сложный':
                    level = 'Сложный'
                else:
                    level = 'Лёгкий'
            if event.key == pygame.K_LEFT and cell == 1:
                if level != 'Лёгкий':
                    level = 'Лёгкий'
                else:
                    level = 'Сложный'
            if event.key == pygame.K_DOWN:
                cell = (cell + 1) % 3
            if event.key == pygame.K_UP:
                cell = (cell - 1) % 3
            if cell == 0:
                pacmen_start_screen_sprites.update(230, 205)
            elif cell == 1:
                pacmen_start_screen_sprites.update(100, 295)
            else:
                pacmen_start_screen_sprites.update(260, 385)


def end_screen(fl):
    global win_music
    if fl:
        game_over_image = pygame.image.load('data/game_over.png')  # Музыка при проигрыше
        screen.blit(game_over_image, (225, 325))
        end_screen_enemy.draw(screen)
        end_screen_enemy.update()
    else:
        if not win_music:
            # Музыка при выигрыши
            music_win = random.choice(['data/sound_win.mp3', 'data/sound_win_2.mp3'])
            pygame.mixer.music.load(music_win)
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(volume)
            win_music = True
        win_image = pygame.image.load('data/win.png')
        screen.blit(win_image, (275, 325))
        create_particles((random.randint(0, 800), 0), random.randint(0, 5))
        particles.draw(screen)
        particles.update()


class Particle(pygame.sprite.Sprite):
    global stars
    fire = []
    for scale in (range(30)):
        fire.append(pygame.transform.scale(pygame.image.load(random.choice(stars)),
                                           (scale, scale)))

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
    for i in range(count):
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
        global wall_group
        global coord_x, coord_y, score_count
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if self.rect.x < 0:
            self.rect.x = 830
        if self.rect.x > 830:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = 940
        if self.rect.y > 940:
            self.rect.y = 0
        if x == 0 and y == 0:
            self.rect.x += self.speed_x
            if pygame.sprite.spritecollideany(self, wall_group):
                if fl_HESOYAM is False:
                    self.rect.x -= self.speed_x
                    self.cur_frame = 2
                if rotate_pacman:
                    self.cur_frame = 1
            self.rect.y += self.speed_y
            if pygame.sprite.spritecollideany(self, wall_group):
                if fl_HESOYAM is False:
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
                if fl_HESOYAM is False:
                    self.rect.x -= self.speed_x
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
    def __init__(self, x, y, color=(0, 0, 0)):
        super().__init__(wall_group)
        self.image = pygame.Surface((title_width - 6, title_height - 6))
        pygame.draw.rect(self.image, color,
                         (0, 0, title_width - 6, title_height - 6), 2)
        self.rect = self.image.get_rect().move(title_width * x,
                                               title_height * y)


class Point(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, point_group)
        self.image = pygame.Surface((title_width - 10, title_height - 10))
        pygame.draw.circle(self.image, (255, 255, 173), (15, 15), 5, 0)
        self.rect = self.image.get_rect().move(title_width * x - 3,
                                               title_height * y)


attemp = 0


# Класс который создаёт и управляет врагами
class Enemy(pygame.sprite.Sprite):
    def __init__(self, sheet, color, columns, rows, x, y):
        global level
        super().__init__(all_sprites, left_enemy_group)
        self.frames = []
        self.color_enemy = color
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x * title_width, y * title_width)
        self.speed_x = 6
        self.speed_y = 0
        # Выбор скорости врага
        self.speed_enemy = 6
        if level == 2:
            self.speed_enemy = 10
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
        global attemp, fl_death
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
                Wall(13, 13)
                Wall(14, 13)
                wall_group.draw(screen)
        elif self.start_enemy_motion and not pygame.sprite.spritecollideany(self, wall_group):
            if self.rect.x > 402:
                self.rect.x -= 6
            else:
                self.rect.x += 6
        elif not self.start_enemy_motion:
            Wall(13, 13)
            Wall(14, 13)
            wall_group.draw(screen)

            if attemp < 20:
                self.way_enemy = random.choice(['up', 'left', 'right'])
                attemp += 1
            # Если пакман движется вниз то выполнится это условие
            if self.way_enemy == 'down':
                self.x_coord = self.rect.x
                self.y_coord = self.rect.y
                self.frames = []
                self.cut_sheet(pygame.image.load(self.color_enemy + '_down.png'), 2, 1)
                self.cur_frame = 0
                self.image = self.frames[self.cur_frame]
                self.rect.x = self.x_coord
                self.rect.y = self.y_coord
                self.rect.y += self.speed_enemy
                if pygame.sprite.spritecollideany(self, wall_group):
                    self.rect.y -= self.speed_enemy
                    self.way_enemy = random.choice(['down', 'up', 'left', 'right'])
            # Если пакман движется вверх то выполнится это условие
            if self.way_enemy == 'up':
                self.x_coord = self.rect.x
                self.y_coord = self.rect.y
                self.frames = []
                self.cut_sheet(pygame.image.load(self.color_enemy + '_up.png'), 2, 1)
                self.cur_frame = 0
                self.image = self.frames[self.cur_frame]
                self.rect.x = self.x_coord
                self.rect.y = self.y_coord
                self.rect.y -= self.speed_enemy
                if pygame.sprite.spritecollideany(self, wall_group):
                    self.rect.y += self.speed_enemy
                    self.way_enemy = random.choice(['down', 'up', 'left', 'right'])
            # Если пакман движется влево то выполнится это условие
            if self.way_enemy == 'left':
                self.x_coord = self.rect.x
                self.y_coord = self.rect.y
                self.frames = []
                self.cut_sheet(pygame.image.load(self.color_enemy + '_left.png'), 2, 1)
                self.cur_frame = 0
                self.image = self.frames[self.cur_frame]
                self.rect.x = self.x_coord
                self.rect.y = self.y_coord
                self.rect.x -= self.speed_enemy
                if pygame.sprite.spritecollideany(self, wall_group):
                    self.rect.x += self.speed_enemy
                    self.way_enemy = random.choice(['down', 'up', 'left', 'right'])
            # Если пакман движется вправо то выполнится это условие
            if self.way_enemy == 'right':
                self.x_coord = self.rect.x
                self.y_coord = self.rect.y
                self.frames = []
                self.cut_sheet(pygame.image.load(self.color_enemy + '_right.png'), 2, 1)
                self.cur_frame = 0
                self.image = self.frames[self.cur_frame]
                self.rect.x = self.x_coord
                self.rect.y = self.y_coord
                self.rect.x += self.speed_enemy
                if pygame.sprite.spritecollideany(self, wall_group):
                    self.rect.x -= self.speed_enemy
                    self.way_enemy = random.choice(['down', 'up', 'left', 'right'])

        if pygame.sprite.spritecollideany(self, player_group):
            if fl_GOD is False:
                global volume
                pygame.mixer.music.load('data/game_over.mp3')
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(volume)
                fl_death = True
            else:
                self.kill()


def load_level(filename):
    filename = 'data/' + filename
    with open(filename, 'r') as mapFile:
        level_map = [line for line in mapFile]
    return level_map


r, g, b = (random.randrange(0, 255), random.randrange(0, 255),
           random.randrange(0, 255))


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Point(x, y)
            if level[y][x] == '#':
                Wall(x, y, (r, g, b))
            if level[y][x] == '@':
                Player(pygame.image.load('data/Pac-man_right.png'), 3, 1, x, y)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '$':
                color_enemy = random.choice(['data/orange_enemy',
                                             'data/blue_enemy',
                                             'data/pink_enemy',
                                             'data/red_enemy'])
                Enemy(pygame.image.load(color_enemy + '_right.png').convert_alpha(), color_enemy,
                      2, 1, x, y)
            if level[y][x] == '%':
                color_enemy = random.choice(['data/orange_enemy',
                                             'data/blue_enemy',
                                             'data/pink_enemy',
                                             'data/red_enemy'])
                Enemy(pygame.image.load(color_enemy + '_left.png').convert_alpha(), color_enemy,
                      2, 1, x, y)


pacmen_start_screen_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
start_screen_sprites = pygame.sprite.Group()
enemy_start_screen_sprites = pygame.sprite.Group()
left_enemy_group = pygame.sprite.Group()

PacmenStart()
start_screen()
Startmenuenemy(pygame.image.load('data/start_enemy.png').convert_alpha(), 4, 1, 0, 800)

main_running = True
menu_running = True
settings_running = True
pause = False
game_running = True

while main_running:
    while menu_running:
        screen.fill((0, 0, 0))
        start_screen()
        pacmen_start_screen_sprites.draw(screen)
        enemy_start_screen_sprites.draw(screen)
        enemy_start_screen_sprites.update()
        pygame.display.flip()

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if not pause:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        fl_GOD = not fl_GOD
                    if event.key == pygame.K_h:
                        fl_HESOYAM = not fl_HESOYAM
                    if event.key == pygame.K_RIGHT:
                        for i in player_group:
                            if fl_HESOYAM or not i.wall(15, 0) and prev_pac_man != 'right':
                                player_group = pygame.sprite.Group()
                                Player(pygame.image.load('data/Pac-man_right.png').convert_alpha(),
                                       3, 1,
                                       coord_x / title_width, coord_y / title_height, 6, 0)
                                prev_pac_man = 'right'
                                rotate_pacman = False
                    if event.key == pygame.K_DOWN:
                        for i in player_group:
                            if fl_HESOYAM or not i.wall(0, 15) and prev_pac_man != 'down':
                                player_group = pygame.sprite.Group()
                                Player(pygame.image.load('data/Pac-man_down.png').convert_alpha(),
                                       1, 3,
                                       coord_x / title_width, coord_y / title_height, 0, 6)
                                prev_pac_man = 'down'
                                rotate_pacman = False
                    if event.key == pygame.K_LEFT:
                        for i in player_group:
                            if fl_HESOYAM or not i.wall(-15, 0) and prev_pac_man != 'left':
                                player_group = pygame.sprite.Group()
                                Player(pygame.image.load('data/Pac-man_left.png').convert_alpha(),
                                       3, 1,
                                       coord_x / title_width, coord_y / title_height, -6, 0)
                                prev_pac_man = 'left'
                                rotate_pacman = True
                    if event.key == pygame.K_UP:
                        for i in player_group:
                            if fl_HESOYAM or not i.wall(0, -15) and prev_pac_man != 'up':
                                player_group = pygame.sprite.Group()
                                Player(pygame.image.load('data/Pac-man_up.png').convert_alpha(), 1,
                                       3,
                                       coord_x / title_width, coord_y / title_height, 0, -6)
                                prev_pac_man = 'up'
                                rotate_pacman = True
                    if event.key == pygame.K_ESCAPE:
                        pause = True
                        pygame.mixer.music.pause()
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.unpause()
                        pause = False
        if not pause:
            random_number = random.randrange(0, 3)
            if random_number == 0:
                r += random.randrange(0, 30)
            elif random_number == 1:
                g += random.randrange(0, 30)
            else:
                b += random.randrange(0, 30)
            wall_group = pygame.sprite.Group()
            if r > 255 or b > 255 or g > 255:
                r, g, b = (random.randrange(0, 60), random.randrange(0, 60),
                           random.randrange(0, 60))
            screen.fill((0, 0, 0))
            generate_level(load_level('rainbow_level.txt'))
            score_counter()
            all_sprites.draw(screen)
            wall_group.draw(screen)
            time.sleep(0.06)
            player_group.update()
            left_enemy_group.update()
            pygame.display.flip()
            if fl_death is True or len(point_group) == 0:
                game_running = False
                end_screen_running = True
        else:
            screen2 = pygame.Surface((width, height))
            screen2.set_colorkey((255, 255, 255))
            screen2.set_alpha(7)
            screen.blit(screen2, (0, 0))
            pygame.display.flip()

    end_screen_enemy = pygame.sprite.Group()
    End_screen_enemies(pygame.image.load('data/end_screen_error.png').convert_alpha(), 2, 1, 0, 516)
    End_screen_enemies(pygame.image.load('data/end_screen_error2.png').convert_alpha(), 2, 1, 0,
                       290)

    while end_screen_running:
        number = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                number = 0
                end_screen_running = False
                menu_running = True
                volume = 0.1
                fl_death = False
                pygame.mixer.music.load('data/pacman_beginning.mp3')
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(volume)
                pacmen_start_screen_sprites = pygame.sprite.Group()
                player_group = pygame.sprite.Group()
                start_screen_sprites = pygame.sprite.Group()
                enemy_start_screen_sprites = pygame.sprite.Group()
                left_enemy_group = pygame.sprite.Group()
                PacmenStart()
                start_screen()
                Startmenuenemy(pygame.image.load('data/start_enemy.png').convert_alpha(), 4, 1, 0,
                               800)
                menu_running = True
                is_load_level = False
                all_sprites = pygame.sprite.Group()
                wall_group = pygame.sprite.Group()
                point_group = pygame.sprite.Group()
                pygame.mouse.set_visible(False)
                end_screen_enemy = pygame.sprite.Group()
                particles = pygame.sprite.Group()
                settings_group = pygame.sprite.Group()
                change_value = pygame.sprite.Group()
                attemp = 0

        screen.fill((0, 0, 0))
        if number == 1:
            end_screen(fl_death)
        pygame.display.flip()

pygame.quit()
