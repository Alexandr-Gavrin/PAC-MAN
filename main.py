import pygame

pygame.init()
width, height = 950, 650
screen = pygame.display.set_mode((width, height))


def start_screen():
    title = pygame.image.load('data/title.png')
    screen.blit(title, (250, 0))
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
    pacmen = pygame.sprite.Sprite()


class PacmenStart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(pacmen_start_screen_sprites)
        self.image = pygame.image.load('data/start_pacman2.0.png')
        self.rect = self.image.get_rect()
        self.rect.x = 350
        self.rect.y = 210

    def update(self, *args):
        print(12)
        if args and args[0].type == pygame.KEYDOWN and args[0].key == pygame.K_DOWN:
            print(1)
            if self.rect.x == 350:
                print(2)
                self.rect.y -= 20
                self.rect.x -= 50


running = True
all_sprites = pygame.sprite.Group()
start_screen_sprites = pygame.sprite.Group()
pacmen_start_screen_sprites = pygame.sprite.Group()
enemy_start_screen_sprites = pygame.sprite.Group()
PacmenStart()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            PacmenStart.update(event)
    screen.fill((0, 0, 0))
    start_screen()
    pacmen_start_screen_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
